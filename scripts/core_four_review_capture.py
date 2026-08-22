#!/usr/bin/env python3
"""Capture deterministic Core Four review states."""
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

VIEWPORTS = {"desktop-1440": {"width": 1440, "height": 900}, "tablet-768": {"width": 768, "height": 1024}, "mobile-390": {"width": 390, "height": 844}, "mobile-375": {"width": 375, "height": 812}}
PRODUCTS = ["balanceoil-plus-300ml", "biolimitless-vitamin-d3-k2", "biolimitless-zinc-copper", "biolimitless-magnesium-glycinate"]

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--base-url",required=True); parser.add_argument("--output-dir",type=Path,required=True); args=parser.parse_args(); args.output_dir.mkdir(parents=True,exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch()
        for label,viewport in VIEWPORTS.items():
            context=browser.new_context(viewport=viewport,reduced_motion="reduce"); page=context.new_page()
            for name,path in [("home","index.html"),("campaign","core-four.html"),("products","shop.html"),("library","library.html?collection=core-four"),("evidence","evidence.html?collection=core-four")]:
                page.goto(args.base_url.rstrip("/")+"/"+path,wait_until="networkidle")
                if name=="products": page.locator("[data-shop-collection]").click()
                page.screenshot(path=args.output_dir/f"{name}-{label}.png",full_page=True)
            if label in {"desktop-1440","mobile-375"}:
                for product in PRODUCTS:
                    page.goto(args.base_url.rstrip("/")+f"/products/{product}.html",wait_until="networkidle"); page.screenshot(path=args.output_dir/f"product-{product}-{label}.png",full_page=True)
                for query in ["core four","omega 3","d3k2","zinc copper","magnesium glycinate"]:
                    page.goto(args.base_url.rstrip("/")+"/explore.html",wait_until="networkidle"); page.locator("[data-search-input]").fill(query); page.locator("[data-search-form]").evaluate("form=>form.requestSubmit()"); page.wait_for_timeout(100); page.screenshot(path=args.output_dir/f"search-{query.replace(' ','-')}-{label}.png",full_page=True)
            context.close()
        browser.close()

if __name__=="__main__": main()
