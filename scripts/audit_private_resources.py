#!/usr/bin/env python3
"""Create a deterministic, read-only audit of a private resource library.

The detailed output is intentionally local-only. BioCare ignores ``_private/``
and its public build never imports this module or reads its output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote, unquote


ROOT = Path(__file__).resolve().parents[1]
PRIVATE_ROOT = ROOT / "_private"

RIGHTS_CLASSES = (
    "PUBLIC WEBSITE ELIGIBLE",
    "RESEARCH / REFERENCE ONLY",
    "ONE-TO-ONE ONLY",
    "INTERNAL / PARTNER ONLY",
    "EXCLUDED",
)

EVIDENCE_ROLES = (
    "manufacturer_product_fact",
    "manufacturer_label",
    "manufacturer_testing_procedure",
    "manufacturer_quality_document",
    "manufacturer_policy",
    "manufacturer_approved_claim",
    "independent_guideline",
    "systematic_review",
    "meta_analysis",
    "peer_reviewed_primary_study",
    "government_public_health",
    "research_lead_only",
    "internal_compliance_rule",
    "excluded_business_material",
)

EXCLUDED_PATTERNS = (
    r"compensation", r"business-presentation", r"salespresentation", r"short-presentation",
    r"partner-enrollment", r"pay-point", r"price-list", r"customerpoints",
    r"get-started", r"goal-plan", r"weekly-chart", r"director-trip",
    r"brand-ambassador", r"ambassador-application", r"influencer-application",
    r"(?:^|-)events?(?:-|_|$)", r"zinzinoevent", r"customerorderform", r"customersubscriptionterms", r"transferofcountry",
    r"shared-shopping-cart", r"join-teamzinzino", r"lifestyle-guide",
)

INTERNAL_PATTERNS = (
    r"marketing-rules", r"health-claims", r"partnercontract", r"policiesandprocedures",
    r"partner-online-sales", r"integritypolicy", r"social-selling", r"social-media",
    r"social-content", r"social-guide", r"social-media-hashtags", r"prospecting",
    r"change-facebook", r"change-instagram", r"communication-tips", r"trustpilot",
    r"before-after", r"how-to-navigate-facebook", r"signing-up-for-.*newsletter",
    r"tips-for-video-calls", r"gocore", r"go-core", r"instagram-and-facebook-names",
    r"marketing-rules-and-ethics-presentation",
)

RESEARCH_PATTERNS = (
    r"affron", r"antioxidant-effects", r"balance-skin-study", r"bioavailability",
    r"epaanddha", r"evidenceofthepositive", r"fainadrop", r"fontani", r"fromalgatoomega",
    r"internationaljournal", r"jnfs_", r"measurementofomega", r"ncbi_", r"omega-3fatty",
    r"omega-6-omega-3", r"omega3andpregnancy", r"optimalheart", r"preventative-health",
    r"reductionofheart", r"sd_maternal", r"serumpolyunsaturated", r"simopoulos",
    r"theimportanceoftheomega", r"treatmentofmajor", r"vitamin-d-the-essentials",
    r"what-a-single-drop", r"who_", r"whonutrition", r"skin-serum-and-effects",
)

TOPIC_RULES = {
    "omega-3": (r"omega", r"fatty acid", r"epa", r"dha", r"balanceoil"),
    "testing-and-biomarkers": (r"test", r"blood spot", r"biomarker", r"hba1c", r"measurement"),
    "vitamin-d": (r"vitamin d", r"vitamin-d"),
    "gut-and-digestion": (r"gut", r"microbi", r"beta.?glucan", r"baker.?s yeast"),
    "skin-and-collagen": (r"skin", r"collagen", r"elasticity"),
    "saffron-and-mood": (r"affron", r"saffron", r"mood", r"depress"),
    "pregnancy": (r"pregnan", r"maternal", r"fetal", r"foetal"),
    "quality-and-certification": (r"certificate", r"conformity", r"quality", r"halal", r"kosher", r"vegan"),
    "partner-compliance": (r"marketing rule", r"health claim", r"partner contract", r"policies and procedures"),
    "business-operations": (r"compensation", r"pay point", r"enrollment", r"career", r"prospect", r"business presentation"),
}

DEPARTMENT_BY_TOPIC = {
    "omega-3": "omega-nutrition",
    "testing-and-biomarkers": "test-measure",
    "vitamin-d": "daily-wellness",
    "gut-and-digestion": "gut-digestion",
    "skin-and-collagen": "healthy-aging",
    "saffron-and-mood": "daily-wellness",
    "pregnancy": "daily-wellness",
    "quality-and-certification": "daily-wellness",
}

ARTICLE_BY_TOPIC = {
    "omega-3": ["omega-3-what-the-numbers-mean", "food-vs-omega-3-supplements"],
    "testing-and-biomarkers": ["how-to-read-a-health-study", "should-you-test-your-omega-3-levels"],
    "gut-and-digestion": ["gut-health-101", "gut-testing-biomarkers"],
    "skin-and-collagen": ["how-to-read-a-health-study"],
    "quality-and-certification": ["how-to-read-a-supplement-label"],
}

PRODUCT_RULES = {
    "balance-test": (r"balance.?test", r"dried blood spot", r"single drop of blood"),
    "hba1c-test": (r"hba1c",),
    "vitamin-d-test": (r"vitamin d test", r"vitamin-d-test"),
    "balanceoil-plus-300ml": (r"balanceoil", r"balance oil"),
    "balanceoil-tutti-frutti": (r"tutti.?frutti",),
    "collagen-boozt": (r"collagen boozt", r"collagen-boozt"),
    "skin-serum": (r"skin serum", r"skin-serum"),
    "viva-plus": (r"viva",),
}

DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
PMID_RE = re.compile(r"\bPMID\s*[:#]?\s*(\d{6,9})\b", re.IGNORECASE)
NCT_RE = re.compile(r"\bNCT\d{8}\b", re.IGNORECASE)
URL_RE = re.compile(r"https://[^\s<>\]\[\"']+", re.IGNORECASE)
SECRET_RE = re.compile(
    r"authorization\s*:\s*bearer|gh[pousr]_[A-Za-z0-9_]{20,}|github_token|"
    r"api[_-]?key\s*[:=]|access[_-]?token\s*[:=]|refresh[_-]?token\s*[:=]|"
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    re.IGNORECASE,
)


def git(source: Path, *arguments: str) -> str:
    safe_source = source.as_posix()
    result = subprocess.run(
        ["git", "-c", f"safe.directory={safe_source}", "-C", str(source), *arguments],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_key(value: str) -> str:
    value = unquote(value).lower().replace(".pdf", "").replace(".txt", "")
    return re.sub(r"[^a-z0-9]+", "", value)


def normalized_title(stem: str) -> str:
    value = unicodedata.normalize("NFKC", stem)
    value = re.sub(r"[_-]+", " ", value)
    value = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", value)
    value = re.sub(r"\.{2,}", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def resource_id(stem: str) -> str:
    value = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode("ascii").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:96]


def manifest_records(source: Path) -> tuple[list[str], dict[str, str]]:
    paths = [line.strip() for line in (source / "_manifest.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
    by_key: dict[str, str] = {}
    for path in paths:
        name = Path(unquote(path)).name
        if name.lower().endswith(".pdf"):
            by_key.setdefault(normalized_key(name), path)
    return paths, by_key


def classify(filename: str) -> tuple[str, str]:
    key = filename.lower()
    for pattern in EXCLUDED_PATTERNS:
        if re.search(pattern, key):
            return "EXCLUDED", "Business, recruiting, event, pricing, compensation, or customer/partner administration is outside the public wellness mission."
    for pattern in INTERNAL_PATTERNS:
        if re.search(pattern, key):
            return "INTERNAL / PARTNER ONLY", "The resource governs partner conduct, compliance, operations, or platform use and is not consumer website material."
    for pattern in RESEARCH_PATTERNS:
        if re.search(pattern, key):
            return "RESEARCH / REFERENCE ONLY", "The resource is a scientific or technical research lead; the private extraction is not a public claim license or citation target."
    return "ONE-TO-ONE ONLY", "Repository governance marks partner materials non-redistributable; this consumer/product resource may inform private explanation only."


def evidence_role(filename: str, classification: str) -> str:
    key = filename.lower()
    if classification == "EXCLUDED":
        return "excluded_business_material"
    if classification == "RESEARCH / REFERENCE ONLY":
        return "research_lead_only"
    if classification == "INTERNAL / PARTNER ONLY":
        if re.search(r"marketing|health-claims|policies|contract|integrity", key):
            return "manufacturer_policy"
        return "internal_compliance_rule"
    if re.search(r"certificate|conformity|quality-symbol|halal|kosher|vegan", key):
        return "manufacturer_quality_document"
    if re.search(r"test-sendings|hba1c|oxidative-stability|questionnaire|sample-destruction", key):
        return "manufacturer_testing_procedure"
    return "manufacturer_product_fact"


def topics_for(filename: str, text: str) -> list[str]:
    haystack = f"{filename}\n{text[:50000]}".lower()
    topics = [topic for topic, patterns in TOPIC_RULES.items() if any(re.search(pattern, haystack) for pattern in patterns)]
    return sorted(topics or ["general-reference"])


def products_for(filename: str, text: str) -> list[str]:
    haystack = f"{filename}\n{text[:20000]}".lower()
    return sorted(product_id for product_id, patterns in PRODUCT_RULES.items() if any(re.search(pattern, haystack) for pattern in patterns))


def market_for(filename: str, text: str) -> str:
    key = filename.lower()
    if re.search(r"usa|us\b|en-us", key):
        return "US"
    if "glo" in key:
        return "GLOBAL"
    if "eu" in key or "europe" in key:
        return "EU"
    if re.search(r"united states|u\.s\.a\.", text[:10000], re.IGNORECASE):
        return "US"
    return "UNSPECIFIED"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-path", type=Path, required=True)
    parser.add_argument("--source-repo-sha", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    source = args.source_path.resolve()
    output = args.output_dir.resolve()
    private_root = PRIVATE_ROOT.resolve()
    if private_root != output and private_root not in output.parents:
        raise SystemExit(f"Private audit output must stay under {private_root}")
    if source == output or source in output.parents or output in source.parents:
        raise SystemExit("Audit output must not overlap the private source repository")
    if not (source / "README.md").is_file() or not (source / "docs").is_dir():
        raise SystemExit("Source repository governance or docs directory is missing")

    before_sha = git(source, "rev-parse", "HEAD")
    before_status = git(source, "status", "--porcelain=v1", "--untracked-files=all")
    if before_sha != args.source_repo_sha:
        raise SystemExit(f"Source SHA mismatch: expected {args.source_repo_sha}, found {before_sha}")

    manifest, manifest_by_key = manifest_records(source)
    doc_paths = sorted((source / "docs").glob("*.txt"), key=lambda path: path.name.casefold())
    resources: list[dict] = []
    hash_groups: dict[str, list[str]] = defaultdict(list)
    secret_files: list[str] = []

    for path in doc_paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        digest = sha256(path)
        hash_groups[digest].append(path.name)
        classification, reason = classify(path.name)
        role = evidence_role(path.name, classification)
        topics = topics_for(path.name, text)
        departments = sorted({DEPARTMENT_BY_TOPIC[topic] for topic in topics if topic in DEPARTMENT_BY_TOPIC})
        article_ids = sorted({slug for topic in topics for slug in ARTICLE_BY_TOPIC.get(topic, [])})
        dois = sorted({match.rstrip(".,;)") for match in DOI_RE.findall(text)}, key=str.casefold)
        pmids = sorted(set(PMID_RE.findall(text)))
        trials = sorted({match.upper() for match in NCT_RE.findall(text)})
        urls = sorted({match.rstrip(".,;)") for match in URL_RE.findall(text)}, key=str.casefold)
        if SECRET_RE.search(text):
            secret_files.append(path.name)
        source_path = manifest_by_key.get(normalized_key(path.name))
        source_url = f"https://zinzinowebstorage.blob.core.windows.net/{quote(source_path, safe='/:%')}" if source_path else None
        page_count = max(1, text.count("\f") + 1)
        table_signal = len(re.findall(r"(?m)^\S.*\s{3,}\S", text))
        figure_signal = bool(re.search(r"\b(fig(?:ure)?|chart|graph)\s*\d*", text, re.IGNORECASE))
        contains_claims = bool(re.search(r"\b(?:supports?|helps?|improves?|reduces?|prevents?|treats?|benefits?)\b", text, re.IGNORECASE))
        business_signal = bool(re.search(r"\b(?:commission|income|career|rank|recruit|downline|pay point|enrollment point|business opportunity)\b", text, re.IGNORECASE))
        references_signal = bool(dois or pmids or re.search(r"\breferences\b|\bbibliography\b", text, re.IGNORECASE))
        products = products_for(path.name, text)
        recommendation = {
            "EXCLUDED": "Do not use in public content, search, metadata, reports, or structured data.",
            "INTERNAL / PARTNER ONLY": "Use only to govern internal compliance decisions; never publish or link this private copy.",
            "ONE-TO-ONE ONLY": "Use only for private explanation where permitted; independently verify any fact before public use.",
            "RESEARCH / REFERENCE ONLY": "Use as a lead to locate the original publisher, DOI, PubMed record, guideline, or stronger review.",
            "PUBLIC WEBSITE ELIGIBLE": "Eligible only after final public-source and rights verification.",
        }[classification]
        resources.append(
            {
                "resource_id": resource_id(path.stem),
                "private_filename": path.name,
                "normalized_title": normalized_title(path.stem),
                "original_filename": Path(unquote(source_path)).name if source_path else None,
                "source_type": "extracted_pdf_text",
                "manufacturer": "Zinzino" if role != "research_lead_only" else "third_party_or_manufacturer_selected",
                "topics": topics,
                "related_product_ids": products,
                "related_skus": [],
                "related_department_ids": departments,
                "related_article_ids": article_ids,
                "language": "en",
                "market": market_for(path.name, text),
                "publication_date": None,
                "update_date": None,
                "original_blob_path": source_path,
                "original_source_url": source_url,
                "source_document_type": "PDF",
                "page_count_estimate": page_count,
                "file_size": path.stat().st_size,
                "sha256": digest,
                "extraction_appears_complete": len(text.strip()) >= 200,
                "tables_may_be_unreliable": table_signal >= 3,
                "figures_missing_from_extraction": figure_signal,
                "contains_product_claims": contains_claims,
                "contains_business_or_recruiting_content": business_signal,
                "cites_independent_evidence": references_signal,
                "doi": dois,
                "pmid": pmids,
                "trial_registration": trials,
                "detected_public_urls": urls,
                "equivalent_source_in_biocare": bool(article_ids),
                "equivalent_public_source_exists": False,
                "public_use_evidence": "none_found",
                "usage_restriction": "private_repository_governance_non_redistributable",
                "rights_classification": classification,
                "classification_reason": reason,
                "evidence_role": role,
                "recommended_website_use": recommendation,
                "limitations": [
                    "Extracted text can interleave columns and omits figures.",
                    "The private copy is not a public citation target or publication license.",
                ],
                "required_independent_verification": classification in {"RESEARCH / REFERENCE ONLY", "ONE-TO-ONE ONLY"} or contains_claims,
            }
        )

    after_sha = git(source, "rev-parse", "HEAD")
    after_status = git(source, "status", "--porcelain=v1", "--untracked-files=all")
    if (before_sha, before_status) != (after_sha, after_status):
        raise SystemExit("Private source repository changed during the read-only audit")

    duplicate_groups = [names for names in hash_groups.values() if len(names) > 1]
    class_totals = Counter(resource["rights_classification"] for resource in resources)
    role_totals = Counter(resource["evidence_role"] for resource in resources)
    payload = {
        "schema_version": "1.0",
        "source_repository": "TheMindfulMatrix/zinzino-library",
        "source_repo_sha": before_sha,
        "source_branch": git(source, "branch", "--show-current"),
        "source_status_before": before_status,
        "source_status_after": after_status,
        "governance_files_read": ["README.md", "INDEX.md", "_manifest.txt"],
        "manifest_entry_count": len(manifest),
        "resource_count": len(resources),
        "rights_classes": list(RIGHTS_CLASSES),
        "evidence_roles": list(EVIDENCE_ROLES),
        "classification_totals": {name: class_totals.get(name, 0) for name in RIGHTS_CLASSES},
        "evidence_role_totals": {name: role_totals.get(name, 0) for name in EVIDENCE_ROLES},
        "duplicate_sha256_groups": duplicate_groups,
        "secret_pattern_files": secret_files,
        "deterministic": True,
        "public_runtime_dependency": False,
        "resources": resources,
    }
    output.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    (output / "resources.json").write_text(serialized, encoding="utf-8", newline="\n")
    summary = {
        "source_repo_sha": before_sha,
        "resource_count": len(resources),
        "manifest_entry_count": len(manifest),
        "classification_totals": payload["classification_totals"],
        "evidence_role_totals": payload["evidence_role_totals"],
        "duplicate_groups": len(duplicate_groups),
        "secret_pattern_files": len(secret_files),
        "private_source_unchanged": True,
    }
    (output / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
