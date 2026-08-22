from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
import urllib.parse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("daily_site_audit", ROOT / "scripts" / "daily_site_audit.py")
assert SPEC and SPEC.loader
audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = audit
SPEC.loader.exec_module(audit)


class DailySiteAuditTests(unittest.TestCase):
    base = "https://example.test/BioCare/"

    def make_site(self, root: Path) -> None:
        (root / "assets").mkdir()
        (root / "index.html").write_text(
            '<!doctype html><html><head><link rel="preconnect" href="https://fonts.example">'
            '<link rel="stylesheet" href="assets/site.css?v=1"></head>'
            '<body><img src="assets/logo.svg" alt=""><a href="about.html">About</a>'
            '<a href="https://external.test/reference">Reference</a></body></html>\n',
            encoding="utf-8",
        )
        (root / "about.html").write_text(
            '<!doctype html><html><body><a href="./">Home</a></body></html>\n',
            encoding="utf-8",
        )
        (root / "assets" / "site.css").write_text(
            '.brand { background-image: url("./logo.svg"); }\n',
            encoding="utf-8",
        )
        (root / "assets" / "logo.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>\n", encoding="utf-8")
        (root / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f"<url><loc>{self.base}</loc></url>"
            f"<url><loc>{self.base}about.html</loc></url>"
            "</urlset>\n",
            encoding="utf-8",
        )

    def fetcher_for(self, root: Path, *, corrupt_index: bool = False):
        def fetcher(url: str, **_kwargs):
            parsed = urllib.parse.urlsplit(url)
            relative = parsed.path.removeprefix("/BioCare/") or "index.html"
            body = (root / relative).read_bytes()
            if corrupt_index and relative == "index.html":
                body += b"changed"
            content_type = "text/html" if relative.endswith(".html") else "image/svg+xml" if relative.endswith(".svg") else "text/css"
            return audit.FetchResult(url, url, 200, content_type, body)

        return fetcher

    def test_normalize_base_and_safe_path_mapping(self):
        self.assertEqual(audit.normalize_base("https://example.test/BioCare"), self.base)
        with self.assertRaises(ValueError):
            audit.normalize_base("http://example.test/BioCare/")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(
                audit.url_to_local_path(self.base, self.base, root),
                root.resolve() / "index.html",
            )
            with self.assertRaises(ValueError):
                audit.url_to_local_path("https://example.test/Other/index.html", self.base, root)

    def test_component_status_validation(self):
        self.assertEqual(audit.parse_component_status(["build=0", "validate=2"]), {"build": 0, "validate": 2})
        with self.assertRaises(ValueError):
            audit.parse_component_status(["validate=not-a-number"])

    def test_happy_path_audits_every_page_and_internal_resource(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_site(root)
            report = audit.run_audit(
                repository_root=root,
                production_base=self.base,
                component_statuses={"build": 0, "validate": 0},
                timeout=1,
                workers=2,
                check_external=False,
                fetcher=self.fetcher_for(root),
            )
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["publicPages"], {"checked": 2, "passed": 2, "warnings": 0, "failed": 0})
        self.assertEqual(report["internalResources"], {"checked": 2, "passed": 2, "warnings": 0, "failed": 0})
        self.assertEqual(report["externalLinks"]["discovered"], 1)
        self.assertEqual(report["externalLinks"]["checked"], 0)

    def test_byte_mismatch_and_component_failure_fail_the_audit(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_site(root)
            report = audit.run_audit(
                repository_root=root,
                production_base=self.base,
                component_statuses={"build": 1},
                timeout=1,
                workers=2,
                check_external=False,
                fetcher=self.fetcher_for(root, corrupt_index=True),
            )
        self.assertEqual(report["status"], "fail")
        self.assertEqual(report["publicPages"]["failed"], 1)
        self.assertEqual(report["totals"]["failures"], 2)

    def test_external_link_classification_avoids_protected_site_noise(self):
        protected = audit.external_link_check(
            "https://protected.test/",
            lambda url, **_kwargs: audit.FetchResult(url, url, 403, "text/html", b"", "forbidden"),
            1,
        )
        missing = audit.external_link_check(
            "https://missing.test/",
            lambda url, **_kwargs: audit.FetchResult(url, url, 404, "text/html", b"", "not found"),
            1,
        )
        self.assertEqual(protected.status, "warning")
        self.assertEqual(missing.status, "fail")

    def test_markdown_report_is_safe_for_issue_reuse(self):
        report = {
            "status": "pass",
            "generatedAtUtc": "2026-08-21T08:00:00Z",
            "repositorySha": "abc123",
            "productionBase": self.base,
            "trigger": "schedule",
            "runUrl": "https://github.com/example/actions/runs/1",
            "componentStatuses": {"build": 0},
            "publicPages": {"checked": 2, "passed": 2, "warnings": 0, "failed": 0},
            "internalResources": {"checked": 2, "passed": 2, "warnings": 0, "failed": 0},
            "externalLinks": {"checked": 1, "passed": 1, "warnings": 0, "failed": 0},
            "checks": [],
        }
        rendered = audit.markdown_report(report)
        self.assertIn("<!-- biocare-daily-audit -->", rendered)
        self.assertIn("**Status: PASS**", rendered)
        self.assertIn("made no website, branch, deployment, or pull-request changes", rendered)


if __name__ == "__main__":
    unittest.main()
