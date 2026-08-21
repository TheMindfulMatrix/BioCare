#!/usr/bin/env python3
"""Create a sanitized public-source manifest from an explicit reviewed allowlist."""

from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit


ALLOWED_CLASS = "PUBLIC WEBSITE ELIGIBLE"
BLOCKED_CLASSES = {"RESEARCH / REFERENCE ONLY", "ONE-TO-ONE ONLY", "INTERNAL / PARTNER ONLY", "EXCLUDED"}
BLOCKED_ROLES = {"research_lead_only", "internal_compliance_rule", "excluded_business_material"}
BLOCKED_HOSTS = {
    "github.com",
    "raw.githubusercontent.com",
    "api.github.com",
    "zinzinowebstorage.blob.core.windows.net",
}
SENSITIVE_QUERY_KEYS = {"token", "access_token", "auth", "authorization", "sig", "signature", "se", "sp", "sv"}
RESTRICTED_TERMS = re.compile(
    r"\b(?:compensation|commission|income|recruit(?:ing)?|downline|rank advancement|business opportunity|pay point|enrollment point)\b",
    re.IGNORECASE,
)
REQUIRED_FIELDS = {
    "id",
    "title",
    "publisher",
    "manufacturer",
    "resource_type",
    "evidence_role",
    "topic_ids",
    "department_ids",
    "product_ids",
    "article_ids",
    "public_url",
    "final_url",
    "publication_date",
    "checked_date",
    "market",
    "language",
    "public_use_status",
    "independence_status",
    "public_summary",
    "scope",
    "limitations",
    "rights_evidence",
    "status",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_public_url(value: str) -> None:
    parsed = urlsplit(value)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not host:
        raise ValueError("Public sources require an absolute HTTPS URL")
    if host in BLOCKED_HOSTS or host.endswith(".githubusercontent.com") or "zinzino-library" in value.lower():
        raise ValueError("Private, repository, and temporary blob URLs cannot be promoted")
    query_keys = {key.lower() for key, _ in parse_qsl(parsed.query, keep_blank_values=True)}
    if query_keys & SENSITIVE_QUERY_KEYS:
        raise ValueError("Signed, authenticated, or tokenized URLs cannot be promoted")


def promote(audit: dict, allowlist: dict) -> dict:
    if allowlist.get("source_repo_sha") != audit.get("source_repo_sha"):
        raise ValueError("Allowlist source SHA must match the audited private source SHA")
    audited = {record["resource_id"]: record for record in audit.get("resources", [])}
    promoted: list[dict] = []
    seen: set[str] = set()
    for candidate in allowlist.get("records", []):
        resource_id = candidate.get("resource_id")
        if not resource_id or resource_id in seen:
            raise ValueError("Every allowlist resource_id must be explicit and unique")
        seen.add(resource_id)
        source = audited.get(resource_id)
        if not source:
            raise ValueError(f"Allowlisted resource is absent from audit: {resource_id}")
        classification = source.get("rights_classification")
        if classification in BLOCKED_CLASSES or classification != ALLOWED_CLASS:
            raise ValueError(f"Rights are not affirmatively public for {resource_id}: {classification}")
        if source.get("evidence_role") in BLOCKED_ROLES:
            raise ValueError(f"Evidence role cannot be publicly promoted: {source.get('evidence_role')}")
        public_record = candidate.get("public_record")
        if not isinstance(public_record, dict) or set(public_record) != REQUIRED_FIELDS:
            missing = sorted(REQUIRED_FIELDS - set(public_record or {}))
            extra = sorted(set(public_record or {}) - REQUIRED_FIELDS)
            raise ValueError(f"Public record fields mismatch for {resource_id}; missing={missing}, extra={extra}")
        if public_record["id"] != resource_id:
            raise ValueError("Public id must equal the reviewed audit resource id")
        if public_record.get("status") != "published":
            raise ValueError("Promotion writes only explicitly published records")
        if not public_record.get("checked_date") or not public_record.get("rights_evidence"):
            raise ValueError("Checked date and affirmative rights evidence are required")
        if not public_record.get("scope") or not public_record.get("limitations"):
            raise ValueError("Scope and limitations are required")
        validate_public_url(public_record["public_url"])
        validate_public_url(public_record["final_url"])
        public_text = " ".join(str(public_record.get(key, "")) for key in ("title", "public_summary", "scope"))
        if RESTRICTED_TERMS.search(public_text):
            raise ValueError("Business, recruiting, compensation, or partner-administration material cannot be promoted")
        if source.get("evidence_role") in {"peer_reviewed_primary_study", "systematic_review", "meta_analysis"}:
            if not (source.get("doi") or source.get("pmid")) or not candidate.get("independent_citation_verified"):
                raise ValueError("Science promotion requires a matched DOI/PMID and explicit independent citation verification")
        promoted.append(public_record)
    return {
        "schema_version": "1.0",
        "checked_date": allowlist["checked_date"],
        "records": sorted(promoted, key=lambda record: record["id"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--allowlist", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    payload = promote(load(args.audit), load(args.allowlist))
    serialized = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    current = args.output.read_text(encoding="utf-8") if args.output.exists() else ""
    diff = "".join(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            serialized.splitlines(keepends=True),
            fromfile=str(args.output),
            tofile=f"{args.output} (candidate)",
        )
    )
    if args.dry_run:
        print(diff or "No public-manifest changes.")
        return
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(serialized, encoding="utf-8", newline="\n")
    print(diff or "Public manifest written with no content changes.")


if __name__ == "__main__":
    main()
