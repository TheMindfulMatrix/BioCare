import json
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class V8DiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "content/catalog.json").read_text(encoding="utf-8"))
        cls.library = json.loads((ROOT / "content/library.json").read_text(encoding="utf-8"))
        cls.discovery = json.loads((ROOT / "content/discovery.json").read_text(encoding="utf-8"))
        cls.index = json.loads((ROOT / "assets/data/search-index.json").read_text(encoding="utf-8"))
        cls.active = [p for p in cls.catalog["products"] if p["commercial_status"] == "active"]

    def test_complete_canonical_representation(self):
        self.assertEqual({p["id"] for p in self.active}, {r["id"] for r in self.index if r["type"] == "product"})
        self.assertEqual({a["slug"] for a in self.library["articles"] if a["status"] == "published"}, {r["id"] for r in self.index if r["type"] == "guide"})
        self.assertEqual({d["intentId"] for d in self.discovery["departments"]}, {r["id"] for r in self.index if r["type"] == "department"})
        self.assertEqual({j["id"] for j in self.discovery["journeys"]}, {r["id"] for r in self.index if r["type"] == "journey"})

    def test_deferred_products_are_excluded(self):
        deferred = {p["id"] for p in self.catalog["products"] if p["commercial_status"] != "active"}
        self.assertTrue(deferred.isdisjoint({r["id"] for r in self.index}))

    def test_only_verified_label_ingredients_are_indexed(self):
        labels = json.loads((ROOT / "content/product-labels.json").read_text(encoding="utf-8"))
        approved = {r["product_id"] for r in labels["records"] if r["status"] == "approved"}
        for record in (r for r in self.index if r["type"] == "product"):
            self.assertFalse(record.get("ingredients")) if record["id"] not in approved else None

    def test_all_six_department_routes_and_derived_counts(self):
        self.assertEqual(6, len(self.discovery["departments"]))
        published = {a["slug"] for a in self.library["articles"] if a["status"] == "published"}
        for department in self.discovery["departments"]:
            page = (ROOT / "departments" / f'{department["slug"]}.html').read_text(encoding="utf-8")
            product_count = sum(p["intent"] == department["intentId"] for p in self.active)
            guide_count = sum(slug in published for slug in department["articleSlugs"])
            self.assertIn(f"{product_count} products · {guide_count} guides", page)

    def test_search_modes_and_multi_term_matching(self):
        def search(query, mode="everything"):
            terms = query.casefold().split()
            allowed = lambda r: mode == "everything" or (mode == "products" and r["type"] == "product") or (mode == "learn" and r["type"] in {"guide", "journey", "department"})
            return [r for r in self.index if allowed(r) and all(term in json.dumps(r).casefold() for term in terms)]
        self.assertTrue(any(r["id"] == "balance-test" for r in search("BALANCEtest", "products")))
        self.assertTrue(search("omega numbers", "learn"))
        self.assertTrue(search("omega"))
        self.assertEqual([], search("no-such-matrix-result"))

    def test_visual_layers_are_decorative_and_environment_driven(self):
        pages = [ROOT / "index.html", ROOT / "explore.html", ROOT / "know-your-number.html"]
        pages.extend((ROOT / "departments").glob("*.html"))
        for page in pages:
            markup = page.read_text(encoding="utf-8")
            self.assertIn('class="matrix-visual', markup)
            self.assertIn('aria-hidden="true"', markup)
        css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
        self.assertIn("pointer-events:none", css)
        self.assertIn("prefers-reduced-motion:reduce", css)
        for environment in {item["environment"] for item in self.catalog["intents"]}:
            self.assertIn(f'data-environment="{environment}"', (ROOT / "index.html").read_text(encoding="utf-8") + "".join(page.read_text(encoding="utf-8") for page in (ROOT / "departments").glob("*.html")))

    def test_visual_pass_adds_no_runtime_dependency(self):
        markup = (ROOT / "index.html").read_text(encoding="utf-8")
        scripts = [part.split('"', 1)[0] for part in markup.split('<script defer src="')[1:]]
        versions = {
            path: hashlib.sha256((ROOT / path).read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")).hexdigest()[:12]
            for path in ("assets/js/search-relevance.js", "assets/js/enhancements.js")
        }
        self.assertEqual([f"{path}?v={versions[path]}" for path in versions], scripts)
        enhancements = (ROOT / "assets/js/enhancements.js").read_text(encoding="utf-8")
        self.assertIn("root.dataset.universeFilterIds=ids.join", enhancements)
        self.assertIn("root.hidden=matches.length===0", enhancements)
        self.assertIn("b.disabled=availableIntents.indexOf", enhancements)


if __name__ == "__main__":
    unittest.main()
