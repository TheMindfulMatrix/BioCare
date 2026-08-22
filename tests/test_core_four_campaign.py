import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class CoreFourCampaignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.campaign = json.loads((ROOT / "content/campaigns/core-four.json").read_text(encoding="utf-8"))
        cls.catalog = json.loads((ROOT / "content/catalog.json").read_text(encoding="utf-8"))
        cls.products = {item["id"]: item for item in cls.catalog["products"]}

    def test_exactly_four_unique_active_products_in_order(self):
        expected = ["balanceoil-plus-300ml", "biolimitless-vitamin-d3-k2", "biolimitless-zinc-copper", "biolimitless-magnesium-glycinate"]
        self.assertEqual(self.campaign["productIds"], expected)
        self.assertEqual(len(set(expected)), 4)
        self.assertEqual([item["productId"] for item in sorted(self.campaign["items"], key=lambda row: row["position"])], expected)
        self.assertTrue(all(self.products[item].get("commercial_status") == "active" for item in expected))

    def test_campaign_derives_commercial_facts(self):
        serialized = json.dumps(self.campaign)
        for field in ("price", "manufacturer", "destination", "cutout", "sku"):
            self.assertNotIn(f'"{field}"', serialized)

    def test_campaign_page_and_sitemap(self):
        page = (ROOT / "core-four.html").read_text(encoding="utf-8")
        self.assertEqual(page.count("<h1"), 1)
        self.assertIn("The Core Four | The Mindful Matrix", page)
        self.assertIn("CollectionPage", page)
        self.assertIn("core-four.html", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))

    def test_product_pages_have_editorial_marker(self):
        for product_id in self.campaign["productIds"]:
            page = (ROOT / "products" / f"{product_id}.html").read_text(encoding="utf-8")
            self.assertIn("Why it is in The Core Four", page)
            self.assertIn("not a universal recommendation", page)

    def test_search_and_filters_are_wired(self):
        search = json.loads((ROOT / "assets/data/search-index.json").read_text(encoding="utf-8"))
        campaign = [item for item in search if item.get("id") == "core-four"]
        self.assertEqual(len(campaign), 1)
        self.assertEqual(campaign[0]["href"], "core-four.html")
        shop = (ROOT / "shop.html").read_text(encoding="utf-8")
        self.assertIn('data-shop-collection="core-four"', shop)
        payload = json.loads(shop.split('<script type="application/json" data-shop-catalog>', 1)[1].split("</script>", 1)[0])
        filtered = sorted((item for item in payload["products"] if item["coreFour"]), key=lambda item: item["coreFourPosition"])
        self.assertEqual([item["id"] for item in filtered], self.campaign["productIds"])

    def test_claim_and_private_boundaries(self):
        public = "\n".join((ROOT / path).read_text(encoding="utf-8").lower() for path in ["core-four.html", "index.html", "shop.html"])
        for prohibited in ("everyone needs", "essential for everyone", "prevents disease", "boosts immunity", "balances hormones", "doctor recommended"):
            self.assertNotIn(prohibited, public)
        self.assertNotIn("de8c7711a5ca4678d92dd0d0a3ebeba06f7334c7", public)

if __name__ == "__main__": unittest.main()
