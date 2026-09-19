"""Canonical page inventory and fail-closed sitemap mapping for root/subpath hosting."""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

SITEMAP_NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"


def canonical_page_paths(library: dict, discovery: dict, catalog: dict) -> list[str]:
    paths = ["", "start.html", "library.html", "evidence.html", "shop.html",
             "know-your-number.html", "explore.html", "core-four.html", "about.html", "privacy.html", "testing.html", "learning.html", "partners.html"]
    paths.extend(f'departments/{item["slug"]}.html' for item in discovery["departments"])
    paths.extend(f'library/{item["slug"]}.html' for item in library["articles"] if item.get("status") == "published")
    paths.extend(f'products/{item["id"]}.html' for item in catalog["products"] if item.get("commercial_status") == "active")
    if len(paths) != len(set(paths)):
        raise ValueError("Canonical build inventory contains duplicate page paths")
    for path in paths:
        if path.startswith("/") or "\\" in path or any(part in {".", ".."} for part in path.split("/")) or urlsplit(path).scheme:
            raise ValueError(f"Unsafe canonical page path: {path}")
    return paths


def normalize_base_url(value: str) -> str:
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Audit base URL must be an absolute HTTP(S) directory URL without credentials, query, or fragment")
    return value.rstrip("/") + "/"


def canonical_base_url(root: Path) -> str:
    site = json.loads((root / "content/site.json").read_text(encoding="utf-8"))
    return normalize_base_url(site["site"]["metadata"]["canonicalBaseUrl"])


def audited_page_paths(root: Path) -> list[str]:
    """Reject missing, empty, duplicate, wrong-domain, or partial sitemaps."""
    def read(name: str) -> dict:
        return json.loads((root / "content" / name).read_text(encoding="utf-8"))

    paths = canonical_page_paths(read("library.json"), read("discovery.json"), read("catalog.json"))
    base = canonical_base_url(root)
    expected = [base + path for path in paths]
    sitemap = ET.parse(root / "sitemap.xml").getroot()
    if sitemap.tag != f"{{{SITEMAP_NAMESPACE}}}urlset":
        raise ValueError("Invalid sitemap namespace or root element")
    urls = [(node.text or "").strip() for node in sitemap.findall(f"{{{SITEMAP_NAMESPACE}}}url/{{{SITEMAP_NAMESPACE}}}loc")]
    if not urls or len(urls) != len(set(urls)) or set(urls) != set(expected):
        raise ValueError(f"Incomplete sitemap coverage: expected {len(expected)} unique canonical pages, found {len(urls)}")
    missing = [path or "index.html" for path in paths if not (root / (path or "index.html")).is_file()]
    if missing:
        raise ValueError(f"Missing generated pages: {', '.join(missing)}")
    return paths
