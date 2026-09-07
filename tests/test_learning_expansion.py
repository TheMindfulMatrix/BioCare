"""Regression contracts for testing, evidence, and review-only course expansion."""
import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import build, build_learning, site_paths
from scripts.compliance_engine import ComplianceEngine, path_context

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "content" / name).read_text(encoding="utf-8"))


class LearningExpansionTests(unittest.TestCase):
    def test_four_distinct_tests_cover_five_standalone_records(self):
        journeys = load("testing-journeys.json")["journeys"]
        self.assertEqual(len(journeys), 4)
        self.assertEqual({j["id"] for j in journeys}, {"fatty-acids", "gut-markers", "vitamin-d", "hba1c"})
        ids = [pid for journey in journeys for pid in journey["productIds"]]
        self.assertEqual(set(ids), {"balance-test", "gut-health-test", "gut-health-test-x2", "vitamin-d-test", "hba1c-test"})
        self.assertEqual(len(ids), len(set(ids)))

    def test_journeys_use_real_active_products_and_published_guides(self):
        active = {p["id"] for p in load("catalog.json")["products"] if p["commercial_status"] == "active"}
        guides = {a["slug"] for a in load("library.json")["articles"] if a["status"] == "published"}
        for journey in load("testing-journeys.json")["journeys"]:
            self.assertTrue(set(journey["productIds"]) <= active)
            self.assertIn(journey["guide"], guides)
            self.assertEqual(len(journey["steps"]), 4)
            self.assertTrue(journey["boundary"] and journey["availability"])

    def test_new_pages_in_complete_canonical_inventory(self):
        paths = site_paths.audited_page_paths(ROOT)
        self.assertEqual(len(paths), 88)
        self.assertTrue({"testing.html", "learning.html", "partners.html"} <= set(paths))

    def test_all_active_products_have_context_not_proof(self):
        sources = load("resources/public-sources.json")["records"]
        active = [p for p in load("catalog.json")["products"] if p["commercial_status"] == "active"]
        self.assertEqual(len(active), 45)
        for product in active:
            self.assertTrue(any(product["id"] in s["product_ids"] for s in sources), product["id"])
            html = (ROOT / "products" / (product["id"] + ".html")).read_text(encoding="utf-8")
            self.assertIn("not finished-product evidence", html)
            self.assertNotIn("Product-specific documentation", html)

    def test_source_links_never_expose_deferred_products(self):
        active = {p["id"] for p in load("catalog.json")["products"] if p["commercial_status"] == "active"}
        for source in load("resources/public-sources.json")["records"]:
            self.assertTrue(set(source["product_ids"]) <= active, source["id"])

    def test_new_guides_are_explicit_about_review_and_limits(self):
        articles = [a for a in load("library.json")["articles"] if a.get("sourceCheckedDate")]
        self.assertEqual(len(articles), 14)
        sources = {s["id"]: s for s in load("resources/public-sources.json")["records"]}
        for article in articles:
            self.assertIn("not independently clinician-reviewed", article["reviewStatus"])
            self.assertGreaterEqual(len(article["bodySections"]), 3)
            self.assertTrue(article["limitations"] and article["sourceIds"])
            self.assertEqual({sources[s]["public_url"] for s in article["sourceIds"]}, {s["url"] for s in article["sources"]})
            page = (ROOT / "library" / (article["slug"] + ".html")).read_text(encoding="utf-8")
            self.assertIn("Sources checked", page)
            self.assertIn(article["reviewStatus"], page)
            self.assertNotIn("Reviewed by Dr.", page)

    def test_general_habit_guides_do_not_automatically_promote_products(self):
        for slug in ("movement-across-adulthood", "sleep-habits-across-adulthood"):
            page = (ROOT / "library" / (slug + ".html")).read_text(encoding="utf-8")
            self.assertNotIn("Products in this learning context", page)

    def test_core_four_new_topics_have_real_guides_and_specific_nutrient_sources(self):
        items = load("campaigns/core-four.json")["items"]
        expected = [("vitamin-k2-context", "nih-ods-vitamin-k"), ("zinc-copper-balance", "nih-ods-zinc"), ("magnesium-forms-and-safety", "nih-ods-magnesium")]
        for item, (guide, source) in zip(items[1:], expected):
            self.assertFalse(item["educationGap"])
            self.assertIn(guide, item["educationIds"])
            self.assertIn(source, item["evidenceIds"])

    def test_primary_studies_do_not_receive_government_independence_badge(self):
        sources = load("resources/public-sources.json")["records"]
        for source in sources:
            if source["resource_type"] in {"randomized_trial", "observational_study"}:
                self.assertEqual(source["independence_status"], "research_disclosures_required")
                self.assertIn("Research Disclosures Required", build.source_card_markup(source))

    def test_course_sales_cannot_be_activated_with_boolean_flip(self):
        data = {"learning.json": load("learning.json"), "partner-learning.json": load("partner-learning.json")}
        for name in data:
            modified = copy.deepcopy(data)
            modified[name]["salesEnabled"] = True
            with patch.object(build, "load_json", side_effect=lambda p: modified[p.name]):
                with self.assertRaisesRegex(ValueError, "separately reviewed"):
                    build_learning.build_learning_paths({}, build)

    def test_two_distinct_course_curricula_and_no_checkout(self):
        self.assertEqual(len(load("learning.json")["modules"]), 8)
        self.assertEqual(len(load("partner-learning.json")["modules"]), 10)
        for name in ("learning.html", "partners.html"):
            page = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("Not available for purchase", page)
            self.assertNotRegex(page, r'type="(?:email|password|file)"|stripe.com|paypal.com|buy.stripe|data-checkout')
            self.assertNotIn("financial freedom", page.lower())
            self.assertNotIn("guaranteed income", page.lower())

    def test_full_course_manuscripts_are_outside_public_repository(self):
        self.assertFalse(list(ROOT.rglob("everyday-matrix.md")))
        self.assertFalse(list(ROOT.rglob("partner-practice.md")))
        builder = (ROOT / "scripts/build_learning.py").read_text(encoding="utf-8")
        self.assertNotIn("_review/", builder)
        self.assertNotIn("deliverables/", builder)

    def test_new_surfaces_are_in_compliance_audit_scope(self):
        paths = {p.relative_to(ROOT).as_posix() for p in ComplianceEngine().audit_paths()}
        self.assertTrue({"testing.html", "learning.html", "partners.html", "content/testing-journeys.json", "content/learning.json", "content/partner-learning.json", "content/resources/public-sources.json"} <= paths)
        self.assertEqual(path_context(ROOT / "partners.html"), "MLM_RECRUITMENT")
        self.assertEqual(path_context(ROOT / "content/partner-learning.json"), "MLM_RECRUITMENT")

    def test_education_search_stays_separate_from_business_training(self):
        index = json.dumps(json.loads((ROOT / "assets/data/search-index.json").read_text(encoding="utf-8"))).lower()
        self.assertNotIn("partner practice", index)
        self.assertNotIn("compensation plan", index)
        self.assertNotIn("downline", index)

    def test_unknown_publisher_host_is_rejected(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from validate_public_sources import validate_manifest
        manifest = load("resources/public-sources.json")
        manifest["records"][0]["public_url"] = "https://unrelated.example/source"
        with self.assertRaisesRegex(ValueError, "recognized publisher"):
            validate_manifest(manifest)

    def test_study_cannot_be_relabeled_as_independent_government(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from validate_public_sources import validate_manifest
        manifest = load("resources/public-sources.json")
        next(s for s in manifest["records"] if s["id"] == "vital-omega-trial")["independence_status"] = "independent_government"
        with self.assertRaisesRegex(ValueError, "disclosure-aware"):
            validate_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
