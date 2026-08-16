#!/usr/bin/env python3
"""Build The Mindful Matrix dependency-free static site from centralized content."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from urllib.parse import urljoin

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
    if "{{" in output or "}}" in output:
        unresolved = sorted({part.split("}}", 1)[0] for part in output.split("{{")[1:]})
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
) -> str:
    canonical = page_url(metadata, path) if path is not None else ""
    tags = [
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        f"  <title>{esc(title)}</title>",
        f'  <meta name="description" content="{esc(description, attribute=True)}">',
        f"  {GENERATOR_MARKER}",
    ]
    if noindex:
        tags.append('  <meta name="robots" content="noindex, nofollow">')
    if canonical:
        tags.append(f'  <link rel="canonical" href="{esc(canonical, attribute=True)}">')
    tags.extend(
        [
            f'  <meta property="og:title" content="{esc(title, attribute=True)}">',
            f'  <meta property="og:description" content="{esc(description, attribute=True)}">',
            f'  <meta property="og:type" content="{esc(page_type, attribute=True)}">',
        ]
    )
    if canonical:
        tags.append(f'  <meta property="og:url" content="{esc(canonical, attribute=True)}">')
    if image and image.get("src"):
        image_url = page_url(metadata, image["src"])
        tags.append(f'  <meta property="og:image" content="{esc(image_url, attribute=True)}">')
        if image.get("alt"):
            tags.append(f'  <meta property="og:image:alt" content="{esc(image["alt"], attribute=True)}">')
    if page_type == "article":
        if published:
            tags.append(f'  <meta property="article:published_time" content="{esc(published, attribute=True)}">')
        if updated:
            tags.append(f'  <meta property="article:modified_time" content="{esc(updated, attribute=True)}">')
    tags.extend(
        [
            '  <meta name="theme-color" content="#151814">',
            f'  <link rel="icon" href="{prefix}assets/brand/favicon.svg" type="image/svg+xml">',
            '  <link rel="preconnect" href="https://fonts.googleapis.com">',
            '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
            '  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400..600&family=JetBrains+Mono:wght@500&family=Manrope:wght@500..800&display=swap" rel="stylesheet">',
            f'  <link rel="stylesheet" href="{prefix}assets/css/tokens.css">',
            f'  <link rel="stylesheet" href="{prefix}assets/css/base.css">',
            f'  <link rel="stylesheet" href="{prefix}assets/css/site.css">',
            f'  <script defer src="{prefix}assets/js/enhancements.js"></script>',
        ]
    )
    return "\n".join(tags)


def shared_header_markup(*, prefix: str, current: str) -> str:
    home = f"{prefix}index.html"
    start_current = ' aria-current="page"' if current == "start" else ""
    library_current = ' aria-current="page"' if current in {"library", "article"} else ""
    return f'''<header class="site-header section-dark">
    <nav class="nav-shell container-wide" aria-label="Primary navigation">
      <a class="brand-link" href="{home}" aria-label="The Mindful Matrix home"><img src="{prefix}assets/brand/lockup-dark.svg" width="430" height="72" alt="The Mindful Matrix"></a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-links"><span class="visually-hidden">Open navigation</span><span class="nav-toggle__lines" aria-hidden="true"></span></button>
      <ul id="primary-links" class="nav-links">
        <li><a href="{prefix}start.html"{start_current}>Start here</a></li>
        <li><a href="{prefix}library.html"{library_current}>The Library</a></li>
        <li><a href="{home}#shelf">The Shelf</a></li>
        <li><a href="{home}#story">Our story</a></li>
        <li><a class="button button-primary" href="{prefix}start.html">Start here →</a></li>
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
      <nav class="footer-nav" aria-label="Footer navigation"><a href="{prefix}start.html">Start here</a><a href="{prefix}library.html">The Library</a><a href="{home}#shelf">The Shelf</a><a href="{home}#story">Our story</a><a href="{home}#transparency">Transparency</a></nav>
      <div class="footer-meta"><nav class="socials" aria-label="Social links"><a href="{esc(instagram["url"], attribute=True)}" target="_blank" rel="noopener noreferrer">Instagram{external_note()}</a></nav><p class="fine">{esc(site["disclosure"])}</p><p class="copyright">© {int(site["copyrightYear"])} The Mindful Matrix</p></div>
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
    return f'''<article class="matrix-stage" data-matrix-stage="{esc(stage["id"], attribute=True)}" data-reveal>
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
        <div class="testing-card__visual">{image_markup(product, eager=True, sizes="(max-width: 48rem) 90vw, 48vw")}</div>
        <div class="testing-card__content">
          <p class="interface-label">{esc(product["category"])} / Existing product data</p>
          <h3>{esc(product["name"])}</h3>
          <p>{esc(product["description"])}</p>
          <div class="testing-card__why"><span>Why it’s here</span><strong>{esc(testing["why"])}</strong></div>
          <div class="button-row">
            <a class="button button-primary" href="{url}" target="_blank" rel="noopener noreferrer">{esc(testing["measureLinkLabel"])} ↗{external_note()}</a>
            <a class="button button-secondary" href="{url}" target="_blank" rel="noopener noreferrer">Product details ↗{external_note()}</a>
          </div>
        </div>
      </article>'''


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


def shelf_product_markup(product: dict) -> str:
    cutout = product.get("cutout")
    if not cutout:
        return image_markup(product)
    return (
        f'<img class="shelf-card__cutout" src="{esc(cutout["src"], attribute=True)}" '
        f'alt="{esc(product["image"]["alt"], attribute=True)}" '
        f'width="{int(cutout["width"])}" height="{int(cutout["height"])}" '
        'loading="lazy" decoding="async" data-image-role="official-product-cutout">'
    )


def shelf_card_markup(product: dict) -> str:
    return f'''<article class="shelf-card" data-product-id="{esc(product["id"], attribute=True)}" data-reveal>
        <div class="shelf-card__visual artwork-stage">{product_artwork_markup(product)}<div class="shelf-card__product">{shelf_product_markup(product)}</div></div>
        <div class="shelf-card__content">
          <p class="interface-label">{esc(product["category"])}</p>
          <h3>{esc(product["name"])}</h3><p>{esc(product["description"])}</p>
          <details class="why-details"><summary>Why it’s here</summary><p>{esc(product["whyItsHere"])}</p></details>
          <a class="shelf-card__link" href="{esc(product["destination"], attribute=True)}" target="_blank" rel="noopener noreferrer">{esc(product["cta"])} ↗{external_note()}</a>
        </div>
      </article>'''


def published_articles(library: dict) -> list[dict]:
    return [article for article in library["articles"] if article.get("status") == "published"]


def category_name(library: dict, category_id: str) -> str:
    categories = {category["id"]: category["name"] for category in library["categories"]}
    return categories.get(category_id, category_id)


def library_article_markup(article: dict, library: dict) -> str:
    hero = article.get("hero")
    if hero and hero.get("src"):
        visual = (
            f'<img src="{esc(hero["src"], attribute=True)}" alt="{esc(hero.get("alt", ""), attribute=True)}" '
            f'width="{int(hero["width"])}" height="{int(hero["height"])}" loading="lazy" decoding="async">'
        )
    else:
        visual = '<div class="library-card__art" aria-hidden="true"><span class="library-card__line"></span></div>'
    updated = f'<span>Updated {esc(article["updated"])}</span>' if article.get("updated") else ""
    return f'''<article class="library-article" data-library-article data-reveal>
        <div class="library-article__visual">{visual}</div>
        <div class="library-article__content">
          <p class="interface-label">{esc(category_name(library, article["category"]))}</p><h3>{esc(article["title"])}</h3><p>{esc(article["summary"])}</p>
          <div class="library-article__meta"><time datetime="{esc(article["published"], attribute=True)}">{esc(article["published"])}</time><span>{esc(article["readingTime"])}</span>{updated}</div>
          <a class="button button-tertiary" href="library/{esc(article["slug"], attribute=True)}.html">Read the guide →</a>
        </div>
      </article>'''


def category_badges(library: dict) -> str:
    return "".join(f'<span>{esc(category["name"])}</span>' for category in library["categories"])


def library_body_markup(library: dict, library_home: dict) -> str:
    articles = published_articles(library)
    if articles:
        return '<div class="library-article-grid" data-library-state="published">' + "".join(
            library_article_markup(article, library) for article in articles
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
    href = f'#category-{esc(category["id"], attribute=True)}' if count else "#articles"
    return f'''<a class="category-card" href="{href}" data-reveal><span class="category-card__index">{esc(category["id"])}</span><strong>{esc(category["name"])}</strong><small>{availability}</small><span aria-hidden="true">→</span></a>'''


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


def standard_markup(principle: dict) -> str:
    return f'''<li><span>{esc(principle["index"])}</span><div><h3>{esc(principle["name"])}</h3><p>{esc(principle["copy"])}</p></div></li>'''


def editorial_principles_markup(site_data: dict, library: dict) -> str:
    selected = [item for item in site_data["homepage"]["standards"]["principles"] if item["index"] in {"01", "02", "03", "05"}]
    update = library["editorialUpdatePrinciple"]
    selected.append({"index": "06", "name": update["name"], "copy": update["copy"]})
    return "".join(standard_markup(item) for item in selected)


def orientation_stage_markup(stage: dict) -> str:
    destinations = {
        "information": ("See the testing starting point", "index.html#testing"),
        "education": ("Explore the Library", "library.html"),
        "action": ("Explore the Shelf", "index.html#shelf"),
    }
    cta, href = destinations[stage["id"]]
    labels = "".join(f"<li>{esc(label)}</li>" for label in stage["labels"])
    return f'''<li id="{esc(stage["id"], attribute=True)}" class="orientation-stage" data-reveal>
      <div class="orientation-stage__node" aria-hidden="true">{esc(stage["index"])}</div>
      <div class="orientation-stage__body"><p class="interface-label">{esc(stage["name"])}</p><h3>{esc(stage["heading"])}</h3><p>{esc(stage["copy"])}</p><ul aria-label="Related areas">{labels}</ul><strong>{esc(stage["question"])}</strong><a class="button button-tertiary" href="{href}">{cta} →</a></div>
    </li>'''


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
    links = "".join(f'<li><a href="#{esc(section["id"], attribute=True)}">{esc(section["heading"])}</a></li>' for section in article["bodySections"])
    for key, label in (("evidenceNotes", "Evidence notes"), ("limitations", "Limitations"), ("sources", "Sources")):
        if article.get(key):
            links += f'<li><a href="#{key.replace("Notes", "-notes")}">{label}</a></li>'
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
        detail = f'<span>{esc(source["detail"])}</span>' if source.get("detail") else ""
        items.append(f'''<li><a href="{esc(source["url"], attribute=True)}" target="_blank" rel="noopener noreferrer">{esc(source["title"])} ↗{external_note()}</a>{detail}</li>''')
    return f'''<section id="sources" class="article-sources"><h2>Sources</h2><ol>{"".join(items)}</ol></section>'''


def article_related_markup(article: dict, published_by_slug: dict[str, dict], products_by_id: dict[str, dict]) -> str:
    links: list[str] = []
    for slug in article.get("relatedArticles", []):
        related = published_by_slug.get(slug)
        if related:
            links.append(f'<li><span>Library</span><a href="{esc(slug, attribute=True)}.html">{esc(related["title"])} →</a></li>')
    for product_id in article.get("relatedProducts", []):
        product = products_by_id.get(product_id)
        if product:
            links.append(f'<li><span>The Shelf</span><a href="../index.html#shelf">{esc(product["name"])} →</a></li>')
    if not links:
        return ""
    return f'''<section class="article-related"><h2>Related next steps</h2><ul>{"".join(links)}</ul></section>'''


def article_replacements(
    data: dict,
    library: dict,
    article: dict,
    *,
    preview: bool,
) -> dict[str, str]:
    metadata = data["site"]["metadata"]
    prefix = "../"
    title = article["title"] + metadata["articleTitleSuffix"]
    description = article.get("dek") or article["summary"]
    canonical_path = None if preview else f'library/{article["slug"]}.html'
    byline = [f'By {esc(article["author"])}', f'<span>{esc(article["readingTime"])}</span>']
    if article.get("reviewer"):
        byline.append(f'<span>Reviewed by {esc(article["reviewer"])}</span>')
    if article.get("published"):
        byline.append(f'<time datetime="{esc(article["published"], attribute=True)}">Published {esc(article["published"])}</time>')
    if article.get("updated"):
        byline.append(f'<time datetime="{esc(article["updated"], attribute=True)}">Updated {esc(article["updated"])}</time>')
    hero = article.get("hero")
    if hero and hero.get("src"):
        hero_markup = f'''<figure class="article-hero__media"><img src="../{esc(hero["src"], attribute=True)}" alt="{esc(hero.get("alt", ""), attribute=True)}" width="{int(hero["width"])}" height="{int(hero["height"])}" decoding="async"></figure>'''
    else:
        hero_markup = '<div class="article-hero__placeholder" aria-hidden="true"><span></span><img src="../assets/brand/mark-gold.svg" width="64" height="64" alt=""></div>'
    takeaways = article_list_section("key-takeaways", "Key takeaways", article.get("keyTakeaways", []), "article-takeaways")
    published_by_slug = {item["slug"]: item for item in published_articles(library)}
    products_by_id = {product["id"]: product for product in data["products"]}
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
            published=article.get("published"),
            updated=article.get("updated"),
            noindex=preview,
        ),
        "{{SHARED_HEADER}}": shared_header_markup(prefix=prefix, current="article"),
        "{{SHARED_FOOTER}}": shared_footer_markup(data, prefix=prefix),
        "{{PREVIEW_BANNER}}": preview_banner,
        "{{ARTICLE_CATEGORY}}": esc(category_name(library, article["category"])),
        "{{ARTICLE_TITLE}}": esc(article["title"]),
        "{{ARTICLE_DEK}}": esc(description),
        "{{ARTICLE_BYLINE}}": " · ".join(byline),
        "{{ARTICLE_HERO}}": hero_markup,
        "{{ARTICLE_TOC}}": article_toc_markup(article),
        "{{ARTICLE_TAKEAWAYS}}": takeaways,
        "{{ARTICLE_BODY}}": article_body_markup(article),
        "{{ARTICLE_EVIDENCE}}": article_list_section("evidence-notes", "Evidence notes", article.get("evidenceNotes", [])),
        "{{ARTICLE_LIMITATIONS}}": article_list_section("limitations", "Limitations", article.get("limitations", [])),
        "{{ARTICLE_SOURCES}}": article_sources_markup(article.get("sources", [])),
        "{{ARTICLE_RELATED}}": article_related_markup(article, published_by_slug, products_by_id),
    }


def build_home(data: dict, library: dict) -> None:
    products = data["products"]
    products_by_id = {product["id"]: product for product in products}
    featured = products_by_id[data["featuredProductId"]]
    site = data["site"]
    metadata = site["metadata"]
    brand = data["brand"]
    home = data["homepage"]
    page = metadata["pages"]["home"]
    replacements = {
        "{{DOCUMENT_HEAD}}": document_head_markup(metadata, prefix="", title=page["title"], description=site["description"], path=page["path"]),
        "{{SHARED_HEADER}}": shared_header_markup(prefix="", current="home"),
        "{{SHARED_FOOTER}}": shared_footer_markup(data, prefix=""),
        "{{PHILOSOPHY}}": esc(brand["philosophy"]),
        "{{HERO_HEADLINE}}": line_markup(home["hero"]["headline"]),
        "{{HERO_SUPPORT}}": esc(home["hero"]["supportingLine"]),
        "{{HERO_COPY}}": esc(home["hero"]["copy"]),
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
        "{{TESTING_PRODUCT}}": testing_product_markup(featured, home["testing"]),
        "{{LIBRARY_LABEL}}": esc(home["library"]["label"]),
        "{{LIBRARY_HEADING}}": esc(home["library"]["heading"]),
        "{{LIBRARY_COPY}}": esc(home["library"]["copy"]),
        "{{LIBRARY_BODY}}": library_body_markup(library, home["library"]),
        "{{LIBRARY_TRANSITION}}": esc(home["library"]["transition"]),
        "{{SHELF_LABEL}}": esc(home["shelf"]["label"]),
        "{{SHELF_HEADING}}": esc(home["shelf"]["heading"]),
        "{{SHELF_COPY}}": esc(home["shelf"]["copy"]),
        "{{SHELF_CARDS}}": "\n        ".join(shelf_card_markup(product) for product in products),
        "{{STANDARDS_HEADING}}": esc(home["standards"]["heading"]),
        "{{STANDARDS_LIST}}": "\n        ".join(standard_markup(item) for item in home["standards"]["principles"]),
        "{{STANDARDS_STATEMENT}}": line_markup(home["standards"]["statement"]),
        "{{TRANSPARENCY_HEADING}}": esc(home["transparency"]["heading"]),
        "{{TRANSPARENCY_COPY}}": esc(home["transparency"]["copy"]),
        "{{DISCLOSURE}}": esc(site["disclosure"]),
        "{{FINAL_HEADLINE}}": line_markup(home["finalCta"]["headline"]),
        "{{FINAL_RESPONSE}}": line_markup(home["finalCta"]["response"]),
        "{{FINAL_PHILOSOPHY}}": esc(home["finalCta"]["philosophy"]),
    }
    write_output(ROOT / "index.html", render_template("index.html", replacements))


def build_library(data: dict, library: dict) -> None:
    metadata = data["site"]["metadata"]
    page = metadata["pages"]["library"]
    counts = {category["id"]: 0 for category in library["categories"]}
    for article in published_articles(library):
        counts[article["category"]] += 1
    replacements = {
        "{{DOCUMENT_HEAD}}": document_head_markup(metadata, prefix="", title=page["title"], description=page["description"], path=page["path"]),
        "{{SHARED_HEADER}}": shared_header_markup(prefix="", current="library"),
        "{{SHARED_FOOTER}}": shared_footer_markup(data, prefix=""),
        "{{LIBRARY_CATEGORIES}}": "".join(library_category_markup(category, counts[category["id"]]) for category in library["categories"]),
        "{{LIBRARY_INDEX}}": library_index_markup(library, data["homepage"]),
        "{{EDITORIAL_PRINCIPLES}}": editorial_principles_markup(data, library),
    }
    write_output(ROOT / "library.html", render_template("library.html", replacements))


def build_start(data: dict) -> None:
    metadata = data["site"]["metadata"]
    page = metadata["pages"]["start"]
    replacements = {
        "{{DOCUMENT_HEAD}}": document_head_markup(metadata, prefix="", title=page["title"], description=page["description"], path=page["path"]),
        "{{SHARED_HEADER}}": shared_header_markup(prefix="", current="start"),
        "{{SHARED_FOOTER}}": shared_footer_markup(data, prefix=""),
        "{{ORIENTATION_STAGES}}": "".join(orientation_stage_markup(stage) for stage in data["homepage"]["matrix"]["stages"]),
    }
    write_output(ROOT / "start.html", render_template("start.html", replacements))


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
    build_home(data, library)
    build_library(data, library)
    build_start(data)
    build_articles(data, library)
    if args.preview_article:
        build_preview(data, library, args.preview_article.resolve(), args.preview_output)


if __name__ == "__main__":
    main()
