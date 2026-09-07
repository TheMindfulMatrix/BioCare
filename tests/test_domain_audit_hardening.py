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
        self.assertEqual(result["public_pages"], 13)
        self.assertEqual(result["referenced_live_assets"], 2)
        self.assertTrue(all(item["byte_parity"] for item in result["page_results"] + result["asset_results"]))

    def test_root_domain_sitemap_maps_to_relative_files(self):
        self.base = "https://new.example/"
        (self.root / "content/site.json").write_text(json.dumps({"site": {"metadata": {"canonicalBaseUrl": self.base}}}), encoding="utf-8")
        self.write_sitemap([self.base + path for path in self.paths])
        self.assertEqual(self.audit()["public_pages"], 13)

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
                self.assertEqual(report["public_pages"], 13)
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

    def test_invalid_target_url_rejected(self):
        for value in ("", "file:///tmp/", "https://user:password@example.test/", "https://example.test/?q=x"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                site_paths.normalize_base_url(value)


class ProductionContractTests(unittest.TestCase):
    def test_custom_domain_inventory_and_generated_metadata(self):
        self.assertEqual(site_paths.canonical_base_url(ROOT), "https://themindfulmatrixhealth.com/")
        self.assertEqual((ROOT / "CNAME").read_text().strip(), "themindfulmatrixhealth.com")
        paths = site_paths.audited_page_paths(ROOT)
        self.assertEqual(len(paths), 88)
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
