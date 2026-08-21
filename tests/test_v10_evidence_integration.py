from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EvidenceIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads((ROOT / "content" / "resources" / "public-sources.json").read_text(encoding="utf-8"))
        cls.published = [record for record in cls.manifest["records"] if record["status"] == "published"]
        cls.evidence = (ROOT / "evidence.html").read_text(encoding="utf-8")
        cls.search_index = json.loads((ROOT / "assets" / "data" / "search-index.json").read_text(encoding="utf-8"))
        shop = (ROOT / "shop.html").read_text(encoding="utf-8")
        match = re.search(r'<script type="application/json" data-shop-catalog>(.*?)</script>', shop, flags=re.S)
        assert match
        cls.shop_payload = json.loads(match.group(1))

    def test_evidence_page_renders_published_records_only(self) -> None:
        published_ids = {record["id"] for record in self.published}
        rendered_ids = set(re.findall(r'data-public-source="([^"]+)"', self.evidence))
        self.assertEqual(rendered_ids, published_ids)
        self.assertEqual(self.evidence.count('data-public-source="'), len(self.published))

    def test_search_index_has_a_distinct_source_type(self) -> None:
        source_records = [record for record in self.search_index if record["type"] == "source"]
        self.assertEqual({record["id"] for record in source_records}, {record["id"] for record in self.published})
        self.assertTrue(all(record.get("publisher") and record.get("resourceType") for record in source_records))

    def test_every_active_product_has_public_context_with_explicit_relationship(self) -> None:
        self.assertEqual(len(self.shop_payload["products"]), 45)
        allowed = {"product-specific context", "department context — not product evidence"}
        public_ids = {record["id"] for record in self.published}
        for product in self.shop_payload["products"]:
            with self.subTest(product=product["id"]):
                self.assertTrue(product["documentation"])
                self.assertTrue({record["relationship"] for record in product["documentation"]} <= allowed)
                self.assertTrue({record["id"] for record in product["documentation"]} <= public_ids)

    def test_filters_and_progressive_disclosure_are_wired(self) -> None:
        for field in ("topic", "type", "manufacturer", "product", "department", "independence"):
            self.assertIn(f'data-evidence-filter="{field}"', self.evidence)
        script = (ROOT / "assets" / "js" / "enhancements.js").read_text(encoding="utf-8")
        self.assertIn("function initEvidence(root)", script)
        self.assertIn("function documentationMarkup(product)", script)

    def test_private_source_material_does_not_leak(self) -> None:
        public_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "evidence.html", ROOT / "assets" / "data" / "search-index.json", ROOT / "shop.html")
        )
        self.assertNotIn("zinzino-library", public_text.lower())
        self.assertNotIn("de8c7711a5ca4678d92dd0d0a3ebeba06f7334c7", public_text)
        self.assertNotRegex(public_text.lower(), r'(?:href|src)=["\'][^"\']*\.txt(?:[?#"\'])')


if __name__ == "__main__":
    unittest.main()
