#!/usr/bin/env python3
"""Scan V10 public output and review artifacts for private-content or secret leakage."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
PRIVATE_SOURCE_SHA = "de8c7711a5ca4678d92dd0d0a3ebeba06f7334c7"
SECRET_PATTERNS = {
    "github_token": re.compile(r"(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "sensitive_query": re.compile(r"[?&](?:token|sig|signature|session|password|secret|access_key)=[^&\s\"']+", re.IGNORECASE),
    "cookie_or_session": re.compile(r"(?:set-cookie\s*:|sessionid\s*=|authorization\s*:\s*bearer)", re.IGNORECASE),
}
PRIVATE_OUTPUT_PATTERNS = {
    "private_repository_name": re.compile(r"zinzino-library", re.IGNORECASE),
    "private_source_sha": re.compile(PRIVATE_SOURCE_SHA, re.IGNORECASE),
    "raw_text_document_link": re.compile(r"(?:href|src)=[\"'][^\"']*\.txt(?:[?#\"'])", re.IGNORECASE),
    "private_repository_url": re.compile(r"https?://(?:raw\.)?github(?:usercontent)?\.com/[^\s\"']*zinzino-library", re.IGNORECASE),
}
RESTRICTED_PUBLIC_SOURCE_TERMS = re.compile(r"\b(?:downline|recruit(?:ing|ment)?|income opportunity|compensation plan|commission plan)\b", re.IGNORECASE)


def public_pages(root: Path) -> list[Path]:
    sitemap = ET.parse(root / "sitemap.xml").getroot()
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    pages = []
    for element in sitemap.findall("s:url/s:loc", namespace):
        path = urlsplit(element.text or "").path
        relative = path.split("/BioCare/", 1)[1] if "/BioCare/" in path else path.lstrip("/")
        pages.append(root / (relative or "index.html"))
    return pages


def scan(root: Path = ROOT) -> dict:
    public_paths = public_pages(root)
    public_paths += [root / "assets" / "data" / "search-index.json"]
    public_paths += list((root / "assets" / "js").glob("*.js"))
    public_paths += list((root / "assets").rglob("*.map"))
    review_paths = list((root / "reports" / "v10").glob("*"))
    review_paths += list((root / ".github" / "workflows").glob("*.yml"))
    review_paths += list((root / ".github" / "workflows").glob("*.yaml"))
    paths = sorted({path.resolve() for path in public_paths + review_paths if path.is_file()})
    findings: list[dict[str, str]] = []
    public_set = {path.resolve() for path in public_paths}
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern_name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                findings.append({"file": str(path.relative_to(root.resolve())).replace("\\", "/"), "rule": pattern_name})
        if path in public_set:
            for pattern_name, pattern in PRIVATE_OUTPUT_PATTERNS.items():
                if pattern.search(text):
                    findings.append({"file": str(path.relative_to(root.resolve())).replace("\\", "/"), "rule": pattern_name})
    source_surfaces = [root / "evidence.html", root / "content" / "resources" / "public-sources.json", root / "assets" / "data" / "search-index.json"]
    for path in source_surfaces:
        if path.is_file() and RESTRICTED_PUBLIC_SOURCE_TERMS.search(path.read_text(encoding="utf-8")):
            findings.append({"file": str(path.relative_to(root)).replace("\\", "/"), "rule": "business_or_recruiting_source_content"})
    env_files = [path for path in root.rglob(".env*") if ".git" not in path.parts and "_private" not in path.parts]
    for path in env_files:
        findings.append({"file": str(path.relative_to(root)).replace("\\", "/"), "rule": "environment_file"})
    return {
        "schema_version": "1.0",
        "files_scanned": len(paths),
        "public_pages_scanned": len(public_pages(root)),
        "findings": findings,
        "finding_count": len(findings),
        "status": "passed" if not findings else "failed",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = scan()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["findings"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
