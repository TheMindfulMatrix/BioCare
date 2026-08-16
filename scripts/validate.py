#!/usr/bin/env python3
"""Validate content, generated output, and GitHub Pages subpath assumptions."""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.h1_count = 0
        self.images: list[dict[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(str(values["id"]))
        if tag == "h1":
            self.h1_count += 1
        if tag == "img":
            self.images.append(values)
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.references.append((attribute, value))


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    site = json.loads((ROOT / "content" / "site.json").read_text(encoding="utf-8"))
    library = json.loads((ROOT / "content" / "library.json").read_text(encoding="utf-8"))
    products = site.get("products", [])
    ids = [product.get("id") for product in products]

    check(bool(products), "content/site.json must contain products")
    check(len(ids) == len(set(ids)), "Product IDs must be unique")
    check(site.get("featuredProductId") in ids, "featuredProductId must reference a product")
    check(isinstance(library.get("articles"), list), "content/library.json articles must be a list")
    article_schema = library.get("schema", {})
    required_article_fields = article_schema.get("required", [])
    article_ids = [article.get("id") for article in library.get("articles", [])]
    check(len(article_ids) == len(set(article_ids)), "Library article IDs must be unique")
    for article in library.get("articles", []):
        for field in required_article_fields:
            check(bool(article.get(field)), f'{article.get("id", "unknown article")}: missing {field}')
        check(isinstance(article.get("topics"), list) and bool(article.get("topics")), f'{article.get("id")}: topics must be a non-empty list')
        href = article.get("href", "")
        check(href.startswith(("https://", "articles/")), f'{article.get("id")}: unsupported article href')
        article_image = article.get("image")
        if article_image:
            check((ROOT / article_image.get("src", "missing")).is_file(), f'{article.get("id")}: missing article image')
            check(bool(article_image.get("width") and article_image.get("height")), f'{article.get("id")}: article image dimensions required')

    partner_id = site.get("affiliate", {}).get("zinzinoPartnerId")
    for product in products:
        for field in ("id", "name", "category", "description", "whyItsHere", "cta", "destination", "image", "artwork"):
            check(bool(product.get(field)), f'{product.get("id", "unknown")}: missing {field}')
        destination = product.get("destination", "")
        check(urlparse(destination).scheme == "https", f'{product.get("id")}: destination must use HTTPS')
        if "zinzino.com" in destination:
            check(f"/shop/{partner_id}/" in destination, f'{product.get("id")}: Zinzino partner ID mismatch')
        image = product.get("image", {})
        path = ROOT / image.get("src", "missing")
        check(path.is_file(), f'{product.get("id")}: missing image {image.get("src")}')
        source = Path(image.get("src", "missing"))
        widths = [280, 560] if image.get("width") == 560 else [512, 1024]
        for width in widths:
            responsive = ROOT / "img" / "responsive" / f"{source.stem}-{width}.webp"
            check(responsive.is_file(), f'{product.get("id")}: missing responsive image {responsive.relative_to(ROOT)}')
        check(bool(image.get("alt")), f'{product.get("id")}: product image requires alt text')
        check(bool(image.get("width") and image.get("height")), f'{product.get("id")}: image dimensions required')
        artwork = product.get("artwork", {})
        check(bool(artwork.get("status")), f'{product.get("id")}: artwork status is required')
        if artwork.get("src"):
            check((ROOT / artwork["src"]).is_file(), f'{product.get("id")}: missing editorial artwork {artwork["src"]}')
            check(bool(artwork.get("width") and artwork.get("height")), f'{product.get("id")}: artwork dimensions required')

    parser = DocumentParser()
    generated = (ROOT / "index.html").read_text(encoding="utf-8")
    parser.feed(generated)
    check(parser.h1_count == 1, "Generated page must contain exactly one h1")
    check('href="#main-content"' in generated, "Generated page must contain a skip link")
    check("{{" not in generated and "}}" not in generated, "Generated page contains unresolved tokens")

    for image in parser.images:
        check(image.get("alt") is not None, f'Image {image.get("src")} has no alt attribute')
        check(bool(image.get("width") and image.get("height")), f'Image {image.get("src")} lacks dimensions')
    check(generated.count("<picture>") == len(products) + 1, "Testing and Shelf product images must use responsive picture markup")
    check(generated.count("data-artwork-state=") == len(products), "Every Shelf product requires a stable editorial artwork slot")
    check(generated.count("data-library-article") == len(library["articles"]), "Generated Library article count must match content")
    if library["articles"]:
        check('data-library-state="published"' in generated, "Published Library state is required when articles exist")
    else:
        check('data-library-state="empty"' in generated, "Visitor-facing Library empty state is required")
        check("The Library is being built." in generated, "Approved Library empty-state heading is required")
        check("content model is ready" not in generated.lower(), "Developer-facing Library language must not be published")
        check("Coming to the Library" in generated, "Library category preview label is required")
    check('aria-controls="primary-links"' in generated, "Mobile navigation control is required")
    check("assets/brand/lockup-dark.svg" in generated, "Primary brand lockup is required")
    check(">BioCare<" not in generated and "BioCare —" not in generated, "Repository name must not appear as public-facing text")
    check("$127" not in generated, "Unverified legacy price must not be rendered")
    check('data-media-status="awaiting-original-photography"' in generated, "Founder media placeholder is required until original photography is supplied")
    check("<span>Trust isn't something we claim.</span><span>It's something we earn.</span>" in generated, "Standards payoff must preserve its two-part editorial emphasis")
    for section_id in ("top", "problem", "matrix", "choose-path", "story", "testing", "library", "shelf", "standards", "transparency", "start"):
        check(f'id="{section_id}"' in generated, f"Missing production section: {section_id}")
    for product in products:
        check(product["destination"] in generated, f'{product["id"]}: destination missing from generated homepage')
    check(bool(site.get("homepage", {}).get("transparency", {}).get("approvalStatus")), "Transparency review status must remain maintainable in content")
    for brand_asset in ("mark-dark.svg", "mark-light.svg", "mark-gold.svg", "lockup-dark.svg", "lockup-light.svg", "favicon.svg"):
        check((ROOT / "assets" / "brand" / brand_asset).is_file(), f"Missing brand asset: {brand_asset}")

    for attribute, reference in parser.references:
        if reference.startswith(("https://", "http://", "data:", "#")):
            if reference.startswith("#"):
                check(reference[1:] in parser.ids, f"Missing fragment target: {reference}")
            continue
        check(not reference.startswith("/"), f"Root-relative path breaks /BioCare/: {reference}")
        clean = re.split(r"[?#]", reference, maxsplit=1)[0]
        check((ROOT / clean).is_file(), f"Missing relative {attribute}: {reference}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    print(f"Validation passed: {len(products)} products, {len(library['articles'])} library articles, /BioCare/ paths safe")


if __name__ == "__main__":
    main()
