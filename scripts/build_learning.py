"""Testing and learning surfaces; no checkout, sign-in, or health-data collection."""
from __future__ import annotations


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
    esc = api.esc
    status = '<p class="learning-review-status">In development · Not available for purchase. Course outlines and a free sample are available here; enrollment and checkout are not open.</p>'
    modules = "".join(f'<li><strong>{esc(item["title"])}</strong><p>{esc(item["outcome"])} <a href="library/{esc(item["guide"], attribute=True)}.html">Read the free guide →</a></p></li>' for item in wellness["modules"])
    body = section(f'<div class="learning-grid"><article class="learning-card" id="everyday"><p class="learning-card__number">PATH 01 / EVERYDAY LIFE</p><h2>{esc(wellness["title"])}</h2><p>{esc(wellness["audience"])}</p><p>{esc(wellness["description"])}</p>{status}<a class="button button-primary" href="#sample">Try a free planning lesson →</a></article><article class="learning-card"><p class="learning-card__number">PATH 02 / INDEPENDENT BUSINESS</p><h2>{esc(partner["title"])}</h2><p>{esc(partner["audience"])}</p><p>{esc(partner["description"])}</p>{status}<a class="button button-secondary" href="partners.html">Explore partner learning →</a></article></div>', tone="warm")
    body += section(f'<div class="learning-reading"><h2>Everyday Matrix: the proposed curriculum</h2><p>Food, movement, rest, and informed decisions. No product purchase or testing is required. This is general adult education, not personal medical advice or clinician-reviewed training.</p><ol>{modules}</ol></div>')
    sample = wellness["sample"]
    body += section(f'<div class="learning-reading" id="sample"><p class="section-kicker">A free sample · Original planning exercise</p><h2>{esc(sample["title"])}</h2><p>{esc(sample["text"])}</p><h3>Try it on paper</h3><p>{esc(sample["practice"])}</p><details class="learning-course-module"><summary>{esc(sample["question"])}</summary><p>{esc(sample["answer"])}</p></details><p class="learning-note">Keep notes privately. This website does not collect your habit records, medical history, test results, or course answers.</p></div>', tone="warm")
    body += section('<div class="learning-reading"><h2>Learn at your own pace.</h2><p>Use the free Library now. The courses are being prepared separately, and their scope and terms will be reviewed before any enrollment opens. Neither course is required to use the site or explore optional products.</p><a class="button button-secondary" href="library.html">Return to the free Library →</a></div>')
    page(api, data, "learning.html", "Learning paths", "Small steps.\nA clearer direction.", "Two separate learning paths: everyday habits and responsible business skills. Explore the outlines, try a free lesson, and take what is useful.", body, [("#everyday", "Choose a path"), ("#sample", "Try a lesson")])
    business_modules = "".join(f'<li><strong>{esc(item["title"])}</strong><p>{esc(item["outcome"])}</p></li>' for item in partner["modules"])
    source_links = "".join(f'<li><a href="{esc(item["url"], attribute=True)}" target="_blank" rel="noopener noreferrer">{esc(item["title"])} ↗{api.external_note()}</a></li>' for item in partner["sources"])
    body = section(f'<div class="learning-reading"><h2>Curious is enough.</h2><p>You can learn about the work before deciding whether it fits. There is no application, enrollment fee, or obligation on this page.</p><p class="learning-note">The Mindful Matrix is an independent partner, not Zinzino corporate. A commercial relationship may benefit us if you purchase or join through our partner connections. This is not an official Zinzino course.</p><h3>Make the business decision separately.</h3><p>Participation involves costs and uncertain results. The FTC cautions that many participants in legitimate multilevel marketing businesses earn little or nothing, and some lose money. Review current local agreements, costs, cancellation terms, and any official disclosures before deciding.</p><a href="https://consumer.ftc.gov/articles/multi-level-marketing-businesses-and-pyramid-schemes" target="_blank" rel="noopener noreferrer">Read the FTC consumer guide ↗{api.external_note()}</a></div>', tone="warm")
    body += section(f'<div class="learning-reading" id="curriculum"><p class="section-kicker">Original course in development</p><h2>{esc(partner["title"])}</h2>{status}<p>The curriculum focuses on skills and informed decisions, with no earnings or lifestyle promises. It is separate from the everyday-habits course.</p><ol>{business_modules}</ol></div>')
    body += section('<div class="learning-reading"><h2>Start with a few honest questions.</h2><ul><li>What are my actual obligations, recurring costs, and exit options?</li><li>Can I explain the product facts and their limits without making medical claims?</li><li>Do I have a realistic time and spending limit?</li><li>Can people say no without pressure or repeated messages?</li></ul><p>Keep financial, customer, and health records private. This website does not collect applications or host team meetings.</p><p>Questions about the learning plan? Use the contact details on our About page. There is no automatic enrollment or marketing signup.</p><a class="button button-secondary" href="about.html">About &amp; contact →</a></div>', tone="warm")
    body += section(f'<div class="learning-reading"><h2>Inspect the sources.</h2><p>Public guidance and official help pages, checked September 6, 2026. The Zinzino link is a commercial company source. Links do not imply endorsement or permission to resell the source material.</p><ul class="learning-source-links">{source_links}</ul></div>')
    page(api, data, "partners.html", "Partner learning", "Learn the work.\nChoose your direction.", "A calm introduction to independent partner work, with responsibilities, practical skills, and room to decide whether it fits.", body, [("#curriculum", "Explore the curriculum"), ("learning.html", "Everyday habits instead")])


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
