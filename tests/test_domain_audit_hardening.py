import http.client
import json
import subprocess
import tempfile
import unittest
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

from scripts import daily_audit, site_paths

ROOT = Path(__file__).resolve().parents[1]


class AuditCoverageTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "content").mkdir()
        self.base = "https://canonical.example/BioCare/"
        for name, data in {
            "site.json": {"site": {"metadata": {"canonicalBaseUrl": self.base}}},
            "library.json": {"articles": []}, "discovery.json": {"departments": []},
            "catalog.json": {"products": []},
        }.items():
            (self.root / "content" / name).write_text(json.dumps(data), encoding="utf-8")
        self.paths = site_paths.canonical_page_paths({"articles": []}, {"departments": []}, {"products": []})
        for path in self.paths:
            (self.root / (path or "index.html")).write_text('<html><link href="assets/site.css" rel="stylesheet"><h1>Fixture</h1></html>', encoding="utf-8")
        (self.root / "assets").mkdir()
        (self.root / "assets/site.css").write_text('body{background:url("pixel.png")}', encoding="utf-8")
        (self.root / "assets/pixel.png").write_bytes(b"image fixture")
        self.write_sitemap([self.base + path for path in self.paths])
        self.write_robots()

    def write_robots(self):
        (self.root / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {self.base}sitemap.xml\n", encoding="utf-8")

    def write_sitemap(self, urls, namespace=site_paths.SITEMAP_NAMESPACE):
        root = ET.Element("urlset", xmlns=namespace)
        for url in urls:
            ET.SubElement(ET.SubElement(root, "url"), "loc").text = url
        ET.ElementTree(root).write(self.root / "sitemap.xml", encoding="utf-8")

    def fetch_fixture(self, url):
        self.assertTrue(url.startswith("http://preview.example/review/"))
        relative = url.removeprefix("http://preview.example/review/") or "index.html"
        return {"status": 200, "body": daily_audit.build_bytes(self.root / relative), "final_url": url}

    def audit(self, fetcher=None):
        return daily_audit.audit_site(self.root, "http://preview.example/review/", "fixture-sha", fetcher=fetcher or self.fetch_fixture)

    def test_complete_inventory_honors_target_base_and_checks_css_assets(self):
        result = self.audit()
        self.assertEqual(result["overall_status"], "HEALTHY")
        self.assertEqual(result["public_pages"], 10)
        self.assertEqual(result["referenced_live_assets"], 2)
        self.assertTrue(all(item["byte_parity"] for item in result["page_results"] + result["asset_results"]))
        self.assertEqual(result["canonical_base_url"], self.base)
        self.assertEqual([item["path"] for item in result["crawl_metadata_results"]], ["robots.txt", "sitemap.xml"])
        self.assertTrue(all(item["passed"] and item["byte_parity"] for item in result["crawl_metadata_results"]))
        self.assertFalse(result["crawl_metadata_failures"])

    def test_root_domain_sitemap_maps_to_relative_files(self):
        self.base = "https://new.example/"
        (self.root / "content/site.json").write_text(json.dumps({"site": {"metadata": {"canonicalBaseUrl": self.base}}}), encoding="utf-8")
        self.write_sitemap([self.base + path for path in self.paths])
        self.write_robots()
        result = self.audit()
        self.assertEqual(result["public_pages"], 10)
        self.assertEqual(result["overall_status"], "HEALTHY")

    def metadata_response(self, relative, response):
        def fetcher(url):
            if url.endswith("/" + relative):
                return {"status": 200, "body": b"", "final_url": url, **response}
            return self.fetch_fixture(url)
        return self.audit(fetcher)

    def assert_metadata_failure(self, relative, response):
        report = self.metadata_response(relative, response)
        # This exact page/asset parity was sufficient for the old false HEALTHY.
        self.assertEqual(report["overall_status"], "ACTION REQUIRED")
        self.assertEqual(report["public_pages"], 10)
        self.assertFalse(report["page_regressions"])
        self.assertFalse(report["broken_live_assets"])
        self.assertEqual(len(report["crawl_metadata_results"]), 2)
        self.assertEqual([item["path"] for item in report["crawl_metadata_failures"]], [relative])
        failure = report["crawl_metadata_failures"][0]
        self.assertTrue(failure["validation_errors"])
        self.assertFalse(report["changes_made"])
        return failure

    def test_live_missing_and_unreadable_metadata_never_passes_from_page_parity(self):
        for relative in ("robots.txt", "sitemap.xml"):
            for status in (404, 403, 500, None):
                with self.subTest(relative=relative, status=status):
                    failure = self.assert_metadata_failure(relative, {"status": status, "error": "offline fixture"})
                    self.assertEqual(failure["status"], status)
                    self.assertEqual(failure["error"], "offline fixture")
            with self.subTest(relative=relative, status="failed read after HTTP 200"):
                failure = self.assert_metadata_failure(relative, {"body": daily_audit.build_bytes(self.root / relative), "error": "incomplete read"})
                self.assertIn("incomplete read", failure["validation_errors"][0])

    def test_live_metadata_redirects_fail_even_when_content_is_valid(self):
        for relative in ("robots.txt", "sitemap.xml"):
            for final in ("https://foreign.example/" + relative, self.base + relative,
                          "http://preview.example/review/wrong/" + relative, None):
                with self.subTest(relative=relative, final_url=final):
                    failure = self.assert_metadata_failure(relative, {"body": daily_audit.build_bytes(self.root / relative), "final_url": final})
                    self.assertTrue(failure["byte_parity"])
                    self.assertIn("redirect", " ".join(failure["validation_errors"]))

    def test_metadata_fetch_and_local_read_errors_are_reported(self):
        for relative in ("robots.txt", "sitemap.xml"):
            for error in (OSError("fixture read failed"), urllib.error.URLError("fixture offline"), http.client.IncompleteRead(b"partial", 50)):
                with self.subTest(relative=relative, error=error):
                    def broken(url):
                        if url.endswith("/" + relative):
                            raise error
                        return self.fetch_fixture(url)
                    result = self.audit(broken)
                    failure = result["crawl_metadata_failures"][0]
                    self.assertEqual(result["overall_status"], "ACTION REQUIRED")
                    self.assertEqual(failure["path"], relative)
                    self.assertIn(str(error), failure["error"])
        valid = daily_audit.build_bytes(self.root / "robots.txt")
        (self.root / "robots.txt").unlink()
        self.assert_metadata_failure("robots.txt", {"body": valid})

    def test_live_robots_requires_public_crawl_policy_and_canonical_sitemap(self):
        valid = daily_audit.build_bytes(self.root / "robots.txt")
        for body in (b"", b"<html>not robots</html>", b"\xff",
                     valid.replace(b"canonical.example", b"foreign.example"),
                     valid.replace(self.base.encode(), b"http://preview.example/review/"),
                     valid.replace(b"Allow: /", b"Disallow: /"),
                     valid.replace(b"User-agent: *", b"User-agent: SpecificBot"),
                     valid.replace(b"Allow: /", b"Allow: /\nDisallow: /library.html"),
                     valid + b"Sitemap: https://foreign.example/sitemap.xml\n",
                     valid + f"Sitemap: {self.base}sitemap.xml\n".encode(),
                     valid.replace(b"Sitemap:", b"Unused-extension:"),
                     b"Allow: /\n" + valid):
            with self.subTest(body=body):
                self.assert_metadata_failure("robots.txt", {"body": body})

    def test_live_robots_allows_comments_case_whitespace_and_unrelated_extensions(self):
        body = ("\ufeff# CDN extension\r\nContent-Signal: search=yes,ai-input=no\r\n"
                "User-agent: SpecificBot\r\nAllow: /\r\n"
                "user-agent: * # Public crawlers\r\nALLOW : /\r\nDisallow:\r\n"
                "Crawl-delay: 2\r\nFuture-directive: example\r\n"
                f"sitemap: {self.base}sitemap.xml # Generated sitemap\r\n").encode("utf-8")
        result = self.metadata_response("robots.txt", {"body": body})
        self.assertEqual(result["overall_status"], "HEALTHY")
        self.assertFalse(result["crawl_metadata_results"][0]["byte_parity"])

    def test_live_robots_checks_all_wildcard_groups(self):
        body = daily_audit.build_bytes(self.root / "robots.txt")
        body += b"\nUser-agent: *\nDisallow: /\n"
        self.assert_metadata_failure("robots.txt", {"body": body})

    def test_live_robots_cannot_override_public_policy_for_named_crawlers(self):
        valid = daily_audit.build_bytes(self.root / "robots.txt")
        for agent in ("Googlebot", "googlebot", "Googlebot-News", "Bingbot", "SpecificBot"):
            with self.subTest(agent=agent):
                self.assert_metadata_failure("robots.txt", {"body": valid + f"\nUser-agent: {agent}\nDisallow: /\n".encode()})

    def test_live_sitemap_validates_exact_canonical_inventory(self):
        urls = [self.base + path for path in self.paths]
        for bad in ([], urls[:-1], urls + urls[:1], urls + [""],
                    [url.replace("canonical.example", "foreign.example") for url in urls],
                    [url.replace(self.base, "http://preview.example/review/") for url in urls],
                    urls[:-1] + [self.base + "unexpected.html"],
                    urls[:-1] + [urls[-1] + "?tracking=true"],
                    urls[:-1] + [urls[-1] + "#fragment"]):
            root = ET.Element("urlset", xmlns=site_paths.SITEMAP_NAMESPACE)
            for url in bad:
                ET.SubElement(ET.SubElement(root, "url"), "loc").text = url
            with self.subTest(urls=bad):
                self.assert_metadata_failure("sitemap.xml", {"body": ET.tostring(root)})

    def test_live_sitemap_rejects_malformed_structure_namespace_and_empty_content(self):
        valid = daily_audit.build_bytes(self.root / "sitemap.xml")
        for body in (b"", b"<broken", b"\xff", b"<html>not sitemap</html>",
                     valid.replace(b"schemas/sitemap", b"sitemap"),
                     valid.replace(b"<urlset", b"<sitemapindex").replace(b"</urlset>", b"</sitemapindex>"),
                     valid.replace(b"</urlset>", b"<url /></urlset>"),
                     valid.replace(b"</urlset>", b"<url><loc /><loc /></url></urlset>"),
                     valid.replace(b"</urlset>", b"<url xmlns=''><loc>foreign</loc></url></urlset>"),
                     valid.replace(b"</loc>", b"<nested /></loc>", 1)):
            with self.subTest(body=body):
                self.assert_metadata_failure("sitemap.xml", {"body": body})

    def test_live_sitemap_accepts_equivalent_xml_formatting_and_valid_extensions(self):
        root = ET.Element("urlset", xmlns=site_paths.SITEMAP_NAMESPACE)
        for path in reversed(self.paths):
            entry = ET.SubElement(root, "url")
            ET.SubElement(entry, "loc").text = self.base + path
            ET.SubElement(entry, "lastmod").text = "2026-09-10"
        report = self.metadata_response("sitemap.xml", {"body": ET.tostring(root)})
        self.assertEqual(report["overall_status"], "HEALTHY")
        self.assertEqual(report["crawl_metadata_results"][1]["declared_public_pages"], 10)

    def test_lazy_json_and_social_assets_are_included_and_missing_assets_fail(self):
        for name in ("lazy.png", "social.png", "label.png"):
            (self.root / "assets" / name).write_bytes(b"fixture")
        markup = '<img data-src="assets/lazy.png"><meta property="og:image" content="assets/social.png"><script type="application/json" data-shop-catalog>{"label":{"image":"assets/label.png"}}</script>'
        (self.root / "index.html").write_text(markup, encoding="utf-8")
        report = self.audit()
        self.assertEqual(report["referenced_live_assets"], 5)
        self.assertEqual(report["overall_status"], "HEALTHY")
        (self.root / "assets/label.png").unlink()
        self.assertIn("Missing expected local asset", self.audit()["coverage_errors"][0])

    def test_malformed_embedded_data_cannot_silently_shrink_asset_coverage(self):
        (self.root / "index.html").write_text('<script type="application/json">not json</script>', encoding="utf-8")
        self.assertEqual(self.audit()["overall_status"], "ACTION REQUIRED")

    def test_empty_incomplete_duplicate_and_wrong_domain_sitemaps_fail_closed(self):
        urls = [self.base + path for path in self.paths]
        for bad in ([], urls[:-1], urls + urls[:1], [url.replace("canonical.example", "wrong.example") for url in urls], urls[:-1] + [self.base + "unexpected.html"]):
            with self.subTest(urls=bad):
                self.write_sitemap(bad)
                result = self.audit()
                self.assertEqual(result["overall_status"], "ACTION REQUIRED")
                self.assertTrue(result["coverage_errors"])
                self.assertEqual(result["public_pages"], 0)

    def test_wrong_namespace_is_not_a_healthy_zero_page_audit(self):
        self.write_sitemap([self.base + path for path in self.paths], "http://www.sitemaps.org/sitemap/0.9")
        self.assertIn("namespace", self.audit()["coverage_errors"][0])

    def test_malformed_and_missing_sitemap_produce_actionable_failure(self):
        path = self.root / "sitemap.xml"
        path.write_text("<broken", encoding="utf-8")
        self.assertEqual(self.audit()["overall_status"], "ACTION REQUIRED")
        path.unlink()
        self.assertTrue(self.audit()["coverage_errors"])

    def test_missing_generated_page_cannot_be_skipped(self):
        (self.root / "library.html").unlink()
        self.assertIn("Missing generated", self.audit()["coverage_errors"][0])

    def test_empty_and_missing_asset_coverage_fail_closed(self):
        for path in self.paths:
            (self.root / (path or "index.html")).write_text("<h1>No assets</h1>", encoding="utf-8")
        self.assertIn("Empty asset", self.audit()["coverage_errors"][0])
        (self.root / "index.html").write_text('<img src="assets/missing.png">', encoding="utf-8")
        self.assertIn("Missing expected local asset", self.audit()["coverage_errors"][0])

    def test_page_http_error_and_body_drift_are_not_healthy(self):
        for status, body in ((404, b"missing"), (200, b"wrong build"), (None, b"")):
            with self.subTest(status=status):
                def broken(url):
                    return {"status": status, "body": body, "final_url": url} if url.endswith("library.html") else self.fetch_fixture(url)
                report = self.audit(broken)
                self.assertEqual(report["public_pages"], 10)
                self.assertEqual(len(report["page_regressions"]), 1)
                self.assertEqual(report["overall_status"], "ACTION REQUIRED")

    def test_asset_body_drift_is_not_healthy(self):
        def broken(url):
            return {"status": 200, "body": b"stale", "final_url": url} if url.endswith("pixel.png") else self.fetch_fixture(url)
        self.assertEqual(len(self.audit(broken)["broken_live_assets"]), 1)

    def test_network_failure_becomes_evidence(self):
        with patch.object(daily_audit.urllib.request, "urlopen", side_effect=urllib.error.URLError("offline")):
            response = daily_audit.fetch("https://example.invalid/")
        self.assertIsNone(response["status"])
        self.assertIn("offline", response["error"])

    def test_real_fetch_records_http_and_incomplete_body_errors(self):
        with patch.object(daily_audit.urllib.request, "urlopen", side_effect=urllib.error.HTTPError("https://example.invalid/robots.txt", 404, "missing", {}, None)):
            response = daily_audit.fetch("https://example.invalid/robots.txt")
        self.assertEqual(response["status"], 404)
        self.assertIn("404", response["error"])
        with patch.object(daily_audit.urllib.request, "urlopen") as opener:
            opener.return_value.__enter__.return_value.read.side_effect = http.client.IncompleteRead(b"partial", 50)
            response = daily_audit.fetch("https://example.invalid/sitemap.xml")
        self.assertIsNone(response["status"])
        self.assertIn("IncompleteRead", response["error"])

    def test_cli_exits_nonzero_and_writes_evidence_for_missing_live_metadata(self):
        for relative in ("robots.txt", "sitemap.xml"):
            with self.subTest(relative=relative):
                def missing(url):
                    if url.endswith("/" + relative):
                        return {"status": 404, "body": b"", "final_url": url, "error": "missing fixture"}
                    return self.fetch_fixture(url)
                output = self.root / "reports" / "audit.json"
                argv = ["daily_audit.py", "--root", str(self.root),
                        "--base-url", "http://preview.example/review/", "--audited-sha", "fixture-sha",
                        "--output", str(output)]
                with patch("sys.argv", argv), patch.object(daily_audit, "fetch", side_effect=missing), patch("builtins.print"), self.assertRaises(SystemExit) as failure:
                    daily_audit.main()
                self.assertEqual(failure.exception.code, 1)
                report = json.loads(output.read_text(encoding="utf-8"))
                self.assertEqual(report["overall_status"], "ACTION REQUIRED")
                self.assertEqual(report["audited_repository_sha"], "fixture-sha")
                self.assertEqual(report["public_pages"], 10)
                self.assertEqual([item["path"] for item in report["crawl_metadata_failures"]], [relative])
                self.assertFalse(report["changes_made"])

    def test_invalid_target_url_rejected(self):
        for value in ("", "file:///tmp/", "https://user:password@example.test/", "https://example.test/?q=x"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                site_paths.normalize_base_url(value)


class ProductionContractTests(unittest.TestCase):
    def test_custom_domain_inventory_and_generated_metadata(self):
        self.assertEqual(site_paths.canonical_base_url(ROOT), "https://themindfulmatrixhealth.com/")
        self.assertEqual((ROOT / "CNAME").read_text().strip(), "themindfulmatrixhealth.com")
        paths = site_paths.audited_page_paths(ROOT)
        self.assertEqual(len(paths), 71)
        for relative in paths:
            markup = (ROOT / (relative or "index.html")).read_text(encoding="utf-8")
            self.assertIn(f'rel="canonical" href="https://themindfulmatrixhealth.com/{relative}"', markup)
            self.assertNotIn("themindfulmatrix.github.io/BioCare", markup)

    def test_workflow_targets_custom_domain_and_retains_read_only_boundary(self):
        workflow = (ROOT / ".github/workflows/daily-site-audit.yml").read_text(encoding="utf-8")
        self.assertEqual(workflow.count("--base-url https://themindfulmatrixhealth.com/"), 2)
        self.assertNotIn("contents: write", workflow)
        self.assertNotIn("pages: write", workflow)

    def test_reduced_motion_reaches_functional_library_initialization(self):
        # Execute the shipped JS with a minimal DOM; the old global early return
        # never registered either listener, so this fails on the production bug.
        program = r'''
const fs=require('fs'),vm=require('vm');
const listeners={};
const field={value:'',textContent:'',setAttribute(){},addEventListener(){}};
const controls={querySelector(){return field;},addEventListener(name,fn){listeners[name]=fn;}};
const document={documentElement:{classList:{add(){}}},getElementById(){return null;},querySelector(s){return s==='[data-library-controls]'?controls:null;},querySelectorAll(){return [];},addEventListener(){}};
const window={matchMedia(){return {matches:true};},addEventListener(){},setTimeout};
vm.runInNewContext(fs.readFileSync(process.argv[1],'utf8'),{document,window,URL,URLSearchParams,location:{search:''},history:{}});
if(!listeners.input||!listeners.reset)throw new Error('Library initialization skipped for reduced motion');
'''
        result = subprocess.run(["node", "-e", program, str(ROOT / "assets/js/enhancements.js")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_xtend_description_and_human_review_status_are_preserved(self):
        catalog = json.loads((ROOT / "content/catalog.json").read_text(encoding="utf-8"))
        product = next(item for item in catalog["products"] if item["id"] == "xtend-plus")
        self.assertEqual(product["description"], "Multi-immune food supplement with 22 naturally derived micro- and phytonutrients")
        claims = json.loads((ROOT / "content/compliance/claims.json").read_text(encoding="utf-8"))
        claim = next(item for item in claims["claims"] if item["claim_id"] == "CLAIM_PRODUCT_XTEND_PLUS_DESCRIPTION")
        self.assertEqual(claim["review_status"], "HUMAN_REVIEW_REQUIRED")
        self.assertEqual(claim["compliance_state"], "YELLOW")


if __name__ == "__main__":
    unittest.main()
