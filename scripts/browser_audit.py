#!/usr/bin/env python3
"""Responsive browser audit for every canonical page, with four home screenshots."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

if __package__:
    from .site_paths import audited_page_paths, normalize_base_url
else:
    from site_paths import audited_page_paths, normalize_base_url

VIEWPORTS = {
    "desktop-1440": {"width": 1440, "height": 900},
    "tablet-768": {"width": 768, "height": 1024},
    "mobile-390": {"width": 390, "height": 844},
    "mobile-375": {"width": 375, "height": 812},
}


def library_checks(page) -> dict:
    query = page.locator("[data-library-query]")
    cards = page.locator("[data-library-article]:visible")
    initial = cards.count()
    query.fill("omega")
    search_count = cards.count()
    query.fill("zzzauditnomatch")
    checks = {
        "searchNarrowsResults": 0 < search_count < initial,
        "noResults": cards.count() == 0 and page.locator("[data-library-empty]").is_visible(),
    }
    query.fill("")
    category = page.locator("select[data-library-category]")
    choice = category.locator("option").nth(1).get_attribute("value")
    category.select_option(choice)
    checks["categoryFilters"] = cards.count() > 0 and cards.evaluate_all("(items, choice) => items.every(item => item.dataset.libraryCategory === choice)", choice)
    category.select_option("all")
    page.locator("button[data-library-core-four]").click()
    checks["coreFourFilters"] = 0 < cards.count() < initial and cards.evaluate_all("items => items.every(item => item.dataset.libraryCoreFour === 'true')") and "collection=core-four" in page.url
    page.locator("[data-library-controls] button[type=reset]").click()
    # Reset filtering is scheduled after the browser restores form defaults.
    page.wait_for_function("document.querySelector('[data-library-count]').textContent.startsWith(String(document.querySelectorAll('[data-library-article]').length) + ' ')")
    checks["clearRestoresAll"] = cards.count() == initial and "collection=" not in page.url and page.locator("button[data-library-core-four]").get_attribute("aria-pressed") == "false"
    checks["dockCurrentPage"] = page.locator(".mobile-dock [aria-current=page]").count() == 1
    return checks


def tablet_hero_checks(page) -> dict:
    """Check actual artwork, not just viewport overflow or image availability."""
    return page.evaluate("""() => {
        const img = document.querySelector('.hero-product__cutout img');
        const rect = img.getBoundingClientRect();
        const content = document.querySelector('.home-hero__content').getBoundingClientRect();
        const canvas = document.createElement('canvas');
        canvas.width = img.naturalWidth; canvas.height = img.naturalHeight;
        const context = canvas.getContext('2d');
        context.drawImage(img, 0, 0);
        const pixels = context.getImageData(0, 0, canvas.width, canvas.height).data;
        let left = canvas.width, top = canvas.height, right = -1, bottom = -1;
        for (let y = 0; y < canvas.height; y++) for (let x = 0; x < canvas.width; x++) {
            if (pixels[(y * canvas.width + x) * 4 + 3] <= 32) continue;
            left = Math.min(left, x); right = Math.max(right, x);
            top = Math.min(top, y); bottom = Math.max(bottom, y);
        }
        const scale = Math.min(rect.width / canvas.width, rect.height / canvas.height);
        const xOffset = rect.left + (rect.width - canvas.width * scale) / 2;
        const yOffset = rect.top + (rect.height - canvas.height * scale) / 2;
        const artwork = {left:xOffset + left * scale, right:xOffset + (right + 1) * scale,
            top:yOffset + top * scale, bottom:yOffset + (bottom + 1) * scale};
        const overlaps = (a, b) => a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
        const labels = ['.hero-product__caption', '.hero-product__tap', '.hero-product__signal', '.hero-data'];
        return {
            artworkMeasured: right >= left && bottom >= top,
            imageBeforeCopy: rect.bottom <= content.top,
            artworkBeforeCopy: artwork.bottom <= content.top,
            labelsClearOfPackaging: labels.every(selector => [...document.querySelectorAll(selector)].every(el =>
                !el.getClientRects().length || !overlaps(el.getBoundingClientRect(), artwork)))
        };
    }""")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--browser-channel", help="Optional installed browser, e.g. chrome, for local review")
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    paths = audited_page_paths(root)
    base = normalize_base_url(args.base_url)
    results = []
    motion_results = []
    all_console_errors: list[str] = []
    all_console_warnings: list[str] = []
    all_http_errors: list[dict] = []
    all_failed_requests: list[dict[str, str]] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(**({"channel": args.browser_channel} if args.browser_channel else {}))
        for viewport_name, viewport in VIEWPORTS.items():
            context = browser.new_context(viewport=viewport, reduced_motion="reduce")
            page = context.new_page()
            page.on("console", lambda message: all_console_errors.append(message.text) if message.type == "error" else None)
            page.on("console", lambda message: all_console_warnings.append(message.text) if message.type == "warning" else None)
            page.on("pageerror", lambda error: all_console_errors.append(str(error)))
            page.on("response", lambda response: all_http_errors.append({"url": response.url, "status": response.status}) if response.status >= 400 else None)
            def record_failed_request(request) -> None:
                error_text = request.failure or "unknown request failure"
                # Chromium cancels deferred image requests during the next page
                # navigation. Those browser lifecycle aborts are not network or
                # asset failures and made the scheduled audit report false alarms.
                if "ERR_ABORTED" not in error_text:
                    all_failed_requests.append({"url": request.url, "error": error_text})
            page.on("requestfailed", record_failed_request)
            for relative in paths:
                url = base + relative
                response = page.goto(url, wait_until="networkidle")
                metrics = page.evaluate("""() => ({
                    overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
                    brokenImages: [...document.images].filter(img => img.complete && img.naturalWidth === 0).map(img => img.currentSrc || img.src),
                    h1Count: document.querySelectorAll('h1').length,
                    duplicateIds: [...document.querySelectorAll('[id]')].map(el => el.id).filter((id, i, all) => all.indexOf(id) !== i),
                    unnamedControls: [...document.querySelectorAll('button,a,input,select')].filter(el => {
                      if (el.hidden || el.getAttribute('aria-hidden') === 'true') return false;
                      const labels = el.labels ? [...el.labels].map(label => label.textContent.trim()).join('') : '';
                      const imageAlt = el.querySelector ? [...el.querySelectorAll('img')].map(img => img.alt.trim()).join('') : '';
                      return !(el.getAttribute('aria-label') || el.textContent.trim() || el.getAttribute('title') || el.getAttribute('placeholder') || labels || imageAlt);
                    }).length
                })""")
                result = {"viewport": viewport_name, "path": relative or "index.html", "status": response.status if response else None, **metrics}
                if relative == "library.html":
                    result["libraryChecks"] = library_checks(page)
                    motion_results.append({"viewport": viewport_name, "motion": "reduce", "checks": result["libraryChecks"]})
                if relative == "explore.html":
                    search = page.locator("[data-search-input]")
                    search.fill("omega")
                    page.locator("[data-search-form]").evaluate("form => form.requestSubmit()")
                    page.wait_for_timeout(50)
                    result["searchChecks"] = {
                        "resultsVisible": page.locator("[data-search-results]").is_visible(),
                        "resultsPresent": page.locator("[data-search-results] .search-result").count() > 0,
                        "urlState": "q=omega" in page.url,
                    }
                if relative == "shop.html":
                    initial_visible = page.locator("[data-shop-product]:visible").count()
                    page.locator("[data-shop-sort]").select_option("name")
                    sorted_names = page.locator("[data-shop-product]:visible h2").all_text_contents()
                    sort_ok = sorted_names == sorted(sorted_names, key=str.casefold)
                    load_button = page.locator("[data-shop-load-more]")
                    if load_button.is_visible():
                        load_button.click()
                    loaded_visible = page.locator("[data-shop-product]:visible").count()
                    page.locator("[data-product-open]:visible").first.click()
                    inspector_open = page.locator("[data-product-inspector]").evaluate("dialog => dialog.open")
                    page.keyboard.press("Escape")
                    result["shopChecks"] = {
                        "sortApplied": sort_ok and "sort=name" in page.url,
                        "loadMoreAppendOnly": loaded_visible > initial_visible,
                        "inspectorOpened": inspector_open,
                    }
                if not relative:
                    if 704.16 <= viewport["width"] <= 896:
                        result["tabletHeroChecks"] = tablet_hero_checks(page)
                    result["mobileHeroChecks"] = page.evaluate(r"""() => ({
                        productNamePresent: document.body.innerText.includes('Balance Test Basic Kit'),
                        featuredJourneyPresent: /featured testing journey/i.test(document.body.innerText),
                        forbiddenSkuAbsent: !/kit\s*\/\s*sku/i.test(document.body.innerText),
                        heroVisible: !!document.querySelector('.hero-product') && document.querySelector('.hero-product').getBoundingClientRect().height > 0
                    })""")
                    page.screenshot(path=output / f"home-{viewport_name}.png", full_page=False)
                results.append(result)
            context.close()
            context = browser.new_context(viewport=viewport, reduced_motion="no-preference")
            page = context.new_page()
            page.on("console", lambda message: all_console_errors.append(message.text) if message.type == "error" else all_console_warnings.append(message.text) if message.type == "warning" else None)
            page.on("pageerror", lambda error: all_console_errors.append(str(error)))
            page.on("response", lambda response: all_http_errors.append({"url": response.url, "status": response.status}) if response.status >= 400 else None)
            page.on("requestfailed", record_failed_request)
            page.goto(base + "library.html", wait_until="networkidle")
            motion_results.append({"viewport": viewport_name, "motion": "no-preference", "checks": library_checks(page)})
            context.close()
        browser.close()
    payload = {"viewports": VIEWPORTS, "pages_per_viewport": len(paths), "results": results, "library_motion_results": motion_results}
    payload["summary"] = {
        "overflow_failures": sum(item["overflow"] for item in results),
        "broken_images": sum(len(item["brokenImages"]) for item in results),
        "bad_h1_counts": sum(item["h1Count"] != 1 for item in results),
        "duplicate_ids": sum(len(item["duplicateIds"]) for item in results),
        "unnamed_controls": sum(item["unnamedControls"] for item in results),
        "console_errors": all_console_errors,
        "console_warnings": all_console_warnings,
        "http_errors": all_http_errors,
        "bad_page_statuses": sum(item["status"] != 200 for item in results),
        "coverage_failures": int(len(results) != len(paths) * len(VIEWPORTS) or not results or len(motion_results) != 2 * len(VIEWPORTS)),
        "library_motion_failures": sum(not value for result in motion_results for value in result["checks"].values()),
        "failed_requests": all_failed_requests,
        "functional_failures": sum(
            not value
            for item in results
            for group in (item.get("searchChecks", {}), item.get("shopChecks", {}), item.get("mobileHeroChecks", {}), item.get("tabletHeroChecks", {}))
            for value in group.values()
        ),
    }
    (output / "browser-audit.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload["summary"], indent=2))
    if any((payload["summary"][key] for key in ("overflow_failures", "broken_images", "bad_h1_counts", "duplicate_ids", "unnamed_controls", "functional_failures", "bad_page_statuses", "coverage_failures", "library_motion_failures"))) or all_console_errors or all_console_warnings or all_http_errors or all_failed_requests:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
