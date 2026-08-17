#!/usr/bin/env python3
"""Validate content, multipage output, and GitHub Pages subpath assumptions."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.references: list[tuple[str, str]] = []
        self.h1_count = 0
        self.images: list[dict[str, str | None]] = []
        self.canonicals: list[str] = []
        self.titles: list[str] = []
        self.descriptions: list[str] = []
        self.heading_levels: list[int] = []
        self.blank_target_links: list[dict[str, str | None]] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(str(values["id"]))
        if tag == "h1":
            self.h1_count += 1
        if re.fullmatch(r"h[1-6]", tag):
            self.heading_levels.append(int(tag[1]))
        if tag == "img":
            self.images.append(values)
        if tag == "title":
            self._in_title = True
        if tag == "meta" and values.get("name") == "description" and values.get("content"):
            self.descriptions.append(str(values["content"]))
        if tag == "link" and values.get("rel") == "canonical" and values.get("href"):
            self.canonicals.append(str(values["href"]))
        if tag == "a" and values.get("target") == "_blank":
            self.blank_target_links.append(values)
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.references.append((attribute, str(value)))
        if values.get("srcset"):
            for candidate in str(values["srcset"]).split(","):
                self.references.append(("srcset", candidate.strip().split()[0]))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.titles.append(data.strip())


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def is_external(reference: str) -> bool:
    return reference.startswith(("https://", "http://", "mailto:", "tel:", "data:"))


def resolve_local_reference(page: Path, reference: str) -> tuple[Path, str]:
    path_part, _, fragment = reference.partition("#")
    path_part = path_part.split("?", 1)[0]
    target = page if not path_part else (page.parent / unquote(path_part)).resolve()
    return target, fragment


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", header[16:24])


def json_ld_records(generated: str, label: object) -> list[dict]:
    scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', generated, flags=re.DOTALL)
    records: list[dict] = []
    for raw in scripts:
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as error:
            check(False, f"{label}: invalid JSON-LD: {error}")
            continue
        check(payload.get("@context") == "https://schema.org", f"{label}: JSON-LD must use schema.org context")
        graph = payload.get("@graph")
        records.extend(graph if isinstance(graph, list) else [payload])
    return records


def validate_content(site: dict, library: dict) -> None:
    products = site.get("products", [])
    ids = [product.get("id") for product in products]
    check(bool(products), "content/site.json must contain products")
    check(len(ids) == len(set(ids)), "Product IDs must be unique")
    check(site.get("featuredProductId") in ids, "featuredProductId must reference a product")

    metadata = site.get("site", {}).get("metadata", {})
    check(metadata.get("canonicalBaseUrl") == "https://themindfulmatrix.github.io/BioCare/", "Canonical base must preserve the verified /BioCare/ GitHub Pages URL")
    check(set(metadata.get("pages", {})) == {"home", "library", "start", "shop"}, "Home, Library, Start and Shop metadata are required")
    social_image = metadata.get("socialImage", {})
    social_image_path = ROOT / social_image.get("src", "missing")
    check(social_image_path.is_file(), "Default social preview image is required")
    if social_image_path.is_file():
        check(png_dimensions(social_image_path) == (social_image.get("width"), social_image.get("height")), "Default social preview dimensions must match the source file")
    check(bool(social_image.get("alt")), "Default social preview requires alt text")
    check("categories" not in site.get("homepage", {}).get("library", {}), "Library categories must have one source of truth in content/library.json")
    start_here = site.get("homepage", {}).get("startHere", {})
    start_stages = start_here.get("stages", [])
    check([stage.get("id") for stage in start_stages] == ["information", "education", "action"], "Start Here must preserve the Information, Education, Action sequence")
    start_pathways = start_here.get("pathways", {}).get("items", [])
    check(len(start_pathways) == 4, "Start Here requires four visitor-intent pathways")
    for pathway in start_pathways:
        check(bool(pathway.get("heading") and pathway.get("copy") and pathway.get("cta") and pathway.get("href")), "Start Here pathways require heading, copy, CTA and destination")
        check(not str(pathway.get("href", "")).startswith("/"), "Start Here pathways must preserve /BioCare/ relative paths")
    testing_education = site.get("homepage", {}).get("testing", {}).get("education", {})
    check(bool(testing_education.get("heading") and testing_education.get("copy") and testing_education.get("cta") and testing_education.get("href")), "Testing requires an education-first pathway")

    categories = library.get("categories", [])
    category_ids = [category.get("id") for category in categories]
    check(len(category_ids) == 6 and len(category_ids) == len(set(category_ids)), "Library requires six unique categories")
    check(all(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(value or "")) for value in category_ids), "Library category IDs must be URL-safe")
    check(isinstance(library.get("articles"), list), "content/library.json articles must be a list")
    schema = library.get("schema", {})
    required = schema.get("required", [])
    published_required = schema.get("publishedRequired", [])
    optional = schema.get("optional", [])
    check(len(optional) == len(set(optional)), "Library optional schema fields must not be duplicated")
    statuses = set(schema.get("statusValues", []))
    slugs = [article.get("slug") for article in library.get("articles", [])]
    check(len(slugs) == len(set(slugs)), "Library article slugs must be unique")
    published_slugs = {article.get("slug") for article in library.get("articles", []) if article.get("status") == "published"}
    for article in library.get("articles", []):
        label = article.get("slug", "unknown article")
        for field in required:
            check(bool(article.get(field)), f"{label}: missing {field}")
        check(bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(article.get("slug", "")))), f"{label}: slug must be URL-safe")
        check(article.get("status") in statuses, f"{label}: unsupported article status")
        check(article.get("category") in category_ids, f"{label}: unknown category")
        body_sections = article.get("bodySections", [])
        check(isinstance(body_sections, list) and bool(body_sections), f"{label}: bodySections must be a non-empty list")
        section_ids = [section.get("id") for section in body_sections]
        check(len(section_ids) == len(set(section_ids)), f"{label}: body section IDs must be unique")
        for section in body_sections:
            check(bool(section.get("id") and section.get("heading")), f"{label}: body section requires id and heading")
            check(isinstance(section.get("blocks"), list) and bool(section.get("blocks")), f"{label}: body section requires blocks")
            for block in section.get("blocks", []):
                block_type = block.get("type", "paragraph")
                check(block_type in {"paragraph", "subheading", "list", "termList", "quote", "callout"}, f"{label}: unsupported body block")
                if block_type == "termList":
                    check(isinstance(block.get("items"), list) and bool(block.get("items")), f"{label}: termList requires items")
                    for item in block.get("items", []):
                        check(bool(item.get("term") and item.get("definition")), f"{label}: termList items require term and definition")
        if article.get("status") == "published":
            for field in published_required:
                check(bool(article.get(field)), f"{label}: published article missing {field}")
        evidence_labels = article.get("evidenceLabels", [])
        if evidence_labels:
            levels = [item.get("level") for item in evidence_labels]
            check(levels == ["established", "supported", "debated", "action"], f"{label}: evidence labels must use the established, supported, debated, action sequence")
            for item in evidence_labels:
                check(bool(item.get("label") and item.get("meaning")), f"{label}: evidence labels require visible label and meaning")
                check(isinstance(item.get("items"), list) and bool(item.get("items")), f"{label}: evidence labels require scannable items")
        evidence_summary = article.get("evidenceSummary")
        if evidence_summary:
            check(bool(evidence_summary.get("heading") and evidence_summary.get("statement")), f"{label}: evidence summary requires heading and closing statement")
            groups = evidence_summary.get("groups", [])
            check([group.get("level") for group in groups] == ["established", "supported", "debated"], f"{label}: evidence summary requires established, supported and debated groups")
            for group in groups:
                check(bool(group.get("label")), f"{label}: evidence summary groups require visible labels")
                check(isinstance(group.get("items"), list) and bool(group.get("items")), f"{label}: evidence summary groups require items")
        for source in article.get("sources", []):
            check(urlparse(source.get("url", "")).scheme == "https", f"{label}: source URLs must use HTTPS")
            check(bool(source.get("organization")), f"{label}: source organization required")
            check(bool(source.get("citation")), f"{label}: source citation required")
            check(bool(source.get("title")), f"{label}: source title required")
            check(bool(source.get("detail")), f"{label}: source-use explanation required")
        for related_slug in article.get("relatedArticles", []):
            check(related_slug != label, f"{label}: article cannot link to itself")
            check(related_slug in published_slugs, f"{label}: related article must reference a published slug")
        if article.get("relatedArticles"):
            check(bool(article.get("relatedReadingHeading") and article.get("relatedReadingIntro")), f"{label}: related reading requires contextual heading and introduction")
        optional_action = article.get("optionalAction")
        if optional_action:
            check(bool(optional_action.get("label") and optional_action.get("heading") and optional_action.get("copy")), f"{label}: optional action requires label, heading and copy")
            check(isinstance(optional_action.get("ctas"), list) and bool(optional_action.get("ctas")), f"{label}: optional action requires CTAs")
            for cta in optional_action.get("ctas", []):
                check(bool(cta.get("label") and cta.get("href")), f"{label}: optional action CTA requires label and href")
                check(not str(cta.get("href", "")).startswith("/"), f"{label}: optional action CTA must preserve /BioCare/ relative paths")
        educational_content = json.dumps(
            {
                "bodySections": article.get("bodySections", []),
                "evidenceLabels": evidence_labels,
                "evidenceSummary": evidence_summary,
            },
            ensure_ascii=False,
        ).lower()
        for product_term in ("balanceoil", "balancetest"):
            check(product_term not in educational_content, f"{label}: direct product promotion appears inside educational content")
        hero = article.get("hero")
        if hero:
            check((ROOT / hero.get("src", "missing")).is_file(), f"{label}: missing hero image")
            check(hero.get("alt") is not None, f"{label}: hero image alt behavior required")
            check(bool(hero.get("width") and hero.get("height")), f"{label}: hero dimensions required")

    catalog = site.get("catalog", {})
    partner_id = site.get("affiliate", {}).get("zinzinoPartnerId")
    check(catalog.get("affiliate", {}).get("zinzinoPartnerId") == partner_id == "2021428066", "Catalog and site affiliate identifiers must match the verified partner ID")
    intents = catalog.get("intents", [])
    intent_ids = [intent.get("id") for intent in intents]
    check(intent_ids == ["test-measure", "omega-nutrition", "gut-digestion", "daily-wellness", "performance-recovery", "healthy-aging"], "Product intents must preserve the approved six-part visitor taxonomy")
    intent_names = [intent.get("name") for intent in intents]
    check(intent_names == ["Test & Measure", "Omega & Nutrition", "Gut & Digestion", "Daily Wellness", "Active Nutrition & Tools", "Skin & Collagen"], "Visitor-facing product taxonomy must preserve the neutral release-candidate labels")
    check(len({product.get("sku") for product in products}) == len(products), "Verified product SKUs must be unique")
    check(len({product.get("destination") for product in products}) == len(products), "Verified individual product destinations must be unique")
    check(len({product.get("cutout", {}).get("sourceAsset") for product in products}) == len(products), "Official product source assets must be unique")
    check("$" not in json.dumps(products, ensure_ascii=False), "Unapproved pricing must not enter the verified product catalog")
    legacy_destinations = {
        "https://www.zinzino.com/shop/2021428066/us/en-us/products/balance-supplements-kits/910465",
        "https://www.zinzino.com/shop/2021428066/us/en-us/products/shop/home-health-tests",
        "https://www.zinzino.com/shop/2021428066/us/en-us/products/premier-kits/balance-supplements-kits",
        "https://www.zinzino.com/shop/2021428066/us/en-us/products/shop/gut-health-supplements",
        "https://www.zinzino.com/shop/2021428066/us/en-us/products/shop/gut-health-supplements/302790",
        "https://www.zinzino.com/shop/2021428066/us/en-us/products/shop",
        "https://biolimitless.com/me/matrix/",
    }
    current_destinations = {product.get("destination") for product in products}
    current_destinations.update(item.get("destination") for item in catalog.get("fallbackDestinations", []))
    check(legacy_destinations.issubset(current_destinations), "All seven previously verified commercial destinations must remain intact")
    for product in products:
        label = product.get("id", "unknown")
        for field in ("id", "name", "manufacturer", "sku", "intent", "category", "productKind", "purchaseModel", "description", "descriptionSource", "whyItsHere", "variantGroup", "variantLabel", "officialProductPage", "cta", "destination", "cutout", "artwork"):
            check(bool(product.get(field)), f"{label}: missing {field}")
        check("verified" not in product.get("whyItsHere", "").lower(), f"{label}: Why It's Here should provide product context rather than verification boilerplate")
        check(bool(product.get("environment")), f"{label}: decorative Shelf environment is required")
        check(product.get("intent") in intent_ids, f"{label}: unknown product intent")
        check(product.get("manufacturer") == "Zinzino", f"{label}: manufacturer must remain explicit")
        check(product.get("sku") in product.get("officialProductPage", ""), f"{label}: official product page must contain the exact SKU")
        check(urlparse(product.get("officialProductPage", "")).scheme == "https", f"{label}: official product page must use HTTPS")
        destination = product.get("destination", "")
        check(urlparse(destination).scheme == "https", f"{label}: destination must use HTTPS")
        if "zinzino.com" in destination:
            check(f"/shop/{partner_id}/" in destination, f"{label}: Zinzino partner ID mismatch")
        cutout = product.get("cutout")
        if cutout:
            cutout_path = ROOT / cutout.get("src", "missing")
            source_path = ROOT / cutout.get("sourceAsset", "missing")
            check(cutout_path.is_file(), f"{label}: missing product cutout")
            check(bool(cutout.get("alt")), f"{label}: official product cutout requires alt text")
            check(bool(cutout.get("width") and cutout.get("height")), f"{label}: cutout dimensions required")
            check(source_path.is_file(), f"{label}: missing immutable cutout source")
            check(cutout_path.resolve() != source_path.resolve(), f"{label}: official source and production cutout must remain separate files")
            check(product.get("sku") in cutout.get("sourceUrl", ""), f"{label}: official image URL must contain the exact SKU")
            if cutout_path.is_file():
                check(png_dimensions(cutout_path) == (cutout.get("width"), cutout.get("height")), f"{label}: cutout dimensions do not match its PNG")
            if source_path.is_file():
                provenance_path = ROOT / cutout.get("provenance", source_path.parent / "provenance.json")
                check(provenance_path.is_file(), f"{label}: official source requires provenance.json")
                if provenance_path.is_file():
                    try:
                        provenance_payload = json.loads(provenance_path.read_text(encoding="utf-8"))
                    except json.JSONDecodeError as error:
                        check(False, f"{label}: invalid provenance JSON: {error}")
                        provenance_payload = {}
                    if isinstance(provenance_payload.get("assets"), list):
                        provenance = next((item for item in provenance_payload["assets"] if item.get("downloaded_filename") == source_path.name), {})
                    else:
                        provenance = provenance_payload
                    expected_dimensions = provenance.get("pixel_dimensions", {})
                    check(provenance.get("direct_from_zinzino") is True, f"{label}: provenance must confirm direct manufacturer origin")
                    check(provenance.get("downloaded_filename") == source_path.name, f"{label}: provenance filename mismatch")
                    check(provenance.get("sha256", "").lower() == sha256(source_path), f"{label}: official source SHA-256 mismatch")
                    check(png_dimensions(source_path) == (expected_dimensions.get("width"), expected_dimensions.get("height")), f"{label}: provenance dimensions mismatch")
                    production_filename = provenance.get("production_filename")
                    if production_filename:
                        check(production_filename == cutout.get("src"), f"{label}: provenance production filename mismatch")
                        if cutout_path.is_file() and "byte-for-byte copy" in provenance.get("alteration", ""):
                            check(sha256(cutout_path) == sha256(source_path), f"{label}: declared untouched production copy differs from official source")
        artwork = product.get("artwork", {})
        check(bool(artwork.get("status")), f"{label}: artwork status is required")
        if artwork.get("src"):
            check((ROOT / artwork["src"]).is_file(), f"{label}: missing editorial artwork {artwork['src']}")
            check(bool(artwork.get("width") and artwork.get("height")), f"{label}: artwork dimensions required")


def public_pages(library: dict) -> list[Path]:
    pages = [ROOT / "index.html", ROOT / "library.html", ROOT / "start.html", ROOT / "shop.html"]
    pages.extend(ROOT / "library" / f'{article["slug"]}.html' for article in library["articles"] if article.get("status") == "published")
    return pages


def validate_page(page: Path, *, preview: bool = False) -> DocumentParser:
    label = page.relative_to(ROOT) if ROOT in page.parents else page
    check(page.is_file(), f"Missing generated page: {label}")
    if not page.is_file():
        return DocumentParser()
    generated = page.read_text(encoding="utf-8")
    parser = DocumentParser()
    parser.feed(generated)
    check('<html lang="en">' in generated, f"{label}: document language must be declared")
    check(parser.h1_count == 1, f"{label}: must contain exactly one h1")
    check(bool(parser.heading_levels) and parser.heading_levels[0] == 1, f"{label}: heading hierarchy must begin with h1")
    for previous, current in zip(parser.heading_levels, parser.heading_levels[1:]):
        check(current <= previous + 1, f"{label}: heading hierarchy skips from h{previous} to h{current}")
    check(len(parser.ids) == len(set(parser.ids)), f"{label}: contains duplicate IDs")
    skip_target = re.search(r'<a class="skip-link" href="#([^"]+)"', generated)
    check(bool(skip_target), f"{label}: functional skip link required")
    if skip_target:
        check(f'<main id="{skip_target.group(1)}"' in generated, f"{label}: skip link must target the main landmark")
    check('<header ' in generated and '<nav ' in generated and '<footer ' in generated, f"{label}: header, navigation and footer landmarks required")
    check(not re.search(r"{{[A-Z0-9_]+}}", generated), f"{label}: unresolved template token")
    check(len(parser.titles) == 1 and bool(parser.titles[0]), f"{label}: unique title required")
    check(len(parser.descriptions) == 1 and bool(parser.descriptions[0]), f"{label}: unique description required")
    check('aria-controls="primary-links"' in generated, f"{label}: mobile navigation control required")
    check('meta name="generator" content="The Mindful Matrix static builder"' in generated, f"{label}: builder marker required")
    for blank_link in parser.blank_target_links:
        rel_tokens = set(str(blank_link.get("rel") or "").split())
        check({"noopener", "noreferrer"}.issubset(rel_tokens), f"{label}: target=_blank link requires noopener noreferrer")
    if preview:
        check('name="robots" content="noindex, nofollow"' in generated, f"{label}: preview must be noindex")
        check(not parser.canonicals, f"{label}: preview must not have a canonical URL")
        check("Non-public article template preview" in generated, f"{label}: preview banner required")
        check(not json_ld_records(generated, label), f"{label}: preview must not publish structured data")
    else:
        check('name="robots" content="index, follow"' in generated, f"{label}: public page must be indexable")
        check(len(parser.canonicals) == 1, f"{label}: one canonical URL required")
        if parser.canonicals:
            check(parser.canonicals[0].startswith("https://themindfulmatrix.github.io/BioCare/"), f"{label}: canonical must preserve /BioCare/")
        required_meta = ("og:title", "og:description", "og:type", "og:url", "og:image", "og:image:alt", "twitter:card", "twitter:title", "twitter:description", "twitter:image", "twitter:image:alt")
        for name in required_meta:
            attribute = "property" if name.startswith("og:") else "name"
            check(f'<meta {attribute}="{name}"' in generated, f"{label}: missing {name} social metadata")
        records = json_ld_records(generated, label)
        types = {record.get("@type") for record in records}
        check({"Organization", "WebSite"}.issubset(types), f"{label}: Organization and WebSite structured data required")
        if page.parent == ROOT / "library":
            check({"Article", "BreadcrumbList"}.issubset(types), f"{label}: article and breadcrumb structured data required")
        elif page.name != "index.html":
            check("BreadcrumbList" in types, f"{label}: breadcrumb structured data required")
    for image in parser.images:
        check(image.get("alt") is not None, f"{label}: image {image.get('src')} has no alt attribute")
        check(bool(image.get("width") and image.get("height")), f"{label}: image {image.get('src')} lacks dimensions")
    return parser


def validate_references(page: Path, parser: DocumentParser, parsers: dict[Path, DocumentParser]) -> None:
    label = page.relative_to(ROOT) if ROOT in page.parents else page
    for attribute, reference in parser.references:
        if is_external(reference):
            continue
        check(not reference.startswith("/"), f"{label}: root-relative path breaks /BioCare/: {reference}")
        target, fragment = resolve_local_reference(page, reference)
        check(ROOT.resolve() == target or ROOT.resolve() in target.parents, f"{label}: reference escapes repository: {reference}")
        check(target.is_file(), f"{label}: missing relative {attribute}: {reference}")
        if fragment and target.is_file() and target.suffix.lower() == ".html":
            target_parser = parsers.get(target)
            if target_parser is None:
                target_parser = validate_page(target)
                parsers[target] = target_parser
            check(fragment in target_parser.ids, f"{label}: missing fragment target: {reference}")


def validate_public_output(site: dict, library: dict, preview_path: Path | None) -> None:
    pages = public_pages(library)
    parsers: dict[Path, DocumentParser] = {}
    for page in pages:
        parsers[page.resolve()] = validate_page(page.resolve())
    if preview_path:
        preview = preview_path.resolve()
        parsers[preview] = validate_page(preview, preview=True)
    for page, parser in list(parsers.items()):
        validate_references(page, parser, parsers)
        if page in {item.resolve() for item in pages}:
            generated = page.read_text(encoding="utf-8")
            check(site["site"]["disclosure"] in generated, f"{page.relative_to(ROOT)}: affiliate disclosure must remain visible")

    public_parsers = [parsers[page.resolve()] for page in pages if page.resolve() in parsers]
    titles = [parser.titles[0] for parser in public_parsers if parser.titles]
    canonicals = [parser.canonicals[0] for parser in public_parsers if parser.canonicals]
    check(len(titles) == len(set(titles)), "Public pages must have unique titles")
    check(len(canonicals) == len(set(canonicals)), "Public pages must have unique canonical URLs")
    canonical_base = site["site"]["metadata"]["canonicalBaseUrl"]
    expected_urls: list[str] = []
    for page in pages:
        relative = page.relative_to(ROOT).as_posix()
        relative = "" if relative == "index.html" else relative
        expected = canonical_base + relative
        expected_urls.append(expected)
        parser = parsers[page.resolve()]
        if parser.canonicals:
            check(parser.canonicals[0] == expected, f"{page.relative_to(ROOT)}: canonical URL does not match output path")

    sitemap_path = ROOT / "sitemap.xml"
    robots_path = ROOT / "robots.txt"
    check(sitemap_path.is_file(), "sitemap.xml is required")
    check(robots_path.is_file(), "robots.txt is required")
    if sitemap_path.is_file():
        try:
            root = ET.parse(sitemap_path).getroot()
            namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            sitemap_urls = [element.text for element in root.findall("s:url/s:loc", namespace)]
            check(len(sitemap_urls) == len(set(sitemap_urls)) and set(sitemap_urls) == set(expected_urls), "Sitemap must exactly match public generated pages")
        except ET.ParseError as error:
            check(False, f"sitemap.xml is invalid XML: {error}")
    if robots_path.is_file():
        robots = robots_path.read_text(encoding="utf-8")
        check("User-agent: *" in robots and "Allow: /" in robots, "robots.txt must allow public crawling")
        check(f"Sitemap: {canonical_base}sitemap.xml" in robots, "robots.txt must reference the /BioCare/ sitemap")

    article_dir = ROOT / "library"
    actual_article_pages = set(article_dir.glob("*.html")) if article_dir.exists() else set()
    expected_article_pages = {ROOT / "library" / f'{article["slug"]}.html' for article in library["articles"] if article.get("status") == "published"}
    check(actual_article_pages == expected_article_pages, "Public article output must exactly match published article records")
    for article in library["articles"]:
        if article.get("status") != "published":
            check(not (article_dir / f'{article["slug"]}.html').exists(), f"Draft article generated publicly: {article['slug']}")

    home = (ROOT / "index.html").read_text(encoding="utf-8")
    cutout_count = sum(1 for product in site["products"] if product.get("cutout"))
    featured = next(product for product in site["products"] if product["id"] == site["featuredProductId"])
    testing_cutout_count = 1 if featured.get("cutout") else 0
    hero_cutout_count = 1 if featured.get("cutout") else 0
    check(home.count('data-image-role="official-product-cutout"') == cutout_count + testing_cutout_count + hero_cutout_count, "Every configured Product Universe, testing, and hero cutout must render as a separate foreground image")
    check(home.count('data-universe-product=') == len(site["products"]), "Homepage Product Universe must render every verified product")
    check(home.count("data-artwork-state=") == len(site["products"]), "Every Product Universe item requires a stable environmental artwork slot")
    check(home.count("data-universe-intent=") == len(site["catalog"]["intents"]), "Homepage must expose every approved product intent")
    check('data-universe-status aria-live="polite" aria-atomic="true"' in home, "Product Universe requires a concise live selected-state announcement")
    universe_start = home.find('<div class="product-universe"')
    universe_end = home.find('<section id="problem"')
    universe_markup = home[universe_start:universe_end]
    eager_universe_cutouts = re.findall(r'<img[^>]+loading="eager"[^>]+data-image-role="official-product-cutout"', universe_markup)
    lazy_universe_cutouts = re.findall(r'<img[^>]+loading="lazy"[^>]+data-image-role="official-product-cutout"', universe_markup)
    check(len(eager_universe_cutouts) == 1 and len(lazy_universe_cutouts) == len(site["products"]) - 1, "Homepage must eagerly load only the active Product Universe cutout")
    check(home.count("data-library-article") == len([article for article in library["articles"] if article.get("status") == "published"]), "Homepage Library count must match published content")
    check('data-library-state="empty"' in home if not any(article.get("status") == "published" for article in library["articles"]) else 'data-library-state="published"' in home, "Homepage Library state mismatch")
    check("content model is ready" not in home.lower(), "Developer-facing Library language must not be published")
    check('data-media-status="awaiting-original-photography"' in home, "Founder media placeholder must remain")
    check("<span>Trust isn't something we claim.</span><span>It's something we earn.</span>" in home, "Standards payoff must remain")
    check("$127" not in home, "Unverified legacy price must not be rendered")
    check('assets/product-cutouts/zinzino/balance-test-basic-kit-910465.png' in home, "Verified Balance cutout must remain the rendered foreground")
    check('assets/artwork/shelf/balance-test-basic-kit-cinematic.webp' in home, "Approved Balance artwork must remain")
    testing_guide = 'href="library/should-you-test-your-omega-3-levels.html"'
    featured_destination = next(product["destination"] for product in site["products"] if product["id"] == site["featuredProductId"])
    check(testing_guide in home, "Testing section must link to the testing education guide")
    check('data-matrix-field' in home, "Homepage must include the progressively enhanced Matrix field")
    check(home.find('<section id="shelf"') < home.find('<section id="problem"'), "The Product Universe must follow the hero without an educational gate")
    check(home.count(f'href="{featured_destination}"') >= 3, "Featured product must be directly reachable from navigation, hero, and product content")
    check(f'Shop all {len(site["products"])} options' in home, "Hero must expose the complete Shelf count")
    check(home.count('class="product-universe__why"') == len(site["products"]), "Every Product Universe item must show why it is included before its commercial link")
    check(f'href="{featured_destination}" target="_blank" rel="sponsored noopener noreferrer">{featured["cta"]}' in home, "Primary navigation must provide a direct sponsored route to the featured product")
    for product in site["products"]:
        check(product["destination"] in home, f"{product['id']}: destination missing from homepage")
        escaped_destination = re.escape(product["destination"])
        check(bool(re.search(rf'href="{escaped_destination}"[^>]+rel="[^"]*sponsored', home)), f"{product['id']}: commercial link must be marked sponsored")
    shop = (ROOT / "shop.html").read_text(encoding="utf-8")
    check(shop.count('data-product-sku=') == len(site["products"]), "Shop must render every verified SKU exactly once")
    check(shop.count('data-image-role="official-product-cutout"') == cutout_count, "Shop must render every official product image as a separate foreground")
    for intent in site["catalog"]["intents"]:
        check(f'id="intent-{intent["id"]}"' in shop, f"Shop missing intent section: {intent['name']}")
    for product in site["products"]:
        check(shop.count(f'data-product-sku="{product["sku"]}"') == 1, f"{product['id']}: Shop SKU must be unique")
        check(product["destination"] in shop, f"{product['id']}: destination missing from Shop")
    for fallback in site["catalog"]["fallbackDestinations"]:
        check(fallback["destination"] in shop, f"{fallback['id']}: verified fallback destination missing from Shop")
    css = (ROOT / "assets" / "css" / "site.css").read_text(encoding="utf-8")
    check("overflow-x: hidden" not in css, "Horizontal overflow must not be concealed in CSS")
    base_css = (ROOT / "assets" / "css" / "base.css").read_text(encoding="utf-8")
    enhancements = (ROOT / "assets" / "js" / "enhancements.js").read_text(encoding="utf-8")
    check("@media (prefers-reduced-motion: reduce)" in base_css and "@media (prefers-reduced-motion: reduce)" in css, "Reduced-motion CSS fallbacks are required")
    check("prefers-reduced-motion: reduce" in enhancements, "Interaction enhancement must respect reduced motion")
    library_page = (ROOT / "library.html").read_text(encoding="utf-8")
    for category in library["categories"]:
        check(category["name"] in library_page, f"Library landing page missing category: {category['name']}")
        count = sum(1 for article in library["articles"] if article.get("status") == "published" and article.get("category") == category["id"])
        if count:
            check(f'href="#category-{category["id"]}"' in library_page, f"{category['name']}: populated category must be interactive")
        else:
            check(f'<div class="category-card" data-availability="coming-soon"' in library_page and f'<span class="category-card__index">{category["id"]}</span>' in library_page, f"{category['name']}: empty category must remain a non-interactive coming-soon card")
    if not any(article.get("status") == "published" for article in library["articles"]):
        check("The Library is being built." in library_page, "Library landing page requires the approved empty state when no articles are published")
    for article in (item for item in library["articles"] if item.get("status") == "published"):
        article_page = (ROOT / "library" / f'{article["slug"]}.html').read_text(encoding="utf-8")
        if article.get("evidenceLabels"):
            for evidence in article["evidenceLabels"]:
                check(f'data-evidence-level="{evidence["level"]}"' in article_page, f"{article['slug']}: missing visible {evidence['label']} evidence label")
        if article.get("evidenceSummary"):
            check('id="what-we-know"' in article_page, f"{article['slug']}: missing evidence summary")
        if article.get("optionalAction"):
            check('id="optional-action"' in article_page, f"{article['slug']}: optional action must remain structurally separate")
        check('id="article-journey"' in article_page, f"{article['slug']}: missing standardized end-of-article journey")
        check("Keep learning" in article_page and "Understand your next step" in article_page, f"{article['slug']}: end-of-article journey choices are incomplete")
        for related_slug in article.get("relatedArticles", []):
            check(f'href="{related_slug}.html"' in article_page, f"{article['slug']}: missing related-article link to {related_slug}")
        if not article.get("reviewer"):
            check("Reviewed by" not in article_page, f"{article['slug']}: unapproved reviewer rendered")
        records = json_ld_records(article_page, article["slug"])
        article_record = next((record for record in records if record.get("@type") == "Article"), {})
        check(("datePublished" in article_record) == bool(article.get("publishedIso")), f"{article['slug']}: structured publication date must only use approved ISO data")
        check(("dateModified" in article_record) == bool(article.get("updatedIso")), f"{article['slug']}: structured modified date must only use approved ISO data")
        check("reviewedBy" not in article_record, f"{article['slug']}: structured data must not invent a reviewer")
    start_page = (ROOT / "start.html").read_text(encoding="utf-8")
    for stage_id in ("information", "education", "action"):
        check(f'id="{stage_id}"' in start_page, f"Start Here missing orientation stage: {stage_id}")
    check(start_page.count("data-start-pathway=") == 4, "Start Here must render four visitor-intent pathways")
    check("This page is an orientation, not a diagnostic." in start_page, "Start Here must state its non-diagnostic scope")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", type=Path, help="Also validate a non-public article preview")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    site = json.loads((ROOT / "content" / "site.json").read_text(encoding="utf-8"))
    library = json.loads((ROOT / "content" / "library.json").read_text(encoding="utf-8"))
    catalog = json.loads((ROOT / "content" / "catalog.json").read_text(encoding="utf-8"))
    site["catalog"] = catalog
    site["affiliate"] = catalog["affiliate"]
    site["products"] = catalog["products"]
    site["featuredProductId"] = catalog["featuredProductId"]
    validate_content(site, library)
    validate_public_output(site, library, args.preview)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    published_count = sum(1 for article in library["articles"] if article.get("status") == "published")
    print(f"Validation passed: 4 core pages, {published_count} published articles, {len(site['products'])} verified products, /BioCare/ paths safe")


if __name__ == "__main__":
    main()
