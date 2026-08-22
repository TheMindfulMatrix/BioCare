#!/usr/bin/env python3
"""Inventory public runtime assets separately from archived source artwork."""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ASSET_PATTERN = re.compile(r"(?:\.\./)*assets/[A-Za-z0-9_./-]+(?:\?[A-Za-z0-9_.=&-]+)?")


def public_pages(root: Path) -> list[Path]:
    sitemap = ET.parse(root / "sitemap.xml").getroot()
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    pages: list[Path] = []
    for node in sitemap.findall("s:url/s:loc", namespace):
        path = urlsplit(node.text or "").path
        relative = path.split("/BioCare/", 1)[-1]
        pages.append(root / (relative or "index.html"))
    return pages


def normalize_reference(page: Path, value: str, root: Path) -> str | None:
    clean = value.split("?", 1)[0].split("#", 1)[0]
    page_dir = page.relative_to(root).parent.as_posix()
    relative = posixpath.normpath(posixpath.join(page_dir, clean))
    if relative.startswith("assets/") and (root / PurePosixPath(relative)).is_file():
        return relative
    return None


def inventory(root: Path) -> dict:
    runtime: set[str] = set()
    pages = public_pages(root)
    for page in pages:
        markup = page.read_text(encoding="utf-8")
        for match in ASSET_PATTERN.findall(markup):
            reference = normalize_reference(page, match, root)
            if reference:
                runtime.add(reference)

    # CSS can introduce additional local runtime assets through url().
    pending = [item for item in runtime if item.endswith(".css")]
    while pending:
        css_relative = pending.pop()
        css_path = root / PurePosixPath(css_relative)
        for raw in re.findall(r"url\((?:['\"])?([^)'\"]+)", css_path.read_text(encoding="utf-8")):
            if raw.startswith(("data:", "http://", "https://", "#")):
                continue
            resolved = posixpath.normpath(posixpath.join(PurePosixPath(css_relative).parent.as_posix(), raw.split("?", 1)[0]))
            candidate = root / PurePosixPath(resolved)
            if resolved.startswith("assets/") and candidate.is_file() and resolved not in runtime:
                runtime.add(resolved)
                if resolved.endswith(".css"):
                    pending.append(resolved)

    all_public = sorted(path for path in (root / "assets").rglob("*") if path.is_file())
    archived = sorted(path for path in (root / "_source-assets").rglob("*") if path.is_file())
    runtime_paths = sorted(root / PurePosixPath(item) for item in runtime)
    runtime_set = {path.resolve() for path in runtime_paths}
    orphaned = [path for path in all_public if path.resolve() not in runtime_set]

    def entry(path: Path) -> dict:
        return {"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size}

    return {
        "schema_version": "1.0.0",
        "public_page_count": len(pages),
        "repository_asset_bytes_before_boundary": sum(path.stat().st_size for path in all_public + archived),
        "repository_asset_count_before_boundary": len(all_public) + len(archived),
        "public_assets_directory_bytes": sum(path.stat().st_size for path in all_public),
        "public_assets_directory_count": len(all_public),
        "referenced_runtime_asset_bytes": sum(path.stat().st_size for path in runtime_paths),
        "referenced_runtime_asset_count": len(runtime_paths),
        "excluded_source_archive_bytes": sum(path.stat().st_size for path in archived),
        "excluded_source_archive_count": len(archived),
        "published_payload_reduction_bytes": sum(path.stat().st_size for path in archived),
        "largest_runtime_assets": [entry(path) for path in sorted(runtime_paths, key=lambda item: item.stat().st_size, reverse=True)[:15]],
        "orphaned_public_assets": [entry(path) for path in orphaned],
        "archived_source_assets": [entry(path) for path in archived],
        "notes": [
            "The before-boundary figure is repository asset storage, not initial page-transfer weight.",
            "Leading-underscore _source-assets is excluded by GitHub Pages' Jekyll publishing boundary.",
            "Orphaned assets are reported for review and are not deleted automatically.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = inventory(args.root.resolve())
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    print(payload, end="")


if __name__ == "__main__":
    main()
