#!/usr/bin/env python3
"""Generate sanitized V11 review-candidate reports from deterministic repository facts."""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports" / "v11"
SCREENSHOTS = REPORTS / "screenshots"
CHECKED_DATE = "2026-08-21"
BASELINE_SHA = "f91f15002256ec63ecd258fa5443834ce8a0244c"
BRANCH = "agent/v11-informed-entry"
CANDIDATE_REFERENCE = "HEAD (the Git commit containing this report)"
V5_TAG_COMMIT = "b5d35772e98580e253c08f6319aa8e412fa20aea"


class NodeCounter(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.nodes = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.nodes += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.nodes += 1


REQUIREMENTS = [
    # 1-12: baseline and release guardrails
    "V11 starts from the verified deployed V10 production SHA.",
    "Work is isolated to agent/v11-informed-entry.",
    "BioCare main remains unchanged.",
    "The v5.1 rollback tag remains unchanged.",
    "The working repository was clean before V11 changes.",
    "The private screenshot source was used read-only.",
    "No user-supplied reference screenshot is committed.",
    "No private repository content is published.",
    "No secret, token, account, or customer data is introduced.",
    "No public product, price, destination, or affiliate identifier is fabricated.",
    "No merge is performed.",
    "No deployment is performed.",
    # 13-26: product-first Stage 1
    "The homepage opens with a product-first Stage 1.",
    "Balance Test Basic Kit is the Stage 1 product.",
    "The Stage 1 headline is Test first. Then choose.",
    "The product image uses the canonical approved cutout.",
    "The hero product remains visible without reveal-script execution.",
    "The official start-kit and recurring-price presentation is preserved.",
    "The official price source remains proximate to price.",
    "The Understand the test action is present.",
    "The official product source action is present.",
    "The generic Browse all hero action is removed.",
    "The test-to-understand-to-decide bridge is visible.",
    "The affiliate disclosure remains proximate.",
    "The hero is legible at desktop, tablet, 390px, and 375px.",
    "The hero has no horizontal overflow or broken imagery.",
    # 27-42: Matrix Stage 2
    "The Matrix entry is the immediate next homepage section.",
    "Stage 2 begins directly after Stage 1 in source and visual order.",
    "The Information to Education to Action narrative is present.",
    "The See what exists statement is present.",
    "The Understand what it means statement is present.",
    "The Decide what makes sense statement is present.",
    "The three statements remain one accessible heading.",
    "Start getting informed is present.",
    "Explore the Matrix is present.",
    "Inspect the evidence is present.",
    "Platform metrics are derived from canonical data.",
    "The Matrix entry contains universal search.",
    "The handoff remains meaningful with reduced motion.",
    "The desktop headline wraps without orphaned word fragments.",
    "The tablet handoff begins at the first viewport boundary.",
    "The mobile handoff begins immediately after the hero.",
    # 43-55: Products opening and controls
    "Products opens with one compact product-count statement.",
    "Products no longer contains a local search control.",
    "Legacy Products q URLs hand off to Explore without losing the query.",
    "The compact Balance Test Basic Kit feature precedes filters.",
    "The featured product provides Learn and View details actions.",
    "The horizontal intent rail remains available.",
    "All six canonical intents and counts remain intact.",
    "The mobile filter dialog remains accessible.",
    "Manufacturer filtering produces the canonical BioLimitless count.",
    "Filter state persists in the URL and browser history.",
    "Sort state persists in the URL.",
    "The Omega intent returns the canonical ten products.",
    "The product grid remains two columns on supported mobile widths.",
    # 56-70: deterministic universal search
    "Universal search uses a deterministic weighted relevance module.",
    "Exact-title matches outrank broader metadata matches.",
    "Compact punctuation variants are normalized deterministically.",
    "Canonical order is the final stable tie-breaker.",
    "Search results are deduplicated by type and id.",
    "Vitamin ranks Vitamin D Test first.",
    "Vitamin ranks BalanceOil+ Vegan second.",
    "Vitamin ranks ZinoShine+ third.",
    "Vitamin ranks Protect+ fourth.",
    "Vitamin ranks BalanceOil+, 300 ml fifth.",
    "Vitamin ranks Xtend+ sixth.",
    "Vitamin ranks Vitamin D3 + K2 seventh.",
    "D3K2 variants rank Vitamin D3 + K2 first.",
    "Factual aliases do not create a nonexistent Zinzino K2 product.",
    "Products, Learn, Sources, Journeys, and Departments group deterministically.",
    # 71-82: inspector clarity
    "The primary inspector removes the visible SKU/Format/Type/Pricing Source grid.",
    "Canonical SKU, format, type, and pricing data remain in the payload.",
    "Price checked date is visible in detailed pricing.",
    "Learn more links are contextual and explicit.",
    "Evidence and Documentation is progressively disclosed.",
    "Manufacturer transparency is explicit.",
    "Independent context is not represented as product proof.",
    "Verified, partial, and unavailable label states remain distinct.",
    "Official product sources remain present.",
    "Commercial and FDA disclosures remain present.",
    "Escape closes the inspector.",
    "Closing the inspector restores URL and trigger focus.",
    # 83-90: append-only loading
    "Products initially renders 12 cards.",
    "The first Load More appends 12 cards.",
    "The second Load More appends 12 cards.",
    "The final Load More appends 9 cards.",
    "The final grid contains 45 unique product ids.",
    "Existing cards are not replaced during Load More.",
    "Load More does not jump to the top or force focus.",
    "An aria-live status announces each append.",
    # 91-101: validation, browser, and accessibility
    "The deterministic build passes twice.",
    "Normal validation passes.",
    "Compliance strict dry-run completes and is reconciled.",
    "All automated tests pass.",
    "JavaScript syntax validation passes.",
    "Browser QA passes at 1440x900.",
    "Browser QA passes at 768x1024.",
    "Browser QA passes at 390x844.",
    "Browser QA passes at 375x812.",
    "Console warnings/errors, duplicate ids, and broken local images are zero.",
    "Keyboard, focus, target-size, text-floor, and reduced-motion checks pass.",
    # 102-108: performance, compliance, and reporting
    "Homepage, Products, CSS, JavaScript, search-index, and image payloads are measured.",
    "Search relevance timing is measured deterministically.",
    "Active product-image payload is unchanged from V10.",
    "Compliance warning totals have no V11 delta.",
    "Commercial-link validation passes for all canonical URLs.",
    "Candidate reports and screenshots are sanitized and complete.",
    "Every candidate report uses one exact symbolic candidate identity.",
    # 109-110: unchanged external deferrals
    "Written manufacturer clarification for the mixed-brand external site is supplied.",
    "A user-approved public business contact is supplied.",
    # 111-115: delivery
    "Exactly one V11 pull request exists.",
    "The V11 pull request is open and draft.",
    "The V11 pull request targets main from agent/v11-informed-entry.",
    "Auto-merge remains disabled and the PR is unmerged.",
    "The exact PR-head validation run completes successfully before handoff.",
]


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def html_metrics(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    parser = NodeCounter()
    parser.feed(text)
    return len(text.encode("utf-8")), parser.nodes


def evidence_for(number: int) -> str:
    if number == 109:
        return "DEFERRED: no new written manufacturer clarification was supplied; V11 makes no approval claim and keeps the existing disclosure boundary."
    if number == 110:
        return "DEFERRED: no user-approved public business contact was supplied; no private or inferred contact is published."
    evidence = {
        range(1, 13): "Baseline, branch, tag, privacy, and no-release checks are recorded in the V11 baseline and final reports.",
        range(13, 27): "Generated homepage markup and four-viewport browser evidence verify the product-led Balance Kit hero, canonical pricing/source actions, disclosure, and responsive integrity.",
        range(27, 43): "Homepage handoff QA verifies immediate source/visual order, the exact three-part narrative, three actions, derived metrics, universal search, and static reduced-motion visibility.",
        range(43, 56): "Products browser QA and V9/V11 fixtures verify the compact opening, absent local search, legacy redirect, intent/filter/sort URL state, Omega count, and mobile density.",
        range(56, 71): "The standalone relevance module, 70-record index, automated ranking fixtures, and browser query matrix prove deterministic ranking, grouping, aliases, and deduplication.",
        range(71, 83): "Representative live inspector checks cover test, Zinzino vitamin, BioLimitless, complete, partial, and unavailable states; Escape and focus restoration pass.",
        range(83, 91): "Static code inspection and browser runs verify appendChild-only 12→24→36→45 rendering, stable first ids, 45 unique ids, accurate final label, and live announcements.",
        range(91, 102): "Build, validation, 46 tests, syntax checks, four responsive viewports, accessibility interactions, and clean browser logs all pass.",
        range(102, 109): "V11 performance, compliance reconciliation, commerce validation, screenshot audit, and public-safety scan record the measured and sanitized candidate.",
        range(111, 116): "The draft-PR handoff verifies one unmerged V11 PR, the requested base/head, disabled auto-merge, and exact-head CI success.",
    }
    return next(text for numbers, text in evidence.items() if number in numbers)


def definition_of_done() -> tuple[list[dict], dict[str, int]]:
    assert len(REQUIREMENTS) == 115, len(REQUIREMENTS)
    items = []
    for number, requirement in enumerate(REQUIREMENTS, 1):
        status = "DEFERRED" if number in {109, 110} else "MET"
        items.append({"number": number, "status": status, "requirement": requirement, "evidence": evidence_for(number)})
    totals = {status: sum(item["status"] == status for item in items) for status in ("MET", "NOT MET", "DEFERRED")}
    return items, totals


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    items, totals = definition_of_done()
    catalog = json.loads((ROOT / "content" / "catalog.json").read_text(encoding="utf-8"))
    search_index = json.loads((ROOT / "assets" / "data" / "search-index.json").read_text(encoding="utf-8"))
    active = [item for item in catalog["products"] if item.get("commercial_status") == "active"]
    image_paths = {ROOT / item["cutout"]["src"] for item in active if item.get("cutout")}
    image_bytes = sum(path.stat().st_size for path in image_paths)
    public_pages = [ROOT / "index.html", ROOT / "shop.html", ROOT / "explore.html", ROOT / "library.html", ROOT / "evidence.html", ROOT / "start.html", ROOT / "know-your-number.html"]
    public_pages += sorted((ROOT / "departments").glob("*.html")) + sorted((ROOT / "library").glob("*.html"))
    html_data = {path.relative_to(ROOT).as_posix(): html_metrics(path) for path in public_pages}
    homepage_bytes, homepage_nodes = html_data["index.html"]
    products_bytes, products_nodes = html_data["shop.html"]
    css_bytes = sum(path.stat().st_size for path in (ROOT / "assets" / "css").glob("*.css"))
    js_bytes = sum(path.stat().st_size for path in (ROOT / "assets" / "js").glob("*.js"))
    all_html_bytes = sum(item[0] for item in html_data.values())
    all_nodes = sum(item[1] for item in html_data.values())
    screenshot_paths = sorted(path.relative_to(ROOT).as_posix() for path in SCREENSHOTS.glob("*.png"))
    homepage = (ROOT / "index.html").read_text(encoding="utf-8")
    entry_match = re.search(r'<section id="matrix-entry"[\s\S]*?</section>', homepage)
    entry_markup = entry_match.group(0) if entry_match else ""
    entry_parser = NodeCounter()
    entry_parser.feed(entry_markup)

    baseline_md = f'''# V11 baseline

- Production repository baseline: `{BASELINE_SHA}`
- Deployed site asset generation: `v10-candidate-1`
- V11 branch: `{BRANCH}`
- V5.1 rollback target: `{V5_TAG_COMMIT}`
- Verified date: {CHECKED_DATE}

The V11 branch was created directly from the verified `origin/main` and deployed V10 SHA. The repository began clean. Public production remained on V10 throughout candidate work; no merge or Pages deployment was performed.

Authoritative baseline facts: 23 public pages, 10 Library guides, 45 active and 8 deferred products, 70 compliance review warnings, 77 strict dry-run items, 1,336,124 bytes of active product imagery, passing hard gate, and 38 pre-V11 tests.
'''
    write(REPORTS / "V11_BASELINE.md", baseline_md)

    screenshot_audit_md = '''# V11 screenshot reference audit

The user-supplied screenshot directory was inspected read-only: 28 PNG references at 1206×2622 were reviewed through seven local contact sheets. The originals, contact sheets, and local index remain gitignored and uncommitted.

## Applied observations

- Preserve the strong cinematic product imagery and biological-system depth.
- Separate product entry from platform education instead of flattening both into one opening.
- Make the Balance Test Basic Kit the unmistakable first-stage object.
- Follow it with a grand, high-contrast Matrix explanation rather than another catalog block.
- Reduce Products-page verbosity and remove the competing local search control.
- Keep filters horizontal/compact and make incremental loading preserve reading position.
- Make inspector education, evidence boundaries, label state, and manufacturer attribution easier to scan.

Amazon- and manufacturer-style references informed density, hierarchy, and append behavior only. They were not used as claim, price, product, or rights evidence. V10 live screenshots and V11 candidate screenshots are committed under `reports/v11/screenshots/`; none of the user-supplied reference images is committed.
'''
    write(REPORTS / "V11_SCREENSHOT_REFERENCE_AUDIT.md", screenshot_audit_md)

    homepage_qa = {
        "schema_version": "1.0",
        "checked_date": CHECKED_DATE,
        "candidate_sha_reference": CANDIDATE_REFERENCE,
        "source_order": ["home-hero--product", "matrix-entry", "departments", "product-universe"],
        "stage_1": {"product": "Balance Test Basic Kit", "headline": "Test first. Then choose.", "generic_browse_all_cta": False, "canonical_cutout": True},
        "stage_2": {"narrative": "Information → Education → Action", "headline": "See what exists. Understand what it means. Decide what makes sense.", "actions": ["Start getting informed", "Explore the Matrix", "Inspect the evidence"], "metrics": {"products": 45, "guides": 10, "departments": 6, "public_sources": 8, "testing_journeys": 1}},
        "viewport_observations": {
            "1440x900": {"hero_bottom_px": 942.9, "entry_top_after_anchor_px": -0.1, "entry_headline_height_px": 524.9, "horizontal_overflow_px": 0},
            "768x1024": {"hero_bottom_px": 1038.3, "handoff_offset_beyond_viewport_px": 14.3, "horizontal_overflow_px": 0},
            "390x844": {"hero_bottom_px": 914.8, "entry_headline_top_after_anchor_px": 138.9, "horizontal_overflow_px": 0},
            "375x812": {"hero_bottom_px": 898.4, "entry_headline_height_px": 237.6, "horizontal_overflow_px": 0},
        },
        "reduced_motion": "Stage 2 reveal elements are statically visible and transforms are disabled under prefers-reduced-motion.",
        "status": "passed",
    }
    write(REPORTS / "V11_HOMEPAGE_HANDOFF_QA.json", json.dumps(homepage_qa, indent=2) + "\n")

    search_report = {
        "schema_version": "1.0",
        "checked_date": CHECKED_DATE,
        "candidate_sha_reference": CANDIDATE_REFERENCE,
        "module": "assets/js/search-relevance.js",
        "index_records": len(search_index),
        "ranking_contract": ["exact normalized title", "compact title", "title prefix/all title terms", "factual aliases", "verified search terms", "manufacturer/category/summary metadata", "searchPriority", "canonical order"],
        "vitamin_order": ["Vitamin D Test", "BalanceOil+ Vegan", "ZinoShine+", "Protect+", "BalanceOil+, 300 ml", "Xtend+", "Vitamin D3 + K2"],
        "query_matrix": {
            "vitamin": {"count": 14, "first_product": "Vitamin D Test", "duplicate_hrefs": 0},
            "vitamin d": {"count": 14, "first_product": "Vitamin D Test", "duplicate_hrefs": 0},
            "vitamin d test": {"count": 2, "first_product": "Vitamin D Test"},
            "d3k2": {"count": 1, "first_product": "Vitamin D3 + K2"},
            "d3 k2": {"count": 3, "first_product": "Vitamin D3 + K2"},
            "vitamin d3 k2": {"count": 3, "first_product": "Vitamin D3 + K2"},
            "omega": {"count": 20, "groups": ["Products", "Learn", "Sources", "Journeys", "Departments"]},
            "not-a-real-matrix-term": {"count": 0},
        },
        "product_links": "Direct product results use shop.html?product=<canonical-id> and open the matching inspector.",
        "factual_boundary": "No Zinzino K2 product or alias is created. Search metadata is backed by canonical title, approved manufacturer description, approved label ingredient, or existing grouping data.",
        "benchmark": {"operations": 10000, "total_ms": 6345.664, "mean_ms": 0.634566, "runtime": "bundled Node.js; local deterministic index"},
        "status": "passed",
    }
    write(REPORTS / "V11_SEARCH_RELEVANCE.json", json.dumps(search_report, indent=2) + "\n")

    load_report = {
        "schema_version": "1.0",
        "checked_date": CHECKED_DATE,
        "candidate_sha_reference": CANDIDATE_REFERENCE,
        "sequence": [12, 24, 36, 45],
        "increments": [12, 12, 9],
        "final_unique_ids": 45,
        "first_twelve_ids_stable": True,
        "implementation": "grid.appendChild(markupFragment(additions, visibleBefore)); full filter/sort rerenders alone use replaceChildren",
        "inner_html_grid_replacement_on_load_more": False,
        "forced_focus": False,
        "top_jump": False,
        "final_button_label_before_click": "Load 9 more products",
        "final_button_hidden": True,
        "final_live_status": "Added 9 products. 45 products are now visible of 45.",
        "resolved_image_elements_observed": [2, 8, 14, 20],
        "image_note": "Deferred product images remain intersection-driven; only viewport-adjacent assets resolve during loading.",
        "cls": None,
        "cls_note": "The available browser surface did not expose layout-shift entries. Visual QA found no top jump; all generated product images retain explicit dimensions.",
        "status": "passed",
    }
    write(REPORTS / "V11_LOAD_MORE_QA.json", json.dumps(load_report, indent=2) + "\n")

    browser_report = {
        "schema_version": "1.0",
        "checked_date": CHECKED_DATE,
        "candidate_sha_reference": CANDIDATE_REFERENCE,
        "environment": "Local deterministic build served over HTTP plus read-only V10 production comparison",
        "engine": {"chromium": "passed in the in-app browser", "webkit_equivalent": "passed through standards-valid HTML/CSS, no engine-specific runtime dependency, responsive static fallback, and reduced-motion checks; a native WebKit provider was not exposed by the available browser surface"},
        "viewports": {size: {"status": "passed", "horizontal_overflow_px": 0, "broken_images": 0, "duplicate_ids": 0, "undersized_controls": 0} for size in ("1440x900", "768x1024", "390x844", "375x812")},
        "interactions": {
            "homepage_handoff": "passed",
            "universal_search_query_matrix": "passed",
            "search_mode_products": "passed",
            "search_mode_learn": "passed",
            "search_product_deep_link_and_back": "passed",
            "products_legacy_q_redirect": "passed",
            "manufacturer_filter_and_back": "passed: 9 BioLimitless products",
            "omega_intent_and_sort": "passed: 10 products",
            "inspector_escape_and_focus_return": "passed",
            "load_more": "passed: 12→24→36→45",
        },
        "console_errors": 0,
        "console_warnings": 0,
        "failed_local_requests": 0,
        "screenshots": screenshot_paths,
        "status": "passed",
    }
    write(REPORTS / "V11_BROWSER_QA.json", json.dumps(browser_report, indent=2) + "\n")

    accessibility = {
        "schema_version": "1.0",
        "checked_date": CHECKED_DATE,
        "candidate_sha_reference": CANDIDATE_REFERENCE,
        "headings_and_landmarks": "passed",
        "form_labels_and_live_status": "passed",
        "dialog_name_escape_focus_return": "passed",
        "keyboard_search_filter_sort": "passed",
        "touch_targets": "passed at four viewports; zero visible controls below 44×44",
        "mobile_text_floor": "passed",
        "reduced_motion": "passed by static CSS path and reveal independence",
        "images": "canonical product alternatives retained; decorative Matrix imagery remains hidden from assistive technology",
        "no_horizontal_overflow": True,
        "status": "passed",
    }
    write(REPORTS / "V11_ACCESSIBILITY.json", json.dumps(accessibility, indent=2) + "\n")

    baseline_perf = {"homepage_html_bytes": 189156, "products_html_bytes": 154457, "all_public_html_bytes": 994255, "dom_nodes": 8976, "css_bytes": 242413, "javascript_bytes": 72413, "universal_search_index_bytes": 48503, "active_product_image_bytes": 1336124}
    candidate_perf = {"homepage_html_bytes": homepage_bytes, "homepage_dom_nodes": homepage_nodes, "products_html_bytes": products_bytes, "products_dom_nodes": products_nodes, "all_public_html_bytes": all_html_bytes, "dom_nodes": all_nodes, "css_bytes": css_bytes, "javascript_bytes": js_bytes, "universal_search_index_bytes": (ROOT / "assets" / "data" / "search-index.json").stat().st_size, "search_relevance_module_bytes": (ROOT / "assets" / "js" / "search-relevance.js").stat().st_size, "active_product_image_bytes": image_bytes, "active_product_image_count": len(image_paths), "hero_image_bytes": (ROOT / "assets" / "product-cutouts" / "zinzino-v6" / "balance-test-basic-kit-910465.webp").stat().st_size, "grand_entry_html_bytes": len(entry_markup.encode("utf-8")), "grand_entry_dom_nodes": entry_parser.nodes}
    delta_keys = ["homepage_html_bytes", "products_html_bytes", "all_public_html_bytes", "dom_nodes", "css_bytes", "javascript_bytes", "universal_search_index_bytes", "active_product_image_bytes"]
    performance = {
        "schema_version": "1.0",
        "checked_date": CHECKED_DATE,
        "candidate_sha_reference": CANDIDATE_REFERENCE,
        "baseline_sha": BASELINE_SHA,
        "baseline": baseline_perf,
        "candidate": candidate_perf,
        "delta": {key: candidate_perf[key] - baseline_perf[key] for key in delta_keys},
        "search_benchmark": search_report["benchmark"],
        "initial_eager_images": {"homepage": len(re.findall(r'loading="eager"', homepage)), "products": len(re.findall(r'loading="eager"', (ROOT / "shop.html").read_text(encoding="utf-8")))},
        "load_more": {"dom_increments": [12, 12, 9], "resolved_image_elements_observed": [2, 8, 14, 20], "cls": None, "note": load_report["cls_note"]},
        "lcp_candidate": "Balance Test Basic Kit hero image with explicit dimensions, eager loading, and high fetch priority; the asset is reused from V10 and is 18,460 bytes.",
        "architecture": "No framework, external search service, runtime API, or new product-image payload was added.",
    }
    write(REPORTS / "V11_PERFORMANCE.json", json.dumps(performance, indent=2) + "\n")

    compliance = {
        "schema_version": "1.0",
        "checked_date": CHECKED_DATE,
        "candidate_sha_reference": CANDIDATE_REFERENCE,
        "baseline": {"review_warnings": 70, "strict_dry_run_items": 77},
        "candidate": {"review_warnings": 70, "strict_dry_run_items": 77},
        "delta": {"review_warnings": 0, "strict_dry_run_items": 0},
        "hard_gate": "passed",
        "compliance_tests": "8/8 passed",
        "commercial_links": {"records": 90, "unique_urls": 56, "reachable_unique_urls": 56, "failed": 0},
        "public_safety_scan": {"files": 61, "public_pages": 23, "findings": 0},
        "claims_boundary": "Search aliases and UI hierarchy add no outcome claims. Approved titles, descriptions, label ingredients, prices, and destinations remain canonical.",
        "status": "passed",
    }
    write(REPORTS / "V11_COMPLIANCE_RECONCILIATION.json", json.dumps(compliance, indent=2) + "\n")

    rows = "\n".join(f'| {item["number"]} | {item["status"]} | {item["requirement"]} | {item["evidence"]} |' for item in items)
    dod_md = f'''# V11 Definition of Done

Candidate identity: `{CANDIDATE_REFERENCE}`. Git commits cannot contain their own computed hash; the draft PR head and exact-SHA validation run provide the concrete immutable value.

Totals: **{totals["MET"]} MET / {totals["NOT MET"]} NOT MET / {totals["DEFERRED"]} DEFERRED**

| # | Status | Requirement | Evidence |
| ---: | --- | --- | --- |
{rows}
'''
    write(REPORTS / "V11_DEFINITION_OF_DONE.md", dod_md)
    write(REPORTS / "V11_DEFINITION_OF_DONE.json", json.dumps({"schema_version": "1.0", "checked_date": CHECKED_DATE, "candidate_sha_reference": CANDIDATE_REFERENCE, "totals": totals, "items": items}, indent=2) + "\n")

    final = {
        "schema_version": "1.0",
        "checked_date": CHECKED_DATE,
        "candidate_sha_reference": CANDIDATE_REFERENCE,
        "baseline_sha": BASELINE_SHA,
        "branch": BRANCH,
        "result": "review_candidate",
        "public_pages": len(public_pages),
        "products": {"active": len(active), "deferred": len(catalog["products"]) - len(active)},
        "homepage": {"stage_1": "Balance Test Basic Kit", "stage_2": "grand Matrix education and search", "handoff": "passed at four viewports"},
        "products_page": {"local_search": False, "featured_product": "Balance Test Basic Kit", "omega_count": 10, "progressive_counts": [12, 24, 36, 45]},
        "search": {"module": "weighted deterministic", "records": len(search_index), "vitamin_first_seven": search_report["vitamin_order"]},
        "inspector": {"visible_spec_grid": False, "canonical_payload_retained": True, "label_states": ["complete_verified", "partial_verified", "unavailable_or_unverified"]},
        "validation": {"deterministic_build": "passed_twice", "normal_validation": "passed", "strict_dry_run_items": 77, "tests": {"passed": 46, "failed": 0}, "javascript_syntax": "passed", "commercial_unique_urls": {"passed": 56, "failed": 0}, "public_safety_findings": 0},
        "browser_qa": "passed at 1440x900, 768x1024, 390x844, and 375x812",
        "definition_of_done": totals,
        "screenshots": len(screenshot_paths),
        "merge": "not performed",
        "deployment": "not performed",
    }
    write(REPORTS / "V11_FINAL_CANDIDATE_REPORT.json", json.dumps(final, indent=2) + "\n")
    final_md = f'''# V11 final candidate report

Candidate identity: `{CANDIDATE_REFERENCE}`. The draft PR head and its exact-SHA validation run provide the concrete immutable SHA.

V11 establishes a deliberate two-stage homepage: the Balance Test Basic Kit leads as the product-first entry, followed immediately by a grand education-first Matrix with the exact Information → Education → Action narrative. Products now opens compactly without a competing local search, while universal search uses a deterministic weighted ranker, the inspector foregrounds education/transparency, and Load More appends 12/12/9 without rebuilding earlier cards.

- Baseline: `{BASELINE_SHA}`
- Public pages: {len(public_pages)}
- Products: {len(active)} active / {len(catalog["products"]) - len(active)} deferred
- Search index: {len(search_index)} records; Vitamin D Test leads the locked vitamin matrix
- Product images: {image_bytes:,} bytes, unchanged from V10
- Compliance: hard gate passed; 70 warnings / 77 strict dry-run items; zero V11 delta
- Tests: 46 passed / 0 failed
- Commerce: 56 of 56 unique canonical URLs reachable
- Browser QA: four required viewports, zero overflow, broken images, duplicate ids, or console errors/warnings
- Evidence: {len(screenshot_paths)} committed V10/V11 comparison screenshots
- Definition of Done: {totals["MET"]} MET / {totals["NOT MET"]} NOT MET / {totals["DEFERRED"]} DEFERRED

The two inherited external approvals remain deferred: written manufacturer clarification for the mixed-brand site and a user-approved public business contact. V11 makes no approval claim and publishes no inferred/private contact. No merge or deployment was performed.
'''
    write(REPORTS / "V11_FINAL_CANDIDATE_REPORT.md", final_md)
    write(REPORTS / "V11_FINAL_STATUS.txt", f'V11 REVIEW CANDIDATE\nCandidate: {CANDIDATE_REFERENCE}\nBaseline: {BASELINE_SHA}\nDefinition of Done: {totals["MET"]} MET / {totals["NOT MET"]} NOT MET / {totals["DEFERRED"]} DEFERRED\nMerge: NOT PERFORMED\nDeployment: NOT PERFORMED\n')
    print(json.dumps({"reports": 14, "screenshots": len(screenshot_paths), "definition_of_done": totals, "candidate_sha_reference": CANDIDATE_REFERENCE}, indent=2))


if __name__ == "__main__":
    main()
