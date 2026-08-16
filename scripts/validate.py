#!/usr/bin/env python3
"""Validate content, multipage output, and GitHub Pages subpath assumptions."""

from __future__ import annotations

import argparse
import json
import re
import sys
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
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(str(values["id"]))
        if tag == "h1":
            self.h1_count += 1
        if tag == "img":
            self.images.append(values)
        if tag == "title":
            self._in_title = True
        if tag == "meta" and values.get("name") == "description" and values.get("content"):
            self.descriptions.append(str(values["content"]))
        if tag == "link" and values.get("rel") == "canonical" and values.get("href"):
            self.canonicals.append(str(values["href"]))
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


def validate_content(site: dict, library: dict) -> None:
    products = site.get("products", [])
    ids = [product.get("id") for product in products]
    check(bool(products), "content/site.json must contain products")
    check(len(ids) == len(set(ids)), "Product IDs must be unique")
    check(site.get("featuredProductId") in ids, "featuredProductId must reference a product")

    metadata = site.get("site", {}).get("metadata", {})
    check(metadata.get("canonicalBaseUrl") == "https://themindfulmatrix.github.io/BioCare/", "Canonical base must preserve the verified /BioCare/ GitHub Pages URL")
    check(set(metadata.get("pages", {})) == {"home", "library", "start"}, "Home, Library and Start metadata are required")
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

    partner_id = site.get("affiliate", {}).get("zinzinoPartnerId")
    for product in products:
        label = product.get("id", "unknown")
        for field in ("id", "name", "category", "description", "whyItsHere", "cta", "destination", "image", "artwork"):
            check(bool(product.get(field)), f"{label}: missing {field}")
        destination = product.get("destination", "")
        check(urlparse(destination).scheme == "https", f"{label}: destination must use HTTPS")
        if "zinzino.com" in destination:
            check(f"/shop/{partner_id}/" in destination, f"{label}: Zinzino partner ID mismatch")
        image = product.get("image", {})
        check((ROOT / image.get("src", "missing")).is_file(), f"{label}: missing image {image.get('src')}")
        source = Path(image.get("src", "missing"))
        widths = [280, 560] if image.get("width") == 560 else [512, 1024]
        for width in widths:
            responsive = ROOT / "img" / "responsive" / f"{source.stem}-{width}.webp"
            check(responsive.is_file(), f"{label}: missing responsive image {responsive.relative_to(ROOT)}")
        check(bool(image.get("alt")), f"{label}: product image requires alt text")
        check(bool(image.get("width") and image.get("height")), f"{label}: image dimensions required")
        cutout = product.get("cutout")
        if cutout:
            check((ROOT / cutout.get("src", "missing")).is_file(), f"{label}: missing product cutout")
            check(bool(cutout.get("width") and cutout.get("height")), f"{label}: cutout dimensions required")
            check((ROOT / cutout.get("sourceAsset", "missing")).is_file(), f"{label}: missing immutable cutout source")
        artwork = product.get("artwork", {})
        check(bool(artwork.get("status")), f"{label}: artwork status is required")
        if artwork.get("src"):
            check((ROOT / artwork["src"]).is_file(), f"{label}: missing editorial artwork {artwork['src']}")
            check(bool(artwork.get("width") and artwork.get("height")), f"{label}: artwork dimensions required")


