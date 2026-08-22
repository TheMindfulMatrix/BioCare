import json
import re
import unicodedata
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def normalize(value):
    text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode("ascii")
    text = text.casefold().replace("&", " and ").replace("+", " ")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text)).strip()


def _values(value):
    if isinstance(value, list):
        return value
    return [] if value is None else [value]


def search_score(record, raw_query):
    query = normalize(raw_query)
    if not query:
        return None
    compact = query.replace(" ", "")
    terms = query.split()
    title = normalize(record.get("title"))
    aliases = [normalize(value) for value in _values(record.get("searchAliases") or record.get("aliases"))]
    verified = [normalize(value) for key in ("searchTerms", "topicIds", "verifiedIngredients") for value in _values(record.get(key))]
    manufacturer_title = normalize(f'{record.get("manufacturer", "")} {record.get("title", "")}')
    category = normalize(" ".join(str(record.get(key) or "") for key in ("category", "intent", "department", "productKind", "type", "searchGroup")))
    summary = normalize(f'{record.get("summary", "")} {record.get("description", "")}')
    broader = normalize(" ".join(str(record.get(key) or "") for key in ("publisher", "resourceType", "evidenceRole", "independence")) + " " + " ".join(str(value) for key in ("keywords", "terms", "topics", "products", "intents") for value in _values(record.get(key))))
    candidates = []

    def consider(value, reason):
        candidates.append((value, reason))

    all_terms = lambda text: bool(terms) and all(term in text for term in terms)
    all_whole = lambda text: bool(terms) and all(f" {term} " in f" {text} " for term in terms)
    if title == query:
        consider(1300, "exact-title")
    if title.replace(" ", "") == compact:
        consider(1260, "exact-title-compact")
    if title.startswith(query):
        consider(1050, "title-prefix")
    if all_whole(title):
        consider(920, "all-title-terms")
    for alias in aliases:
        if alias == query or alias.replace(" ", "") == compact:
            consider(900, "exact-alias")
        elif alias.startswith(query):
            consider(820, "alias-prefix")
        elif all_terms(alias):
            consider(780, "alias-terms")
    if all_whole(title):
        consider(760 + min(len(terms), 5) * 8, "whole-word-title")
    if any(value == query or value.replace(" ", "") == compact for value in verified):
        consider(700, "verified-term-exact")
    if any(all_terms(value) for value in verified):
        consider(640, "verified-term")
    if all_terms(manufacturer_title):
        consider(520, "manufacturer-title")
    if all_terms(category):
        consider(360, "category-intent-kind")
    if all_terms(summary):
        consider(230, "summary")
    if all_terms(broader):
        consider(120, "broader-metadata")
    if not candidates:
        return None
    base, reason = max(candidates)
    return base + int(record.get("searchPriority") or 0), reason


def ranked(records, query, record_type=None):
    scored = []
    seen = set()
    for position, record in enumerate(records):
        if record_type and record["type"] != record_type:
            continue
        result = search_score(record, query)
        key = (record["type"], record["id"])
        if result is None or key in seen:
            continue
        seen.add(key)
        scored.append((record, result[0], int(record.get("order", position)), result[1]))
    scored.sort(key=lambda item: (-item[1], item[2], item[0]["id"]))
    return scored


