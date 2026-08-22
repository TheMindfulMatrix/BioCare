import hashlib
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import build

ROOT = Path(__file__).resolve().parents[1]


class V102HardeningTests(unittest.TestCase):
    def test_generated_assets_use_content_hashes(self):
        markup = (ROOT / "index.html").read_text(encoding="utf-8")
        for relative in (
            "assets/css/tokens.css",
            "assets/css/base.css",
            "assets/css/site.css",
            "assets/js/search-relevance.js",
            "assets/js/enhancements.js",
        ):
            canonical = (ROOT / relative).read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
            digest = hashlib.sha256(canonical).hexdigest()[:12]
            self.assertIn(f'{relative}?v={digest}', markup)
        self.assertNotIn("v11-candidate-1", markup)

    def test_asset_version_is_stable_and_invalidates_on_content_change(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset = root / "assets/test.css"
            asset.parent.mkdir(parents=True)
            asset.write_text("body{color:#111}", encoding="utf-8")
            with patch.object(build, "ROOT", root):
                first = build.asset_version("assets/test.css")
                self.assertEqual(first, build.asset_version("assets/test.css"))
                asset.write_text("body{color:#222}", encoding="utf-8")
                self.assertNotEqual(first, build.asset_version("assets/test.css"))

    def test_source_artwork_is_outside_public_assets(self):
        self.assertFalse((ROOT / "assets/source-artwork").exists())
        archive = ROOT / "_source-assets/source-artwork"
        self.assertTrue(archive.is_dir())
        self.assertGreater(len(list(archive.rglob("*.png"))), 0)

    def test_asset_inventory_is_deterministic(self):
        command = ["python", "scripts/asset_inventory.py"]
        first = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True).stdout
        second = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True).stdout
        self.assertEqual(first, second)
        payload = json.loads(first)
        self.assertGreater(payload["excluded_source_archive_bytes"], 20_000_000)

    def test_daily_workflow_uses_default_branch_without_checkout_credentials(self):
        workflow = (ROOT / ".github/workflows/daily-site-audit.yml").read_text(encoding="utf-8")
        self.assertIn("github.event.repository.default_branch", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertNotRegex(workflow, re.compile(r"git (?:reset|clean|switch|checkout)"))
        self.assertNotIn("pull_request", workflow)
        self.assertNotIn("issues: write", workflow)


if __name__ == "__main__":
    unittest.main()
