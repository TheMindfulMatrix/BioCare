#!/usr/bin/env python3
"""Generate the dependency-free production homepage from centralized content."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def esc(value: object, *, attribute: bool = False) -> str:
    return html.escape(str(value), quote=attribute)


def external_note() -> str:
    return '<span class="visually-hidden"> (opens in a new tab)</span>'


def line_markup(lines: list[str]) -> str:
    return "".join(f"<span>{esc(line)}</span>" for line in lines)


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
        return '<span class="shelf-card__artwork" data-artwork-state="placeholder" aria-hidden="true"></span>'
    return (
        f'<img class="shelf-card__artwork" src="{esc(source, attribute=True)}" alt="" '
        f'width="{int(artwork["width"])}" height="{int(artwork["height"])}" '
        'loading="lazy" decoding="async" data-artwork-state="ready">'
    )


def shelf_card_markup(product: dict) -> str:
    return f'''<article class="shelf-card" data-reveal>
        <div class="shelf-card__visual">{product_artwork_markup(product)}<div class="shelf-card__product">{image_markup(product)}</div></div>
        <div class="shelf-card__content">
          <p class="interface-label">{esc(product["category"])}</p>
          <h3>{esc(product["name"])}</h3><p>{esc(product["description"])}</p>
          <details class="why-details"><summary>Why it’s here</summary><p>{esc(product["whyItsHere"])}</p></details>
          <a class="shelf-card__link" href="{esc(product["destination"], attribute=True)}" target="_blank" rel="noopener noreferrer">{esc(product["cta"])} ↗{external_note()}</a>
        </div>
      </article>'''


def library_article_markup(article: dict) -> str:
    topics = " / ".join(esc(topic) for topic in article["topics"])
    image = article.get("image")
    if image:
        visual = (
            f'<img src="{esc(image["src"], attribute=True)}" alt="{esc(image.get("alt", ""), attribute=True)}" '
            f'width="{int(image["width"])}" height="{int(image["height"])}" loading="lazy" decoding="async">'
        )
    else:
        visual = '<div class="library-card__art" aria-hidden="true"><span class="library-card__line"></span></div>'
    reading_time = f'<span>{esc(article["readingTime"])}</span>' if article.get("readingTime") else ""
    return f'''<article class="library-article" data-library-article data-reveal>
        <div class="library-article__visual">{visual}</div>
        <div class="library-article__content">
          <p class="interface-label">{topics}</p><h3>{esc(article["title"])}</h3><p>{esc(article["summary"])}</p>
          <div class="library-article__meta"><time datetime="{esc(article["published"], attribute=True)}">{esc(article["published"])}</time>{reading_time}</div>
          <a class="button button-tertiary" href="{esc(article["href"], attribute=True)}">Read the guide →</a>
        </div>
      </article>'''


def library_body_markup(library: dict, library_home: dict) -> str:
    articles = library["articles"]
    if articles:
        return '<div class="library-article-grid" data-library-state="published">' + "".join(
            library_article_markup(article) for article in articles
        ) + "</div>"
    categories = "".join(f'<span>{esc(category)}</span>' for category in library_home["categories"])
    return f'''<div class="library-layout" data-library-state="empty">
        <article class="library-status-card" data-reveal>
          <div class="library-card__art" aria-hidden="true"><span class="library-card__line"></span></div>
          <div class="library-status-card__content"><h3>{esc(library_home["status"])}</h3><p>{esc(library_home["statusCopy"])}</p></div>
        </article>
        <div class="library-categories" data-reveal><p class="component-label">{esc(library_home["categoriesLabel"])}</p>{categories}</div>
      </div>'''


def standard_markup(principle: dict) -> str:
    return f'''<li><span>{esc(principle["index"])}</span><div><h3>{esc(principle["name"])}</h3><p>{esc(principle["copy"])}</p></div></li>'''


def main() -> None:
    data = json.loads((ROOT / "content" / "site.json").read_text(encoding="utf-8"))
    library_data = json.loads((ROOT / "content" / "library.json").read_text(encoding="utf-8"))
    products = data["products"]
    products_by_id = {product["id"]: product for product in products}
    featured = products_by_id[data["featuredProductId"]]
    site = data["site"]
    brand = data["brand"]
    home = data["homepage"]
    instagram = site["instagram"]

    replacements = {
        "{{SITE_NAME}}": esc(site["name"]),
        "{{SITE_DESCRIPTION}}": esc(site["description"], attribute=True),
        "{{INSTAGRAM_URL}}": esc(instagram["url"], attribute=True),
        "{{DISCLOSURE}}": esc(site["disclosure"]),
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
        "{{LIBRARY_BODY}}": library_body_markup(library_data, home["library"]),
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
        "{{FINAL_HEADLINE}}": line_markup(home["finalCta"]["headline"]),
        "{{FINAL_RESPONSE}}": line_markup(home["finalCta"]["response"]),
        "{{FINAL_PHILOSOPHY}}": esc(home["finalCta"]["philosophy"]),
    }

    output = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
    for token, value in replacements.items():
        output = output.replace(token, value)
    if "{{" in output or "}}" in output:
        raise RuntimeError("Unresolved template token in generated index.html")
    (ROOT / "index.html").write_text(output, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