class V11CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.shop = (ROOT / "shop.html").read_text(encoding="utf-8")
        cls.home_template = (ROOT / "templates/index.html").read_text(encoding="utf-8")
        cls.shop_template = (ROOT / "templates/shop.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
        cls.js = (ROOT / "assets/js/enhancements.js").read_text(encoding="utf-8")
        cls.relevance_js = (ROOT / "assets/js/search-relevance.js").read_text(encoding="utf-8")
        cls.catalog = json.loads((ROOT / "content/catalog.json").read_text(encoding="utf-8"))
        cls.library = json.loads((ROOT / "content/library.json").read_text(encoding="utf-8"))
        cls.discovery = json.loads((ROOT / "content/discovery.json").read_text(encoding="utf-8"))
        cls.sources = json.loads((ROOT / "content/resources/public-sources.json").read_text(encoding="utf-8"))
        cls.search_index = json.loads((ROOT / "assets/data/search-index.json").read_text(encoding="utf-8"))
        payload = re.search(r'<script type="application/json" data-shop-catalog>(.*?)</script>', cls.shop, flags=re.S)
        cls.shop_payload = json.loads(payload.group(1))
        cls.active = [product for product in cls.catalog["products"] if product["commercial_status"] == "active"]

    def test_two_stage_homepage_order_and_static_visibility(self):
        hero = self.home.index('data-home-stage="product"')
        grand = self.home.index('data-home-stage="matrix"')
        departments = self.home.index('aria-labelledby="home-departments-title"')
        self.assertLess(hero, grand)
        self.assertLess(grand, departments)
        self.assertIn('loading="eager"', self.home[hero:grand])
        self.assertNotIn('class="home-discovery', self.home)
        self.assertRegex(self.home_template, r'</section>\s*<section id="matrix-entry"')
        self.assertIn(".grand-entry [data-reveal] { opacity:1!important; transform:none!important; }", self.css)

    def test_grand_entry_narrative_actions_and_derived_metrics(self):
        for text in (
            "Information → Education → Action",
            "See what exists.",
            "Understand what it means.",
            "Decide what makes sense.",
            "Start getting informed",
            "Explore the Matrix",
            "Inspect the evidence",
            "What do you want to understand?",
        ):
            self.assertIn(text, self.home)
        expected = {
            "curated products": len(self.active),
            "practical guides": sum(article["status"] == "published" for article in self.library["articles"]),
            "departments": len(self.discovery["departments"]),
            "public sources": sum(record["status"] == "published" for record in self.sources["records"]),
            "testing journeys": len(self.discovery["journeys"]),
        }
        for label, count in expected.items():
            self.assertIn(f"<strong>{count:02d}</strong><span>{label}</span>", self.home)

    def test_products_opening_has_one_count_and_no_local_search(self):
        order = [
            self.shop.index('class="shop-hero shop-hero--compact'),
            self.shop.index('class="shop-featured-section'),
            self.shop.index('class="catalog-intents'),
            self.shop.index('class="catalog-toolbar'),
            self.shop.index('class="catalog-grid'),
        ]
        self.assertEqual(order, sorted(order))
        self.assertEqual(1, self.shop.count("45</strong> curated products"))
        self.assertNotIn("data-shop-search", self.shop)
        self.assertNotIn("catalog-search", self.shop_template)
        self.assertIn('class="header-search"', self.shop)
        self.assertIn("Featured testing journey", self.shop)
        self.assertIn('data-product-open="balance-basic-kit"', self.shop)
        self.assertIn('legacyParams.has("q")', self.js)
        self.assertIn('new URL("explore.html", location.href)', self.js)

    def test_weighted_search_and_vitamin_matrix(self):
        self.assertIn("window.MatrixSearchRelevance", self.js)
        self.assertIn("searchRelevance.rank", self.js)
        self.assertIn("exact-title", self.relevance_js)
        self.assertIn("canonicalOrder", self.relevance_js)
        expected_prefix = [
            "vitamin-d-test",
            "balanceoil-plus-vegan",
            "zinoshine-plus",
            "protect-plus",
            "balanceoil-plus-300ml",
            "xtend-plus",
            "biolimitless-vitamin-d3-k2",
        ]
        for query in ("vitamin", "vitamin d"):
            self.assertEqual(expected_prefix, [item[0]["id"] for item in ranked(self.search_index, query, "product")[:7]])
        self.assertEqual("vitamin-d-test", ranked(self.search_index, "vitamin d test", "product")[0][0]["id"])
        for query in ("d3k2", "d3 k2", "vitamin d3 k2"):
            self.assertEqual("biolimitless-vitamin-d3-k2", ranked(self.search_index, query, "product")[0][0]["id"])
        self.assertEqual("balance-test", ranked(self.search_index, "Balance Test", "product")[0][0]["id"])
        self.assertEqual([], ranked(self.search_index, "no-such-matrix-result"))

    def test_search_groups_are_stable_and_unique(self):
        for query in ("omega", "magnesium", "collagen", "label", "evidence", "sources", "testing", "Zinzino", "BioLimitless"):
            results = ranked(self.search_index, query)
            self.assertTrue(results, query)
            identities = [(item[0]["type"], item[0]["id"]) for item in results]
            self.assertEqual(len(identities), len(set(identities)))
        for label in ("Products", "Learn", "Sources", "Journeys", "Departments"):
            self.assertIn(f'label:"{label}"', self.js)

    def test_search_metadata_is_factual_and_verified_ingredients_remain_locked(self):
        labels = json.loads((ROOT / "content/product-labels.json").read_text(encoding="utf-8"))
        approved = {record["product_id"]: [item["ingredient"] for item in record["ingredients"]] for record in labels["records"] if record["status"] == "approved"}
        for record in (item for item in self.search_index if item["type"] == "product"):
            self.assertEqual(approved.get(record["id"], []), record["verifiedIngredients"])
            aliases = " ".join(record.get("searchAliases", [])).casefold()
            self.assertNotRegex(aliases, r"diagnos|disease|symptom|treat|cure|prevent")
        zinzino_k2 = [record for record in self.search_index if record["type"] == "product" and record.get("manufacturer") == "Zinzino" and any("k2" in normalize(alias) for alias in record.get("searchAliases", []))]
        self.assertEqual([], zinzino_k2)

    def test_inspector_primary_view_is_simplified_but_payload_is_complete(self):
        for token in ("SKU</dt>", "Format</dt>", "Type</dt>", "Pricing source</dt>", "product-inspector__facts"):
            self.assertNotIn(token, self.js)
        for token in ("Learn more", "Evidence &amp; Documentation", "Manufacturer transparency", "Official product source", "Price checked"):
            self.assertIn(token, self.js)
        for record in self.shop_payload["products"]:
            for key in ("sku", "variantLabel", "productKind", "price", "label", "documentation", "department"):
                self.assertIn(key, record)

    def test_load_more_is_append_only_and_accessibly_announced(self):
        self.assertIn("grid.appendChild(markupFragment(additions", self.js)
        self.assertIn("grid.replaceChildren(markupFragment(visible", self.js)
        self.assertNotIn("grid.innerHTML", self.js)
        self.assertIn('loadMore.addEventListener("click", appendMoreProducts)', self.js)
        self.assertIn("products are now visible", self.js)
        self.assertNotIn("loadStatus.focus", self.js)
        self.assertIn('aria-live="polite" aria-atomic="true"', self.shop)


if __name__ == "__main__":
    unittest.main()
