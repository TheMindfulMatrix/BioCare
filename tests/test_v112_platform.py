import json
import html
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class V112PlatformTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "content/catalog.json").read_text(encoding="utf-8"))
        cls.active = [p for p in cls.catalog["products"] if p.get("commercial_status") == "active"]

    def test_every_active_product_has_one_dedicated_page(self):
        actual = {p.stem for p in (ROOT / "products").glob("*.html")}
        self.assertEqual(actual, {p["id"] for p in self.active})
        for product in self.active:
            page = (ROOT / "products" / f'{product["id"]}.html').read_text(encoding="utf-8")
            self.assertIn(f'<h1>{html.escape(product["name"])}</h1>', page)
            self.assertIn('Department context — not product-specific evidence', page)

    def test_product_schema_has_no_unverified_commercial_or_review_data(self):
        prohibited = {"offers", "aggregateRating", "review"}
        for path in (ROOT / "products").glob("*.html"):
            payloads = re.findall(r'<script type="application/ld\+json">(.*?)</script>', path.read_text(encoding="utf-8"), re.S)
            joined = json.dumps([json.loads(item) for item in payloads])
            for key in prohibited:
                self.assertNotIn(f'"{key}"', joined)

    def test_search_and_cards_route_to_product_pages(self):
        index = json.loads((ROOT / "assets/data/search-index.json").read_text(encoding="utf-8"))
        products = [item for item in index if item["type"] == "product"]
        self.assertEqual(len(products), len(self.active))
        self.assertTrue(all(item["href"].startswith("products/") for item in products))
        self.assertIn('href="products/balance-basic-kit.html"', (ROOT / "shop.html").read_text(encoding="utf-8"))

    def test_mobile_dock_and_library_filters_are_permanent(self):
        for page in (ROOT / "index.html", ROOT / "products/balance-basic-kit.html", ROOT / "library.html"):
            self.assertIn('class="mobile-dock"', page.read_text(encoding="utf-8"))
        library = (ROOT / "library.html").read_text(encoding="utf-8")
        self.assertIn("data-library-controls", library)
        self.assertIn("data-library-category", library)

    def test_relationship_rules_are_explicit(self):
        relationships = json.loads((ROOT / "content/relationships.json").read_text(encoding="utf-8"))
        self.assertEqual(relationships["schemaVersion"], "1.0")
        self.assertIn("productEvidence", relationships["rules"])
        self.assertIn("relatedProducts", relationships["rules"])


if __name__ == "__main__":
    unittest.main()
