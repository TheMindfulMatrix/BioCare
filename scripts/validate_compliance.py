#!/usr/bin/env python3
"""Validate Compliance Engine v1 registries, hard gates, and strict-mode policy."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from compliance_engine import CLAIM_TYPES, COMPLIANCE, ROOT, ComplianceEngine, normalize

REQUIRED_CLAIM_FIELDS = {
    "claim_id",
    "exact_text",
    "normalized_text",
    "claim_type",
    "claim_subtype",
    "subject",
    "manufacturer",
    "product_id",
    "ingredient",
    "context",
    "commercial_context",
    "editorial_context",
    "evidence_level",
    "evidence_scope",
    "supporting_sources",
    "source_type",
    "source_date",
    "approved_wording",
    "required_qualification",
    "required_disclosure",
    "prohibited_contexts",
    "allowed_contexts",
    "risk_level",
    "compliance_state",
    "review_status",
    "review_reason",
    "reviewed_at",
    "reviewed_by",
    "expiration_or_recheck_date",
    "notes",
    "verified_price",
    "currency",
    "manufacturer_source",
    "verified_at",
    "price_type",
}
REQUIRED_EVIDENCE_FIELDS = {
    "evidence_id",
    "title",
    "organization",
    "authors",
    "publication",
    "year",
    "url",
    "pmid",
    "doi",
    "evidence_type",
    "population",
    "intervention",
    "comparator",
    "outcomes",
    "limitations",
    "supports_claim_ids",
    "does_not_support",
    "commercial_relevance",
    "manufacturer_relationship",
    "reviewed_at",
}
EVIDENCE_LEVELS = {"ESTABLISHED", "SUPPORTED", "DEBATED", "INSUFFICIENT", "MANUFACTURER_ONLY"}
EVIDENCE_SCOPES = {"INGREDIENT_ONLY", "FORMULATION_SPECIFIC", "PRODUCT_SPECIFIC", "GENERAL_NUTRITION", "OBSERVATIONAL_ONLY", "MECHANISTIC_ONLY", "OTHER"}
REVIEW_STATES = {"PASS", "PASS_WITH_QUALIFICATION", "HUMAN_REVIEW_REQUIRED", "BLOCKED", "DEFERRED_COMPLIANCE_REVIEW"}
CONTEXTS = {"COMMERCIAL_PRODUCT", "EDITORIAL", "SOCIAL_COMMERCIAL", "MLM_RECRUITMENT", "MIXED_PUBLIC"}
PRICE_TYPES = {"RETAIL", "PREMIER", "SUBSCRIPTION", "ONE_TIME", "STARTER_KIT", "RANGE"}


def read_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path.relative_to(ROOT)}: invalid or unreadable JSON: {error}")
        return {}


def unique(records: list[dict[str, Any]], field: str, label: str, errors: list[str]) -> set[str]:
    values = [record.get(field) for record in records]
    if any(not value for value in values):
        errors.append(f"{label}: every record requires {field}")
    if len(values) != len(set(values)):
        errors.append(f"{label}: duplicate {field}")
    return {str(value) for value in values if value}


def valid_https(url: str | None) -> bool:
    return bool(url and urlparse(url).scheme == "https" and urlparse(url).netloc)


def validate_compliance(*, strict: bool = False) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    version = read_json(COMPLIANCE / "version.json", errors)
    sources_payload = read_json(COMPLIANCE / "authoritative-sources.json", errors)
    rules_payload = read_json(COMPLIANCE / "rules.json", errors)
    claims_payload = read_json(COMPLIANCE / "claims.json", errors)
    evidence_payload = read_json(COMPLIANCE / "evidence.json", errors)
    products_payload = read_json(COMPLIANCE / "products.json", errors)
    disclosures_payload = read_json(COMPLIANCE / "disclosures.json", errors)
    social_payload = read_json(COMPLIANCE / "social-policy.json", errors)
    site = read_json(ROOT / "content" / "site.json", errors)
    catalog = read_json(ROOT / "content" / "catalog.json", errors)
    if errors:
        return {"errors": errors, "warnings": warnings, "summary": {}}

    if version.get("engine_version") != "1.0.0" or version.get("ruleset_version") != "1.0.0":
        errors.append("Compliance version files must declare engine/ruleset 1.0.0")
    if version.get("reviewed_by") != "Mindful Matrix compliance ruleset":
        errors.append("Machine-reviewed records must transparently identify the Mindful Matrix compliance ruleset")
    forbidden_certifications = ("legally guaranteed", "fully compliant", "immune from liability", "ftc approved", "safe harbor")
    compliance_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted(COMPLIANCE.glob("*")) if path.is_file())
    for phrase in forbidden_certifications:
        if phrase in compliance_text.casefold():
            errors.append(f"Compliance files contain prohibited certification language: {phrase}")

    authoritative_sources = sources_payload.get("sources", [])
    source_ids = unique(authoritative_sources, "source_id", "authoritative sources", errors)
    for source in authoritative_sources:
        if source.get("organization") not in {"Federal Trade Commission", "U.S. Food and Drug Administration"}:
            errors.append(f"{source.get('source_id')}: policy authority must be FTC or FDA in v1")
        if not valid_https(source.get("url")):
            errors.append(f"{source.get('source_id')}: authoritative source requires an HTTPS URL")
        if source.get("status") == "PROPOSED_RULE_NOT_FINAL_AS_REVIEWED" and "PROPOSED" not in source.get("status", ""):
            errors.append(f"{source.get('source_id')}: proposed rule status must remain explicit")

    rules = rules_payload.get("rules", [])
    rule_defaults = rules_payload.get("rule_defaults", {})
    if rule_defaults != {"jurisdiction": "US", "state": "MO", "required_fields": [], "required_disclosure": None}:
        errors.append("Compliance rule defaults must explicitly define US/MO jurisdiction, required fields, and disclosure")
    unique(rules, "rule_id", "compliance rules", errors)
    for rule in rules:
        if rule.get("risk") not in {"GREEN", "YELLOW", "RED"}:
            errors.append(f"{rule.get('rule_id')}: unsupported risk state")
        if not set(rule.get("contexts", [])).issubset(CONTEXTS):
            errors.append(f"{rule.get('rule_id')}: unsupported context")
        if not set(rule.get("claim_types", [])).issubset(CLAIM_TYPES):
            errors.append(f"{rule.get('rule_id')}: unsupported claim type")
        if not set(rule.get("authoritative_sources", [])).issubset(source_ids):
            errors.append(f"{rule.get('rule_id')}: unknown authoritative source")
        if rule.get("match", {}).get("mode") not in {"always", "regex_any", "cooccurrence"}:
            errors.append(f"{rule.get('rule_id')}: unsupported match mode")
        patterns = list(rule.get("match", {}).get("patterns", []))
        patterns += [pattern for group in rule.get("match", {}).get("groups", []) for pattern in group]
        for pattern in patterns:
            try:
                re.compile(pattern, re.I)
            except re.error as error:
                errors.append(f"{rule.get('rule_id')}: invalid regex {pattern}: {error}")

    evidence = evidence_payload.get("evidence", [])
    evidence_ids = unique(evidence, "evidence_id", "evidence registry", errors)
    for item in evidence:
        missing = REQUIRED_EVIDENCE_FIELDS - set(item)
        if missing:
            errors.append(f"{item.get('evidence_id')}: missing evidence fields {sorted(missing)}")
        if not valid_https(item.get("url")):
            errors.append(f"{item.get('evidence_id')}: evidence requires an HTTPS URL")

    claims = claims_payload.get("claims", [])
    claim_ids = unique(claims, "claim_id", "claim registry", errors)
    disclosure_ids = {item.get("disclosure_id") for item in disclosures_payload.get("disclosures", [])}
    today = date.fromisoformat(version["last_policy_review"])
    for claim in claims:
        claim_id = claim.get("claim_id", "unknown")
        missing = REQUIRED_CLAIM_FIELDS - set(claim)
        if missing:
            errors.append(f"{claim_id}: missing claim fields {sorted(missing)}")
        if claim.get("normalized_text") != normalize(str(claim.get("exact_text", ""))):
            errors.append(f"{claim_id}: normalized_text mismatch")
        if claim.get("claim_type") not in CLAIM_TYPES:
            errors.append(f"{claim_id}: unsupported claim type")
        if claim.get("context") not in CONTEXTS:
            errors.append(f"{claim_id}: unsupported context")
        if not set(claim.get("allowed_contexts", [])).issubset(CONTEXTS):
            errors.append(f"{claim_id}: unsupported allowed context")
        if not set(claim.get("prohibited_contexts", [])).issubset(CONTEXTS):
            errors.append(f"{claim_id}: unsupported prohibited context")
        if set(claim.get("allowed_contexts", [])) & set(claim.get("prohibited_contexts", [])):
            errors.append(f"{claim_id}: a context cannot be both allowed and prohibited")
        if claim.get("evidence_level") not in EVIDENCE_LEVELS:
            errors.append(f"{claim_id}: unsupported evidence level")
        if claim.get("evidence_scope") not in EVIDENCE_SCOPES:
            errors.append(f"{claim_id}: unsupported evidence scope")
        if claim.get("compliance_state") not in {"GREEN", "YELLOW", "RED"}:
            errors.append(f"{claim_id}: unsupported compliance state")
        if claim.get("review_status") not in REVIEW_STATES:
            errors.append(f"{claim_id}: unsupported review status")
        if claim.get("reviewed_by") != "Mindful Matrix compliance ruleset":
            errors.append(f"{claim_id}: reviewer identity must not imply attorney review")
        unknown_evidence = set(claim.get("supporting_sources", [])) - evidence_ids
        if unknown_evidence:
            errors.append(f"{claim_id}: unknown evidence {sorted(unknown_evidence)}")
        if claim.get("compliance_state") == "RED" and claim.get("commercial_context") and claim.get("review_status") in {"PASS", "PASS_WITH_QUALIFICATION"}:
            errors.append(f"{claim_id}: RED commercial claim cannot be approved for rendering")
        if claim.get("review_status") == "DEFERRED_COMPLIANCE_REVIEW" and claim.get("allowed_contexts"):
            errors.append(f"{claim_id}: deferred claim cannot have allowed contexts")
        unknown_disclosures = set(claim.get("required_disclosure", [])) - disclosure_ids
        if unknown_disclosures:
            errors.append(f"{claim_id}: unknown disclosure IDs {sorted(unknown_disclosures)}")
        if claim.get("requires_dshea_disclaimer") and (
            claim.get("disclaimer_text") != site["site"]["fdaDisclaimer"] or not claim.get("requires_claim_adjacent_disclaimer")
        ):
            errors.append(f"{claim_id}: DSHEA claim must preserve exact wording and claim-adjacent placement tracking")
        if claim.get("evidence_scope") == "INGREDIENT_ONLY" and claim.get("product_id") and claim.get("compliance_state") == "GREEN":
            errors.append(f"{claim_id}: ingredient-only evidence cannot GREEN-light a finished-product claim")
        if claim.get("claim_type") == "PRICE_CLAIM":
            if not claim.get("verified_price") or claim.get("currency") != "USD":
                errors.append(f"{claim_id}: price claim requires verified_price and USD currency")
            if not valid_https(claim.get("manufacturer_source")) or not claim.get("verified_at"):
                errors.append(f"{claim_id}: price claim requires manufacturer_source and verified_at")
            if not claim.get("price_type") or not set(claim["price_type"]).issubset(PRICE_TYPES):
                errors.append(f"{claim_id}: price claim has unsupported or missing price_type")
        elif any(claim.get(field) for field in ("verified_price", "currency", "manufacturer_source", "verified_at", "price_type")):
            errors.append(f"{claim_id}: non-price claim contains price-only metadata")
        recheck = claim.get("expiration_or_recheck_date")
        if strict and recheck and date.fromisoformat(recheck) < today:
            errors.append(f"{claim_id}: required review expired")
        if strict and claim.get("commercial_context") and claim.get("compliance_state") == "YELLOW" and claim.get("review_status") not in {"PASS_WITH_QUALIFICATION"}:
            errors.append(f"{claim_id}: unresolved YELLOW commercial claim in strict mode")
        if strict and claim.get("commercial_context") and not claim.get("supporting_sources"):
            errors.append(f"{claim_id}: commercial claim lacks evidence links in strict mode")

    for item in evidence:
        unknown_claims = set(item.get("supports_claim_ids", [])) - claim_ids
        if unknown_claims:
            errors.append(f"{item.get('evidence_id')}: unknown supported claims {sorted(unknown_claims)}")
        expected_claims = {claim["claim_id"] for claim in claims if item["evidence_id"] in claim.get("supporting_sources", [])}
        if set(item.get("supports_claim_ids", [])) != expected_claims:
            errors.append(f"{item.get('evidence_id')}: supports_claim_ids must exactly mirror claim evidence links")

    health_claim_requirements = {
        "claim_authority",
        "authorized_wording",
        "required_qualifying_language",
        "source_url",
        "last_verified",
    }
    for collection_name in ("authorized_health_claims", "qualified_health_claims"):
        collection = claims_payload.get(collection_name)
        if not isinstance(collection, list):
            errors.append(f"{collection_name}: must be an explicit list")
            continue
        for index, record in enumerate(collection):
            if not health_claim_requirements.issubset(record):
                errors.append(f"{collection_name}[{index}]: missing authority or exact-wording controls")
            if not valid_https(record.get("source_url")):
                errors.append(f"{collection_name}[{index}]: source_url must be authoritative HTTPS")

    expected_disclosures = {
        "DISCLOSURE_ZINZINO_PARTNER": site["site"]["affiliateDisclosure"],
        "DISCLOSURE_BIOLIMITLESS_PARTNER": site["site"]["biolimitlessAffiliateDisclosure"],
        "DISCLOSURE_FDA_DSHEA_PLURAL": site["site"]["fdaDisclaimer"],
    }
    actual_disclosures = {item["disclosure_id"]: item["exact_text"] for item in disclosures_payload.get("disclosures", [])}
    if actual_disclosures != expected_disclosures:
        errors.append("Approved Zinzino, BioLimitless, and FDA disclosure wording must be preserved exactly")

    product_records = products_payload.get("products", [])
    product_ids = unique(product_records, "product_id", "product compliance registry", errors)
    catalog_products = {product["id"]: product for product in catalog.get("products", [])}
    if product_ids != set(catalog_products):
        errors.append("Product compliance registry must exactly match the current catalog inventory")
    valid_statuses = set(products_payload.get("allowed_statuses", []))
    for record in product_records:
        product_id = record["product_id"]
        product = catalog_products.get(product_id, {})
        status = record.get("compliance_status")
        if status not in valid_statuses:
            errors.append(f"{product_id}: invalid compliance status")
        expected_status = "DEFERRED_COMPLIANCE_REVIEW" if product.get("commercial_status") == "deferred_compliance_review" else "ACTIVE"
        if status != expected_status:
            errors.append(f"{product_id}: catalog and compliance status mismatch")
        blocked = status in {"DEFERRED_COMPLIANCE_REVIEW", "BLOCKED_PUBLIC"}
        control_fields = ("public_cta_allowed", "price_cta_allowed", "product_universe_allowed", "shop_rendering_allowed", "promotional_social_generation_allowed")
        if blocked and any(record.get(field) for field in control_fields):
            errors.append(f"{product_id}: deferred/blocked product has an enabled public or social control")
        expected_disclosure = "DISCLOSURE_ZINZINO_PARTNER" if product.get("manufacturer") == "Zinzino" else "DISCLOSURE_BIOLIMITLESS_PARTNER"
        if record.get("required_disclosure") != expected_disclosure:
            errors.append(f"{product_id}: missing material-connection disclosure mapping")

        price = product.get("price", {})
        if product.get("commercial_status") == "active":
            if price.get("currency") != "USD" or not valid_https(price.get("official_price_source")) or not price.get("price_verified_at"):
                errors.append(f"{product_id}: active price requires USD, official source, and verification date")
            elif (today - date.fromisoformat(price["price_verified_at"])).days > int(version["price_recheck_days"]):
                errors.append(f"{product_id}: active price verification expired")

    for page_name in ("index.html", "shop.html"):
        page = ROOT / page_name
        if not page.is_file():
            continue
        generated = page.read_text(encoding="utf-8")
        for record in product_records:
            if record["compliance_status"] in {"DEFERRED_COMPLIANCE_REVIEW", "BLOCKED_PUBLIC"}:
                product = catalog_products[record["product_id"]]
                if product.get("destination") in generated or f'data-product-id="{record["product_id"]}"' in generated:
                    errors.append(f"{record['product_id']}: deferred/blocked product leaked into {page_name}")

    required_social_checks = {
        "CLAIM_CLASSIFICATION",
        "EVIDENCE_MATCH",
        "AFFILIATE_RELATIONSHIP",
        "DISCLOSURE_PLACEMENT",
        "TESTIMONIAL",
        "PRICE",
        "DISEASE_CLAIM",
        "MLM_EARNINGS",
    }
    if not required_social_checks.issubset(set(social_payload.get("required_checks", []))):
        errors.append("Social compliance policy is missing required commercial checks")
    if social_payload.get("commercial_brief_requirements", {}).get("instruction") != "Do not strengthen, paraphrase, or extend approved claims.":
        errors.append("Social policy must preserve the no-strengthening instruction exactly")

    gate = (COMPLIANCE / "codex-production-gate.txt").read_text(encoding="utf-8")
    for required in ("Only use claims explicitly listed as GREEN or approved YELLOW", "Do not activate, promote, price, render, or link a deferred or blocked product", "Do not create MLM earnings"):
        if required not in gate:
            errors.append(f"Codex production gate missing: {required}")

    engine = ComplianceEngine()
    audit = engine.audit_repository()
    audit_red = [finding for finding in audit["findings"] if finding["risk"] == "RED"]
    for finding in audit_red:
        errors.append(f"{finding['location']}: hard-rule RED claim: {finding['exact_text']}")
    unresolved = [finding for finding in audit["findings"] if finding["strict_failure"] and finding["risk"] == "YELLOW"]
    if strict:
        for finding in unresolved:
            errors.append(f"{finding['location']}: unresolved strict-mode YELLOW claim: {finding['exact_text']}")
    else:
        for finding in unresolved:
            warnings.append(f"{finding['location']}: {finding['required_action']}: {finding['exact_text']}")

    warnings = sorted(set(warnings))
    errors = sorted(set(errors))
    status_counts = Counter(record["compliance_status"] for record in product_records)
    summary = {
        "claims": len(claims),
        "evidence": len(evidence),
        "rules": len(rules),
        "products": len(product_records),
        "active_products": status_counts["ACTIVE"] + status_counts["ACTIVE_WITH_RESTRICTIONS"],
        "deferred_products": status_counts["DEFERRED_COMPLIANCE_REVIEW"],
        "blocked_products": status_counts["BLOCKED_PUBLIC"],
        "audit": audit["summary"],
        "strict": strict,
    }
    return {"errors": errors, "warnings": warnings, "summary": summary}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Fail unresolved YELLOW and unregistered commercial health claims")
    parser.add_argument("--dry-run", action="store_true", help="Report strict failures without a non-zero exit")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = parse_args()
    result = validate_compliance(strict=args.strict)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        summary = result["summary"]
        print(
            f"Compliance validation: claims={summary.get('claims', 0)} evidence={summary.get('evidence', 0)} "
            f"rules={summary.get('rules', 0)} products={summary.get('products', 0)} "
            f"errors={len(result['errors'])} warnings={len(result['warnings'])} strict={args.strict}"
        )
        for error in result["errors"]:
            print(f"ERROR: {error}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
        if args.dry_run and result["errors"]:
            print(f"DRY RUN: strict mode would fail with {len(result['errors'])} issue(s)")
    if result["errors"] and not args.dry_run:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
