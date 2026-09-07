"""Testing and learning surfaces; no checkout, sign-in, or health-data collection."""
from __future__ import annotations

if __package__:
    from . import build_academy
else:
    import build_academy


def section(body: str, *, tone: str = "light") -> str:
    return f'<section class="section-{tone} section-pad"><div class="container">{body}</div></section>'


def build_testing(data: dict, library: dict, api) -> None:
    journeys = api.load_json(api.ROOT / "content/testing-journeys.json")
    products = {p["id"]: p for p in api.active_products(data["catalog"])}
    cards = []
    for index, journey in enumerate(journeys["journeys"], 1):
        esc = api.esc
        product = products[journey["productIds"][0]]
        steps = "".join(f'<li><strong>{esc(title)}</strong>{esc(text)}</li>' for title, text in journey["steps"])
        connections = "".join(f'<a href="products/{esc(pid, attribute=True)}.html">{esc(products[pid]["name"])} details →</a>' for pid in journey["productIds"])
        cards.append(f'''<article class="learning-card" id="{esc(journey["id"], attribute=True)}">
          <p class="learning-card__number">JOURNEY {index:02d} / {esc(journey["testName"])}</p>
          <img class="learning-card__image" src="{esc(product["cutout"]["src"], attribute=True)}" alt="{esc(product["cutout"]["alt"], attribute=True)}" width="560" height="560" loading="lazy">
          <h2>{esc(journey["title"])}</h2><h3>What it measures</h3><p>{esc(journey["measures"])}</p>
          <p class="learning-note">{esc(journey["boundary"])}</p>
          <ol class="learning-steps">{steps}</ol>
          <a class="button button-primary" href="library/{esc(journey["guide"], attribute=True)}.html">Read the independent context →</a>
          <details><summary>Optional test products &amp; official instructions</summary>
            <p>{esc(journey["availability"])}</p><p>These are optional commercial tools, not a requirement for using this Library. Product details retain the catalog's dated prices; the manufacturer confirms current terms.</p>
            <p>{esc(data["site"]["affiliateDisclosure"])}</p>
            <div class="learning-products">{connections}</div>
            <a href="{esc(journey["sourceUrl"], attribute=True)}" target="_blank" rel="noopener noreferrer">Manufacturer's test information ↗{api.external_note()}</a>
          </details>
        </article>''')
    body = section('<div class="learning-grid">' + "".join(cards) + "</div>", tone="warm")
    body += section('''<div class="learning-reading"><h2>Keep results private. Keep care connected.</h2>
      <p>Use the official test portal and the instructions supplied with your kit. Do not send test IDs, laboratory reports, medical histories or genetic data to The Mindful Matrix. We do not collect or interpret results here.</p>
      <p>A home test does not replace medical assessment. If you have symptoms or an unexpected result, contact a qualified healthcare professional; do not wait for a retest or change prescribed treatment yourself.</p>
      <a class="button button-secondary" href="https://www.zinzinotest.com/" target="_blank" rel="noopener noreferrer">Open Zinzino's results portal ↗<span class="visually-hidden"> (opens in a new tab)</span></a>
      <p class="fine">This is a separate website with its own privacy terms. No test information is passed by this link.</p></div>''')
    body += section(f'<div class="learning-reading"><h2>How this comparison was prepared</h2><p>US listings checked {journeys["checkedDate"]}: four distinct tests, five standalone product listings. The Gut Health Test x2 is a quantity option. The Balance Test Basic Kit remains a separate bundle, not another test method.</p><p>Manufacturer pages describe the test. Independent education explains the broader context; it does not certify the test or endorse a purchase.</p><a href="{journeys["catalogSource"]}" target="_blank" rel="noopener noreferrer">Inspect the official US test catalog ↗{api.external_note()}</a></div>', tone="warm")
    page(api, data, "testing.html", "Testing journeys", "A clearer question.\nA more useful measurement.", "Explore all four Zinzino test types before considering a purchase. Understand what each measures, where interpretation stops, and what to ask next.", body, [(f'#{j["id"]}', j["testName"]) for j in journeys["journeys"]])


def build_learning_paths(data: dict, api) -> None:
    wellness = api.load_json(api.ROOT / "content/learning.json")
    partner = api.load_json(api.ROOT / "content/partner-learning.json")
    if wellness.get("salesEnabled") is not False or partner.get("salesEnabled") is not False:
        raise ValueError("Course sales require a separately reviewed implementation")
    build_academy.render(data, wellness, partner, api)


def page(api, data: dict, path: str, eyebrow: str, title: str, intro: str, body: str, links=()) -> None:
    metadata = data["site"]["metadata"]
    api.write_output(api.ROOT / path, api.render_template("learning.html", {
        "{{DOCUMENT_HEAD}}": api.document_head_markup(metadata, prefix="", title=eyebrow + " | The Mindful Matrix", description=intro, path=path, structured_data=[api.organization_schema(metadata), api.website_schema(metadata), api.breadcrumb_schema(metadata, [("Home", ""), (eyebrow, path)])]),
        "{{SHARED_HEADER}}": api.shared_header_markup(data, prefix="", current=path.removesuffix(".html")),
        "{{SHARED_FOOTER}}": api.shared_footer_markup(data, prefix=""),
        "{{EYEBROW}}": api.esc(eyebrow),
        "{{TITLE}}": api.esc(title).replace("\n", "<br>"),
        "{{INTRO}}": api.esc(intro),
        "{{HERO_LINKS}}": '<nav class="learning-links" aria-label="On this page">' + "".join(f'<a href="{api.esc(href, attribute=True)}">{api.esc(label)} →</a>' for href, label in links) + "</nav>" if links else "",
        "{{BODY}}": body,
    }))
