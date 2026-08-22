import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class V9MobileCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "content/catalog.json").read_text(encoding="utf-8"))
        cls.labels = json.loads((ROOT / "content/product-labels.json").read_text(encoding="utf-8"))
        cls.site = json.loads((ROOT / "content/site.json").read_text(encoding="utf-8"))
        cls.active = [product for product in cls.catalog["products"] if product["commercial_status"] == "active"]
        cls.deferred = [product for product in cls.catalog["products"] if product["commercial_status"] != "active"]
        cls.shop = (ROOT / "shop.html").read_text(encoding="utf-8")
        cls.template = (ROOT / "templates/shop.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
        cls.js = (ROOT / "assets/js/enhancements.js").read_text(encoding="utf-8")
        match = re.search(r'<script type="application/json" data-shop-catalog>(.*?)</script>', cls.shop, flags=re.S)
        if not match:
            raise AssertionError("V9 catalog payload missing")
        cls.payload = json.loads(match.group(1))

    def test_authoritative_inventory_and_payload(self):
        self.assertEqual(45, len(self.active))
        self.assertEqual(8, len(self.deferred))
        self.assertEqual(45, self.payload["activeCount"])
        self.assertEqual(12, self.payload["initialCount"])
        self.assertEqual([product["id"] for product in self.active], [record["id"] for record in self.payload["products"]])
        self.assertTrue({product["id"] for product in self.deferred}.isdisjoint({record["id"] for record in self.payload["products"]}))

    def test_locked_mobile_page_order(self):
        markers = [
            'class="shop-hero shop-hero--compact',
            'class="shop-featured-section',
            'class="catalog-intents',
            'class="catalog-toolbar',
            'class="catalog-disclosure-line',
            'class="catalog-grid',
            'class="shop-learn',
            'class="shop-disclosures',
        ]
        positions = [self.shop.index(marker) for marker in markers]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("Every verified product", self.shop)
        self.assertLess(self.shop.index('class="catalog-grid'), self.shop.index(self.site["site"]["affiliateDisclosure"]))

    def test_horizontal_intent_rail_uses_canonical_intents(self):
        self.assertEqual(7, self.shop.count("data-shop-intent="))
        self.assertIn('data-shop-intent="all" aria-pressed="true"', self.shop)
        self.assertIn("<strong>Testing</strong>", self.shop)
        for intent in self.catalog["intents"]:
            self.assertIn(f'data-shop-intent="{intent["id"]}"', self.shop)
            self.assertIn(f'id="intent-{intent["id"]}"', self.shop)
        self.assertIn('role="group" aria-label="Product intents"', self.shop)

    def test_progressive_compact_grid(self):
        self.assertEqual(12, self.shop.count("data-shop-product"))
        self.assertEqual(3, self.shop.count('loading="eager"'))
        self.assertEqual(10, self.shop.count('loading="lazy"'))
        self.assertEqual(12, self.shop.count('class="catalog-card__inspect"'))
        self.assertIn("appendMoreProducts", self.js)
        self.assertIn("grid.appendChild(markupFragment", self.js)
        self.assertIn("matches.slice(0, Math.min(limit, matches.length))", self.js)

    def test_two_column_mobile_density_and_safe_fallback(self):
        self.assertIn(".catalog-grid { grid-template-columns:repeat(2,minmax(0,1fr));", self.css)
        self.assertIn("@media (max-width:20.5rem)", self.css)
        self.assertIn(".catalog-grid { grid-template-columns:1fr; }", self.css)
        self.assertIn("aspect-ratio:1", self.css)
        self.assertIn("object-fit:contain", self.css)

    def test_search_filter_sort_and_url_state(self):
        self.assertNotIn("Search all 45 curated products", self.shop)
        self.assertNotIn("data-shop-search", self.shop)
        self.assertIn('class="header-search"', self.shop)
        self.assertIn('value="canonical"', self.shop)
        self.assertIn('value="name"', self.shop)
        self.assertIn('value="manufacturer"', self.shop)
        self.assertNotIn('value="price', self.shop)
        kinds = sorted({product["productKind"] for product in self.active}, key=str.casefold)
        for kind in kinds:
            self.assertIn(f'name="filter-kind" value="{kind}"', self.shop)
        for token in ("URLSearchParams", "popstate", "history.pushState", "history.replaceState", "legacyParams.has(\"q\")"):
            self.assertIn(token, self.js)

    def test_accessible_filter_sheet_and_single_inspector(self):
        self.assertEqual(1, self.shop.count("data-shop-filter-dialog"))
        self.assertEqual(1, self.shop.count("data-product-inspector>"))
        self.assertIn('aria-labelledby="catalog-filter-title"', self.shop)
        self.assertIn('aria-labelledby="product-inspector-title"', self.shop)
        self.assertIn("filterDialog.addEventListener(\"cancel\"", self.js)
        self.assertIn("inspector.addEventListener(\"cancel\"", self.js)
        self.assertIn("lastProductFocusId", self.js)
        self.assertNotIn("data-inspector-product=", self.shop)

    def test_label_states_and_verified_ingredient_search(self):
        payload = {record["id"]: record for record in self.payload["products"]}
        source = {record["product_id"]: record for record in self.labels["records"]}
        states = {record["label"]["state"] for record in payload.values()}
        self.assertEqual({"complete_verified", "partial_verified", "unavailable_or_unverified"}, states)
        for product_id, record in payload.items():
            expected = [item["ingredient"] for item in source[product_id]["ingredients"]] if source[product_id]["status"] == "approved" else []
            self.assertEqual(expected, record["verifiedIngredients"])

    def test_pricing_semantics_remain_canonical(self):
        payload = {record["id"]: record for record in self.payload["products"]}
        for product in self.active:
            self.assertEqual(product["price"]["pricing_model"], payload[product["id"]]["price"]["pricing_model"])
            self.assertEqual(product["price"]["price_verified_at"], payload[product["id"]]["price"]["price_verified_at"])
        for model in ("starter_subscription", "retail_premier", "one_time_autoship", "one_time_range"):
            self.assertIn(f'price.pricing_model === "{model}"', self.js)

    def test_disclosure_proximity_and_no_marketplace_claims(self):
        grid = self.shop.index('class="catalog-grid')
        compact = self.shop.index("Official manufacturer links may earn The Mindful Matrix a commission.")
        full = self.shop.index(self.site["site"]["affiliateDisclosure"])
        self.assertLess(compact, grid)
        self.assertGreater(full, grid)
        self.assertIn('aria-describedby="inspector-source-disclosure"', self.js)
        self.assertIn('rel="sponsored noopener noreferrer"', self.js)
        for prohibited in ("Best Seller", "Most Purchased", "Add to cart", "Prime", "review count", "purchase count"):
            self.assertNotIn(prohibited, self.shop)

    def test_learning_and_no_javascript_routes_remain_available(self):
        for route in ("library.html", "know-your-number.html", "start.html", "explore.html"):
            self.assertIn(f'href="{route}"', self.shop)
        self.assertIn("Learn before you choose.", self.shop)
        self.assertIn("<noscript>", self.shop)
        for product in self.active:
            self.assertIn(product["destination"], self.shop)


if __name__ == "__main__":
    unittest.main()
