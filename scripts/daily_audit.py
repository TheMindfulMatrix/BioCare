#!/usr/bin/env python3
"""Read-only repository/live parity checks for the permanent daily audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit


def fetch(url: str) -> tuple[int, bytes]:
    request = urllib.request.Request(url, headers={"User-Agent": "MindfulMatrixDailyAudit/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--audited-sha", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    sitemap = ET.parse(root / "sitemap.xml").getroot()
    namespace = {"s": "http://www.sitemaps.org/sitemap/0.9"}
    urls = [node.text or "" for node in sitemap.findall("s:url/s:loc", namespace)]
    page_results = []
    asset_urls: set[str] = set()
    for url in urls:
        status, body = fetch(url)
        path = urlsplit(url).path.split("/BioCare/", 1)[-1]
        local = root / (path or "index.html")
        local_body = local.read_bytes() if local.is_file() else b""
        parity = status == 200 and hashlib.sha256(body).digest() == hashlib.sha256(local_body).digest()
        page_results.append({"url": url, "status": status, "byte_parity": parity})
        if status == 200:
            markup = body.decode("utf-8", errors="replace")
            for value in re.findall(r'(?:src|href)=["\']([^"\']+)', markup):
                clean = value.split("#", 1)[0]
                if clean.startswith(("assets/", "../assets/")):
                    asset_urls.add(urllib.parse.urljoin(url, clean))
    asset_results = []
    for url in sorted(asset_urls):
        status, _ = fetch(url)
        asset_results.append({"url": url, "status": status})
    regressions = [item for item in page_results if item["status"] != 200 or not item["byte_parity"]]
    broken_assets = [item for item in asset_results if item["status"] != 200]
    overall = "HEALTHY" if not regressions and not broken_assets else "ACTION REQUIRED"
    report = {
        "overall_status": overall,
        "audited_repository_sha": args.audited_sha,
        "live_deployment_sha": None,
        "live_deployment_sha_note": "Set by the workflow when the Pages deployment API exposes a matching SHA.",
        "public_pages": len(page_results),
        "page_regressions": regressions,
        "referenced_live_assets": len(asset_results),
        "broken_live_assets": broken_assets,
        "next_actions": [
            "Address confirmed page or asset regressions before optional improvements.",
            "Review the current compliance triage queue without weakening the hard gate.",
            "Review asset-inventory orphan candidates before any future removal.",
        ],
        "changes_made": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    if overall != "HEALTHY":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
