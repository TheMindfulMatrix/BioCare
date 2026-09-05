#!/usr/bin/env python3
"""Read-only, fail-closed repository/live parity checks for the daily audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

if __package__:
    from .site_paths import audited_page_paths, canonical_base_url, normalize_base_url
else:
    from site_paths import audited_page_paths, canonical_base_url, normalize_base_url


def fetch(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "MindfulMatrixDailyAudit/2.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return {"status": response.status, "body": response.read(), "final_url": response.url}
    except urllib.error.HTTPError as error:
        return {"status": error.code, "body": b"", "final_url": error.url, "error": str(error)}
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        return {"status": None, "body": b"", "final_url": None, "error": str(error)}


class AssetReferences(HTMLParser):
    def __init__(self, markup: str):
        super().__init__()
        self.references: list[str] = []
        self.data_references: list[str] = []
        self.json_chunks = None
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.references.extend(values[name] for name in ("src", "href", "poster", "data-src") if values.get(name))
        if tag == "meta" and (values.get("property") == "og:image" or values.get("name") == "twitter:image") and values.get("content"):
            self.references.append(values["content"])
        if values.get("srcset"):
            self.references.extend(item.strip().split()[0] for item in values["srcset"].split(",") if item.strip())
        if tag == "script" and values.get("type") in {"application/json", "application/ld+json"}:
            self.json_chunks = []

    def handle_data(self, data):
        if self.json_chunks is not None:
            self.json_chunks.append(data)

    def handle_endtag(self, tag):
        if tag != "script" or self.json_chunks is None:
            return

        def strings(value):
            if isinstance(value, str):
                self.data_references.append(value)
            elif isinstance(value, dict):
                for item in value.values():
                    strings(item)
            elif isinstance(value, list):
                for item in value:
                    strings(item)

        strings(json.loads("".join(self.json_chunks)))
        self.json_chunks = None


def asset_paths(root: Path, pages: list[str]) -> list[str]:
    """Discover expected assets from the build, never from possibly broken live HTML."""
    base = canonical_base_url(root)
    assets: set[str] = set()

    def add(reference: str, source: str) -> None:
        absolute = urljoin(base + source, reference)
        parsed = urlsplit(absolute)
        if parsed.scheme not in {"http", "https"} or not absolute.startswith(base):
            return
        relative = unquote(absolute[len(base):].split("?", 1)[0].split("#", 1)[0])
        if not relative.startswith(("assets/", "img/")):
            return
        target = (root / relative).resolve()
        if not target.is_relative_to(root):
            raise ValueError(f"Asset reference escapes the build: {relative}")
        if not target.is_file():
            raise ValueError(f"Missing expected local asset: {relative}")
        assets.add(relative)

    for relative in pages:
        markup = AssetReferences((root / (relative or "index.html")).read_text(encoding="utf-8"))
        for reference in markup.references:
            add(reference, relative)
        # Canonical search/catalog payload paths are build-root-relative, even
        # when embedded on nested product pages; JS applies the page prefix.
        for reference in markup.data_references:
            if reference.startswith(("assets/", "img/", base)):
                add(reference, "")
    scanned: set[str] = set()
    while pending := sorted(path for path in assets - scanned if path.endswith(".css")):
        for relative in pending:
            scanned.add(relative)
            css = (root / relative).read_text(encoding="utf-8")
            for reference in re.findall(r"url\(\s*['\"]?([^)'\"\s]+)", css):
                add(reference, relative)
    if not assets:
        raise ValueError("Empty asset coverage: refusing to report a healthy audit")
    return sorted(assets)


def build_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    # GitHub's Linux checkout and the canonical builder use LF text bytes.
    if path.suffix in {".html", ".css", ".js", ".json", ".svg", ".xml", ".txt"}:
        data = data.replace(b"\r\n", b"\n")
    return data


def audit_site(root: Path, base_url: str, audited_sha: str, *, fetcher=None) -> dict:
    root = root.resolve()
    report = {
        "overall_status": "ACTION REQUIRED",
        "audited_repository_sha": audited_sha,
        "base_url": base_url,
        "public_pages": 0,
        "referenced_live_assets": 0,
        "coverage_errors": [],
        "page_results": [],
        "asset_results": [],
        "page_regressions": [],
        "broken_live_assets": [],
        "changes_made": False,
        "next_actions": ["Address confirmed coverage, page, or asset failures before optional improvements.",
                         "Preserve and review the inherited compliance advisory queue."],
    }
    try:
        base = normalize_base_url(base_url)
        pages = audited_page_paths(root)
        assets = asset_paths(root, pages)
    except (ValueError, OSError, KeyError, ET.ParseError) as error:
        report["coverage_errors"].append(str(error))
        return report

    fetcher = fetcher or fetch

    def inspect(relative: str) -> dict:
        url = base + relative
        response = fetcher(url)
        body = response.get("body", b"")
        expected = build_bytes(root / (relative or "index.html"))
        return {"path": relative or "index.html", "url": url,
                "status": response.get("status"), "final_url": response.get("final_url"),
                "error": response.get("error"),
                "byte_parity": response.get("status") == 200 and hashlib.sha256(body).digest() == hashlib.sha256(expected).digest()}

    with ThreadPoolExecutor(max_workers=6) as pool:
        report["page_results"] = list(pool.map(inspect, pages))
        report["asset_results"] = list(pool.map(inspect, assets))
    report["public_pages"] = len(report["page_results"])
    report["expected_public_pages"] = len(pages)
    report["referenced_live_assets"] = len(report["asset_results"])
    report["page_regressions"] = [item for item in report["page_results"] if not item["byte_parity"]]
    report["broken_live_assets"] = [item for item in report["asset_results"] if not item["byte_parity"]]
    if not report["page_regressions"] and not report["broken_live_assets"]:
        report["overall_status"] = "HEALTHY"
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--audited-sha", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit_site(args.root, args.base_url, args.audited_sha)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: value for key, value in report.items() if key not in {"page_results", "asset_results"}}, indent=2))
    if report["overall_status"] != "HEALTHY":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
