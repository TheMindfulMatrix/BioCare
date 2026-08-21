#!/usr/bin/env python3
"""Build The Mindful Matrix dependency-free static site from centralized content."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_MARKER = '<meta name="generator" content="The Mindful Matrix static builder">'


def esc(value: object, *, attribute: bool = False) -> str:
    return html.escape(str(value), quote=attribute)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def render_template(name: str, replacements: dict[str, str]) -> str:
    output = (ROOT / "templates" / name).read_text(encoding="utf-8")
    for token, value in replacements.items():
        output = output.replace(token, value)
    unresolved = sorted(set(re.findall(r"{{([A-Z0-9_]+)}}", output)))
    if unresolved:
        raise RuntimeError(f"Unresolved template token in {name}: {', '.join(unresolved)}")
    return output


def write_output(path: Path, output: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(output, encoding="utf-8", newline="\n")


def external_note() -> str:
    return '<span class="visually-hidden"> (opens in a new tab)</span>'


def line_markup(lines: list[str]) -> str:
    return "".join(f"<span>{esc(line)}</span>" for line in lines)


def page_url(metadata: dict, path: str) -> str:
    return urljoin(metadata["canonicalBaseUrl"], path)


def json_ld_markup(records: list[dict]) -> str:
    if not records:
        return ""
    payload = records[0] if len(records) == 1 else {"@context": "https://schema.org", "@graph": records}
    if "@context" not in payload:
        payload = {"@context": "https://schema.org", **payload}
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'  <script type="application/ld+json">{serialized}</script>'


def organization_schema(metadata: dict) -> dict:
    return {
        "@type": "Organization",
        "@id": page_url(metadata, "#organization"),
        "name": "The Mindful Matrix",
        "url": metadata["canonicalBaseUrl"],
        "logo": page_url(metadata, "assets/brand/lockup-dark.svg"),
    }


def website_schema(metadata: dict) -> dict:
    return {
        "@type": "WebSite",
        "@id": page_url(metadata, "#website"),
        "name": "The Mindful Matrix",
        "url": metadata["canonicalBaseUrl"],
        "publisher": {"@id": page_url(metadata, "#organization")},
    }


def breadcrumb_schema(metadata: dict, items: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": position,
                "name": name,
                "item": page_url(metadata, path),
            }
            for position, (name, path) in enumerate(items, start=1)
        ],
    }


def shop_collection_schema(metadata: dict, products: list[dict]) -> dict:
    canonical = page_url(metadata, "shop.html")
    return {
        "@type": "CollectionPage",
        "@id": canonical + "#collection",
        "name": "Product Universe",
        "url": canonical,
        "description": "A curated catalog of optional wellness products organized by visitor intent.",
        "isPartOf": {"@id": page_url(metadata, "#website")},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(products),
            "itemListElement": [
                {"@type": "ListItem", "position": index, "name": product["name"], "url": canonical + f'#product-{product["id"]}'}
                for index, product in enumerate(products, start=1)
            ],
        },
    }


def article_schema(metadata: dict, article: dict, description: str, category: str) -> dict:
    canonical = page_url(metadata, f'library/{article["slug"]}.html')
    image = article.get("hero") or metadata.get("socialImage")
    record: dict[str, object] = {
        "@type": "Article",
        "@id": canonical + "#article",
        "headline": article["title"],
        "description": description,
        "mainEntityOfPage": canonical,
        "author": {"@type": "Organization", "name": article["author"]},
        "publisher": {"@id": page_url(metadata, "#organization")},
        "isPartOf": {"@id": page_url(metadata, "#website")},
        "articleSection": category,
    }
    if image and image.get("src"):
        record["image"] = {
            "@type": "ImageObject",
            "url": page_url(metadata, image["src"]),
            "width": int(image["width"]),
            "height": int(image["height"]),
        }
    if article.get("publishedIso"):
        record["datePublished"] = article["publishedIso"]
    if article.get("updatedIso"):
        record["dateModified"] = article["updatedIso"]
    return record


def document_head_markup(
    metadata: dict,
    *,
    prefix: str,
    title: str,
    description: str,
    path: str | None,
    page_type: str = "website",
    image: dict | None = None,
    published: str | None = None,
    updated: str | None = None,
    noindex: bool = False,
    structured_data: list[dict] | None = None,
) -> str:
    canonical = page_url(metadata, path) if path is not None else ""
    social_image = image or metadata.get("socialImage")
    asset_version = esc(metadata.get("assetVersion", "1"), attribute=True)
    asset_suffix = f"?v={asset_version}"

    # Keep identity and social metadata at the start of the static document so
    # link-preview crawlers do not need to traverse presentation resources.
    tags = [
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        f"  <title>{esc(title)}</title>",
        f'  <meta name="description" content="{esc(description, attribute=True)}">',
    ]
    if canonical:
        tags.append(f'  <link rel="canonical" href="{esc(canonical, attribute=True)}">')
    tags.extend(
        [
            f'  <meta property="og:title" content="{esc(title, attribute=True)}">',
            f'  <meta property="og:type" content="{esc(page_type, attribute=True)}">',
        ]
    )
    if canonical:
        tags.append(f'  <meta property="og:url" content="{esc(canonical, attribute=True)}">')
    if social_image and social_image.get("src"):
        image_url = page_url(metadata, social_image["src"])
        image_type = social_image.get("type") or {
            ".jpeg": "image/jpeg",
            ".jpg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }.get(Path(social_image["src"]).suffix.lower())
        tags.append(f'  <meta property="og:image" content="{esc(image_url, attribute=True)}">')
        if social_image.get("alt"):
            tags.append(f'  <meta property="og:image:alt" content="{esc(social_image["alt"], attribute=True)}">')
        if image_type:
            tags.append(f'  <meta property="og:image:type" content="{esc(image_type, attribute=True)}">')
        if social_image.get("width") and social_image.get("height"):
            tags.append(f'  <meta property="og:image:width" content="{int(social_image["width"])}">')
            tags.append(f'  <meta property="og:image:height" content="{int(social_image["height"])}">')
    tags.extend(
        [
            f'  <meta property="og:description" content="{esc(description, attribute=True)}">',
            '  <meta property="og:site_name" content="The Mindful Matrix">',
            '  <meta property="og:locale" content="en_US">',
            '  <meta name="twitter:card" content="summary_large_image">',
            f'  <meta name="twitter:title" content="{esc(title, attribute=True)}">',
            f'  <meta name="twitter:description" content="{esc(description, attribute=True)}">',
        ]
    )
    if social_image and social_image.get("src"):
        tags.append(f'  <meta name="twitter:image" content="{esc(image_url, attribute=True)}">')
        if social_image.get("alt"):
            tags.append(f'  <meta name="twitter:image:alt" content="{esc(social_image["alt"], attribute=True)}">')
    if page_type == "article":
        if published:
            tags.append(f'  <meta property="article:published_time" content="{esc(published, attribute=True)}">')
        if updated:
            tags.append(f'  <meta property="article:modified_time" content="{esc(updated, attribute=True)}">')
    tags.append(f"  {GENERATOR_MARKER}")
    if noindex:
        tags.append('  <meta name="robots" content="noindex, nofollow">')
    else:
        tags.append('  <meta name="robots" content="index, follow">')
    tags.extend(
        [
            '  <meta name="theme-color" content="#151814">',
            f'  <link rel="icon" href="{prefix}assets/brand/favicon.svg" type="image/svg+xml">',
            '  <link rel="preconnect" href="https://fonts.googleapis.com">',
            '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
            '  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400..600&amp;family=JetBrains+Mono:wght@500&amp;family=Manrope:wght@500..800&amp;display=swap" rel="stylesheet">',
            f'  <link rel="stylesheet" href="{prefix}assets/css/tokens.css{asset_suffix}">',
            f'  <link rel="stylesheet" href="{prefix}assets/css/base.css{asset_suffix}">',
            f'  <link rel="stylesheet" href="{prefix}assets/css/site.css{asset_suffix}">',
            f'  <script defer src="{prefix}assets/js/enhancements.js{asset_suffix}"></script>',
        ]
    )
    if structured_data and not noindex:
        tags.append(json_ld_markup(structured_data))
    return "\n".join(tags)


def shared_header_markup(data: dict, *, prefix: str, current: str) -> str:
    home = f"{prefix}index.html"
    explore_current = ' aria-current="page"' if current in {"explore", "department"} else ""
    start_current = ' aria-current="page"' if current == "start" else ""
    library_current = ' aria-current="page"' if current in {"library", "article"} else ""
    shop_current = ' aria-current="page"' if current == "shop" else ""
    products_by_id = {product["id"]: product for product in data["products"]}
    featured = products_by_id[data["featuredProductId"]]
    featured_url = esc(featured["destination"], attribute=True)
    return f'''<header class="site-header section-dark">
    <nav class="nav-shell container-wide" aria-label="Primary navigation">
      <a class="brand-link" href="{home}" aria-label="The Mindful Matrix home"><img src="{prefix}assets/brand/lockup-dark.svg" width="430" height="72" alt="The Mindful Matrix"></a>
      <form class="header-search" role="search" action="{prefix}explore.html"><label class="visually-hidden" for="matrix-search-{current}">Search the Matrix</label><input id="matrix-search-{current}" name="q" type="search" autocomplete="off" placeholder="Search the Matrix…"><button type="submit" aria-label="Submit Matrix search">Search</button></form>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-links"><span class="visually-hidden">Open navigation</span><span class="nav-toggle__lines" aria-hidden="true"></span></button>
      <ul id="primary-links" class="nav-links">
        <li><a href="{prefix}explore.html"{explore_current}>Explore</a></li>
        <li><a href="{prefix}shop.html"{shop_current}>Products</a></li>
        <li><a href="{prefix}library.html"{library_current}>Library</a></li>
        <li><a href="{prefix}start.html"{start_current}>Start Here</a></li>
      </ul>
    </nav>
  </header>'''


def shared_footer_markup(data: dict, *, prefix: str) -> str:
    site = data["site"]
    philosophy = data["brand"]["philosophy"]
    instagram = site["instagram"]
    home = f"{prefix}index.html"
    return f'''<footer class="site-footer section-dark">
    <div class="footer-grid container-wide">
      <div><a href="{home}" aria-label="The Mindful Matrix home"><img class="footer-lockup" src="{prefix}assets/brand/lockup-dark.svg" width="430" height="72" alt="The Mindful Matrix"></a><p class="footer-philosophy">{esc(philosophy)}</p></div>
      <nav class="footer-nav" aria-label="Footer navigation"><a href="{prefix}explore.html">Explore</a><a href="{prefix}start.html">Start here</a><a href="{prefix}library.html">The Library</a><a href="{prefix}shop.html">All products</a><a href="{home}#story">Our story</a><a href="{home}#transparency">Transparency</a></nav>
      <div class="footer-meta"><nav class="socials" aria-label="Social links"><a href="{esc(instagram["url"], attribute=True)}" target="_blank" rel="noopener noreferrer">Instagram{external_note()}</a></nav><p class="fine" data-fda-disclaimer>{esc(site["fdaDisclaimer"])}</p><p class="fine">{esc(site["disclosure"])}</p><p class="copyright">© {int(site["copyrightYear"])} The Mindful Matrix</p></div>
    </div>
  </footer>'''


def image_markup(product: dict, *, eager: bool = False, sizes: str = "(max-width: 48rem) 90vw, 42vw") -> str:
    image = product["image"]
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    source = Path(image["src"])
    widths = [280, 560] if int(image["width"]) == 560 else [512, 1024]
    srcset = ", ".join(f"img/responsive/{source.stem}-{width}.webp {width}w" for width in widths)
    fallback = (
        f'<img src="{esc(image["src"], attribute=True)}" alt="{esc(image["alt"], attribute=True)}" '
        f'width="{int(image["width"])}" height="{int(image["height"])}" '
        f'loading="{loading}" decoding="async"{priority}>'
    )
    return f'<picture><source type="image/webp" srcset="{esc(srcset, attribute=True)}" sizes="{esc(sizes, attribute=True)}">{fallback}</picture>'


def matrix_stage_markup(stage: dict) -> str:
    labels = "".join(f"<li>{esc(label)}</li>" for label in stage["labels"])
    return f'''<article class="matrix-stage" data-matrix-stage="{esc(stage["id"], attribute=True)}" data-matrix-index="{esc(stage["index"], attribute=True)}" data-reveal>
          <div class="matrix-stage__node" aria-hidden="true"><span>{esc(stage["index"])}</span></div>
          <div class="matrix-stage__content">
            <p class="interface-label">{esc(stage["name"])} / {esc(stage["index"])}</p>
            <h3>{esc(stage["heading"])}</h3>
            <p>{esc(stage["copy"])}</p>
            <ul class="matrix-labels" aria-label="Related areas">{labels}</ul>
            <strong class="matrix-question">{esc(stage["question"])}</strong>
          </div>
        </article>'''


def path_card_markup(path: dict) -> str:
    return f'''<article class="journey-card">
          <span class="journey-card__index">{esc(path["index"])} / {esc(path["id"])}</span>
          <span class="node" aria-hidden="true"></span>
          <h3>{esc(path["name"])}</h3><p>{esc(path["copy"])}</p>
          <a href="{esc(path["href"], attribute=True)}">{esc(path["cta"])} →</a>
        </article>'''


def testing_product_markup(product: dict, testing: dict) -> str:
    url = esc(product["destination"], attribute=True)
    return f'''<article class="testing-card" data-reveal>
        <div class="testing-card__visual"><span class="testing-card__scan" aria-hidden="true"></span><span class="testing-card__orbit testing-card__orbit--one" aria-hidden="true"></span><span class="testing-card__orbit testing-card__orbit--two" aria-hidden="true"></span><span class="testing-card__marker testing-card__marker--one" aria-hidden="true">Sample / 01</span><span class="testing-card__marker testing-card__marker--two" aria-hidden="true">Signal / Ready</span><div class="testing-card__product">{shelf_product_markup(product, eager=True)}</div></div>
        <div class="testing-card__content">
          <p class="interface-label">{esc(product["category"])} / Optional tool</p>
          <h3>{esc(product["name"])}</h3>
          <p>{esc(product["description"])}</p>
          {price_markup(product)}
          <div class="testing-card__why"><span>Why it’s here</span><strong>{esc(testing["why"])}</strong></div>
          <div class="button-row">
            <a class="button button-primary" href="{url}" target="_blank" rel="sponsored noopener noreferrer">{esc(testing["measureLinkLabel"])} ↗{external_note()}</a>
            <a class="button button-secondary" href="{url}" target="_blank" rel="sponsored noopener noreferrer">Product details ↗{external_note()}</a>
          </div>
        </div>
      </article>'''


def testing_workflow_markup() -> str:
    stages = [
        ("01", "Sample", "Starting point"),
        ("02", "Measurement", "A result"),
        ("03", "Interpretation", "Context matters"),
        ("04", "Next step", "An informed choice"),
    ]
    items = "".join(
        f'''<li data-workflow-step><span class="testing-workflow__node">{index}</span><div><strong>{esc(name)}</strong><small>{esc(note)}</small></div></li>'''
        for index, name, note in stages
    )
    return f'''<div class="testing-workflow" data-testing-workflow data-reveal>
        <div class="testing-workflow__track" aria-hidden="true"><span data-workflow-progress></span></div>
        <ol>{items}</ol>
      </div>'''


def hero_actions_markup(product: dict, product_count: int, affiliate_note: str) -> str:
    url = esc(product["destination"], attribute=True)
    return f'''{price_markup(product, context="hero")}
          <div class="hero-actions button-row">
            <a class="button button-primary" href="know-your-number.html">Learn: know your number →</a>
            <a class="button button-secondary" href="{url}" target="_blank" rel="sponsored noopener noreferrer">Official product source ↗{external_note()}</a>
            <a class="button button-secondary" href="shop.html">Browse all {product_count} curated products →</a>
          </div>
          <div class="hero-context"><span>Information → Education → Action</span><span>Test → Understand → Decide</span><a href="#matrix">Just browsing? Enter the Matrix ↓</a></div>
          <p id="hero-affiliate-disclosure" class="hero-affiliate-note" data-affiliate-disclosure>{esc(affiliate_note)}</p>'''


def hero_product_markup(product: dict) -> str:
    artwork = product.get("artwork", {})
    artwork_markup = ""
    if artwork.get("src"):
        artwork_markup = (
            f'<img class="hero-product__background" src="{esc(artwork["src"], attribute=True)}" alt="" data-parallax-depth="0.55" '
            f'width="{int(artwork["width"])}" height="{int(artwork["height"])}" '
            'loading="eager" decoding="async">'
        )
    url = esc(product["destination"], attribute=True)
    return f'''<div class="hero-product" data-product-id="{esc(product["id"], attribute=True)}">
            <span class="hero-product__orbit hero-product__orbit--outer" data-parallax-depth="0.35" aria-hidden="true"></span>
            <span class="hero-product__orbit hero-product__orbit--inner" data-parallax-depth="0.8" aria-hidden="true"></span>
            <span class="hero-product__channel hero-product__channel--gold" data-parallax-depth="1.1" aria-hidden="true"></span>
            <span class="hero-product__channel hero-product__channel--green" data-parallax-depth="0.65" aria-hidden="true"></span>
            <a class="hero-product__stage" href="{url}" target="_blank" rel="sponsored noopener noreferrer" aria-label="View {esc(product["name"], attribute=True)} on Zinzino (opens in a new tab)">
              {artwork_markup}
              <span class="hero-product__pedestal" data-parallax-depth="0.5" aria-hidden="true"></span>
              <div class="hero-product__cutout" data-parallax-depth="0.22">{shelf_product_markup(product, eager=True)}</div>
              <div class="hero-product__signal hero-product__signal--one" data-parallax-depth="1.15" aria-hidden="true"><span>01</span> Test</div>
              <div class="hero-product__signal hero-product__signal--two" data-parallax-depth="0.8" aria-hidden="true"><span>02</span> Learn</div>
              <div class="hero-product__signal hero-product__signal--three" data-parallax-depth="1.35" aria-hidden="true"><span>03</span> Choose</div>
              <span class="hero-product__tap">View the kit ↗</span>
            </a>
            <div class="hero-product__caption" data-parallax-depth="0.9"><span>Featured starting point</span><strong>{esc(product["name"])}</strong><small>{esc(product["productKind"])} / SKU {esc(product["sku"])}</small></div>
          </div>'''


def universe_intents_markup(catalog: dict) -> str:
    return "".join(
        f'''<button class="product-universe__intent" type="button" data-universe-intent="{esc(intent["id"], attribute=True)}" data-intent-featured="{esc(intent["featuredProductId"], attribute=True)}" data-intent-index="{esc(intent["index"], attribute=True)}" data-intent-name="{esc(intent["name"], attribute=True)}" data-intent-description="{esc(intent["description"], attribute=True)}" data-intent-environment="{esc(intent["environment"], attribute=True)}" aria-controls="universe-products" aria-pressed="{'true' if index == 0 else 'false'}"><span>{esc(intent["index"])}</span><strong>{esc(intent["name"])}</strong><small>{esc(intent["shortName"])}</small></button>'''
        for index, intent in enumerate(catalog["intents"])
    )


def universe_roster_markup(products: list[dict], featured_id: str) -> str:
    return "".join(
        f'''<button type="button" data-universe-select="{esc(product["id"], attribute=True)}" data-product-intent="{esc(product["intent"], attribute=True)}" aria-controls="universe-products" aria-pressed="{'true' if product["id"] == featured_id else 'false'}"><span>{index:02d}</span><strong>{esc(product["name"])}</strong></button>'''
        for index, product in enumerate(products, start=1)
    )


def testing_education_markup(testing: dict) -> str:
    education = testing["education"]
    return f'''<section class="testing-education" aria-labelledby="testing-education-title" data-reveal>
        <div><p class="interface-label">{esc(education["label"])}</p><h3 id="testing-education-title">{esc(education["heading"])}</h3><p>{esc(education["copy"])}</p></div>
        <a class="button button-tertiary" href="{esc(education["href"], attribute=True)}">{esc(education["cta"])} →</a>
      </section>'''


def product_artwork_markup(product: dict) -> str:
    artwork = product.get("artwork", {})
    source = artwork.get("src")
    if not source:
        return '<span class="shelf-card__artwork artwork-stage__background" data-artwork-state="placeholder" aria-hidden="true"></span>'
    return (
        f'<img class="shelf-card__artwork artwork-stage__background" src="{esc(source, attribute=True)}" alt="" '
        f'width="{int(artwork["width"])}" height="{int(artwork["height"])}" '
        'loading="lazy" decoding="async" data-artwork-state="ready">'
    )


def shelf_product_markup(product: dict, *, eager: bool = False) -> str:
    cutout = product.get("cutout")
    if not cutout:
        return image_markup(product, eager=eager)
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    return (
        f'<img class="shelf-card__cutout" src="{esc(cutout["src"], attribute=True)}" '
        f'alt="{esc(cutout["alt"], attribute=True)}" '
        f'width="{int(cutout["width"])}" height="{int(cutout["height"])}" '
        f'loading="{loading}" decoding="async"{priority} data-image-role="official-product-cutout">'
    )


def product_name_modifier(name: str) -> str:
    if len(name) >= 42:
        return " product-name--very-long"
    if len(name) >= 30:
        return " product-name--long"
    return ""


def active_products(catalog: dict) -> list[dict]:
    return [product for product in catalog["products"] if product.get("commercial_status", "active") == "active"]


def curated_products(catalog: dict) -> list[dict]:
    return [product for product in active_products(catalog) if product.get("curated", True)]


def money(value: int | float) -> str:
    number = float(value)
    return f"${number:,.0f}" if number.is_integer() else f"${number:,.2f}"


def affiliate_source_url(product: dict) -> str:
    """Return the official manufacturer source with the established partner attribution."""
    source = product["price"].get("affiliate_price_source") or product["price"]["official_price_source"]
    if product["manufacturer"] == "Zinzino":
        return source.replace("/shop/site/US/en-US/", "/shop/2021428066/us/en-us/", 1)
    if product["manufacturer"] == "BioLimitless":
        parsed = urlsplit(source)
        query = parse_qsl(parsed.query, keep_blank_values=True)
        if not any(key == "me" for key, _ in query):
            query.append(("me", "matrix"))
        return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))
    return source


def price_markup(product: dict, *, context: str = "detail") -> str:
    price = product["price"]
    model = price["pricing_model"]
    items: list[str] = []
    def price_item(value: str, label: str, role: str) -> str:
        return f'<span class="product-price__item product-price__item--{role}" data-price-role="{role}"><strong>{value}</strong> {label}</span>'
    if model == "starter_subscription":
        items = [price_item(money(price["start_price"]), esc(price["start_label"]), "primary"), price_item(f'{money(price["recurring_price"])}/mo', esc(price["recurring_label"]), "supporting")]
    elif model == "retail_premier":
        items = [price_item(money(price["premier_price"]), "Premier price", "primary"), price_item(money(price["retail_price"]), "retail", "reference")] if price.get("premier_price") is not None else [price_item(money(price["retail_price"]), "retail", "primary")]
    elif model == "one_time_autoship":
        items = [price_item(f'{money(price["autoship_price"])}/mo', "Subscribe &amp; Save", "primary"), price_item(money(price["one_time_price"]), "one-time", "reference")]
    elif model == "one_time_range":
        items = [price_item(f'{money(price["one_time_price_min"])}–{money(price["one_time_price_max"])}', "one-time · format varies", "primary")]
    else:
        items = [price_item(money(price["one_time_price"]), "one-time", "primary")]
    verified = esc(price["price_verified_at"], attribute=True)
    source = esc(affiliate_source_url(product), attribute=True)
    product_name = esc(product["name"], attribute=True)
    helper = ""
    if context == "detail" and product["manufacturer"] == "Zinzino" and price.get("premier_price") is not None:
        helper = '<small>Premier pricing may require an eligible Premier purchase or customer status. Checkout reflects the current applicable price.</small>'
    disclosure_id = "shop-affiliate-disclosure" if context == "compact" else ("hero-affiliate-disclosure" if context == "hero" else "shelf-affiliate-disclosure")
    return f'<div class="product-price product-price--{esc(context, attribute=True)}" data-price-record data-price-model="{esc(model, attribute=True)}" data-price-verified="{verified}"><div>{"".join(items)}</div>{helper}<a class="product-price__source" href="{source}" target="_blank" rel="sponsored noopener noreferrer" aria-describedby="{disclosure_id}" aria-label="Official price source for {product_name} (opens in a new tab)">Official price source ↗{external_note()}</a></div>'


def product_reference(product: dict, *, prefix: str = "") -> str:
    sku = product.get("sku")
    return f'{prefix}SKU {esc(sku)}' if sku else f'{prefix}BioLimitless product'


def biolimitless_disclosure(product: dict) -> str:
    if product["manufacturer"] != "BioLimitless":
        return ""
    return '<p class="fine product-material-connection" data-biolimitless-disclosure>BioLimitless links use the Matrix partner referral. I may earn compensation from qualifying purchases.</p>'


def universe_product_markup(product: dict, *, index: int, active: bool = False) -> str:
    active_attribute = ' data-active="true"' if active else ""
    name_modifier = product_name_modifier(product["name"])
    related = product.get("relatedEducation")
    related_markup = ""
    if related:
        related_markup = f'<a class="product-universe__learn" href="{esc(related["href"], attribute=True)}">{esc(related["label"])} →</a>'
    return f'''<article class="product-universe__product{name_modifier}" data-universe-product="{esc(product["id"], attribute=True)}" data-product-intent="{esc(product["intent"], attribute=True)}" data-manufacturer="{esc(product["manufacturer"], attribute=True)}" data-environment="{esc(product["environment"], attribute=True)}" aria-labelledby="universe-product-title-{esc(product["id"], attribute=True)}"{active_attribute}>
        <div class="product-universe__visual artwork-stage">
          {product_artwork_markup(product)}
          <span class="product-universe__orbit product-universe__orbit--one" aria-hidden="true"></span>
          <span class="product-universe__orbit product-universe__orbit--two" aria-hidden="true"></span>
          <span class="product-universe__pedestal" aria-hidden="true"></span>
          <div class="product-universe__cutout">{shelf_product_markup(product, eager=active)}</div>
          <span class="product-universe__sku">{product_reference(product)}</span>
          <span class="product-universe__number" aria-hidden="true">{index:02d}</span>
        </div>
        <div class="product-universe__content">
          <p class="interface-label">{esc(product["category"])} / {esc(product["productKind"])}</p>
          <h3 id="universe-product-title-{esc(product["id"], attribute=True)}">{esc(product["name"])}</h3>
          <p class="product-universe__description">{esc(product["description"])}</p>
          <dl class="product-universe__facts"><div><dt>Manufacturer</dt><dd>{esc(product["manufacturer"])}</dd></div><div><dt>Format</dt><dd>{esc(product["variantLabel"])}</dd></div></dl>
          {price_markup(product)}
          <div class="product-universe__why"><span>Why it’s here</span><p>{esc(product["whyItsHere"])}</p></div>{biolimitless_disclosure(product)}
          <div class="button-row"><a class="button button-primary" href="{esc(product["destination"], attribute=True)}" target="_blank" rel="sponsored noopener noreferrer">{esc(product["cta"])} ↗{external_note()}</a>{related_markup}</div>
        </div>
      </article>'''


def universe_product_payload(product: dict, *, index: int) -> dict:
    return {
        "id": product["id"], "index": index, "name": product["name"], "manufacturer": product["manufacturer"], "sku": product.get("sku"),
        "intent": product["intent"], "category": product["category"], "productKind": product["productKind"], "variantLabel": product["variantLabel"],
        "description": product["description"], "whyItsHere": product["whyItsHere"], "environment": product["environment"], "destination": product["destination"],
        "cta": product["cta"], "price": {**product["price"], "affiliate_price_source": affiliate_source_url(product)}, "cutout": product.get("cutout"),
        "artwork": product.get("artwork"), "relatedEducation": product.get("relatedEducation"),
    }


def universe_data_markup(products: list[dict]) -> str:
    payload = [universe_product_payload(product, index=index) for index, product in enumerate(products, start=1)]
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/json" data-universe-data>{serialized}</script>'


def product_label_panel_markup(product: dict, label_record: dict | None) -> str:
    if not label_record or label_record.get("status") != "approved":
        return ""
    ingredients = label_record.get("ingredients", [])
    rows=[]
    for ingredient in ingredients:
        amount=ingredient.get("amount")
        amount_text=f'{esc(amount)} {esc(ingredient.get("unit", ""))}'.strip() if ingredient.get("disclosed", amount is not None) and amount is not None else "Amount not disclosed by manufacturer."
        rows.append(f'<li><span>{esc(ingredient["ingredient"])}</span><strong>{amount_text}</strong></li>')
    source=esc(label_record["source_url"],attribute=True); checked=esc(label_record["checked_date"])
    serving=esc(label_record.get("serving_size") or "Not stated"); servings=esc(label_record.get("servings_per_container") or "Not stated")
    return f'''<details class="product-label-panel"><summary>View full label information</summary><div class="product-label-panel__body"><dl><div><dt>Serving size</dt><dd>{serving}</dd></div><div><dt>Servings per container</dt><dd>{servings}</dd></div></dl><ul>{"".join(rows)}</ul><p>Checked {checked} against the official manufacturer source.</p><a href="{source}" target="_blank" rel="sponsored noopener noreferrer" aria-label="Full label source for {esc(product["name"], attribute=True)} (opens in a new tab)">View manufacturer label source ↗{external_note()}</a></div></details>'''


def shop_intent_rail_label(intent: dict) -> str:
    return "Testing" if intent["id"] == "test-measure" else intent["shortName"]


def shop_intent_rail_markup(intents: list[dict], products: list[dict]) -> str:
    counts = {intent["id"]: sum(1 for product in products if product["intent"] == intent["id"]) for intent in intents}
    buttons = [
        f'<button type="button" data-shop-intent="all" aria-pressed="true"><strong>All</strong><small>{len(products)}</small></button>'
    ]
    for intent in intents:
        buttons.append(
            f'<button id="intent-{esc(intent["id"], attribute=True)}" type="button" data-shop-intent="{esc(intent["id"], attribute=True)}" aria-pressed="false">'
            f'<strong>{esc(shop_intent_rail_label(intent))}</strong><small>{counts[intent["id"]]}</small></button>'
        )
    return "".join(buttons)


def shop_price_summary_markup(product: dict) -> str:
    price = product["price"]
    model = price["pricing_model"]
    if model == "starter_subscription":
        lines = [(money(price["start_price"]), esc(price["start_label"]), "primary"), (f'{money(price["recurring_price"])}/mo', esc(price["recurring_label"]), "supporting")]
    elif model == "retail_premier":
        lines = [(money(price["premier_price"]), "Premier", "primary"), (money(price["retail_price"]), "retail", "reference")] if price.get("premier_price") is not None else [(money(price["retail_price"]), "retail", "primary")]
    elif model == "one_time_autoship":
        lines = [(f'{money(price["autoship_price"])}/mo', "Subscribe &amp; Save", "primary"), (money(price["one_time_price"]), "one-time", "reference")]
    elif model == "one_time_range":
        lines = [(f'{money(price["one_time_price_min"])}–{money(price["one_time_price_max"])}', "one-time range", "primary")]
    else:
        lines = [(money(price["one_time_price"]), "one-time", "primary")]
    return '<div class="catalog-price" data-price-model="{}">{}</div>'.format(
        esc(model, attribute=True),
        "".join(f'<span class="catalog-price__{role}"><strong>{value}</strong><small>{label}</small></span>' for value, label, role in lines),
    )


def shop_label_payload(label_record: dict | None) -> dict:
    if not label_record:
        return {"state": "unavailable_or_unverified", "ingredients": []}
    approved = label_record.get("status") == "approved"
    return {
        "state": label_record.get("verificationStatus", "unavailable_or_unverified"),
        "status": label_record.get("status", "pending"),
        "servingSize": label_record.get("serving_size") if approved else None,
        "servingsPerContainer": label_record.get("servings_per_container") if approved else None,
        "ingredients": label_record.get("ingredients", []) if approved else [],
        "sourceUrl": label_record.get("source_url") if approved else None,
        "checkedDate": label_record.get("checked_date") if approved else None,
    }


def evidence_collection_schema(metadata: dict, sources: list[dict]) -> dict:
    canonical = page_url(metadata, "evidence.html")
    return {
        "@type": "CollectionPage",
        "@id": canonical + "#collection",
        "name": "Evidence & Documentation",
        "url": canonical,
        "description": "A reviewed index of published public references with visible scope and limitations.",
        "isPartOf": {"@id": page_url(metadata, "#website")},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(sources),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": index,
                    "name": source["title"],
                    "url": canonical + f'#source-{source["id"]}',
                }
                for index, source in enumerate(sources, start=1)
            ],
        },
    }


def published_sources(manifest: dict) -> list[dict]:
    return [record for record in manifest.get("records", []) if record.get("status") == "published"]


def source_type_label(value: str) -> str:
    return value.replace("_", " ").title()


def source_card_markup(source: dict, *, prefix: str = "", compact: bool = False) -> str:
    manufacturer = source.get("manufacturer") or "Independent public source"
    topics = " · ".join(item.replace("-", " ").title() for item in source.get("topic_ids", []))
    attributes = {
        "topic": ",".join(source.get("topic_ids", [])),
        "type": source["resource_type"],
        "manufacturer": source.get("manufacturer") or "independent",
        "product": ",".join(source.get("product_ids", [])),
        "department": ",".join(source.get("department_ids", [])),
        "independence": source["independence_status"],
        "search": " ".join(
            [source["title"], source["publisher"], source["public_summary"], source["scope"], source["limitations"]]
            + source.get("topic_ids", [])
        ).lower(),
    }
    data_attributes = " ".join(
        f'data-source-{name}="{esc(value, attribute=True)}"' for name, value in attributes.items()
    )
    if compact:
        return f'''<article class="source-card source-card--compact" {data_attributes}><p class="interface-label">{esc(source_type_label(source["resource_type"]))}</p><h3>{esc(source["title"])}</h3><p>{esc(source["public_summary"])}</p><a href="{prefix}evidence.html?source={esc(source["id"], attribute=True)}">Inspect source context →</a></article>'''
    date = source.get("publication_date") or "Date not stated"
    return f'''<article id="source-{esc(source["id"], attribute=True)}" class="source-card" data-public-source="{esc(source["id"], attribute=True)}" {data_attributes}>
      <header><p class="interface-label">{esc(source_type_label(source["resource_type"]))}</p><span>{esc(manufacturer)}</span><h3>{esc(source["title"])}</h3><p class="source-card__publisher">{esc(source["publisher"])}</p></header>
      <dl class="source-card__meta"><div><dt>Published</dt><dd>{esc(date)}</dd></div><div><dt>Link checked</dt><dd>{esc(source["checked_date"])}</dd></div><div><dt>Topics</dt><dd>{esc(topics)}</dd></div></dl>
      <p>{esc(source["public_summary"])}</p>
      <details><summary>Scope and limitations</summary><h4>Scope</h4><p>{esc(source["scope"])}</p><h4>Limitations</h4><p>{esc(source["limitations"])}</p></details>
      <a class="source-card__link" href="{esc(source["public_url"], attribute=True)}" target="_blank" rel="noopener noreferrer" aria-label="Open public source: {esc(source["title"], attribute=True)} (opens in a new tab)">Open public source ↗{external_note()}</a>
    </article>'''


def product_documentation(product: dict, sources: list[dict]) -> list[dict]:
    exact = [source for source in sources if product["id"] in source.get("product_ids", [])]
    department = [source for source in sources if product["intent"] in source.get("department_ids", []) and source not in exact]
    return [
        {
            "id": source["id"],
            "relationship": "product-specific context" if source in exact else "department context — not product evidence",
        }
        for source in (exact + department)[:3]
    ]


def shop_product_payload(product: dict, *, index: int, label_record: dict | None, sources: list[dict]) -> dict:
    label = shop_label_payload(label_record)
    return {
        "id": product["id"],
        "index": index,
        "name": product["name"],
        "manufacturer": product["manufacturer"],
        "sku": product.get("sku"),
        "intent": product["intent"],
        "category": product["category"],
        "productKind": product["productKind"],
        "purchaseModel": product.get("purchaseModel"),
        "variantLabel": product["variantLabel"],
        "description": product["description"],
        "whyItsHere": product["whyItsHere"],
        "environment": product["environment"],
        "destination": product["destination"],
        "cta": product["cta"],
        "price": {**product["price"], "affiliate_price_source": affiliate_source_url(product)},
        "cutout": product.get("cutout"),
        "relatedEducation": product.get("relatedEducation"),
        "label": label,
        "documentation": product_documentation(product, sources),
        "verifiedIngredients": [item["ingredient"] for item in label["ingredients"]],
    }


def shop_catalog_data_markup(data: dict, products: list[dict], label_records: dict[str, dict], sources: list[dict]) -> str:
    catalog = data["catalog"]
    payload = {
        "activeCount": len(products),
        "initialCount": 12,
        "verifiedDate": catalog["verifiedDate"],
        "intents": [
            {
                "id": intent["id"],
                "name": intent["name"],
                "shortName": shop_intent_rail_label(intent),
                "count": sum(1 for product in products if product["intent"] == intent["id"]),
            }
            for intent in catalog["intents"]
        ],
        "sources": [
            {
                "id": source["id"], "title": source["title"], "publisher": source["publisher"],
                "resourceType": source_type_label(source["resource_type"]), "publicUrl": source["public_url"],
                "evidenceUrl": f'evidence.html?source={source["id"]}', "independence": source["independence_status"],
            }
            for source in sources
        ],
        "products": [shop_product_payload(product, index=index, label_record=label_records.get(product["id"]), sources=sources) for index, product in enumerate(products, start=1)],
    }
    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/json" data-shop-catalog>{serialized}</script>'


def shop_compact_card_markup(product: dict, *, index: int) -> str:
    eager = index <= 2
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    cutout = product.get("cutout")
    if cutout:
        source = esc(cutout["src"], attribute=True)
        rendered_source = source if eager else "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
        deferred_source = "" if eager else f' data-src="{source}"'
        image = (
            f'<img src="{rendered_source}"{deferred_source} alt="{esc(cutout["alt"], attribute=True)}" '
            f'width="{int(cutout["width"])}" height="{int(cutout["height"])}" loading="{loading}" decoding="async"{priority}>'
        )
    else:
        image = image_markup(product, eager=eager)
    return f'''<article id="product-{esc(product["id"], attribute=True)}" class="catalog-card{product_name_modifier(product["name"])}" data-shop-product data-product-id="{esc(product["id"], attribute=True)}" data-environment="{esc(product["environment"], attribute=True)}">
        <div class="catalog-card__visual"><span class="catalog-card__node" aria-hidden="true"></span>{image}</div>
        <div class="catalog-card__body"><p class="catalog-card__meta">{esc(product["manufacturer"])} / {esc(product["category"])}</p><h2>{esc(product["name"])}</h2><p class="catalog-card__description">{esc(product["description"])}</p>{shop_price_summary_markup(product)}<button class="catalog-card__inspect" type="button" data-product-open="{esc(product["id"], attribute=True)}" aria-label="View details for {esc(product["name"], attribute=True)}">View details</button></div>
      </article>'''


def shop_initial_cards_markup(products: list[dict]) -> str:
    return "".join(shop_compact_card_markup(product, index=index) for index, product in enumerate(products[:12], start=1))


def shop_filter_intents_markup(intents: list[dict]) -> str:
    options = ['<label><input type="radio" name="filter-intent" value="all" checked><span>All products</span></label>']
    options.extend(f'<label><input type="radio" name="filter-intent" value="{esc(intent["id"], attribute=True)}"><span>{esc(intent["name"])}</span></label>' for intent in intents)
    return "".join(options)


def shop_filter_kinds_markup(products: list[dict]) -> str:
    kinds = sorted({product["productKind"] for product in products}, key=str.casefold)
    return "".join(f'<label><input type="checkbox" name="filter-kind" value="{esc(kind, attribute=True)}"><span>{esc(kind)}</span></label>' for kind in kinds)


def shop_filter_manufacturers_markup(products: list[dict]) -> str:
    manufacturers = sorted({product["manufacturer"] for product in products}, key=str.casefold)
    options = ['<label><input type="radio" name="filter-manufacturer" value="all" checked><span>All manufacturers</span></label>']
    options.extend(f'<label><input type="radio" name="filter-manufacturer" value="{esc(manufacturer, attribute=True)}"><span>{esc(manufacturer)}</span></label>' for manufacturer in manufacturers)
    return "".join(options)


def shop_no_script_markup(products: list[dict], data: dict) -> str:
    links = "".join(
        f'<li><a href="{esc(product["destination"], attribute=True)}" target="_blank" rel="sponsored noopener noreferrer">{esc(product["name"])} — official manufacturer source ↗{external_note()}</a></li>'
        for product in products
    )
    return f'''<noscript><section class="shop-noscript" aria-labelledby="shop-noscript-title"><h2 id="shop-noscript-title">Complete product catalog</h2><p>JavaScript is unavailable, so this list provides every official manufacturer destination.</p><ul>{links}</ul></section></noscript>'''


def shop_fallbacks_markup(fallbacks: list[dict]) -> str:
    return "".join(
        f'''<article class="shop-fallback" data-reveal><p class="interface-label">{esc(item["type"])}</p><h3>{esc(item["name"])}</h3><p>{esc(item["description"])}</p><a href="{esc(item["destination"], attribute=True)}" target="_blank" rel="sponsored noopener noreferrer">Open destination ↗{external_note()}</a></article>'''
        for item in fallbacks
    )


def published_articles(library: dict) -> list[dict]:
    return [article for article in library["articles"] if article.get("status") == "published"]


def category_name(library: dict, category_id: str) -> str:
    categories = {category["id"]: category["name"] for category in library["categories"]}
    return categories.get(category_id, category_id)


def library_article_markup(article: dict, library: dict, *, index: int = 1, archive: bool = False) -> str:
    hero = article.get("hero")
    if hero and hero.get("src"):
        source = f'<source media="(max-width: 44rem)" srcset="{esc(hero["srcSmall"], attribute=True)}" width="{int(hero["smallWidth"])}" height="{int(hero["smallHeight"])}">' if hero.get("srcSmall") else ""
        visual = (
            f'<picture>{source}<img src="{esc(hero["src"], attribute=True)}" alt="{esc(hero.get("alt", ""), attribute=True)}" '
            f'width="{int(hero["width"])}" height="{int(hero["height"])}" loading="lazy" decoding="async"></picture>'
        )
    else:
        visual = '<div class="library-card__art" aria-hidden="true"><span class="library-card__line"></span></div>'
    metadata: list[str] = []
    if article.get("published"):
        datetime = article.get("publishedIso") or article["published"]
        metadata.append(f'<time datetime="{esc(datetime, attribute=True)}">Published {esc(article["published"])}</time>')
    metadata.append(f'<span>{esc(article["readingTime"])}</span>')
    if article.get("evidenceReviewed"):
        metadata.append(f'<span>Evidence reviewed {esc(article["evidenceReviewed"])}</span>')
    if article.get("updated"):
        metadata.append(f'<span>Updated {esc(article["updated"])}</span>')
    archive_attribute = f' data-archive-index="{index:02d}"' if archive else ""
    if archive:
        source_count = len(article.get("sources", []))
        evidence_status = f'Evidence reviewed {esc(article["evidenceReviewed"])}' if article.get("evidenceReviewed") else "Evidence record available"
        visual = f'''<span class="library-article__index" aria-hidden="true">{index:02d}</span><span class="library-article__signal" aria-hidden="true"></span>{visual}<div class="library-article__evidence"><span>{evidence_status}</span><strong>{source_count:02d} sources</strong></div>'''
    return f'''<article class="library-article" data-library-article data-reveal{archive_attribute}>
        <div class="library-article__visual">{visual}</div>
        <div class="library-article__content">
          <p class="interface-label">{esc(category_name(library, article["category"]))}</p><h3>{esc(article["title"])}</h3><p>{esc(article["summary"])}</p>
          <div class="library-article__meta">{"".join(metadata)}</div>
          <a class="button button-tertiary" href="library/{esc(article["slug"], attribute=True)}.html">Read the guide →</a>
        </div>
      </article>'''


def category_badges(library: dict) -> str:
    return "".join(f'<span>{esc(category["name"])}</span>' for category in library["categories"])


def library_body_markup(library: dict, library_home: dict) -> str:
    articles = published_articles(library)
    if articles:
        return '<div class="library-article-grid" data-library-state="published">' + "".join(
            library_article_markup(article, library, index=index, archive=True) for index, article in enumerate(articles, start=1)
        ) + "</div>"
    return f'''<div class="library-layout" data-library-state="empty">
        <article class="library-status-card" data-reveal>
          <div class="library-card__art" aria-hidden="true"><span class="library-card__line"></span></div>
          <div class="library-status-card__content"><h3>{esc(library_home["status"])}</h3><p>{esc(library_home["statusCopy"])}</p></div>
        </article>
        <div class="library-categories" data-reveal><p class="component-label">{esc(library_home["categoriesLabel"])}</p>{category_badges(library)}</div>
      </div>'''


def library_category_markup(category: dict, count: int) -> str:
    availability = f'{count} published guide' + ("" if count == 1 else "s") if count else "Coming soon"
    content = f'''<span class="category-card__index">{esc(category["id"])}</span><strong>{esc(category["name"])}</strong><small>{availability}</small><span aria-hidden="true">{"→" if count else "—"}</span>'''
    if count:
        href = f'#category-{esc(category["id"], attribute=True)}'
        return f'''<a class="category-card" href="{href}" data-reveal>{content}</a>'''
    return f'''<div class="category-card" data-availability="coming-soon" data-reveal>{content}</div>'''


def library_index_markup(library: dict, home: dict) -> str:
    articles = published_articles(library)
    if articles:
        groups: list[str] = []
        for category in library["categories"]:
            matches = [article for article in articles if article["category"] == category["id"]]
            if not matches:
                continue
            cards = "".join(library_article_markup(article, library) for article in matches)
            groups.append(f'''<section id="category-{esc(category["id"], attribute=True)}" class="library-group" aria-labelledby="category-{esc(category["id"], attribute=True)}-title"><h3 id="category-{esc(category["id"], attribute=True)}-title">{esc(category["name"])}</h3><div class="library-article-grid">{cards}</div></section>''')
        return '<div data-library-state="published">' + "".join(groups) + "</div>"
    return f'''<div class="library-empty" data-library-state="empty" data-reveal>
      <div class="library-empty__signal" aria-hidden="true"><span></span><span></span><span></span></div>
      <div><p class="interface-label">Coming to the Library</p><h3>{esc(home["library"]["status"])}</h3><p>{esc(home["library"]["statusCopy"])}</p><div class="library-empty__categories">{category_badges(library)}</div></div>
    </div>'''


def standard_markup(principle: dict, *, interactive: bool = False, active: bool = False) -> str:
    if interactive:
        open_attribute = " open" if active else ""
        return f'''<li class="standards-node" data-standard-node data-standard-index="{esc(principle["index"], attribute=True)}"><details{open_attribute}><summary><span class="standards-node__signal" aria-hidden="true"></span><span class="standards-node__index">{esc(principle["index"])}</span><strong>{esc(principle["name"])}</strong><span class="standards-node__toggle" aria-hidden="true"></span></summary><p>{esc(principle["copy"])}</p></details></li>'''
    return f'''<li><span>{esc(principle["index"])}</span><div><h3>{esc(principle["name"])}</h3><p>{esc(principle["copy"])}</p></div></li>'''


def editorial_principles_markup(site_data: dict, library: dict) -> str:
    selected = [item for item in site_data["homepage"]["standards"]["principles"] if item["index"] in {"01", "02", "03", "05"}]
    update = library["editorialUpdatePrinciple"]
    selected.append({"index": "06", "name": update["name"], "copy": update["copy"]})
    return "".join(standard_markup(item) for item in selected)


def orientation_stage_markup(stage: dict) -> str:
    return f'''<li id="{esc(stage["id"], attribute=True)}" class="orientation-stage" data-reveal>
      <div class="orientation-stage__node" aria-hidden="true">{esc(stage["index"])}</div>
      <div class="orientation-stage__body"><p class="interface-label">{esc(stage["name"])}</p><h3>{esc(stage["heading"])}</h3><p>{esc(stage["copy"])}</p><strong>{esc(stage["question"])}</strong></div>
    </li>'''


def start_pathway_markup(pathway: dict) -> str:
    return f'''<article class="start-pathway" data-start-pathway="{esc(pathway["id"], attribute=True)}" data-reveal>
      <p class="interface-label">{esc(pathway["index"])} / Choose a path</p><h3>{esc(pathway["heading"])}</h3><p>{esc(pathway["copy"])}</p>
      <a class="button button-tertiary" href="{esc(pathway["href"], attribute=True)}">{esc(pathway["cta"])} →</a>
    </article>'''


def article_block_markup(block: dict) -> str:
    block_type = block.get("type", "paragraph")
    if block_type == "paragraph":
        return f'<p>{esc(block["text"])}</p>'
    if block_type == "subheading":
        return f'<h3>{esc(block["text"])}</h3>'
    if block_type == "list":
        items = "".join(f"<li>{esc(item)}</li>" for item in block["items"])
        ordered = block.get("ordered", False)
        return f'<{"ol" if ordered else "ul"}>{items}</{"ol" if ordered else "ul"}>'
    if block_type == "termList":
        items = "".join(
            f'<div><dt>{esc(item["term"])}</dt><dd>{esc(item["definition"])}</dd></div>'
            for item in block["items"]
        )
        return f'<dl class="article-term-list">{items}</dl>'
    if block_type == "quote":
        attribution = f'<cite>{esc(block["attribution"])}</cite>' if block.get("attribution") else ""
        return f'<blockquote><p>{esc(block["text"])}</p>{attribution}</blockquote>'
    if block_type == "callout":
        label = f'<p class="interface-label">{esc(block["label"])}</p>' if block.get("label") else ""
        title = f'<h3>{esc(block["title"])}</h3>' if block.get("title") else ""
        return f'<aside class="article-callout">{label}{title}<p>{esc(block["text"])}</p></aside>'
    raise ValueError(f"Unsupported article block type: {block_type}")


def article_body_markup(article: dict) -> str:
    sections = []
    for section in article["bodySections"]:
        blocks = "".join(article_block_markup(block) for block in section["blocks"])
        sections.append(f'''<section id="{esc(section["id"], attribute=True)}" class="article-section"><h2>{esc(section["heading"])}</h2>{blocks}</section>''')
    return "".join(sections)


def article_toc_markup(article: dict) -> str:
    links = '<li><a href="#evidence-map">Evidence map</a></li>' if article.get("evidenceLabels") else ""
    links += "".join(f'<li><a href="#{esc(section["id"], attribute=True)}">{esc(section["heading"])}</a></li>' for section in article["bodySections"])
    if article.get("evidenceSummary"):
        links += '<li><a href="#what-we-know">What we know</a></li>'
    for key, label in (("evidenceNotes", "Evidence notes"), ("limitations", "Limitations"), ("sources", "Sources")):
        if article.get(key):
            links += f'<li><a href="#{key.replace("Notes", "-notes")}">{label}</a></li>'
    if article.get("relatedArticles") or article.get("optionalAction"):
        links += '<li><a href="#article-journey">Where to go next</a></li>'
    return f'<p class="interface-label">On this page</p><ol>{links}</ol>'


def article_list_section(section_id: str, heading: str, items: list[str], class_name: str = "article-panel") -> str:
    if not items:
        return ""
    return f'''<section id="{section_id}" class="{class_name}"><h2>{esc(heading)}</h2><ul>{"".join(f"<li>{esc(item)}</li>" for item in items)}</ul></section>'''


def article_sources_markup(sources: list[dict]) -> str:
    if not sources:
        return ""
    items = []
    for source in sources:
        citation = f'<span>{esc(source["citation"])}</span>' if source.get("citation") else ""
        detail = f'<p>{esc(source["detail"])}</p>' if source.get("detail") else ""
        items.append(f'''<li><div class="article-source__identity"><strong>{esc(source["organization"])}</strong>{citation}</div><a href="{esc(source["url"], attribute=True)}" target="_blank" rel="noopener noreferrer">{esc(source["title"])} ↗{external_note()}</a>{detail}</li>''')
    return f'''<section id="sources" class="article-sources"><h2>Sources</h2><ol>{"".join(items)}</ol></section>'''


def article_evidence_map_markup(labels: list[dict]) -> str:
    if not labels:
        return ""
    cards = []
    for index, label in enumerate(labels, start=1):
        items = "".join(f'<li>{esc(item)}</li>' for item in label["items"])
        cards.append(
            f'''<section class="evidence-card" data-evidence-level="{esc(label["level"], attribute=True)}" aria-labelledby="evidence-{esc(label["level"], attribute=True)}-title"><div class="evidence-card__label"><span aria-hidden="true">{index:02d}</span><h3 id="evidence-{esc(label["level"], attribute=True)}-title">{esc(label["label"])}</h3></div><p>{esc(label["meaning"])}</p><ul>{items}</ul></section>'''
        )
    return f'''<section id="evidence-map" class="article-evidence-map" aria-labelledby="evidence-map-title"><p class="interface-label">How to read the evidence</p><h2 id="evidence-map-title">Evidence map</h2><div class="evidence-grid">{"".join(cards)}</div></section>'''


def article_evidence_summary_markup(summary: dict | None) -> str:
    if not summary:
        return ""
    groups = []
    for index, group in enumerate(summary["groups"], start=1):
        items = "".join(f'<li>{esc(item)}</li>' for item in group["items"])
        groups.append(
            f'''<section class="evidence-summary__group" data-evidence-level="{esc(group["level"], attribute=True)}"><p class="evidence-summary__label"><span aria-hidden="true">{index:02d}</span>{esc(group["label"])}</p><ul>{items}</ul></section>'''
        )
    return f'''<section id="what-we-know" class="article-evidence-summary" aria-labelledby="what-we-know-title"><p class="interface-label">Evidence in context</p><h2 id="what-we-know-title">{esc(summary["heading"])}</h2><div class="evidence-summary__grid">{"".join(groups)}</div><p class="evidence-summary__statement">{esc(summary["statement"])}</p></section>'''


def article_optional_action_markup(action: dict | None) -> str:
    if not action:
        return ""
    buttons = "".join(
        f'<a class="button {"button-primary" if index == 0 else "button-secondary"}" href="{esc(cta["href"], attribute=True)}">{esc(cta["label"])} →</a>'
        for index, cta in enumerate(action["ctas"])
    )
    return f'''<aside id="optional-action" class="article-action" aria-labelledby="optional-action-title" data-journey-choice="tools"><p class="interface-label">{esc(action["label"])}</p><h3 id="optional-action-title">{esc(action["heading"])}</h3><p>{esc(action["copy"])}</p><div class="button-row">{buttons}</div></aside>'''


def article_related_markup(article: dict, published_by_slug: dict[str, dict]) -> str:
    article_links: list[str] = []
    for slug in article.get("relatedArticles", []):
        related = published_by_slug.get(slug)
        if related:
            article_links.append(f'<li><a href="{esc(slug, attribute=True)}.html">{esc(related["title"])} →</a></li>')
    if not article_links:
        return ""
    heading = article.get("relatedReadingHeading", "Related reading")
    intro = f'<p class="article-journey__copy">{esc(article["relatedReadingIntro"])}</p>' if article.get("relatedReadingIntro") else ""
    return f'''<section class="article-related" data-journey-choice="learning"><p class="interface-label">Keep learning</p><h3>{esc(heading)}</h3>{intro}<ul>{"".join(article_links)}</ul></section>'''


def article_journey_markup(article: dict, published_by_slug: dict[str, dict]) -> str:
    related = article_related_markup(article, published_by_slug)
    orientation = '''<section class="article-orientation" data-journey-choice="orientation"><p class="interface-label">Understand your next step</p><h3>Return to the Matrix</h3><p class="article-journey__copy">Use Information → Education → Action to decide what—if anything—comes next.</p><a class="button button-tertiary" href="../start.html">Review the process →</a></section>'''
    optional = article_optional_action_markup(article.get("optionalAction"))
    choices = related + orientation + optional
    if not choices:
        return ""
    return f'''<section id="article-journey" class="article-journey" aria-labelledby="article-journey-title"><p class="interface-label">Where to go next</p><h2 id="article-journey-title">Choose the next useful step.</h2><p class="article-journey__intro">Keep learning, return to the process, or consider an optional tool only when it answers a clear question.</p><div class="article-journey__grid">{choices}</div></section>'''


def article_replacements(
    data: dict,
    library: dict,
    article: dict,
    *,
    preview: bool,
) -> dict[str, str]:
    metadata = data["site"]["metadata"]
    prefix = "../"
    title = article.get("seoTitle") or article["title"] + metadata["articleTitleSuffix"]
    description = article.get("seoDescription") or article.get("dek") or article["summary"]
    display_dek = article.get("dek") or article["summary"]
    canonical_path = None if preview else f'library/{article["slug"]}.html'
    category = category_name(library, article["category"])
    byline = [f'By {esc(article["author"])}', f'<span>{esc(article["readingTime"])}</span>']
    if article.get("reviewer"):
        byline.append(f'<span>Reviewed by {esc(article["reviewer"])}</span>')
    if article.get("published"):
        datetime = article.get("publishedIso") or article["published"]
        byline.append(f'<time datetime="{esc(datetime, attribute=True)}">Published {esc(article["published"])}</time>')
    if article.get("evidenceReviewed"):
        byline.append(f'<span>Evidence reviewed {esc(article["evidenceReviewed"])}</span>')
    if article.get("updated"):
        if article.get("updatedIso"):
            byline.append(f'<time datetime="{esc(article["updatedIso"], attribute=True)}">Updated {esc(article["updated"])}</time>')
        else:
            byline.append(f'<span>Updated {esc(article["updated"])}</span>')
    hero = article.get("hero")
    if hero and hero.get("src"):
        source = f'<source media="(max-width: 44rem)" srcset="../{esc(hero["srcSmall"], attribute=True)}" width="{int(hero["smallWidth"])}" height="{int(hero["smallHeight"])}">' if hero.get("srcSmall") else ""
        hero_markup = f'''<figure class="article-hero__media"><picture>{source}<img src="../{esc(hero["src"], attribute=True)}" alt="{esc(hero.get("alt", ""), attribute=True)}" width="{int(hero["width"])}" height="{int(hero["height"])}" decoding="async" fetchpriority="high"></picture></figure>'''
    else:
        hero_markup = '<div class="article-hero__placeholder" aria-hidden="true"><span></span><img src="../assets/brand/mark-gold.svg" width="64" height="64" alt=""></div>'
    takeaways = article_list_section("key-takeaways", "Key takeaways", article.get("keyTakeaways", []), "article-takeaways")
    published_by_slug = {item["slug"]: item for item in published_articles(library)}
    preview_banner = '<div class="preview-banner" role="status">Non-public article template preview · fixture content only · not for publication</div>' if preview else ""
    return {
        "{{DOCUMENT_HEAD}}": document_head_markup(
            metadata,
            prefix=prefix,
            title=title,
            description=description,
            path=canonical_path,
            page_type="article",
            image=hero,
            published=article.get("publishedIso"),
            updated=article.get("updatedIso"),
            noindex=preview,
            structured_data=[] if preview else [
                organization_schema(metadata),
                website_schema(metadata),
                article_schema(metadata, article, description, category),
                breadcrumb_schema(metadata, [
                    ("Home", ""),
                    ("The Library", "library.html"),
                    (article["title"], canonical_path),
                ]),
            ],
        ),
        "{{SHARED_HEADER}}": shared_header_markup(data, prefix=prefix, current="article"),
        "{{SHARED_FOOTER}}": shared_footer_markup(data, prefix=prefix),
        "{{PREVIEW_BANNER}}": preview_banner,
        "{{ARTICLE_CATEGORY}}": esc(category),
        "{{ARTICLE_TITLE}}": esc(article["title"]),
        "{{ARTICLE_DEK}}": esc(display_dek),
        "{{ARTICLE_BYLINE}}": " · ".join(byline),
        "{{ARTICLE_DISCLOSURE}}": f'<p class="article-disclosure" role="note">{esc(article["educationDisclosure"])}</p>' if article.get("educationDisclosure") else "",
        "{{ARTICLE_AFFILIATE_DISCLOSURE}}": "" if preview else f'<p class="article-affiliate-disclosure" role="note" data-affiliate-disclosure>{esc(data["site"]["affiliateDisclosure"])}</p>',
        "{{ARTICLE_HERO}}": hero_markup,
        "{{ARTICLE_TOC}}": article_toc_markup(article),
        "{{ARTICLE_TAKEAWAYS}}": takeaways,
        "{{ARTICLE_EVIDENCE_MAP}}": article_evidence_map_markup(article.get("evidenceLabels", [])),
        "{{ARTICLE_BODY}}": article_body_markup(article),
        "{{ARTICLE_EVIDENCE_SUMMARY}}": article_evidence_summary_markup(article.get("evidenceSummary")),
        "{{ARTICLE_EVIDENCE}}": article_list_section("evidence-notes", "Evidence notes", article.get("evidenceNotes", [])),
        "{{ARTICLE_LIMITATIONS}}": article_list_section("limitations", "Limitations", article.get("limitations", [])),
        "{{ARTICLE_SOURCES}}": article_sources_markup(article.get("sources", [])),
        "{{ARTICLE_JOURNEY}}": article_journey_markup(article, published_by_slug),
    }


def discovery_records(data: dict, library: dict, discovery: dict, sources: list[dict]) -> list[dict]:
    records=[]
    labels={item["product_id"]:item for item in data["productLabels"].get("records",[]) if item.get("status")=="approved"}
    departments={item["intentId"]:item for item in discovery["departments"]}
    for department in discovery["departments"]:
        product_count=sum(product.get("commercial_status")=="active" and product["intent"]==department["intentId"] for product in data["catalog"]["products"])
        guide_count=sum(article.get("status")=="published" and article["slug"] in department["articleSlugs"] for article in library["articles"])
        records.append({"id":department["intentId"],"type":"department","title":department["title"],"summary":department["description"],"href":f'departments/{department["slug"]}.html',"terms":[department["title"],department["description"]],"productCount":product_count,"guideCount":guide_count,"environment":next(item["environment"] for item in data["catalog"]["intents"] if item["id"]==department["intentId"])})
    for index,product in enumerate(active_products(data["catalog"])):
        ingredients=[item["ingredient"] for item in labels.get(product["id"],{}).get("ingredients",[])]
        cutout=product.get("cutout") or product.get("image") or {}
        records.append({"id":product["id"],"type":"product","title":product["name"],"summary":product["description"],"href":f'explore.html?product={product["id"]}&mode=products',"manufacturer":product["manufacturer"],"intent":product["intent"],"department":departments[product["intent"]]["title"],"category":product["category"],"productKind":product["productKind"],"variant":product["variantLabel"],"ingredients":ingredients,"image":{"src":cutout.get("src"),"alt":cutout.get("alt",product["name"])},"order":index})
    for article in published_articles(library):
        related=[d["intentId"] for d in discovery["departments"] if article["slug"] in d["articleSlugs"]]
        hero=article.get("hero") or {}
        records.append({"id":article["slug"],"type":"guide","title":article["title"],"summary":article["summary"],"href":f'library/{article["slug"]}.html',"category":category_name(library,article["category"]),"intents":related,"image":{"src":hero.get("srcSmall") or hero.get("src"),"alt":hero.get("alt","")},"evidenceReviewed":article.get("evidenceReviewed")})
    for journey in discovery["journeys"]:
        records.append({"id":journey["id"],"type":"journey","title":journey["title"],"summary":journey["summary"],"href":journey["href"],"keywords":journey["keywords"]})
    for source in sources:
        records.append({
            "id": source["id"], "type": "source", "title": source["title"],
            "summary": source["public_summary"], "href": f'evidence.html?source={source["id"]}',
            "publisher": source["publisher"], "resourceType": source_type_label(source["resource_type"]),
            "evidenceRole": source["evidence_role"], "topics": source.get("topic_ids", []),
            "manufacturer": source.get("manufacturer") or "Independent public source",
            "intents": source.get("department_ids", []), "products": source.get("product_ids", []),
            "independence": source["independence_status"], "checkedDate": source["checked_date"],
        })
    return records


def universal_search_markup(records: list[dict], *, prefix: str = "") -> str:
    payload=json.dumps(records,ensure_ascii=False,separators=(",", ":")).replace("</","<\\/")
    return f'''<div class="matrix-search" data-matrix-search data-prefix="{prefix}"><form role="search" action="{prefix}explore.html" data-search-form><label for="universal-search">Search products, guides, testing journeys, and public sources</label><div><input id="universal-search" name="q" type="search" autocomplete="off" placeholder="Search products, guides, ingredients, sources…" data-search-input><button type="submit">Search</button></div></form><div class="search-modes" role="group" aria-label="Search result type"><button type="button" data-search-mode="everything" aria-pressed="true">Everything</button><button type="button" data-search-mode="products" aria-pressed="false">Products</button><button type="button" data-search-mode="learn" aria-pressed="false">Learn</button></div><p class="search-status" data-search-status aria-live="polite">Enter a term or browse the departments below.</p><div class="search-results" data-search-results hidden></div><button class="search-clear" type="button" data-search-clear hidden>Clear search</button><script type="application/json" data-search-index>{payload}</script></div>'''


def evidence_controls_markup(sources: list[dict], data: dict, discovery: dict) -> str:
    product_names = {product["id"]: product["name"] for product in active_products(data["catalog"])}
    department_names = {item["intentId"]: item["title"] for item in discovery["departments"]}
    values = {
        "topic": {item: item.replace("-", " ").title() for source in sources for item in source.get("topic_ids", [])},
        "type": {item: source_type_label(item) for item in {source["resource_type"] for source in sources}},
        "manufacturer": {"independent": "Independent public source", **{source["manufacturer"]: source["manufacturer"] for source in sources if source.get("manufacturer")}},
        "product": {item: product_names.get(item, item.replace("-", " ").title()) for source in sources for item in source.get("product_ids", [])},
        "department": {item: department_names.get(item, item.replace("-", " ").title()) for source in sources for item in source.get("department_ids", [])},
        "independence": {item: item.replace("_", " ").title() for item in {source["independence_status"] for source in sources}},
    }
    labels = {"topic": "Topic", "type": "Resource type", "manufacturer": "Source relationship", "product": "Related product", "department": "Department", "independence": "Independence"}
    selects = []
    for field in ("topic", "type", "manufacturer", "product", "department", "independence"):
        options = "".join(f'<option value="{esc(value, attribute=True)}">{esc(label)}</option>' for value, label in sorted(values[field].items(), key=lambda item: item[1]))
        selects.append(f'<label>{labels[field]}<select data-evidence-filter="{field}"><option value="all">All {labels[field].lower()}s</option>{options}</select></label>')
    return f'''<form class="evidence-controls" role="search" data-evidence-controls><label class="evidence-controls__search">Search sources<input type="search" autocomplete="off" placeholder="Search title, publisher, topic, scope…" data-evidence-search></label><div class="evidence-controls__filters">{"".join(selects)}</div><button class="button button-secondary" type="reset" data-evidence-reset hidden>Clear filters</button></form>'''


def matrix_visual_markup(*, intensity: str = "medium", environment: str = "matrix") -> str:
    return f'''<div class="matrix-visual matrix-visual--{esc(intensity,attribute=True)}" data-matrix-visual data-environment="{esc(environment,attribute=True)}" aria-hidden="true"><span class="matrix-visual__field"></span><span class="matrix-visual__cell matrix-visual__cell--a"></span><span class="matrix-visual__cell matrix-visual__cell--b"></span><svg class="matrix-visual__path" viewBox="0 0 1200 420" preserveAspectRatio="none"><path d="M-40 315 C170 120 330 370 520 195 S850 70 1240 235"/><path d="M-20 85 C230 280 400 42 650 215 S980 355 1230 92"/><circle cx="520" cy="195" r="5"/><circle cx="850" cy="118" r="4"/><circle cx="1030" cy="272" r="5"/></svg><span class="matrix-visual__scan"></span><span class="matrix-visual__caption">BIOLOGICAL SIGNAL / DECORATIVE FIELD</span></div>'''


def catalog_commercial_disclosures(site: dict, products: list[dict]) -> str:
    paragraphs = []
    if any(product["manufacturer"] == "Zinzino" for product in products):
        paragraphs.append(f'<p class="fine" data-affiliate-disclosure>{esc(site["affiliateDisclosure"])}</p>')
    if any(product["manufacturer"] == "BioLimitless" for product in products):
        paragraphs.append(f'<p class="fine" data-biolimitless-disclosure>{esc(site["biolimitlessAffiliateDisclosure"])}</p>')
    return '<div id="shop-affiliate-disclosure" class="commercial-notes" role="note" aria-label="Commercial relationship disclosures">' + "".join(paragraphs) + "</div>"


def compact_product_card(product: dict, *, prefix: str = "", index: int = 1) -> str:
    image=product.get("cutout") or product.get("image"); related=product.get("relatedEducation")
    learn=f'<a href="{prefix}{esc(related["href"],attribute=True)}">{esc(related["label"])} →</a>' if related else ""
    return f'''<article class="discovery-product scan-frame" data-discovery-product data-id="{esc(product["id"],attribute=True)}" data-manufacturer="{esc(product["manufacturer"],attribute=True)}" data-intent="{esc(product["intent"],attribute=True)}" data-environment="{esc(product["environment"],attribute=True)}" data-category="{esc(product["productKind"],attribute=True)}" data-name="{esc(product["name"].lower(),attribute=True)}" data-order="{index}"><div class="discovery-product__stage"><span class="signal-node" aria-hidden="true"></span><img src="{prefix}{esc(image["src"],attribute=True)}" width="{int(image["width"])}" height="{int(image["height"])}" alt="{esc(image["alt"],attribute=True)}" loading="lazy" decoding="async"></div><div><p class="interface-label">{esc(product["manufacturer"])} / {esc(product["category"])}</p><h3>{esc(product["name"])}</h3>{price_markup(product,context="compact")}<div class="discovery-product__links"><a class="button button-primary" href="{esc(product["destination"],attribute=True)}" target="_blank" rel="sponsored noopener noreferrer" aria-label="Official product source for {esc(product["name"],attribute=True)} (opens in a new tab)">Official source ↗{external_note()}</a>{learn}</div></div></article>'''


def department_cards(data: dict, library: dict, discovery: dict, sources: list[dict], *, prefix: str = "") -> str:
    products=active_products(data["catalog"]); published={item["slug"] for item in published_articles(library)}; cards=[]
    for position,item in enumerate(discovery["departments"],start=1):
        product_count=sum(product["intent"]==item["intentId"] for product in products); guide_count=sum(slug in published for slug in item["articleSlugs"]); source_count=sum(item["intentId"] in source.get("department_ids",[]) for source in sources)
        environment=next(intent["environment"] for intent in data["catalog"]["intents"] if intent["id"]==item["intentId"])
        cards.append(f'''<a class="department-card department-signature" data-environment="{esc(environment,attribute=True)}" href="{prefix}departments/{item["slug"]}.html"><span class="department-card__number" aria-hidden="true">{position:02d}</span><span class="department-card__biome" aria-hidden="true"><i></i><i></i><i></i></span><p class="interface-label">{esc(item["title"])}</p><strong>{product_count} products · {guide_count} guides · {source_count} sources</strong><span>{esc(item["description"])}</span><b>Explore department →</b></a>''')
    return "".join(cards)


def explore_catalog_markup(products: list[dict], catalog: dict) -> str:
    manufacturers=sorted({p["manufacturer"] for p in products}); kinds=sorted({p["productKind"] for p in products})
    controls=f'''<div class="explore-toolbar" data-explore-toolbar><label>Manufacturer<select data-filter="manufacturer"><option value="all">All manufacturers</option>{''.join(f'<option>{esc(x)}</option>' for x in manufacturers)}</select></label><label>Department<select data-filter="intent"><option value="all">All departments</option>{''.join(f'<option value="{esc(x["id"],attribute=True)}">{esc(x["name"])}</option>' for x in catalog["intents"])}</select></label><label>Product kind<select data-filter="category"><option value="all">All kinds</option>{''.join(f'<option>{esc(x)}</option>' for x in kinds)}</select></label><label>Sort<select data-filter="sort"><option value="canonical">Featured / canonical</option><option value="name">Name A–Z</option><option value="manufacturer-sort">Manufacturer</option></select></label><p data-explore-count aria-live="polite">Showing 12 of {len(products)}</p><div data-filter-chips></div><button type="button" data-filter-reset hidden>Clear all</button></div>'''
    cards="".join(compact_product_card(product,index=index) for index,product in enumerate(products,start=1))
    return controls+f'<div class="discovery-card-grid" data-explore-grid>{cards}</div><p data-explore-empty hidden>No products match these filters.</p><button class="button button-secondary load-more" type="button" data-load-more>Load more products</button><noscript><p><a href="shop.html">Browse the complete Products page.</a></p></noscript>'


def build_home(data: dict, library: dict, discovery: dict, sources: list[dict]) -> None:
    catalog = data["catalog"]
    public_products = active_products(catalog)
    products = curated_products(catalog)
    products_by_id = {product["id"]: product for product in public_products}
    featured = products_by_id[data["featuredProductId"]]
    site = data["site"]
    metadata = site["metadata"]
    brand = data["brand"]
    home = data["homepage"]
    page = metadata["pages"]["home"]
    replacements = {
        "{{DOCUMENT_HEAD}}": document_head_markup(
            metadata,
            prefix="",
            title=page["title"],
            description=site["description"],
            path=page["path"],
            structured_data=[organization_schema(metadata), website_schema(metadata)],
        ),
        "{{SHARED_HEADER}}": shared_header_markup(data, prefix="", current="home"),
        "{{SHARED_FOOTER}}": shared_footer_markup(data, prefix=""),
        "{{PHILOSOPHY}}": esc(brand["philosophy"]),
        "{{HERO_HEADLINE}}": line_markup(home["hero"]["headline"]),
        "{{HERO_SUPPORT}}": esc(home["hero"]["supportingLine"]),
        "{{HERO_COPY}}": esc(home["hero"]["copy"]),
        "{{HERO_ACTIONS}}": hero_actions_markup(featured, len(public_products), site["affiliateSourceDisclosure"]),
        "{{HERO_PRODUCT}}": hero_product_markup(featured),
        "{{HERO_MATRIX_VISUAL}}": matrix_visual_markup(intensity="high", environment="balance"),
        "{{UNIVERSAL_SEARCH}}": universal_search_markup(discovery_records(data, library, discovery, sources)),
        "{{DEPARTMENT_CARDS}}": department_cards(data, library, discovery, sources),
        "{{PROBLEM_HEADLINE}}": line_markup(home["problem"]["headline"]),
        "{{PROBLEM_COPY}}": esc(home["problem"]["copy"]),
        "{{PROBLEM_THEMES}}": "".join(f"<li>{esc(theme)}</li>" for theme in home["problem"]["themes"]),
        "{{PROBLEM_CONCLUSION}}": esc(home["problem"]["conclusion"]),
        "{{MATRIX_HEADING}}": esc(home["matrix"]["heading"]),
        "{{MATRIX_INTRO}}": esc(home["matrix"]["introduction"]),
        "{{MATRIX_STAGES}}": "\n        ".join(matrix_stage_markup(stage) for stage in home["matrix"]["stages"]),
        "{{MATRIX_CONCLUSION}}": esc(home["matrix"]["conclusion"]),
        "{{MATRIX_CONCLUSION_COPY}}": esc(home["matrix"]["conclusionCopy"]),
        "{{CHOOSE_HEADING}}": esc(home["choosePath"]["heading"]),
        "{{PATH_CARDS}}": "\n        ".join(path_card_markup(path) for path in home["choosePath"]["paths"]),
        "{{FOUNDER_LABEL}}": esc(home["founder"]["label"]),
        "{{FOUNDER_HEADING}}": esc(home["founder"]["heading"]),
        "{{FOUNDER_PARAGRAPHS}}": "".join(f"<p>{esc(paragraph)}</p>" for paragraph in home["founder"]["paragraphs"]),
        "{{FOUNDER_STATEMENT}}": esc(home["founder"]["statement"]),
        "{{FOUNDER_PHILOSOPHY}}": esc(home["founder"]["philosophy"]),
        "{{FOUNDER_CONTEXT}}": esc(home["founder"]["philosophyContext"]),
        "{{FOUNDER_TRANSITION}}": esc(home["founder"]["transition"]),
        "{{TESTING_LABEL}}": esc(home["testing"]["label"]),
        "{{TESTING_HEADING}}": esc(home["testing"]["heading"]),
        "{{TESTING_COPY}}": esc(home["testing"]["copy"]),
        "{{TESTING_WORKFLOW}}": testing_workflow_markup(),
        "{{TESTING_EDUCATION}}": testing_education_markup(home["testing"]),
        "{{TESTING_PRODUCT}}": testing_product_markup(featured, home["testing"]),
        "{{LIBRARY_LABEL}}": esc(home["library"]["label"]),
        "{{LIBRARY_HEADING}}": esc(home["library"]["heading"]),
        "{{LIBRARY_COPY}}": esc(home["library"]["copy"]),
        "{{LIBRARY_BODY}}": library_body_markup(library, home["library"]),
        "{{LIBRARY_COUNT}}": f'{len(published_articles(library)):02d} published guides',
        "{{LIBRARY_TRANSITION}}": esc(home["library"]["transition"]),
        "{{SHELF_LABEL}}": esc(home["shelf"]["label"]),
        "{{SHELF_HEADING}}": esc(home["shelf"]["heading"]),
        "{{SHELF_COPY}}": esc(home["shelf"]["copy"]),
        "{{AFFILIATE_DISCLOSURE}}": esc(site["affiliateDisclosure"]),
        "{{BIOLIMITLESS_AFFILIATE_DISCLOSURE}}": esc(site["biolimitlessAffiliateDisclosure"]),
        "{{PRICING_DISCLOSURE}}": esc(site["pricingDisclosure"]),
        "{{SHELF_COUNT}}": f'{len(products):02d} curated products',
        "{{PRODUCT_COUNT}}": str(len(public_products)),
        "{{DISCOVERY_INTENTS}}": "".join(f'<option value="{esc(item["id"], attribute=True)}">{esc(item["name"])}</option>' for item in catalog["intents"]),
        "{{DISCOVERY_CATEGORIES}}": "".join(f'<option value="{esc(item, attribute=True)}">{esc(item)}</option>' for item in sorted({product["category"] for product in public_products})),
        "{{UNIVERSE_INTENTS}}": universe_intents_markup(catalog),
        "{{UNIVERSE_PRODUCTS}}": universe_product_markup(featured, index=products.index(featured) + 1, active=True),
        "{{UNIVERSE_DATA}}": universe_data_markup(products),
        "{{UNIVERSE_ROSTER}}": universe_roster_markup(products, data["featuredProductId"]),
        "{{STANDARDS_HEADING}}": esc(home["standards"]["heading"]),
        "{{STANDARDS_LIST}}": "\n        ".join(standard_markup(item, interactive=True, active=index == 0) for index, item in enumerate(home["standards"]["principles"])),
        "{{STANDARDS_STATEMENT}}": line_markup(home["standards"]["statement"]),
        "{{TRANSPARENCY_HEADING}}": esc(home["transparency"]["heading"]),
        "{{TRANSPARENCY_COPY}}": esc(home["transparency"]["copy"]),
        "{{DISCLOSURE}}": esc(site["disclosure"]),
        "{{FINAL_HEADLINE}}": line_markup(home["finalCta"]["headline"]),
        "{{FINAL_RESPONSE}}": line_markup(home["finalCta"]["response"]),
        "{{FINAL_PHILOSOPHY}}": esc(home["finalCta"]["philosophy"]),
    }
    write_output(ROOT / "index.html", render_template("index.html", replacements))


def build_explore(data: dict, library: dict, discovery: dict, sources: list[dict]) -> None:
    metadata=data["site"]["metadata"]; products=active_products(data["catalog"]); path="explore.html"
    records=discovery_records(data,library,discovery,sources)
    replacements={"{{DOCUMENT_HEAD}}":document_head_markup(metadata,prefix="",title="Explore Products and Education | The Mindful Matrix",description="Search verified products, testing tools, Library guides, public references, and education journeys in one place.",path=path,structured_data=[organization_schema(metadata),website_schema(metadata),breadcrumb_schema(metadata,[("Home",""),("Explore",path)])]),"{{SHARED_HEADER}}":shared_header_markup(data,prefix="",current="explore"),"{{SHARED_FOOTER}}":shared_footer_markup(data,prefix=""),"{{EXPLORE_MATRIX_VISUAL}}":matrix_visual_markup(intensity="high",environment="discovery"),"{{WORKSPACE_MATRIX_VISUAL}}":matrix_visual_markup(intensity="medium",environment="evidence"),"{{SEARCH}}":universal_search_markup(records),"{{DEPARTMENTS}}":department_cards(data,library,discovery,sources),"{{COMMERCIAL_DISCLOSURES}}":catalog_commercial_disclosures(data["site"],products),"{{CATALOG}}":explore_catalog_markup(products,data["catalog"])}
    write_output(ROOT/path,render_template("explore.html",replacements))
    write_output(ROOT/"assets"/"data"/"search-index.json",json.dumps(records,ensure_ascii=False,indent=2)+"\n")


def build_departments(data: dict, library: dict, discovery: dict, sources: list[dict]) -> None:
    metadata=data["site"]["metadata"]; products=active_products(data["catalog"]); articles={item["slug"]:item for item in published_articles(library)}; journeys={item["id"]:item for item in discovery["journeys"]}; expected=set()
    for position,department in enumerate(discovery["departments"],start=1):
        path=f'departments/{department["slug"]}.html'; expected.add(ROOT/path); matches=[p for p in products if p["intent"]==department["intentId"]]; guides=[articles[s] for s in department["articleSlugs"] if s in articles]; department_sources=[source for source in sources if department["intentId"] in source.get("department_ids",[])]
        guides_markup="".join(f'<article class="learn-card"><p class="interface-label">Guide</p><h3>{esc(a["title"])}</h3><p>{esc(a["summary"])}</p><a href="../library/{esc(a["slug"],attribute=True)}.html">Read the evidence →</a></article>' for a in guides)
        journey_markup="".join(f'<article class="journey-callout"><p class="interface-label">Testing journey</p><h3>{esc(journeys[j]["title"])}</h3><p>{esc(journeys[j]["summary"])}</p><a href="../{esc(journeys[j]["href"],attribute=True)}">Open journey →</a></article>' for j in department["journeys"] if j in journeys)
        environment=next(intent["environment"] for intent in data["catalog"]["intents"] if intent["id"]==department["intentId"])
        replacements={"{{DOCUMENT_HEAD}}":document_head_markup(metadata,prefix="../",title=f'{department["title"]} | The Mindful Matrix',description=department["description"],path=path,structured_data=[organization_schema(metadata),website_schema(metadata),breadcrumb_schema(metadata,[("Home",""),("Explore","explore.html"),(department["title"],path)])]),"{{SHARED_HEADER}}":shared_header_markup(data,prefix="../",current="department"),"{{SHARED_FOOTER}}":shared_footer_markup(data,prefix="../"),"{{DEPARTMENT_MATRIX_VISUAL}}":matrix_visual_markup(intensity="high",environment=environment),"{{DEPARTMENT_ENVIRONMENT}}":esc(environment,attribute=True),"{{DEPARTMENT_INDEX}}":f'{position:02d}',"{{DEPARTMENT_ID}}":esc(department["intentId"],attribute=True),"{{DEPARTMENT_TITLE}}":esc(department["title"]),"{{DEPARTMENT_DESCRIPTION}}":esc(department["description"]),"{{PRODUCT_COUNT}}":str(len(matches)),"{{GUIDE_COUNT}}":str(len(guides)),"{{SOURCE_COUNT}}":str(len(department_sources)),"{{COMMERCIAL_DISCLOSURES}}":catalog_commercial_disclosures(data["site"],matches),"{{PRODUCTS}}":"".join(compact_product_card(p,prefix="../",index=i) for i,p in enumerate(matches,start=1)),"{{GUIDES}}":guides_markup,"{{JOURNEYS}}":journey_markup,"{{SOURCES}}":'<div class="source-card-grid">'+"".join(source_card_markup(source,prefix="../",compact=True) for source in department_sources)+'</div>',"{{DISCLOSURE}}":esc(data["site"]["disclosure"])}
        write_output(ROOT/path,render_template("department.html",replacements))
    directory=ROOT/"departments"
    if directory.exists():
        for path in directory.glob("*.html"):
            if path not in expected and GENERATOR_MARKER in path.read_text(encoding="utf-8"): path.unlink()


def build_library(data: dict, library: dict, sources: list[dict]) -> None:
    metadata = data["site"]["metadata"]
    page = metadata["pages"]["library"]
    counts = {category["id"]: 0 for category in library["categories"]}
    for article in published_articles(library):
        counts[article["category"]] += 1
    replacements = {
        "{{DOCUMENT_HEAD}}": document_head_markup(
            metadata,
            prefix="",
            title=page["title"],
            description=page["description"],
            path=page["path"],
            structured_data=[
                organization_schema(metadata),
                website_schema(metadata),
                breadcrumb_schema(metadata, [("Home", ""), ("The Library", page["path"])]),
            ],
        ),
        "{{SHARED_HEADER}}": shared_header_markup(data, prefix="", current="library"),
        "{{SHARED_FOOTER}}": shared_footer_markup(data, prefix=""),
        "{{LIBRARY_CATEGORIES}}": "".join(library_category_markup(category, counts[category["id"]]) for category in library["categories"]),
        "{{EVIDENCE_PATHWAY}}": f'''<section class="library-evidence-pathway section-dark section-pad" aria-labelledby="library-evidence-title"><div class="container library-evidence-pathway__grid"><div><p class="section-kicker">Evidence &amp; documentation</p><h2 id="library-evidence-title">Inspect {len(sources)} public sources.</h2><p>Browse independent references with visible publishers, scope, limitations, checked dates, and original public links.</p></div><a class="button button-primary" href="evidence.html">Open the source index →</a></div></section>''',
        "{{LIBRARY_INDEX}}": library_index_markup(library, data["homepage"]),
        "{{EDITORIAL_PRINCIPLES}}": editorial_principles_markup(data, library),
    }
    write_output(ROOT / "library.html", render_template("library.html", replacements))


def build_evidence(data: dict, discovery: dict, manifest: dict, sources: list[dict]) -> None:
    metadata = data["site"]["metadata"]
    page = metadata["pages"]["evidence"]
    replacements = {
        "{{DOCUMENT_HEAD}}": document_head_markup(metadata,prefix="",title=page["title"],description=page["description"],path=page["path"],structured_data=[organization_schema(metadata),website_schema(metadata),breadcrumb_schema(metadata,[("Home",""),("The Library","library.html"),("Evidence & Documentation",page["path"])]),evidence_collection_schema(metadata,sources)]),
        "{{SHARED_HEADER}}": shared_header_markup(data,prefix="",current="library"),
        "{{SHARED_FOOTER}}": shared_footer_markup(data,prefix=""),
        "{{EVIDENCE_MATRIX_VISUAL}}": matrix_visual_markup(intensity="high",environment="evidence"),
        "{{SOURCE_COUNT}}": str(len(sources)),
        "{{CHECKED_DATE}}": esc(manifest["checked_date"]),
        "{{EVIDENCE_CONTROLS}}": evidence_controls_markup(sources,data,discovery),
        "{{SOURCE_CARDS}}": "".join(source_card_markup(source) for source in sources),
    }
    write_output(ROOT / "evidence.html",render_template("evidence.html",replacements))


def build_start(data: dict) -> None:
    metadata = data["site"]["metadata"]
    page = metadata["pages"]["start"]
    start = data["homepage"]["startHere"]
    pathways = start["pathways"]
    replacements = {
        "{{DOCUMENT_HEAD}}": document_head_markup(
            metadata,
            prefix="",
            title=page["title"],
            description=page["description"],
            path=page["path"],
            structured_data=[
                organization_schema(metadata),
                website_schema(metadata),
                breadcrumb_schema(metadata, [("Home", ""), ("Start Here", page["path"])]),
            ],
        ),
        "{{SHARED_HEADER}}": shared_header_markup(data, prefix="", current="start"),
        "{{SHARED_FOOTER}}": shared_footer_markup(data, prefix=""),
        "{{START_HERO_COPY}}": esc(start["heroCopy"]),
        "{{START_HEADING}}": esc(start["heading"]),
        "{{START_COPY}}": esc(start["copy"]),
        "{{ORIENTATION_STAGES}}": "".join(orientation_stage_markup(stage) for stage in start["stages"]),
        "{{START_NOTE}}": esc(start["note"]),
        "{{PATHWAYS_LABEL}}": esc(pathways["label"]),
        "{{PATHWAYS_HEADING}}": esc(pathways["heading"]),
        "{{PATHWAYS_COPY}}": esc(pathways["copy"]),
        "{{START_PATHWAYS}}": "".join(start_pathway_markup(pathway) for pathway in pathways["items"]),
    }
    write_output(ROOT / "start.html", render_template("start.html", replacements))


def build_shop(data: dict, product_labels: dict, sources: list[dict]) -> None:
    metadata=data["site"]["metadata"]; page=metadata["pages"]["shop"]; catalog=data["catalog"]; products=active_products(catalog)
    label_records={record["product_id"]:record for record in product_labels.get("records",[])}
    replacements={
        "{{DOCUMENT_HEAD}}": document_head_markup(metadata,prefix="",title=page["title"],description=page["description"],path=page["path"],structured_data=[organization_schema(metadata),website_schema(metadata),breadcrumb_schema(metadata,[("Home",""),("Product Universe",page["path"])]),shop_collection_schema(metadata,products)]),
        "{{SHARED_HEADER}}": shared_header_markup(data,prefix="",current="shop"), "{{SHARED_FOOTER}}": shared_footer_markup(data,prefix=""),
        "{{SHOP_COUNT}}":str(len(products)), "{{VERIFIED_DATE}}":esc(catalog["verifiedDate"]),
        "{{SHOP_INTENT_RAIL}}":shop_intent_rail_markup(catalog["intents"],products),
        "{{SHOP_FILTER_INTENTS}}":shop_filter_intents_markup(catalog["intents"]),
        "{{SHOP_FILTER_MANUFACTURERS}}":shop_filter_manufacturers_markup(products),
        "{{SHOP_FILTER_KINDS}}":shop_filter_kinds_markup(products),
        "{{SHOP_INITIAL_CARDS}}":shop_initial_cards_markup(products),
        "{{SHOP_CATALOG_DATA}}":shop_catalog_data_markup(data,products,label_records,sources),
        "{{SHOP_NO_SCRIPT}}":shop_no_script_markup(products,data),
        "{{SHOP_FALLBACKS}}":shop_fallbacks_markup(catalog["fallbackDestinations"]),
        "{{AFFILIATE_DISCLOSURE}}":esc(data["site"]["affiliateDisclosure"]), "{{BIOLIMITLESS_AFFILIATE_DISCLOSURE}}":esc(data["site"]["biolimitlessAffiliateDisclosure"]),
        "{{PRICING_DISCLOSURE}}":esc(data["site"]["pricingDisclosure"]), "{{FDA_DISCLAIMER}}":esc(data["site"]["fdaDisclaimer"]), "{{DISCLOSURE}}":esc(data["site"]["disclosure"]),
    }
    write_output(ROOT / "shop.html", render_template("shop.html", replacements))


def build_know_your_number(data: dict) -> None:
    metadata=data["site"]["metadata"]; page=metadata["pages"]["knowYourNumber"]
    product=next(item for item in active_products(data["catalog"]) if item["id"]==data["featuredProductId"])
    replacements={"{{DOCUMENT_HEAD}}":document_head_markup(metadata,prefix="",title=page["title"],description=page["description"],path=page["path"],structured_data=[organization_schema(metadata),website_schema(metadata),breadcrumb_schema(metadata,[("Home",""),("Know Your Number",page["path"])])]),"{{SHARED_HEADER}}":shared_header_markup(data,prefix="",current="know-your-number"),"{{SHARED_FOOTER}}":shared_footer_markup(data,prefix=""),"{{KYN_MATRIX_VISUAL}}":matrix_visual_markup(intensity="high",environment="signal"),"{{PRODUCT_SOURCE}}":esc(product["destination"],attribute=True),"{{PRODUCT_NAME}}":esc(product["name"]),"{{AFFILIATE_DISCLOSURE}}":esc(data["site"]["affiliateDisclosure"])}
    write_output(ROOT / "know-your-number.html",render_template("know-your-number.html",replacements))


def clean_generated_articles(expected: set[Path]) -> None:
    article_dir = ROOT / "library"
    if not article_dir.exists():
        return
    for path in article_dir.glob("*.html"):
        if path in expected:
            continue
        if GENERATOR_MARKER in path.read_text(encoding="utf-8"):
            path.unlink()


def build_articles(data: dict, library: dict) -> None:
    expected: set[Path] = set()
    for article in published_articles(library):
        path = ROOT / "library" / f'{article["slug"]}.html'
        expected.add(path)
        write_output(path, render_template("article.html", article_replacements(data, library, article, preview=False)))
    clean_generated_articles(expected)


def build_crawl_files(data: dict, library: dict, discovery: dict) -> None:
    metadata = data["site"]["metadata"]
    paths = ["", "start.html", "library.html", "evidence.html", "shop.html", "know-your-number.html", "explore.html"]
    paths.extend(f'departments/{item["slug"]}.html' for item in discovery["departments"])
    paths.extend(f'library/{article["slug"]}.html' for article in published_articles(library))
    urls = "\n".join(f"  <url><loc>{esc(page_url(metadata, path))}</loc></url>" for path in paths)
    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
'''
    write_output(ROOT / "sitemap.xml", sitemap)
    robots = f'''User-agent: *
Allow: /

Sitemap: {page_url(metadata, "sitemap.xml")}
'''
    write_output(ROOT / "robots.txt", robots)


def build_preview(data: dict, library: dict, fixture_path: Path, output_path: Path) -> None:
    fixture = load_json(fixture_path)
    article = fixture.get("article", fixture)
    resolved_output = output_path.resolve()
    if ROOT.resolve() not in resolved_output.parents:
        raise ValueError("Preview output must stay inside the repository checkout")
    write_output(resolved_output, render_template("article.html", article_replacements(data, library, article, preview=True)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-article", type=Path, help="Render a non-public article fixture after the public build")
    parser.add_argument("--preview-output", type=Path, default=ROOT / "_preview" / "article-preview.html", help="Preview output path inside the checkout")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = load_json(ROOT / "content" / "site.json")
    library = load_json(ROOT / "content" / "library.json")
    catalog = load_json(ROOT / "content" / "catalog.json")
    product_labels = load_json(ROOT / "content" / "product-labels.json")
    manufacturer_documents = load_json(ROOT / "content" / "manufacturer-documents.json")
    discovery = load_json(ROOT / "content" / "discovery.json")
    public_source_manifest = load_json(ROOT / "content" / "resources" / "public-sources.json")
    sources = published_sources(public_source_manifest)
    data["catalog"] = catalog
    data["productLabels"] = product_labels
    data["manufacturerDocuments"] = manufacturer_documents
    data["affiliate"] = catalog["affiliate"]
    data["products"] = catalog["products"]
    data["featuredProductId"] = catalog["featuredProductId"]
    build_home(data, library, discovery, sources)
    build_explore(data, library, discovery, sources)
    build_departments(data, library, discovery, sources)
    build_library(data, library, sources)
    build_evidence(data, discovery, public_source_manifest, sources)
    build_start(data)
    build_shop(data, product_labels, sources)
    build_know_your_number(data)
    build_articles(data, library)
    build_crawl_files(data, library, discovery)
    if args.preview_article:
        build_preview(data, library, args.preview_article.resolve(), args.preview_output)


if __name__ == "__main__":
    main()
