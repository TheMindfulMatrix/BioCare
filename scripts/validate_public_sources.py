#!/usr/bin/env python3
"""Validate the sanitized public source manifest and optionally audit live URLs."""

from __future__ import annotations

import argparse
import json
import re
import ssl
from datetime import date
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from promote_public_sources import REQUIRED_FIELDS, RESTRICTED_TERMS, validate_public_url


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "content" / "resources" / "public-sources.json"
ALLOWED_STATUSES = {"published", "pending_review", "pending_external_approval", "rejected"}
ALLOWED_ROLES = {"government_public_health", "independent_guideline"}
ALLOWED_TYPES = {"government_fact_sheet", "government_guideline", "government_consumer_guide", "regulatory_guidance"}
PUBLISHER_HOSTS = {
    "National Institutes of Health, Office of Dietary Supplements": {"ods.od.nih.gov"},
    "National Center for Complementary and Integrative Health": {"www.nccih.nih.gov", "nccih.nih.gov"},
    "MedlinePlus, U.S. National Library of Medicine": {"medlineplus.gov", "www.medlineplus.gov"},
    "U.S. Food and Drug Administration": {"www.fda.gov", "fda.gov"},
    "HHS Office of Disease Prevention and Health Promotion": {"odphp.health.gov", "health.gov"},
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(manifest: dict, *, root: Path = ROOT) -> dict:
    errors: list[str] = []
    if set(manifest) != {"schema_version", "checked_date", "records"}:
        errors.append("Top-level public manifest fields must be exact")
    if manifest.get("schema_version") != "1.0":
        errors.append("Unsupported public manifest schema version")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(manifest.get("checked_date", ""))):
        errors.append("Manifest checked_date must be YYYY-MM-DD")

    catalog = load(root / "content" / "catalog.json")
    library = load(root / "content" / "library.json")
    discovery = load(root / "content" / "discovery.json")
    product_ids = {record["id"] for record in catalog["products"]}
    article_ids = {record["slug"] for record in library["articles"]}
    department_ids = {record["intentId"] for record in discovery["departments"]}
    ids: set[str] = set()
    urls: set[str] = set()
    published = 0
    for index, record in enumerate(manifest.get("records", [])):
        label = record.get("id") or f"record-{index}"
        if set(record) != REQUIRED_FIELDS:
            errors.append(f"{label}: public fields do not match the schema")
            continue
        if record["id"] in ids:
            errors.append(f"{label}: duplicate id")
        ids.add(record["id"])
        if record["public_url"] in urls:
            errors.append(f"{label}: duplicate public URL")
        urls.add(record["public_url"])
        for field in ("public_url", "final_url"):
            try:
                validate_public_url(record[field])
            except ValueError as error:
                errors.append(f"{label}: {field}: {error}")
        if record["status"] not in ALLOWED_STATUSES:
            errors.append(f"{label}: unsupported status")
        if record["status"] == "published":
            published += 1
        if record["evidence_role"] not in ALLOWED_ROLES:
            errors.append(f"{label}: unsupported public evidence role")
        if record["resource_type"] not in ALLOWED_TYPES:
            errors.append(f"{label}: unsupported resource type")
        if record["independence_status"].startswith("independent_") and record["manufacturer"] is not None:
            errors.append(f"{label}: independent source cannot be assigned to a manufacturer")
        if not record["checked_date"] or not record["rights_evidence"] or not record["scope"] or not record["limitations"]:
            errors.append(f"{label}: checked date, rights evidence, scope, and limitations are required")
        if not set(record["department_ids"]) <= department_ids:
            errors.append(f"{label}: unknown department id")
        if not set(record["product_ids"]) <= product_ids:
            errors.append(f"{label}: unknown product id")
        if not set(record["article_ids"]) <= article_ids:
            errors.append(f"{label}: unknown article id")
        public_text = " ".join(str(record[field]) for field in ("title", "public_summary", "scope", "limitations", "rights_evidence"))
        if RESTRICTED_TERMS.search(public_text):
            errors.append(f"{label}: restricted business or compensation language")
        if re.search(r"\.txt\b|zinzino-library|blob\.core\.windows\.net|github(?:usercontent)?\.com", public_text, re.IGNORECASE):
            errors.append(f"{label}: private filename, repository, or blob reference leaked")
    if errors:
        raise ValueError("\n".join(errors))
    return {"record_count": len(manifest.get("records", [])), "published_count": published, "valid": True}


def normalized_words(value: str) -> set[str]:
    return {word for word in re.findall(r"[a-z0-9]+", value.lower()) if len(word) >= 4}


def live_check(record: dict, *, timeout: int) -> dict:
    request = Request(record["public_url"], headers={"User-Agent": "TheMindfulMatrix-PublicSourceAudit/1.0"})
    try:
        with urlopen(request, timeout=timeout, context=ssl.create_default_context()) as response:
            body = response.read(512_000).decode(response.headers.get_content_charset() or "utf-8", errors="replace")
            final_url = response.geturl()
            status_code = response.status
    except HTTPError as error:
        state = "bot_protected" if error.code in {401, 403, 429} else "failed"
        return {"id": record["id"], "status": state, "http_status": error.code, "final_url": error.geturl(), "title_match": None}
    except (URLError, TimeoutError, OSError) as error:
        return {"id": record["id"], "status": "failed", "error": type(error).__name__, "final_url": None, "title_match": None}
    title_match = re.search(r"<title[^>]*>(.*?)</title>", body, re.IGNORECASE | re.DOTALL)
    page_title = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", title_match.group(1)))).strip() if title_match else ""
    expected_host = PUBLISHER_HOSTS.get(record["publisher"], set())
    actual_host = (urlsplit(final_url).hostname or "").lower()
    host_match = actual_host in expected_host
    record_words = normalized_words(record["title"])
    title_words = normalized_words(page_title)
    title_ok = len(record_words & title_words) >= min(2, len(record_words))
    state = "verified" if status_code < 400 and host_match and title_ok else "mismatch"
    return {
        "id": record["id"],
        "status": state,
        "http_status": status_code,
        "final_url": final_url,
        "final_host": actual_host,
        "publisher_match": host_match,
        "title_match": title_ok,
        "page_title": page_title,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--check-urls", action="store_true")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()
    manifest = load(args.manifest)
    summary = validate_manifest(manifest)
    if not args.check_urls:
        print(json.dumps(summary, indent=2, sort_keys=True))
        return
    records = [record for record in manifest["records"] if record["status"] == "published"]
    results = [live_check(record, timeout=args.timeout) for record in records]
    totals = {status: sum(result["status"] == status for result in results) for status in ("verified", "bot_protected", "mismatch", "failed")}
    report = {"checked_date": date.today().isoformat(), "source_count": len(results), "totals": totals, "sources": results}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    if totals["mismatch"] or totals["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
