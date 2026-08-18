#!/usr/bin/env python3
"""Build the reviewed v1 compliance baseline from the current content model.

This is an explicit maintenance tool, not part of the public site build. It writes
internal governance registries only. Generated records remain subject to human and
legal review; they do not certify compliance.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COMPLIANCE = ROOT / "content" / "compliance"
REVIEWED_AT = date(2026, 8, 18)
REVIEWED_BY = "Mindful Matrix compliance ruleset"
DSHEA = "These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease."


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def normalize(text: str) -> str:
    value = unicodedata.normalize("NFKC", text).casefold()
    value = re.sub(r"[^a-z0-9$%]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "_", normalize(value)).strip("_")
    return result[:72] or "record"


def money(value: int | float) -> str:
    return f"${value:,.2f}" if isinstance(value, float) and not value.is_integer() else f"${int(value):,}"


def price_text(price: dict[str, Any]) -> tuple[str, str]:
    model = price["pricing_model"]
    if model == "retail_premier":
        if "premier_price" not in price:
            return f"Retail {money(price['retail_price'])}", "RETAIL"
        return f"Retail {money(price['retail_price'])} / Premier {money(price['premier_price'])}", "RETAIL_PREMIER"
    if model == "starter_subscription":
        return f"Start kit {money(price['start_price'])} / Monthly subscription {money(price['recurring_price'])}", "STARTER_KIT_SUBSCRIPTION"
    if model == "one_time":
        return f"{money(price['one_time_price'])} one-time", "ONE_TIME"
    if model == "one_time_autoship":
        return f"{money(price['one_time_price'])} one-time / {money(price['autoship_price'])} autoship", "ONE_TIME_SUBSCRIPTION"
    if model == "one_time_range":
        return f"{money(price['one_time_price_min'])}–{money(price['one_time_price_max'])} one-time", "RANGE"
    raise ValueError(f"Unsupported price model: {model}")


def price_types(price: dict[str, Any]) -> list[str]:
    return {
        "retail_premier": ["RETAIL"] if "premier_price" not in price else ["RETAIL", "PREMIER"],
        "starter_subscription": ["STARTER_KIT", "SUBSCRIPTION"],
        "one_time": ["ONE_TIME"],
        "one_time_autoship": ["ONE_TIME", "SUBSCRIPTION"],
        "one_time_range": ["ONE_TIME", "RANGE"],
    }[price["pricing_model"]]


def claim_record(
    *,
    claim_id: str,
    exact_text: str,
    claim_type: str,
    claim_subtype: str | None,
    subject: str,
    context: str,
    evidence_level: str,
    evidence_scope: str,
    supporting_sources: list[str],
    source_type: str,
    source_date: str | None,
    compliance_state: str,
    review_status: str,
    review_reason: str,
    manufacturer: str | None = None,
    product_id: str | None = None,
    ingredient: str | None = None,
    approved_wording: str | None = None,
    required_qualification: str | None = None,
    required_disclosure: list[str] | None = None,
    prohibited_contexts: list[str] | None = None,
    allowed_contexts: list[str] | None = None,
    notes: str | None = None,
    requires_dshea_disclaimer: bool = False,
    requires_claim_adjacent_disclaimer: bool = False,
    disclaimer_text: str | None = None,
    disclaimer_placement_rule: str | None = None,
    claim_authority: str | None = None,
    authorized_wording: str | None = None,
    required_qualifying_language: str | None = None,
    source_url: str | None = None,
    last_verified: str | None = None,
    verified_price: dict[str, int | float] | None = None,
    currency: str | None = None,
    manufacturer_source: str | None = None,
    verified_at: str | None = None,
    price_type: list[str] | None = None,
) -> dict[str, Any]:
    risk_level = {"GREEN": "LOW", "YELLOW": "ELEVATED", "RED": "HIGH"}[compliance_state]
    commercial = context in {"COMMERCIAL_PRODUCT", "SOCIAL_COMMERCIAL", "MLM_RECRUITMENT"}
    editorial = context == "EDITORIAL"
    return {
        "claim_id": claim_id,
        "exact_text": exact_text,
        "normalized_text": normalize(exact_text),
        "claim_type": claim_type,
        "claim_subtype": claim_subtype,
        "subject": subject,
        "manufacturer": manufacturer,
        "product_id": product_id,
        "ingredient": ingredient,
        "context": context,
        "commercial_context": commercial,
        "editorial_context": editorial,
        "evidence_level": evidence_level,
        "evidence_scope": evidence_scope,
        "supporting_sources": supporting_sources,
        "source_type": source_type,
        "source_date": source_date,
        "approved_wording": approved_wording if approved_wording is not None else exact_text,
        "required_qualification": required_qualification,
        "required_disclosure": required_disclosure or [],
        "prohibited_contexts": prohibited_contexts or [],
        "allowed_contexts": [context] if allowed_contexts is None else allowed_contexts,
        "risk_level": risk_level,
        "compliance_state": compliance_state,
        "review_status": review_status,
        "review_reason": review_reason,
        "reviewed_at": REVIEWED_AT.isoformat(),
        "reviewed_by": REVIEWED_BY,
        "expiration_or_recheck_date": (REVIEWED_AT + timedelta(days=365)).isoformat(),
        "notes": notes,
        "requires_dshea_disclaimer": requires_dshea_disclaimer,
        "requires_claim_adjacent_disclaimer": requires_claim_adjacent_disclaimer,
        "disclaimer_text": disclaimer_text,
        "disclaimer_placement_rule": disclaimer_placement_rule,
        "claim_authority": claim_authority,
        "authorized_wording": authorized_wording,
        "required_qualifying_language": required_qualifying_language,
        "source_url": source_url,
        "last_verified": last_verified,
        "verified_price": verified_price,
        "currency": currency,
        "manufacturer_source": manufacturer_source,
        "verified_at": verified_at,
        "price_type": price_type or [],
    }


def evidence_record(
    *,
    evidence_id: str,
    title: str,
    organization: str,
    publication: str | None,
    url: str,
    evidence_type: str,
    limitations: str,
    commercial_relevance: str,
    manufacturer_relationship: str,
    authors: list[str] | None = None,
    year: int | None = None,
    pmid: str | None = None,
    doi: str | None = None,
    population: str | None = None,
    intervention: str | None = None,
    comparator: str | None = None,
    outcomes: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "evidence_id": evidence_id,
        "title": title,
        "organization": organization,
        "authors": authors,
        "publication": publication,
        "year": year,
        "url": url,
        "pmid": pmid,
        "doi": doi,
        "evidence_type": evidence_type,
        "population": population,
        "intervention": intervention,
        "comparator": comparator,
        "outcomes": outcomes or [],
        "limitations": limitations,
        "supports_claim_ids": [],
        "does_not_support": "Any stronger, broader, or differently scoped claim not explicitly registered.",
        "commercial_relevance": commercial_relevance,
        "manufacturer_relationship": manufacturer_relationship,
        "reviewed_at": REVIEWED_AT.isoformat(),
    }


def infer_library_evidence_type(source: dict[str, Any]) -> str:
    combined = " ".join(str(source.get(key, "")) for key in ("organization", "citation", "title")).casefold()
    if any(token in combined for token in ("food and drug administration", "federal trade commission", "nih", "cdc", "usda")):
        return "REGULATORY_PRIMARY"
    if "systematic review" in combined or "meta-analysis" in combined:
        return "SYSTEMATIC_REVIEW_META_ANALYSIS"
    if "randomized" in combined or "controlled trial" in combined:
        return "RANDOMIZED_CONTROLLED_TRIAL"
    if "prospective" in combined or "cohort" in combined:
        return "PROSPECTIVE_OBSERVATIONAL"
    if "cross-sectional" in combined:
        return "CROSS_SECTIONAL"
    if "review" in combined or "appraisal" in combined:
        return "NARRATIVE_REVIEW"
    if "consensus" in combined or "guidance" in combined or "association" in combined:
        return "EXPERT_OPINION"
    return "OTHER"


def description_classification(product: dict[str, Any]) -> tuple[str, str, str, bool]:
    text = product["description"].casefold()
    if any(token in text for token in ("support", "promote", "maintain", "improve", "boost", "enhance", "recovery", "metabolic", "immune", "cognitive")):
        return "STRUCTURE_FUNCTION_CLAIM", "MANUFACTURER_DESCRIPTION", "YELLOW", True
    if any(token in text for token in ("test", "blood spot", "report", "measurement", "track")):
        return "FACTUAL_PRODUCT_FACT", "TEST_OR_BIOMARKER_DESCRIPTION", "YELLOW", False
    return "FACTUAL_PRODUCT_FACT", "MANUFACTURER_DESCRIPTION", "GREEN", False


def build() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    catalog = load_json(ROOT / "content" / "catalog.json")
    library = load_json(ROOT / "content" / "library.json")
    site = load_json(ROOT / "content" / "site.json")
    sources = load_json(COMPLIANCE / "authoritative-sources.json")

    evidence: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    products: list[dict[str, Any]] = []

    for source in sources["sources"]:
        evidence.append(
            evidence_record(
                evidence_id=f"EVIDENCE_{source['source_id']}",
                title=source["title"],
                organization=source["organization"],
                publication=None,
                url=source["url"],
                evidence_type="REGULATORY_PRIMARY",
                limitations="Agency guidance, policy, regulation summary, or rulemaking status; not product-specific substantiation.",
                commercial_relevance="Controls claim classification, substantiation, disclosure, or escalation rules.",
                manufacturer_relationship="NONE",
            )
        )

    article_evidence: dict[str, list[str]] = {}
    for article in library["articles"]:
        ids: list[str] = []
        for index, source in enumerate(article.get("sources", []), 1):
            evidence_id = f"EVIDENCE_LIBRARY_{slug(article['slug']).upper()}_{index:02d}"
            ids.append(evidence_id)
            citation = source.get("citation") or None
            year_match = re.search(r"\b(19|20)\d{2}\b", f"{citation or ''} {source.get('title', '')}")
            pmid_match = re.search(r"(?:PMID\s*|pubmed\.ncbi\.nlm\.nih\.gov/)(\d+)", f"{citation or ''} {source.get('url', '')}", re.I)
            doi_match = re.search(r"doi\.org/([^?#]+)", source.get("url", ""), re.I)
            evidence.append(
                evidence_record(
                    evidence_id=evidence_id,
                    title=source["title"],
                    organization=source["organization"],
                    publication=citation,
                    year=int(year_match.group()) if year_match else None,
                    url=source["url"],
                    pmid=pmid_match.group(1) if pmid_match else None,
                    doi=doi_match.group(1) if doi_match else None,
                    evidence_type=infer_library_evidence_type(source),
                    limitations=source.get("detail", "Scope is limited to the cited source and article use."),
                    commercial_relevance="Editorial source. It does not automatically substantiate a finished commercial product.",
                    manufacturer_relationship="NONE_DISCLOSED_IN_LIBRARY_RECORD",
                )
            )
        article_evidence[article["slug"]] = ids

        for group in (article.get("evidenceSummary") or {}).get("groups", []):
            level = group["level"].upper()
            state = "GREEN" if level == "ESTABLISHED" else "YELLOW"
            status = "PASS" if state == "GREEN" else "PASS_WITH_QUALIFICATION"
            for index, statement in enumerate(group.get("items", []), 1):
                claims.append(
                    claim_record(
                        claim_id=f"CLAIM_LIBRARY_{slug(article['slug']).upper()}_{level}_{index:02d}",
                        exact_text=statement,
                        claim_type="RESEARCH_INTERPRETATION",
                        claim_subtype=f"EVIDENCE_SUMMARY_{level}",
                        subject=article["title"],
                        context="EDITORIAL",
                        evidence_level=level,
                        evidence_scope="OTHER",
                        supporting_sources=ids,
                        source_type="MIXED_EDITORIAL_SOURCES",
                        source_date=article.get("evidenceReviewed"),
                        compliance_state=state,
                        review_status=status,
                        review_reason="Registered from the article's existing evidence summary without strengthening its wording.",
                        required_qualification="Preserve the article's context, limitations, population, and uncertainty." if state == "YELLOW" else None,
                        prohibited_contexts=["COMMERCIAL_PRODUCT", "SOCIAL_COMMERCIAL"],
                        allowed_contexts=["EDITORIAL"],
                        notes="The complete article source set is linked because the current article record does not map each sentence to one source.",
                    )
                )

    for product in catalog["products"]:
        evidence_id = f"EVIDENCE_PRODUCT_{slug(product['id']).upper()}"
        source_url = product.get("officialProductPage") or product["price"]["official_price_source"]
        evidence.append(
            evidence_record(
                evidence_id=evidence_id,
                title=f"Official {product['manufacturer']} page for {product['name']}",
                organization=product["manufacturer"],
                publication="Official manufacturer product or catalog page",
                url=source_url,
                evidence_type="MANUFACTURER_SOURCE",
                limitations="Supports current manufacturer-disclosed identity, contents, format, availability, and price only; not independent proof of efficacy, safety, typicality, or superiority.",
                commercial_relevance="Product-specific manufacturer source.",
                manufacturer_relationship="COMMERCIAL_MANUFACTURER_AND_AFFILIATE_PARTNER",
            )
        )
        is_deferred = product["commercial_status"] == "deferred_compliance_review"
        compliance_status = "DEFERRED_COMPLIANCE_REVIEW" if is_deferred else "ACTIVE"
        products.append(
            {
                "product_id": product["id"],
                "name": product["name"],
                "manufacturer": product["manufacturer"],
                "jurisdiction": "US",
                "state": "MO",
                "compliance_status": compliance_status,
                "catalog_commercial_status": product["commercial_status"],
                "public_cta_allowed": not is_deferred,
                "price_cta_allowed": not is_deferred,
                "product_universe_allowed": not is_deferred,
                "shop_rendering_allowed": not is_deferred,
                "promotional_social_generation_allowed": not is_deferred,
                "required_disclosure": "DISCLOSURE_ZINZINO_PARTNER" if product["manufacturer"] == "Zinzino" else "DISCLOSURE_BIOLIMITLESS_PARTNER",
                "review_reason": (product.get("complianceReview") or {}).get("reason") if is_deferred else "Catalog status is active; individual claims remain controlled by the claim registry.",
                "flagged_ingredients": (product.get("complianceReview") or {}).get("flaggedIngredients", []),
                "reviewed_at": REVIEWED_AT.isoformat(),
                "reviewed_by": REVIEWED_BY,
            }
        )

        claim_type, subtype, state, dshea = description_classification(product)
        review_status = "DEFERRED_COMPLIANCE_REVIEW" if is_deferred else ("PASS" if state == "GREEN" else "HUMAN_REVIEW_REQUIRED")
        disclosure = "DISCLOSURE_ZINZINO_PARTNER" if product["manufacturer"] == "Zinzino" else "DISCLOSURE_BIOLIMITLESS_PARTNER"
        required_disclosures = [disclosure] + (["DISCLOSURE_FDA_DSHEA_PLURAL"] if dshea else [])
        claims.append(
            claim_record(
                claim_id=f"CLAIM_PRODUCT_{slug(product['id']).upper()}_DESCRIPTION",
                exact_text=product["description"],
                claim_type=claim_type,
                claim_subtype=subtype,
                subject=product["name"],
                manufacturer=product["manufacturer"],
                product_id=product["id"],
                context="COMMERCIAL_PRODUCT",
                evidence_level="MANUFACTURER_ONLY",
                evidence_scope="PRODUCT_SPECIFIC",
                supporting_sources=[evidence_id],
                source_type="MANUFACTURER_SOURCE",
                source_date=product["price"].get("price_verified_at"),
                compliance_state=state,
                review_status=review_status,
                review_reason=(product.get("complianceReview") or {}).get("reason", "Current manufacturer-sourced wording registered without strengthening.") if is_deferred else "Current wording registered without strengthening; manufacturer sourcing is not independent efficacy substantiation.",
                required_qualification="Preserve exact wording and manufacturer attribution; do not infer diagnosis, treatment, universal benefit, or independent proof." if state == "YELLOW" else None,
                required_disclosure=required_disclosures,
                prohibited_contexts=["MLM_RECRUITMENT"] + (["COMMERCIAL_PRODUCT", "SOCIAL_COMMERCIAL"] if is_deferred else []),
                allowed_contexts=[] if is_deferred else ["COMMERCIAL_PRODUCT", "MIXED_PUBLIC"],
                notes="Ingredient evidence may not be substituted for product-specific evidence.",
                requires_dshea_disclaimer=dshea,
                requires_claim_adjacent_disclaimer=dshea,
                disclaimer_text=DSHEA if dshea else None,
                disclaimer_placement_rule="Adjacent to the claim or linked on the same panel/page as current FDA requirements specify; footer-only placement is not presumed sufficient." if dshea else None,
                source_url=source_url,
                last_verified=product["price"].get("price_verified_at"),
            )
        )

        price_claim, price_type = price_text(product["price"])
        claims.append(
            claim_record(
                claim_id=f"CLAIM_PRODUCT_{slug(product['id']).upper()}_PRICE",
                exact_text=price_claim,
                claim_type="PRICE_CLAIM",
                claim_subtype=price_type,
                subject=product["name"],
                manufacturer=product["manufacturer"],
                product_id=product["id"],
                context="COMMERCIAL_PRODUCT",
                evidence_level="MANUFACTURER_ONLY",
                evidence_scope="PRODUCT_SPECIFIC",
                supporting_sources=[evidence_id],
                source_type="MANUFACTURER_SOURCE",
                source_date=product["price"]["price_verified_at"],
                compliance_state="GREEN",
                review_status="DEFERRED_COMPLIANCE_REVIEW" if is_deferred else "PASS",
                review_reason="Current official manufacturer price source is recorded; the manufacturer checkout remains controlling.",
                required_qualification="Price, eligibility, and purchase options may change; manufacturer checkout controls.",
                required_disclosure=[disclosure],
                prohibited_contexts=["SOCIAL_COMMERCIAL", "MLM_RECRUITMENT"] if is_deferred else ["MLM_RECRUITMENT"],
                allowed_contexts=[] if is_deferred else ["COMMERCIAL_PRODUCT", "MIXED_PUBLIC"],
                notes=f"Currency=USD; price_type={price_type}; deferred status overrides the otherwise supported price record." if is_deferred else f"Currency=USD; price_type={price_type}.",
                source_url=product["price"]["official_price_source"],
                last_verified=product["price"]["price_verified_at"],
                verified_price={
                    key: value
                    for key, value in product["price"].items()
                    if key in {"retail_price", "premier_price", "start_price", "recurring_price", "one_time_price", "autoship_price", "one_time_price_min", "one_time_price_max"}
                },
                currency=product["price"]["currency"],
                manufacturer_source=product["price"]["official_price_source"],
                verified_at=product["price"]["price_verified_at"],
                price_type=price_types(product["price"]),
            )
        )

    disclosure_support = {
        "CLAIM_DISCLOSURE_ZINZINO": ["EVIDENCE_FTC_ENDORSEMENT_GUIDES_FAQ", "EVIDENCE_FTC_DOT_COM_DISCLOSURES"],
        "CLAIM_DISCLOSURE_BIOLIMITLESS": ["EVIDENCE_FTC_ENDORSEMENT_GUIDES_FAQ", "EVIDENCE_FTC_DOT_COM_DISCLOSURES"],
        "CLAIM_DISCLOSURE_FDA_DSHEA": ["EVIDENCE_FDA_SUPPLEMENT_LABELING_CLAIMS", "EVIDENCE_FDA_DSHEA_PLACEMENT_2025"],
    }
    disclosure_claims = [
        ("CLAIM_DISCLOSURE_ZINZINO", site["site"]["affiliateDisclosure"], "AFFILIATE_RELATIONSHIP_CLAIM", "DISCLOSURE_ZINZINO_PARTNER"),
        ("CLAIM_DISCLOSURE_BIOLIMITLESS", site["site"]["biolimitlessAffiliateDisclosure"], "AFFILIATE_RELATIONSHIP_CLAIM", "DISCLOSURE_BIOLIMITLESS_PARTNER"),
        ("CLAIM_DISCLOSURE_FDA_DSHEA", site["site"]["fdaDisclaimer"], "FACTUAL_PRODUCT_FACT", "DISCLOSURE_FDA_DSHEA_PLURAL"),
    ]
    for claim_id, exact, claim_type, disclosure_id in disclosure_claims:
        claims.append(
            claim_record(
                claim_id=claim_id,
                exact_text=exact,
                claim_type=claim_type,
                claim_subtype="REQUIRED_DISCLOSURE",
                subject="The Mindful Matrix disclosures",
                context="COMMERCIAL_PRODUCT",
                evidence_level="ESTABLISHED",
                evidence_scope="OTHER",
                supporting_sources=disclosure_support[claim_id],
                source_type="REGULATORY_PRIMARY",
                source_date=REVIEWED_AT.isoformat(),
                compliance_state="GREEN",
                review_status="PASS",
                review_reason="Exact approved disclosure wording is preserved and checked by the release validator.",
                approved_wording=exact,
                required_disclosure=[disclosure_id],
                allowed_contexts=["COMMERCIAL_PRODUCT", "SOCIAL_COMMERCIAL", "EDITORIAL", "MIXED_PUBLIC"],
                notes="Placement remains context-dependent and is validated separately.",
            )
        )

    testing_texts = [
        ("CLAIM_TESTING_STARTING_POINT", site["homepage"]["testing"]["copy"], "GENERAL_WELLBEING_CLAIM", "YELLOW"),
        ("CLAIM_TESTING_GUIDE_SCOPE", site["homepage"]["testing"]["education"]["copy"], "RESEARCH_INTERPRETATION", "YELLOW"),
        ("CLAIM_START_NON_DIAGNOSTIC", "This page is an orientation, not a diagnostic.", "DIAGNOSTIC_CLAIM", "GREEN"),
    ]
    for claim_id, exact, claim_type, state in testing_texts:
        claims.append(
            claim_record(
                claim_id=claim_id,
                exact_text=exact,
                claim_type=claim_type,
                claim_subtype="TEST_OR_BIOMARKER_CONTEXT",
                subject="Mindful Matrix testing education",
                context="EDITORIAL" if claim_id != "CLAIM_TESTING_STARTING_POINT" else "MIXED_PUBLIC",
                evidence_level="SUPPORTED",
                evidence_scope="OTHER",
                supporting_sources=article_evidence.get("should-you-test-your-omega-3-levels", []),
                source_type="MIXED_EDITORIAL_SOURCES",
                source_date=REVIEWED_AT.isoformat(),
                compliance_state=state,
                review_status="PASS" if state == "GREEN" else "PASS_WITH_QUALIFICATION",
                review_reason="Registered as education-first testing language with explicit limitations.",
                required_qualification="Do not imply diagnosis, complete health status, guaranteed decisions, or replacement for professional interpretation." if state == "YELLOW" else None,
                prohibited_contexts=["COMMERCIAL_PRODUCT"] if claim_id != "CLAIM_START_NON_DIAGNOSTIC" else [],
                allowed_contexts=["EDITORIAL", "MIXED_PUBLIC"],
            )
        )

    claim_ids = {claim["claim_id"] for claim in claims}
    if len(claim_ids) != len(claims):
        raise RuntimeError("Generated duplicate claim IDs")
    evidence_ids = {item["evidence_id"] for item in evidence}
    if len(evidence_ids) != len(evidence):
        raise RuntimeError("Generated duplicate evidence IDs")
    missing = sorted({source for claim in claims for source in claim["supporting_sources"] if source not in evidence_ids})
    if missing:
        raise RuntimeError(f"Claims reference missing evidence IDs: {missing}")

    supports: dict[str, list[str]] = defaultdict(list)
    for claim in claims:
        for evidence_id in claim["supporting_sources"]:
            supports[evidence_id].append(claim["claim_id"])
    for item in evidence:
        item["supports_claim_ids"] = sorted(supports[item["evidence_id"]])

    claims.sort(key=lambda item: item["claim_id"])
    evidence.sort(key=lambda item: item["evidence_id"])
    products.sort(key=lambda item: item["product_id"])
    claims_payload = {
        "schema_version": "1.0.0",
        "ruleset_version": "1.0.0",
        "reviewed_at": REVIEWED_AT.isoformat(),
        "reviewed_by": REVIEWED_BY,
        "authorized_health_claims": [],
        "qualified_health_claims": [],
        "claims": claims,
    }
    evidence_payload = {"schema_version": "1.0.0", "reviewed_at": REVIEWED_AT.isoformat(), "evidence": evidence}
    product_payload = {
        "schema_version": "1.0.0",
        "allowed_statuses": ["ACTIVE", "ACTIVE_WITH_RESTRICTIONS", "DEFERRED_COMPLIANCE_REVIEW", "BLOCKED_PUBLIC"],
        "products": products,
    }
    return claims_payload, evidence_payload, product_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify that committed registries match the deterministic baseline")
    args = parser.parse_args()
    claims, evidence, products = build()
    outputs = {
        COMPLIANCE / "claims.json": claims,
        COMPLIANCE / "evidence.json": evidence,
        COMPLIANCE / "products.json": products,
    }
    if args.check:
        mismatches = [str(path.relative_to(ROOT)) for path, payload in outputs.items() if not path.is_file() or load_json(path) != payload]
        if mismatches:
            raise SystemExit("Compliance baseline mismatch: " + ", ".join(mismatches))
        print(f"Compliance baseline matches: {len(claims['claims'])} claims, {len(evidence['evidence'])} evidence records, {len(products['products'])} products")
        return
    for path, payload in outputs.items():
        write_json(path, payload)
    print(f"Wrote compliance baseline: {len(claims['claims'])} claims, {len(evidence['evidence'])} evidence records, {len(products['products'])} products")


if __name__ == "__main__":
    main()
