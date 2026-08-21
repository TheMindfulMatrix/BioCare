#!/usr/bin/env python3
"""Measure deterministic static-site payload and markup metrics."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


class NodeCounter(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.nodes = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.nodes += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.nodes += 1


def public_pages(root: Path) -> list[Path]:
    sitemap = ET.parse(root / "sitemap.xml").getroot()
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    pages = []
    for element in sitemap.findall("s:url/s:loc", namespace):
        path = urlsplit(element.text or "").path
        marker = "/BioCare/"
        relative = path.split(marker, 1)[1] if marker in path else path.lstrip("/")
        pages.append(root / (relative or "index.html"))
    return pages


def file_bytes(paths: list[Path]) -> int:
    return sum(path.stat().st_size for path in paths if path.is_file())


def image_metrics(root: Path) -> dict:
    catalog_path = root / "content" / "catalog.json"
    if not catalog_path.is_file():
        return {"active_product_image_bytes": None, "active_product_image_count": None}
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    paths: set[Path] = set()
    for product in catalog["products"]:
        if product.get("commercial_status") != "active":
            continue
        for role in ("cutout", "artwork", "image"):
            source = (product.get(role) or {}).get("src")
            if source and not source.startswith(("http://", "https://", "data:")):
                paths.add(root / source)
    return {"active_product_image_bytes": file_bytes(list(paths)), "active_product_image_count": len(paths)}


def measure(root: Path, label: str, git_sha: str) -> dict:
    pages = public_pages(root)
    html_bytes = {str(path.relative_to(root)).replace("\\", "/"): path.stat().st_size for path in pages}
    dom_nodes: dict[str, int] = {}
    lazy_assets = 0
    for path in pages:
        markup = path.read_text(encoding="utf-8")
        parser = NodeCounter()
        parser.feed(markup)
        relative = str(path.relative_to(root)).replace("\\", "/")
        dom_nodes[relative] = parser.nodes
        lazy_assets += len(re.findall(r'loading=["\']lazy["\']', markup))
    css = list((root / "assets" / "css").glob("*.css"))
    javascript = list((root / "assets" / "js").glob("*.js"))
    images = [path for path in (root / "assets").rglob("*") if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"}]
    evidence = root / "evidence.html"
    evidence_markup = evidence.read_text(encoding="utf-8") if evidence.is_file() else ""
    evidence_initial_assets = set(re.findall(r'(?:href|src)=["\']([^"\']+)["\']', evidence_markup))
    evidence_initial_assets = {item.split("#", 1)[0].split("?", 1)[0] for item in evidence_initial_assets if not item.startswith(("http://", "https://", "#"))}
    evidence_initial_assets = {item for item in evidence_initial_assets if Path(item).suffix.lower() in {".css", ".js", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}}
    result = {
        "label": label,
        "git_sha": git_sha,
        "public_page_count": len(pages),
        "html_bytes": sum(html_bytes.values()),
        "html_bytes_by_page": html_bytes,
        "dom_nodes": sum(dom_nodes.values()),
        "dom_nodes_by_page": dom_nodes,
        "css_bytes": file_bytes(css),
        "javascript_bytes": file_bytes(javascript),
        "universal_search_index_bytes": (root / "assets" / "data" / "search-index.json").stat().st_size,
        "public_source_manifest_bytes": (root / "content" / "resources" / "public-sources.json").stat().st_size if (root / "content" / "resources" / "public-sources.json").is_file() else 0,
        "all_image_asset_bytes": file_bytes(images),
        "all_image_asset_count": len(images),
        "lazy_asset_references": lazy_assets,
        "evidence_initial_request_upper_bound": 1 + len(evidence_initial_assets) if evidence_markup else None,
        "evidence_initial_local_assets": sorted(evidence_initial_assets),
        **image_metrics(root),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--git-sha", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = measure(args.root.resolve(), args.label, args.git_sha)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: value for key, value in result.items() if not key.endswith("_by_page")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
