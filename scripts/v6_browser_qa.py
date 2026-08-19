#!/usr/bin/env python3
"""Rendered V6 QA for the review branch.

The script starts local V5.1 and V6 servers, exercises responsive/navigation/
Product Universe behavior, checks unresolved commercial links in Chromium, and
writes review-only screenshots under /tmp plus a committed JSON result.
"""
from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "b5d35772e98580e253c08f6319aa8e412fa20aea"
REPORT_DIR = ROOT / "reports" / "v6"
REVIEW_DIR = Path(os.environ.get("V6_REVIEW_DIR", "/tmp/v6-review"))
OUTPUT = REPORT_DIR / "browser-qa.json"
COMMERCE = REPORT_DIR / "commerce-verification.json"

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


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def start_server(directory: Path, port: int) -> subprocess.Popen[str]:
    process = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--directory", str(directory)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True,
    )
    deadline = time.time() + 15
    while time.time() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"HTTP server exited early for {directory}")
        import urllib.request
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1).close()
            return process
        except Exception:
            time.sleep(0.2)
    process.terminate()
    raise RuntimeError(f"HTTP server did not start for {directory}")


def make_baseline_worktree() -> Path:
    parent = Path("/tmp/v6-baseline")
    if parent.exists():
        shutil.rmtree(parent)
    parent.mkdir(parents=True, exist_ok=True)
    target = parent / "BioCare"
    subprocess.run(["git", "worktree", "add", "--detach", str(target), BASELINE], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return target


def add_observers(page: Page) -> None:
    page.add_init_script("""
      window.__v6perf = {cls: 0, lcp: null};
      try {
        new PerformanceObserver(list => {
          for (const entry of list.getEntries()) {
            if (!entry.hadRecentInput) window.__v6perf.cls += entry.value;
          }
        }).observe({type: 'layout-shift', buffered: true});
        new PerformanceObserver(list => {
          const entries = list.getEntries();
          const last = entries[entries.length - 1];
          if (last) window.__v6perf.lcp = last.startTime;
        }).observe({type: 'largest-contentful-paint', buffered: true});
      } catch (e) {}
    """)


def screenshot(page: Page, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(path), full_page=True)


def side_by_side(left: Path, right: Path, output: Path, title: str) -> None:
    with Image.open(left).convert("RGB") as a, Image.open(right).convert("RGB") as b:
        width = a.width + b.width
        height = max(a.height, b.height) + 48
        canvas = Image.new("RGB", (width, height), "#f4efe4")
        canvas.paste(a, (0, 48)); canvas.paste(b, (a.width, 48))
        draw = ImageDraw.Draw(canvas); font = ImageFont.load_default()
        draw.text((12, 12), f"V5.1 · {title}", fill="#172019", font=font)
        draw.text((a.width + 12, 12), f"V6 · {title}", fill="#172019", font=font)
        output.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(output, "JPEG", quality=85)


def page_checks(page: Page, page_name: str, viewport_name: str) -> dict[str, Any]:
    console_errors: list[str] = []
    console_warnings: list[str] = []
    failed_requests: list[str] = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else console_warnings.append(msg.text) if msg.type == "warning" else None)
    page.on("requestfailed", lambda request: failed_requests.append(f"{request.url}: {request.failure}"))

    response = page.goto(f"http://127.0.0.1:8010/BioCare/{PAGES[page_name]}", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(900)
    status = response.status if response else None
    overflow = page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 1")
    duplicate_ids = page.evaluate("""
      (() => { const ids=[...document.querySelectorAll('[id]')].map(n=>n.id); return ids.filter((id,i)=>ids.indexOf(id)!==i); })()
    """)
    broken_images = page.evaluate("""
      [...document.images].filter(img => img.complete && img.naturalWidth === 0).map(img => img.currentSrc || img.src)
    """)
    perf = page.evaluate("window.__v6perf || {cls:null,lcp:null}")
    result: dict[str, Any] = {
        "page": page_name, "viewport": viewport_name, "status": status,
        "horizontal_overflow": bool(overflow), "duplicate_ids": duplicate_ids,
        "broken_images": broken_images, "console_errors": console_errors,
        "console_warnings": console_warnings, "failed_requests": failed_requests,
        "local_lcp_ms": perf.get("lcp"), "local_cls": perf.get("cls"),
    }

    # Navigation and touch geometry on mobile.
    if viewport_name.startswith("mobile"):
        toggle = page.locator(".nav-toggle")
        if toggle.count():
            toggle.focus(); toggle.press("Enter"); page.wait_for_timeout(100)
            result["mobile_menu_opened"] = toggle.get_attribute("aria-expanded") == "true"
            page.keyboard.press("Escape"); page.wait_for_timeout(100)
            result["mobile_menu_closed_with_escape"] = toggle.get_attribute("aria-expanded") == "false"
        targets = page.evaluate("""
          [...document.querySelectorAll('a,button,summary,input,select,textarea')]
            .filter(el => { const s=getComputedStyle(el), r=el.getBoundingClientRect(); return s.display!=='none' && s.visibility!=='hidden' && r.width>0 && r.height>0; })
            .map(el => { const r=el.getBoundingClientRect(); return {tag:el.tagName, text:(el.getAttribute('aria-label')||el.textContent||'').trim().slice(0,100), w:r.width, h:r.height}; })
            .filter(x => x.w < 44 || x.h < 44)
        """)
        result["undersized_targets"] = targets

    if page_name == "shop":
        result["product_cards"] = page.locator(".shop-product").count()
        result["price_modules"] = page.locator(".product-price").count()
        result["label_panels"] = page.locator("details.product-label-panel").count()
        result["reference_prices"] = page.locator(".product-price__item--reference").count()
        result["reference_line_through"] = page.evaluate("""
          [...document.querySelectorAll('.product-price__item--reference strong')].every(el => getComputedStyle(el).textDecorationLine.includes('line-through'))
        """)
        if result["label_panels"]:
            summary = page.locator("details.product-label-panel summary").first
            summary.focus(); summary.press("Enter"); page.wait_for_timeout(100)
            result["label_panel_keyboard_open"] = page.locator("details.product-label-panel").first.get_attribute("open") is not None
            summary.press("Enter")
        result["source_link_aria_failures"] = page.evaluate("""
          [...document.querySelectorAll('.product-price__source')].filter(a => !/Official price source for /i.test(a.getAttribute('aria-label')||'')).length
        """)

    if page_name == "home":
        result["universe_panels_in_dom"] = page.locator("[data-universe-product]").count()
        result["universe_roster_buttons"] = page.locator("[data-universe-select]").count()
        result["universe_intents"] = page.locator("[data-universe-intent]").count()
        buttons = page.locator("[data-universe-select]")
        ids_seen: set[str] = set()
        stale_failures: list[str] = []
        for index in range(buttons.count()):
            button = buttons.nth(index)
            product_id = button.get_attribute("data-universe-select")
            if button.is_hidden():
                # Activate the button's intent first.
                intent = button.get_attribute("data-product-intent")
                if intent:
                    intent_button = page.locator(f'[data-universe-intent="{intent}"]')
                    if intent_button.count():
                        intent_button.click(); page.wait_for_timeout(40)
            if button.is_visible():
                button.click(); page.wait_for_timeout(35)
                active = page.locator("[data-universe-product]").first.get_attribute("data-universe-product")
                if active:
                    ids_seen.add(active)
                if product_id and active != product_id:
                    stale_failures.append(f"expected {product_id}, saw {active}")
        result["universe_products_selected"] = len(ids_seen)
        result["universe_stale_failures"] = stale_failures
        step_next = page.locator('[data-universe-step="next"]')
        if step_next.count():
            before = page.locator("[data-universe-product]").first.get_attribute("data-universe-product")
            step_next.click(); page.wait_for_timeout(80)
            after = page.locator("[data-universe-product]").first.get_attribute("data-universe-product")
            result["universe_next_control"] = before != after
        result["hero_clarity_text_present"] = page.evaluate("""
          /get informed/i.test(document.querySelector('.hero-copy')?.textContent || document.body.textContent) &&
          /test.*understand.*decide/i.test(document.body.textContent.replace(/\s+/g,' '))
        """)

    return result


def browser_verify_links(browser: Browser) -> list[dict[str, Any]]:
    if not COMMERCE.exists():
        return []
    report = load_json(COMMERCE)
    candidates = [item for item in report.get("items", []) if item.get("classification") != "pass"]
    output: list[dict[str, Any]] = []
    context = browser.new_context(ignore_https_errors=True, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36")
    page = context.new_page()
    for item in candidates:
        entry = {"product_id": item.get("product_id"), "product_name": item.get("product_name"), "url": item.get("attributed_url"), "classification": "unresolved"}
        try:
            response = page.goto(item.get("attributed_url"), wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(1200)
            status = response.status if response else None
            final_url = page.url
            text = page.locator("body").inner_text(timeout=5000)[:200000]
            sku = str(item.get("sku") or "")
            tokens = [t for t in re.findall(r"[a-z0-9]+", str(item.get("product_name") or "").lower()) if len(t) >= 4]
            haystack = (final_url + "\n" + text).lower()
            identity = bool(sku and sku.lower() in haystack) or sum(t in haystack for t in tokens[:5]) >= min(2, len(tokens))
            challenge = any(marker in haystack for marker in ("verify you are human", "access denied", "just a moment", "captcha", "cloudflare"))
            if status and 200 <= status < 400 and identity and not challenge:
                classification = "pass"
            elif challenge or status in (401, 403, 429, 503):
                classification = "bot_protected"
            else:
                classification = "failed"
            entry.update({"status": status, "final_url": final_url, "identity_ok": identity, "challenge": challenge, "classification": classification, "title": page.title()[:200]})
        except Exception as error:
            entry["error"] = f"{type(error).__name__}: {error}"
        output.append(entry)
    context.close()
    return output


def main() -> None:
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    screenshots = REVIEW_DIR / "screenshots"
    comparisons = REVIEW_DIR / "comparisons"
    baseline_root = make_baseline_worktree()
    current_parent = ROOT.parent
    baseline_parent = baseline_root.parent
    current_server = start_server(current_parent, 8010)
    baseline_server = start_server(baseline_parent, 8011)
    results: list[dict[str, Any]] = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            for viewport_name, viewport in VIEWPORTS.items():
                current_context = browser.new_context(viewport=viewport, reduced_motion="reduce" if viewport_name == "mobile375" else "no-preference")
                baseline_context = browser.new_context(viewport=viewport)
                current = current_context.new_page(); baseline = baseline_context.new_page()
                add_observers(current); add_observers(baseline)
                for page_name in PAGES:
                    if viewport_name == "tablet" and page_name not in ("home", "shop"):
                        continue
                    result = page_checks(current, page_name, viewport_name)
                    results.append(result)
                    current_path = screenshots / "v6" / f"{page_name}-{viewport_name}.png"
                    screenshot(current, current_path)
                    baseline.goto(f"http://127.0.0.1:8011/BioCare/{PAGES[page_name]}", wait_until="networkidle", timeout=60000)
                    baseline.wait_for_timeout(600)
                    baseline_path = screenshots / "v5.1" / f"{page_name}-{viewport_name}.png"
                    screenshot(baseline, baseline_path)
                    side_by_side(baseline_path, current_path, comparisons / f"{page_name}-{viewport_name}.jpg", f"{page_name} · {viewport_name}")
                current_context.close(); baseline_context.close()
            external = browser_verify_links(browser)
            browser.close()
    finally:
        for process in (current_server, baseline_server):
            with contextlib.suppress(Exception):
                process.terminate(); process.wait(timeout=5)
        subprocess.run(["git", "worktree", "remove", "--force", str(baseline_root)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    report = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "viewports": VIEWPORTS,
        "pages": results,
        "external_links": external,
        "summary": {
            "pages_checked": len(results),
            "overflow_failures": sum(bool(r.get("horizontal_overflow")) for r in results),
            "broken_images": sum(len(r.get("broken_images", [])) for r in results),
            "console_errors": sum(len(r.get("console_errors", [])) for r in results),
            "failed_requests": sum(len(r.get("failed_requests", [])) for r in results),
            "duplicate_ids": sum(len(r.get("duplicate_ids", [])) for r in results),
            "external_pass": sum(i.get("classification") == "pass" for i in external),
            "external_unresolved": sum(i.get("classification") != "pass" for i in external),
        },
    }
    write_json(OUTPUT, report)


if __name__ == "__main__":
    import contextlib
    import re
    main()
