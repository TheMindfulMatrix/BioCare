#!/usr/bin/env python3
"""Responsive browser audit for every canonical page, with four home screenshots."""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

VIEWPORTS = {
    "desktop-1440": {"width": 1440, "height": 900},
    "tablet-768": {"width": 768, "height": 1024},
    "mobile-390": {"width": 390, "height": 844},
    "mobile-375": {"width": 375, "height": 812},
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    sitemap = ET.parse(root / "sitemap.xml").getroot()
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    paths = [urlsplit(node.text or "").path.split("/BioCare/", 1)[-1] for node in sitemap.findall("s:url/s:loc", namespace)]
    results = []
    all_console_errors: list[str] = []
    all_failed_requests: list[dict[str, str]] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for viewport_name, viewport in VIEWPORTS.items():
            context = browser.new_context(viewport=viewport, reduced_motion="reduce")
            page = context.new_page()
            page.on("console", lambda message: all_console_errors.append(message.text) if message.type == "error" else None)
            def record_failed_request(request) -> None:
                error_text = request.failure or "unknown request failure"
                # Chromium cancels deferred image requests during the next page
                # navigation. Those browser lifecycle aborts are not network or
                # asset failures and made the scheduled audit report false alarms.
                if "ERR_ABORTED" not in error_text:
                    all_failed_requests.append({"url": request.url, "error": error_text})
            page.on("requestfailed", record_failed_request)
            for relative in paths:
                url = args.base_url.rstrip("/") + "/" + relative
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
                    result["mobileHeroChecks"] = page.evaluate(r"""() => ({
                        productNamePresent: document.body.innerText.includes('Balance Test Basic Kit'),
                        featuredJourneyPresent: /featured testing journey/i.test(document.body.innerText),
                        forbiddenSkuAbsent: !/kit\s*\/\s*sku/i.test(document.body.innerText),
                        heroVisible: !!document.querySelector('.hero-product') && document.querySelector('.hero-product').getBoundingClientRect().height > 0
                    })""")
                    page.screenshot(path=output / f"home-{viewport_name}.png", full_page=False)
                results.append(result)
            context.close()
        browser.close()
    payload = {"viewports": VIEWPORTS, "pages_per_viewport": len(paths), "results": results}
    payload["summary"] = {
        "overflow_failures": sum(item["overflow"] for item in results),
        "broken_images": sum(len(item["brokenImages"]) for item in results),
        "bad_h1_counts": sum(item["h1Count"] != 1 for item in results),
        "duplicate_ids": sum(len(item["duplicateIds"]) for item in results),
        "unnamed_controls": sum(item["unnamedControls"] for item in results),
        "console_errors": all_console_errors,
        "failed_requests": all_failed_requests,
        "functional_failures": sum(
            not value
            for item in results
            for group in (item.get("searchChecks", {}), item.get("shopChecks", {}), item.get("mobileHeroChecks", {}))
            for value in group.values()
        ),
    }
    (output / "browser-audit.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(payload["summary"], indent=2))
    if any((payload["summary"][key] for key in ("overflow_failures", "broken_images", "bad_h1_counts", "duplicate_ids", "unnamed_controls", "functional_failures"))) or all_console_errors or all_failed_requests:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
