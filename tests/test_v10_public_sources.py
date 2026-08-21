from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class PublicSourceManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.promote = load_module("promote_public_sources", ROOT / "scripts" / "promote_public_sources.py")
        cls.validate = load_module("validate_public_sources", ROOT / "scripts" / "validate_public_sources.py")
        cls.manifest = json.loads((ROOT / "content" / "resources" / "public-sources.json").read_text(encoding="utf-8"))

    def test_committed_manifest_is_public_safe(self) -> None:
        result = self.validate.validate_manifest(self.manifest)
        self.assertEqual(result, {"record_count": 8, "published_count": 8, "valid": True})

    def test_private_and_signed_urls_are_rejected(self) -> None:
        for url in (
            "https://github.com/TheMindfulMatrix/zinzino-library/blob/master/docs/example.txt",
            "https://raw.githubusercontent.com/TheMindfulMatrix/zinzino-library/master/docs/example.txt",
            "https://example.com/source.pdf?token=secret",
            "https://zinzinowebstorage.blob.core.windows.net/filelibrary/example.pdf",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                self.promote.validate_public_url(url)

    def test_only_published_records_are_render_eligible(self) -> None:
        records = self.manifest["records"] + [{**self.manifest["records"][0], "id": "pending-example", "public_url": "https://example.gov/pending", "final_url": "https://example.gov/pending", "status": "pending_review"}]
        rendered = [record for record in records if record["status"] == "published"]
        self.assertEqual(len(rendered), 8)

    def test_promotion_rejects_unclear_rights(self) -> None:
        base = self.manifest["records"][0]
        audit = {"source_repo_sha": "abc", "resources": [{"resource_id": base["id"], "rights_classification": "RESEARCH / REFERENCE ONLY", "evidence_role": "research_lead_only"}]}
        allowlist = {"source_repo_sha": "abc", "checked_date": "2026-08-21", "records": [{"resource_id": base["id"], "public_record": copy.deepcopy(base)}]}
        with self.assertRaisesRegex(ValueError, "Rights are not affirmatively public"):
            self.promote.promote(audit, allowlist)


if __name__ == "__main__":
    unittest.main()