def public_pages(library: dict) -> list[Path]:
    pages = [ROOT / "index.html", ROOT / "library.html", ROOT / "start.html"]
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
    check(parser.h1_count == 1, f"{label}: must contain exactly one h1")
    check(len(parser.ids) == len(set(parser.ids)), f"{label}: contains duplicate IDs")
    check('class="skip-link"' in generated, f"{label}: skip link required")
    check("{{" not in generated and "}}" not in generated, f"{label}: unresolved template token")
    check(len(parser.titles) == 1 and bool(parser.titles[0]), f"{label}: unique title required")
    check(len(parser.descriptions) == 1 and bool(parser.descriptions[0]), f"{label}: unique description required")
    check('aria-controls="primary-links"' in generated, f"{label}: mobile navigation control required")
    check('meta name="generator" content="The Mindful Matrix static builder"' in generated, f"{label}: builder marker required")
    if preview:
        check('name="robots" content="noindex, nofollow"' in generated, f"{label}: preview must be noindex")
        check(not parser.canonicals, f"{label}: preview must not have a canonical URL")
        check("Non-public article template preview" in generated, f"{label}: preview banner required")
    else:
        check(len(parser.canonicals) == 1, f"{label}: one canonical URL required")
        if parser.canonicals:
            check(parser.canonicals[0].startswith("https://themindfulmatrix.github.io/BioCare/"), f"{label}: canonical must preserve /BioCare/")
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

    public_parsers = [parsers[page.resolve()] for page in pages if page.resolve() in parsers]
    titles = [parser.titles[0] for parser in public_parsers if parser.titles]
    canonicals = [parser.canonicals[0] for parser in public_parsers if parser.canonicals]
    check(len(titles) == len(set(titles)), "Public pages must have unique titles")
    check(len(canonicals) == len(set(canonicals)), "Public pages must have unique canonical URLs")

    article_dir = ROOT / "library"
    actual_article_pages = set(article_dir.glob("*.html")) if article_dir.exists() else set()
    expected_article_pages = {ROOT / "library" / f'{article["slug"]}.html' for article in library["articles"] if article.get("status") == "published"}
    check(actual_article_pages == expected_article_pages, "Public article output must exactly match published article records")
    for article in library["articles"]:
        if article.get("status") != "published":
            check(not (article_dir / f'{article["slug"]}.html').exists(), f"Draft article generated publicly: {article['slug']}")

    home = (ROOT / "index.html").read_text(encoding="utf-8")
    check(home.count("<picture>") == len(site["products"]), "Testing and fallback Shelf images must use responsive picture markup")
    cutout_count = sum(1 for product in site["products"] if product.get("cutout"))
    check(home.count('data-image-role="official-product-cutout"') == cutout_count, "Every configured Shelf cutout must render as a separate foreground image")
    check(home.count('class="shelf-card__visual artwork-stage"') == len(site["products"]), "Every Shelf card requires separate artwork and product layers")
    check(home.count("data-artwork-state=") == len(site["products"]), "Every Shelf product requires a stable editorial artwork slot")
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
    check(home.find(testing_guide) < home.find(featured_destination), "Testing education must appear before the commercial destination")
    check(home.count('class="shelf-card__why"') == len(site["products"]), "Every Shelf item must show why it is included before its commercial link")
    check('href="start.html#pathways">Find your path' in home, "Primary navigation must distinguish Start Here from the pathway shortcut")
    for product in site["products"]:
        check(product["destination"] in home, f"{product['id']}: destination missing from homepage")
    css = (ROOT / "assets" / "css" / "site.css").read_text(encoding="utf-8")
    check("overflow-x: hidden" not in css, "Horizontal overflow must not be concealed in CSS")
    base_css = (ROOT / "assets" / "css" / "base.css").read_text(encoding="utf-8")
    enhancements = (ROOT / "assets" / "js" / "enhancements.js").read_text(encoding="utf-8")
    check("@media (prefers-reduced-motion: reduce)" in base_css and "@media (prefers-reduced-motion: reduce)" in css, "Reduced-motion CSS fallbacks are required")
    check("prefers-reduced-motion: reduce" in enhancements, "Interaction enhancement must respect reduced motion")
    library_page = (ROOT / "library.html").read_text(encoding="utf-8")
    for category in library["categories"]:
        check(category["name"] in library_page, f"Library landing page missing category: {category['name']}")
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
    validate_content(site, library)
    validate_public_output(site, library, args.preview)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    published_count = sum(1 for article in library["articles"] if article.get("status") == "published")
    print(f"Validation passed: 3 core pages, {published_count} published articles, {len(site['products'])} products, /BioCare/ paths safe")


if __name__ == "__main__":
    main()
