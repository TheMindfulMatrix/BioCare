#!/usr/bin/env python3
"""Rendered, responsive, lazy-load, accessibility, and external fallback QA for V6."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "v6" / "finish-browser-qa.json"
EXTERNAL_REPORT = ROOT / "reports" / "v6" / "finish-external-links.json"
EVIDENCE = Path("/tmp/v6-finish-review")
PORT = 8026
BASE = f"http://127.0.0.1:{PORT}/BioCare"
CHECKED_DATE = "2026-08-20"
VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900},
    "tablet": {"width": 768, "height": 1024},
    "mobile390": {"width": 390, "height": 844},
    "mobile375": {"width": 375, "height": 812},
}
PAGES = {
    "home": "index.html",
    "shop": "shop.html",
    "library": "library.html",
    "start": "start.html",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def start_server() -> subprocess.Popen[str]:
    process = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--directory", str(ROOT.parent)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    deadline = time.time() + 15
    while time.time() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Local HTTP server exited before QA")
        try:
            import urllib.request
            urllib.request.urlopen(f"{BASE}/index.html", timeout=1).close()
            return process
        except Exception:
            time.sleep(0.2)
    process.terminate()
    raise RuntimeError("Local HTTP server did not start")


def add_observers(page: Page) -> None:
    page.add_init_script(
        r"""
        window.__finishPerf = {cls: 0, lcp: null};
        try {
          new PerformanceObserver(list => {
            for (const entry of list.getEntries()) {
              if (!entry.hadRecentInput) window.__finishPerf.cls += entry.value;
            }
          }).observe({type: 'layout-shift', buffered: true});
          new PerformanceObserver(list => {
            const entries = list.getEntries();
            const last = entries[entries.length - 1];
            if (last) window.__finishPerf.lcp = last.startTime;
          }).observe({type: 'largest-contentful-paint', buffered: true});
        } catch (error) {}
        """
    )


def lazy_state(page: Page) -> dict[str, int]:
    return page.evaluate(
        r"""
        (() => ({
          lazy_total: [...document.images].filter(img => img.loading === 'lazy').length,
          lazy_incomplete: [...document.images].filter(img => img.loading === 'lazy' && (!img.complete || img.naturalWidth === 0)).length,
          unrevealed: [...document.querySelectorAll('[data-reveal]')].filter(el => !el.classList.contains('is-visible')).length,
        }))()
        """
    )


def stable_scroll(page: Page) -> dict[str, Any]:
    before = lazy_state(page)
    height = page.evaluate("document.documentElement.scrollHeight")
    step = max(280, int(page.viewport_size["height"] * 0.7))
    position = 0
    while position < height:
        page.evaluate("y => window.scrollTo(0, y)", position)
        page.wait_for_timeout(100)
        height = max(height, page.evaluate("document.documentElement.scrollHeight"))
        position += step
    page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
    page.wait_for_timeout(700)
    page.wait_for_function(
        "[...document.images].every(img => img.complete)", timeout=30000
    )
    page.wait_for_timeout(300)
    after = lazy_state(page)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(350)
    return {"before_scroll": before, "after_scroll": after}


def visible_text_metrics(page: Page) -> dict[str, Any]:
    return page.evaluate(
        r"""
        (() => {
          const rows=[];
          for (const el of document.querySelectorAll('body *')) {
            const style=getComputedStyle(el), rect=el.getBoundingClientRect();
            if (style.display==='none' || style.visibility==='hidden' || Number(style.opacity)===0 || rect.width<=0 || rect.height<=0) continue;
            const own=[...el.childNodes].filter(n=>n.nodeType===Node.TEXT_NODE).map(n=>n.textContent.trim()).join(' ').trim();
            if (!own) continue;
            const size=parseFloat(style.fontSize);
            rows.push({tag:el.tagName, selector:el.id ? '#'+el.id : el.className && typeof el.className==='string' ? '.'+el.className.trim().replace(/\s+/g,'.') : el.tagName.toLowerCase(), text:own.slice(0,140), size});
          }
          rows.sort((a,b)=>a.size-b.size);
          return {count:rows.length, minimum:rows.length ? rows[0].size : null, under12:rows.filter(row=>row.size<11.999).length, worst:rows.slice(0,20)};
        })()
        """
    )


def interactive_metrics(page: Page) -> dict[str, Any]:
    return page.evaluate(
        r"""
        (() => {
          const rows=[...document.querySelectorAll('a[href],button,summary,input,select,textarea')]
            .filter(el => { const s=getComputedStyle(el), r=el.getBoundingClientRect(); return s.display!=='none' && s.visibility!=='hidden' && Number(s.opacity)!==0 && r.width>0 && r.height>0; })
            .map(el => { const r=el.getBoundingClientRect(); return {tag:el.tagName, text:(el.getAttribute('aria-label')||el.textContent||'').trim().replace(/\s+/g,' ').slice(0,160), width:r.width, height:r.height}; });
          const undersized=rows.filter(row=>row.width<43.5 || row.height<43.5).sort((a,b)=>Math.min(a.width,a.height)-Math.min(b.width,b.height));
          return {total:rows.length, under44:undersized.length, worst:undersized.slice(0,20)};
        })()
        """
    )


def page_metrics(page: Page, page_name: str, viewport_name: str) -> dict[str, Any]:
    console_errors: list[str] = []
    console_warnings: list[str] = []
    failed_requests: list[str] = []
    page.on(
        "console",
        lambda message: console_errors.append(message.text)
        if message.type == "error"
        else console_warnings.append(message.text)
        if message.type == "warning"
        else None,
    )
    page.on(
        "requestfailed",
        lambda request: failed_requests.append(
            f"{request.url}: {request.failure or 'request failed'}"
        ),
    )
    response = page.goto(
        f"{BASE}/{PAGES[page_name]}", wait_until="networkidle", timeout=60000
    )
    page.wait_for_timeout(600)
    lazy_observation = stable_scroll(page)
    result: dict[str, Any] = {
        "page": page_name,
        "viewport": viewport_name,
        "status": response.status if response else None,
        "horizontal_overflow": page.evaluate(
            "document.documentElement.scrollWidth > document.documentElement.clientWidth + 1"
        ),
        "duplicate_ids": page.evaluate(
            r"""(() => { const ids=[...document.querySelectorAll('[id]')].map(el=>el.id); return [...new Set(ids.filter((id,index)=>ids.indexOf(id)!==index))]; })()"""
        ),
        "broken_images": page.evaluate(
            "[...document.images].filter(img=>img.complete && img.naturalWidth===0).map(img=>img.currentSrc||img.src)"
        ),
        "console_errors": console_errors,
        "console_warnings": console_warnings,
        "failed_requests": failed_requests,
        "perf": page.evaluate("window.__finishPerf || {cls:null,lcp:null}"),
        "lazy_observation": lazy_observation,
    }
    if viewport_name.startswith("mobile"):
        result["text_metrics"] = visible_text_metrics(page)
        result["interactive_metrics"] = interactive_metrics(page)
        toggle = page.locator(".nav-toggle")
        if toggle.count():
            toggle.focus()
            toggle.press("Enter")
            page.wait_for_timeout(100)
            result["mobile_menu_opened"] = toggle.get_attribute("aria-expanded") == "true"
            page.keyboard.press("Escape")
            page.wait_for_timeout(100)
            result["mobile_menu_closed_with_escape"] = toggle.get_attribute("aria-expanded") == "false"

    if page_name == "home":
        result.update(
            page.evaluate(
                r"""
                (() => {
                  const roster=[...document.querySelectorAll('[data-universe-select]')];
                  const intents=[...document.querySelectorAll('[data-universe-intent]')];
                  const bg=document.querySelector('.hero-product__background');
                  const stage=document.querySelector('.hero-product__stage');
                  const bgr=bg?.getBoundingClientRect(), sr=stage?.getBoundingClientRect();
                  return {
                    universe_panels_in_dom: document.querySelectorAll('[data-universe-product]').length,
                    universe_roster_buttons: roster.length,
                    universe_intents: intents.length,
                    hero_clarity_text_present: /practical system for taking a more informed role/i.test(document.body.textContent) && /test\s*→\s*understand\s*→\s*decide/i.test(document.body.textContent),
                    hero_asset: bg && stage ? {
                      src: bg.getAttribute('src'),
                      natural_dimensions: [bg.naturalWidth,bg.naturalHeight],
                      rendered_dimensions: [bgr.width,bgr.height],
                      stage_dimensions: [sr.width,sr.height],
                      rendered_aspect_ratio: bgr.width/bgr.height,
                      source_aspect_ratio: bg.naturalWidth/bg.naturalHeight,
                      ratio_matches: Math.abs((bgr.width/bgr.height)-(bg.naturalWidth/bg.naturalHeight)) < 0.012,
                      object_fit: getComputedStyle(bg).objectFit,
                      loading: bg.loading,
                      fetchpriority: bg.getAttribute('fetchpriority') || 'auto',
                    } : null,
                  };
                })()
                """
            )
        )
        seen: set[str] = set()
        stale: list[str] = []
        buttons = page.locator("[data-universe-select]")
        for index in range(buttons.count()):
            button = buttons.nth(index)
            product_id = button.get_attribute("data-universe-select")
            intent = button.get_attribute("data-product-intent")
            if intent:
                intent_button = page.locator(f'[data-universe-intent="{intent}"]')
                if intent_button.count() and button.is_hidden():
                    intent_button.click()
                    page.wait_for_timeout(20)
            if button.is_visible():
                button.click()
                page.wait_for_timeout(20)
                active = page.locator("[data-universe-product]").first.get_attribute("data-universe-product")
                if active:
                    seen.add(active)
                if product_id and active != product_id:
                    stale.append(f"expected {product_id}, saw {active}")
        result["universe_products_selected"] = len(seen)
        result["universe_stale_failures"] = stale

    if page_name == "shop":
        result.update(
            page.evaluate(
                r"""
                (() => ({
                  product_cards: document.querySelectorAll('article.shop-product').length,
                  price_modules: document.querySelectorAll('.product-price').length,
                  label_panels: document.querySelectorAll('details.product-label-panel').length,
                  manufacturer_panels: document.querySelectorAll('details.manufacturer-transparency').length,
                  reference_prices: document.querySelectorAll('.product-price__item--reference').length,
                  reference_line_through: [...document.querySelectorAll('.product-price__item--reference strong')].every(el=>getComputedStyle(el).textDecorationLine.includes('line-through')),
                  source_name_failures: [...document.querySelectorAll('.product-price__source')].filter(a=>!/^Official price source for .+ \(opens in a new tab\)$/i.test(a.getAttribute('aria-label')||'')).length,
                  view_name_failures: [...document.querySelectorAll('.shop-product a.button-primary')].filter(a=>!/(View product:|Get the kit:).+\(opens in a new tab\)/i.test(a.getAttribute('aria-label')||'')).length,
                }))()
                """
            )
        )
        if page.locator("details.product-label-panel summary").count():
            summary = page.locator("details.product-label-panel summary").first
            summary.focus()
            summary.press("Enter")
            page.wait_for_timeout(80)
            result["label_keyboard_open"] = page.locator("details.product-label-panel").first.get_attribute("open") is not None
            summary.press("Enter")
        if page.locator("details.manufacturer-transparency summary").count():
            summary = page.locator("details.manufacturer-transparency summary").first
            summary.focus()
            summary.press("Enter")
            page.wait_for_timeout(80)
            result["manufacturer_keyboard_open"] = page.locator("details.manufacturer-transparency").first.get_attribute("open") is not None
            summary.press("Enter")

    return result


def browser_fallback(browser: Any) -> list[dict[str, Any]]:
    if not EXTERNAL_REPORT.exists():
        return []
    data = load_json(EXTERNAL_REPORT)
    candidates = [item for item in data["items"] if item.get("status") != 200]
    if not candidates:
        return []
    context = browser.new_context(
        ignore_https_errors=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151 Safari/537.36",
    )
    page = context.new_page()
    output = []
    for item in candidates:
        row = {"url": item["url"], "status": None, "final_url": None, "error": None}
        try:
            response = page.goto(item["url"], wait_until="domcontentloaded", timeout=35000)
            page.wait_for_timeout(500)
            row["status"] = response.status if response else None
            row["final_url"] = page.url
        except Exception as error:
            row["error"] = f"{type(error).__name__}: {error}"
            row["final_url"] = page.url
        output.append(row)
    context.close()
    return output


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    server = start_server()
    try:
        with sync_playwright() as playwright:
            launch_kwargs: dict[str, Any] = {"headless": True}
            executable = shutil.which("chromium") or shutil.which("google-chrome")
            if executable:
                launch_kwargs["executable_path"] = executable
            browser = playwright.chromium.launch(**launch_kwargs)
            pages: list[dict[str, Any]] = []
            required_shots = {
                ("home", "desktop"): "homepage-desktop.png",
                ("home", "mobile375"): "homepage-mobile-375.png",
                ("shop", "desktop"): "shop-desktop.png",
                ("shop", "mobile375"): "shop-mobile-375.png",
            }
            for viewport_name, viewport in VIEWPORTS.items():
                page_names = PAGES if viewport_name in {"desktop", "mobile390", "mobile375"} else {"home": PAGES["home"], "shop": PAGES["shop"]}
                for page_name in page_names:
                    context = browser.new_context(viewport=viewport, device_scale_factor=1, reduced_motion="reduce")
                    page = context.new_page()
                    add_observers(page)
                    metrics = page_metrics(page, page_name, viewport_name)
                    pages.append(metrics)
                    shot = required_shots.get((page_name, viewport_name))
                    if shot:
                        page.screenshot(path=str(EVIDENCE / shot), full_page=True)
                    context.close()
            external_browser_results = browser_fallback(browser)
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=10)

    mobile375 = [item for item in pages if item["viewport"] == "mobile375"]
    mobile390 = [item for item in pages if item["viewport"] == "mobile390"]
    all_lazy_before = sum(item["lazy_observation"]["before_scroll"]["lazy_incomplete"] for item in pages)
    all_lazy_after = sum(item["lazy_observation"]["after_scroll"]["lazy_incomplete"] for item in pages)
    all_reveal_before = sum(item["lazy_observation"]["before_scroll"]["unrevealed"] for item in pages)
    all_reveal_after = sum(item["lazy_observation"]["after_scroll"]["unrevealed"] for item in pages)
    blank_diagnosis = (
        "Previous large blank screenshot regions were capture artifacts: offscreen lazy images and IntersectionObserver reveal elements existed in the DOM before scrolling and resolved after a normal full-document scroll. The production lazy/reveal behavior remains enabled."
        if (all_lazy_before or all_reveal_before) and not all_lazy_after and not all_reveal_after
        else "No unresolved lazy-image or reveal-state gap remained after the full-document exercise; screenshots represent the stable rendered page."
    )
    summary = {
        "pages_checked": len(pages),
        "overflow_failures": sum(item["horizontal_overflow"] for item in pages),
        "broken_images": sum(len(item["broken_images"]) for item in pages),
        "console_errors": sum(len(item["console_errors"]) for item in pages),
        "console_warnings": sum(len(item["console_warnings"]) for item in pages),
        "failed_requests": sum(len(item["failed_requests"]) for item in pages),
        "duplicate_ids": sum(len(item["duplicate_ids"]) for item in pages),
        "minimum_font_size_375": min(item["text_metrics"]["minimum"] for item in mobile375 if item.get("text_metrics", {}).get("minimum") is not None),
        "under12_375": sum(item["text_metrics"]["under12"] for item in mobile375),
        "under44_375": sum(item["interactive_metrics"]["under44"] for item in mobile375),
        "under44_390": sum(item["interactive_metrics"]["under44"] for item in mobile390),
        "hero_clarity_failures": sum(not item.get("hero_clarity_text_present", True) for item in pages if item["page"] == "home"),
        "universe_products_selected": min(item.get("universe_products_selected", 45) for item in pages if item["page"] == "home"),
        "universe_intents": min(item.get("universe_intents", 6) for item in pages if item["page"] == "home"),
        "universe_stale_failures": sum(len(item.get("universe_stale_failures", [])) for item in pages if item["page"] == "home"),
        "external_browser_fallbacks": len(external_browser_results),
        "external_browser_200": sum(item.get("status") == 200 for item in external_browser_results),
    }
    output = {
        "generated_at": CHECKED_DATE,
        "viewports": VIEWPORTS,
        "pages": pages,
        "external_browser_results": external_browser_results,
        "blank_region_diagnosis": blank_diagnosis,
        "lazy_state_totals": {
            "incomplete_before": all_lazy_before,
            "incomplete_after": all_lazy_after,
            "unrevealed_before": all_reveal_before,
            "unrevealed_after": all_reveal_after,
        },
        "summary": summary,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    failures = []
    for key in (
        "overflow_failures", "broken_images", "console_errors", "console_warnings",
        "failed_requests", "duplicate_ids", "under12_375", "under44_375",
        "under44_390", "hero_clarity_failures", "universe_stale_failures",
    ):
        if summary[key]:
            failures.append(f"{key}={summary[key]}")
    if summary["universe_products_selected"] != 45:
        failures.append(f"universe_products_selected={summary['universe_products_selected']}")
    if summary["universe_intents"] != 6:
        failures.append(f"universe_intents={summary['universe_intents']}")
    for item in pages:
        if item["page"] == "shop":
            for key, expected in (
                ("product_cards", 45), ("price_modules", 45), ("label_panels", 4),
                ("manufacturer_panels", 45), ("source_name_failures", 0), ("view_name_failures", 0),
            ):
                if item.get(key) != expected:
                    failures.append(f"{item['viewport']} shop {key}={item.get(key)} expected {expected}")
            if not item.get("reference_line_through"):
                failures.append(f"{item['viewport']} reference price line-through missing")
            if not item.get("label_keyboard_open"):
                failures.append(f"{item['viewport']} label details keyboard interaction failed")
            if not item.get("manufacturer_keyboard_open"):
                failures.append(f"{item['viewport']} manufacturer details keyboard interaction failed")
    print(json.dumps(summary, indent=2))
    if failures:
        raise SystemExit("Browser QA failed: " + "; ".join(failures))


if __name__ == "__main__":
    main()
