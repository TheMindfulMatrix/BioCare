#!/usr/bin/env python3
"""Read-only, fail-closed repository/live parity checks for the daily audit."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

if __package__:
    from .site_paths import SITEMAP_NAMESPACE, audited_page_paths, canonical_base_url, normalize_base_url
else:
    from site_paths import SITEMAP_NAMESPACE, audited_page_paths, canonical_base_url, normalize_base_url


def fetch(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "MindfulMatrixDailyAudit/2.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return {"status": response.status, "body": response.read(), "final_url": response.url}
    except urllib.error.HTTPError as error:
        return {"status": error.code, "body": b"", "final_url": error.url, "error": str(error)}
    except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException) as error:
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


def validate_robots(body: bytes, canonical_base: str) -> dict:
    """Check the generated public crawl policy, tolerating comments/extensions."""
    errors: list[str] = []
    sitemaps: list[str] = []
    groups: list[dict] = []
    current = None
    for number, line in enumerate(body.decode("utf-8-sig").splitlines(), 1):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        name, separator, value = line.partition(":")
        name, value = name.strip().lower(), value.strip()
        if not separator or not name:
            errors.append(f"Malformed robots.txt directive on line {number}")
        elif name == "sitemap":
            sitemaps.append(value)
        elif name == "user-agent":
            if not value:
                errors.append(f"Empty robots.txt user-agent on line {number}")
            if current is None or current["rules"]:
                current = {"agents": [], "rules": []}
                groups.append(current)
            current["agents"].append(value)
        elif name in {"allow", "disallow"}:
            if current is None:
                errors.append(f"robots.txt {name} outside a user-agent group on line {number}")
            else:
                current["rules"].append((name, value))
        # Unrelated extension directives do not change the crawl policy.
    wildcard_rules = [rule for group in groups if "*" in group["agents"] for rule in group["rules"]]
    if ("allow", "/") not in wildcard_rules:
        errors.append("robots.txt must declare User-agent: * with Allow: /")
    if any(name == "disallow" and value for group in groups for name, value in group["rules"]):
        errors.append("robots.txt restricts the expected unrestricted public crawl policy")
    if sitemaps != [canonical_base + "sitemap.xml"]:
        errors.append("robots.txt must declare exactly the configured canonical Sitemap URL")
    return {"sitemap_urls": sitemaps, "validation_errors": errors}


def validate_live_sitemap(body: bytes, expected_urls: list[str]) -> dict:
    """Validate live XML independently of the already validated build sitemap."""
    errors: list[str] = []
    sitemap = ET.fromstring(body)
    namespace = f"{{{SITEMAP_NAMESPACE}}}"
    if sitemap.tag != namespace + "urlset":
        errors.append("Invalid live sitemap namespace or root element")
    urls: list[str] = []
    for entry in sitemap:
        locations = entry.findall(namespace + "loc")
        if entry.tag != namespace + "url" or len(locations) != 1 or len(locations[0]):
            errors.append("Every live sitemap entry must contain exactly one canonical loc element")
            continue
        urls.append((locations[0].text or "").strip())
    duplicates = sorted(url for url, count in Counter(urls).items() if count > 1)
    missing = sorted(set(expected_urls) - set(urls))
    unexpected = sorted(set(urls) - set(expected_urls))
    if not urls or missing or unexpected or duplicates:
        errors.append(f"Incomplete live sitemap coverage: expected {len(expected_urls)} unique canonical pages, found {len(urls)}")
    return {"declared_public_pages": len(urls), "missing_urls": missing,
            "unexpected_urls": unexpected, "duplicate_urls": duplicates,
            "validation_errors": errors}


def inspect_crawl_metadata(root: Path, base: str, canonical_base: str, pages: list[str], fetcher, relative: str) -> dict:
    url = base + relative
    result = {"path": relative, "url": url, "canonical_url": canonical_base + relative,
              "status": None, "final_url": None, "error": None, "byte_parity": False,
              "validation_errors": [], "passed": False}
    try:
        response = fetcher(url)
        result.update({name: response.get(name) for name in ("status", "final_url", "error")})
        body = response.get("body", b"")
        result["byte_parity"] = response.get("status") == 200 and body == build_bytes(root / relative)
        if result["status"] != 200 or result["error"]:
            result["validation_errors"].append(f"Failed to fetch {relative}: HTTP {result['status']}; {result['error'] or 'no successful response'}")
        if result["final_url"] != url:
            result["validation_errors"].append(f"Unexpected {relative} redirect: expected {url}, received {result['final_url']}")
        if result["status"] == 200 and not result["error"]:
            validation = (validate_robots(body, canonical_base) if relative == "robots.txt"
                          else validate_live_sitemap(body, [canonical_base + path for path in pages]))
            result["validation_errors"].extend(validation.pop("validation_errors"))
            result.update(validation)
    except (ValueError, OSError, http.client.HTTPException, ET.ParseError) as error:
        result["error"] = str(error)
        result["validation_errors"].append(f"Unable to read or validate {relative}: {error}")
    # Metadata is checked semantically; formatting/comments/extensions may differ.
    result["passed"] = not result["validation_errors"]
    return result


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
        "crawl_metadata_results": [],
        "crawl_metadata_failures": [],
        "page_regressions": [],
        "broken_live_assets": [],
        "changes_made": False,
        "next_actions": ["Address confirmed coverage, page, asset, or crawl metadata failures before optional improvements.",
                         "Preserve and review the inherited compliance advisory queue."],
    }
    try:
        base = normalize_base_url(base_url)
        canonical_base = canonical_base_url(root)
        report["canonical_base_url"] = canonical_base
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
        report["crawl_metadata_results"] = list(pool.map(
            lambda relative: inspect_crawl_metadata(root, base, canonical_base, pages, fetcher, relative),
            ("robots.txt", "sitemap.xml")))
    report["public_pages"] = len(report["page_results"])
    report["expected_public_pages"] = len(pages)
    report["referenced_live_assets"] = len(report["asset_results"])
    report["page_regressions"] = [item for item in report["page_results"] if not item["byte_parity"]]
    report["broken_live_assets"] = [item for item in report["asset_results"] if not item["byte_parity"]]
    report["crawl_metadata_failures"] = [item for item in report["crawl_metadata_results"] if not item["passed"]]
    if not report["page_regressions"] and not report["broken_live_assets"] and not report["crawl_metadata_failures"]:
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
