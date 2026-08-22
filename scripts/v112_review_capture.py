#!/usr/bin/env python3
"""Capture deterministic representative V11.2 review states."""
from __future__ import annotations
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

STATES = [
    ("product-balance-kit", "products/balance-basic-kit.html"),
    ("product-omega", "products/balanceoil-plus-300ml.html"),
    ("product-gut", "products/zinobiotic-plus.html"),
    ("product-biolimitless", "products/biolimitless-magnesium-glycinate.html"),
    ("library-filtering", "library.html"),
    ("evidence-connectivity", "evidence.html"),
    ("department-omega", "departments/omega-nutrition.html"),
]
VIEWPORTS = {"desktop-1440": {"width": 1440, "height": 1000}, "mobile-390": {"width": 390, "height": 844}, "mobile-375": {"width": 375, "height": 812}}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(); args.output_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for viewport_name, viewport in VIEWPORTS.items():
            context = browser.new_context(viewport=viewport, reduced_motion="reduce")
            page = context.new_page()
            for label, path in STATES:
                page.goto(args.base_url.rstrip("/") + "/" + path, wait_until="networkidle")
                if label == "library-filtering":
                    page.locator("[data-library-query]").fill("omega")
                page.screenshot(path=args.output_dir / f"{label}-{viewport_name}.png", full_page=True)
            page.goto(args.base_url.rstrip("/") + "/explore.html", wait_until="networkidle")
            page.locator("[data-search-input]").fill("omega")
            page.locator("[data-search-form]").evaluate("form => form.requestSubmit()")
            page.wait_for_timeout(100)
            page.screenshot(path=args.output_dir / f"search-results-{viewport_name}.png", full_page=True)
            context.close()
        browser.close()

if __name__ == "__main__": main()
