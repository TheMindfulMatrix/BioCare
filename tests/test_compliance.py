from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compliance_engine import ComplianceEngine  # noqa: E402
from validate_compliance import validate_compliance  # noqa: E402


class ComplianceFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = ComplianceEngine()
        cls.fixtures = json.loads((ROOT / "tests" / "fixtures" / "claim-cases.json").read_text(encoding="utf-8"))["cases"]

    def test_fixture_classification(self) -> None:
        for case in self.fixtures:
            with self.subTest(case=case["id"]):
                finding = self.engine.analyze_text(case["text"], context=case["context"], location=f"fixture:{case['id']}")
                self.assertIsNotNone(finding)
                self.assertEqual(case["expected_risk"], finding.risk)
                self.assertEqual(case["expected_type"], finding.claim_type)

    def test_implied_recovery_combination_escalates(self) -> None:
        finding = self.engine.analyze_text(
            "RECOVERY | Get back faster. | injured athlete",
            context="COMMERCIAL_PRODUCT",
            location="fixture:implied_recovery",
        )
        self.assertIsNotNone(finding)
        self.assertEqual("YELLOW", finding.risk)
        self.assertTrue(finding.implied_claim_review)
        self.assertIn("CE_YELLOW_IMPLIED_CLAIM", finding.matched_rules)

    def test_protective_disclaimer_is_not_a_disease_claim(self) -> None:
        finding = self.engine.analyze_text(
            "This product is not intended to diagnose, treat, cure, or prevent any disease.",
            context="COMMERCIAL_PRODUCT",
            location="fixture:dshea",
        )
        self.assertIsNotNone(finding)
        self.assertNotEqual("RED", finding.risk)

    def test_deferred_products_cannot_render_or_generate_social(self) -> None:
        for product in self.engine.products_payload["products"]:
            if product["compliance_status"] == "DEFERRED_COMPLIANCE_REVIEW":
                self.assertFalse(product["public_cta_allowed"])
                self.assertFalse(product["price_cta_allowed"])
                self.assertFalse(product["product_universe_allowed"])
                self.assertFalse(product["shop_rendering_allowed"])
                self.assertFalse(product["promotional_social_generation_allowed"])

    def test_ingredient_only_evidence_never_greenlights_finished_product(self) -> None:
        violations = [
            claim["claim_id"]
            for claim in self.engine.claims
            if claim["evidence_scope"] == "INGREDIENT_ONLY" and claim["product_id"] and claim["compliance_state"] == "GREEN"
        ]
        self.assertEqual([], violations)

    def test_duplicate_wording_resolves_to_the_current_product(self) -> None:
        claim = next(
            item
            for item in self.engine.claims
            if item["claim_id"] == "CLAIM_PRODUCT_BIOLIMITLESS_BIOZYME_PRICE"
        )
        finding = self.engine.analyze_text(
            claim["exact_text"],
            context="COMMERCIAL_PRODUCT",
            location="fixture:product_specific_price",
            product_id="biolimitless-biozyme",
        )
        self.assertIsNotNone(finding)
        self.assertEqual([claim["claim_id"]], finding.registry_claim_ids)
        self.assertEqual(claim["supporting_sources"], finding.supporting_evidence)

    def test_registered_claim_does_not_cross_contexts_automatically(self) -> None:
        claim = next(
            item
            for item in self.engine.claims
            if item["claim_id"] == "CLAIM_PRODUCT_BALANCE_TEST_DESCRIPTION"
        )
        finding = self.engine.analyze_text(
            claim["exact_text"],
            context="SOCIAL_COMMERCIAL",
            location="fixture:context_mismatch",
            product_id="balance-test",
        )
        self.assertIsNotNone(finding)
        self.assertEqual("YELLOW", finding.risk)
        self.assertEqual("HUMAN_REVIEW_REQUIRED_CONTEXT_MISMATCH", finding.required_action)

    def test_normal_hard_gate_passes(self) -> None:
        result = validate_compliance(strict=False)
        self.assertEqual([], result["errors"])


if __name__ == "__main__":
    unittest.main()
