import copy
import hashlib
import json
import unittest
from pathlib import Path

from scripts import build

ROOT = Path(__file__).resolve().parents[1]


class DesktopHeroTests(unittest.TestCase):
    def setUp(self):
        catalog = json.loads((ROOT / "content/catalog.json").read_text(encoding="utf-8"))
        self.product = next(p for p in catalog["products"] if p["id"] == catalog["featuredProductId"])
        self.desktop = self.product["desktopHero"]

    def test_picture_is_desktop_only_and_keeps_accessible_eager_fallback(self):
        markup = build.hero_image_markup(self.product)
        self.assertIn('media="(min-width: 75rem)"', markup)
        self.assertIn('style="display:contents"', markup)
        self.assertIn(build.shelf_product_markup(self.product, eager=True), markup)
        self.assertIn('fetchpriority="high"', markup)
        self.assertEqual(markup.count('<img '), 1)

    def test_other_product_presentations_keep_original_source(self):
        markup = build.shelf_product_markup(self.product)
        self.assertNotIn(self.desktop["src"], markup)
        self.assertIn(self.product["cutout"]["src"], markup)

    def test_products_without_desktop_variant_keep_existing_markup(self):
        product = copy.deepcopy(self.product)
        del product["desktopHero"]
        self.assertEqual(build.hero_image_markup(product), build.shelf_product_markup(product, eager=True))

    def test_asset_and_source_identity_are_pinned_without_new_public_editorial_copy(self):
        asset = ROOT / self.desktop["src"]
        self.assertLess(asset.stat().st_size, 35000)
        self.assertEqual(hashlib.sha256(asset.read_bytes()).hexdigest(),
                         "22f1181bf5af365233e63b0232b18023efe9a4b2f4f0c9e4d4e7e041d20c7b33")
        self.assertEqual((self.desktop["width"], self.desktop["height"]), (650, 650))
        self.assertEqual(hashlib.sha256((ROOT / self.product["cutout"]["sourceAsset"]).read_bytes()).hexdigest(),
                         "b0cf5653d294e964b849076667f554bab71e01a64733ec1ab6544e0f381cb5e1")
        for path in ["index.html", "sitemap.xml", "assets/data/search-index.json"]:
            self.assertNotIn("_review/editorial-hero-review", (ROOT / path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
