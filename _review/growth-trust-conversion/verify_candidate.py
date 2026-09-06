"""Private, repeatable review QA. No production writes or external submissions.

Requires Playwright and installed Chrome. Uses isolated browser profiles and
loopback servers. A complete browser audit is separately run by --full-browser.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import hashlib
import io
import json
import subprocess
import sys

from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts import daily_audit
from scripts.site_paths import audited_page_paths

BASELINE = "0a8ddc194b8ccea71c173ec6196d0e8a94d388a4"
OUTPUT = ROOT / "_preview/growth/final"
SIZES = [(375, 812), (390, 844), (768, 1024), (896, 1024),
         (1024, 900), (1199, 900), (1200, 900), (1440, 900)]
MAIN_SIZES = [(1440, 900), (768, 1024), (390, 844), (375, 812)]


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        path = Path(self.translate_path(self.path))
        if path.is_dir():
            path = path / "index.html"
        if path.is_file() and path.suffix in {".html", ".css", ".js", ".json", ".svg", ".xml", ".txt"}:
            # Match Git's LF-normalized Linux artifact, not Windows CRLF.
            body = path.read_bytes().replace(b"\r\n", b"\n")
            self.send_response(200)
            self.send_header("Content-Type", self.guess_type(str(path)))
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()


def serve(root):
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(Handler, directory=str(root)))
    Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_port}/"


def inspect_hero(page):
    return page.evaluate("""() => {
      const img = document.querySelector('.hero-product__cutout img');
      return {source: new URL(img.currentSrc).pathname.substring(1),
        overflow: document.documentElement.scrollWidth > innerWidth,
        geometry: Object.fromEntries(['.hero-product__cutout img','.home-hero__content',
          '.hero-product__caption','.hero-product__tap'].map(s => {
            const r = document.querySelector(s).getBoundingClientRect();
            return [s,[r.x,r.y,r.width,r.height]];
          }))};
    }""")


def settled(page, url):
    response = page.goto(url, wait_until="networkidle")
    assert response.status == 200, url
    page.evaluate("document.fonts.ready")
    # Let first-entry motion finish before comparing stable layout.
    page.wait_for_timeout(900)


def prototype_checks(browser, base):
    results = []
    for width, height in MAIN_SIZES:
        for motion in ("reduce", "no-preference"):
            context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion=motion)
            page = context.new_page()
            requests, errors = [], []
            page.on("request", lambda r: requests.append({"url": r.url, "method": r.method}))
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(base + "_review/growth-trust-conversion/email/signup-preview.html", wait_until="networkidle")
            count = len(requests)
            assert page.locator("#signup-email").is_disabled()
            assert page.locator("button[type=submit]").is_disabled()
            assert not page.locator("#signup-consent").is_checked()
            page.locator("#preview-state").select_option("confirmation")
            page.locator("button[type=submit]").click()
            assert page.locator("#signup-email").get_attribute("aria-invalid") == "true"
            assert page.locator("#signup-email").evaluate("el => el === document.activeElement")
            page.locator("#signup-email").fill("not-an-email")
            page.locator("button[type=submit]").click()
            assert page.locator("#signup-email").get_attribute("aria-invalid") == "true"
            page.locator("#signup-email").fill("reader@example.invalid")
            page.locator("button[type=submit]").click()
            assert page.locator("#signup-consent").get_attribute("aria-invalid") == "true"
            page.keyboard.press("Space")
            assert page.locator("#signup-consent").is_checked()
            page.locator("button[type=submit]").click()
            page.wait_for_function("document.querySelector('#signup-status').textContent.includes('No email was sent')")
            assert not page.locator("#signup-consent").is_checked()
            assert page.locator("#signup-email").input_value() == ""
            page.locator("#preview-state").select_option("error")
            page.locator("#signup-email").fill("reader@example.invalid")
            page.locator("#signup-consent").check()
            page.locator("button[type=submit]").click()
            page.wait_for_function("document.querySelector('#signup-error').textContent.includes('Simulated provider error')")
            assert not page.locator("button[type=submit]").is_disabled()
            if motion == "reduce":
                page.screenshot(path=OUTPUT / f"signup-error-{width}.png", full_page=True)
            page.locator("#preview-state").select_option("unavailable")
            assert page.locator("#signup-email").is_disabled()
            assert len(requests) == count, requests[count:]
            assert all(item["method"] == "GET" and item["url"].startswith(base) for item in requests)
            assert page.evaluate("localStorage.length + sessionStorage.length") == 0
            assert not context.cookies()
            assert not page.evaluate("document.documentElement.scrollWidth > innerWidth")
            assert not errors, errors
            results.append({"width": width, "motion": motion, "validation_keyboard_error_reset_pass": True,
                            "network_submissions": 0, "storage_items": 0, "real_subscription_created": False})
            context.close()
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto(base + "_review/growth-trust-conversion/email/signup-preview.html")
    assert page.locator("button[type=submit]").is_disabled()
    assert page.locator("#signup-email").is_disabled()
    context.close()
    return results


def measurement_check(browser, base):
    context = browser.new_context()
    page = context.new_page()
    page.goto(base + "about.html?utm_source=instagram&q=private-health-query")
    assert page.locator('script[src*="growth-measurement"]').count() == 0
    # Explicit isolated test injection; the public pages never load this module.
    page.add_script_tag(path=str(ROOT / "assets/js/growth-measurement.js"))
    payloads = page.evaluate("""() => {
      const payloads = [];
      const options = {enabled:true, send:p => payloads.push(p)};
      MatrixMeasurement.bind(document, options);
      MatrixMeasurement.bind(document, options);
      const click = href => {
        const a = document.createElement('a'); a.href = href; a.rel='sponsored';
        document.body.append(a);
        a.addEventListener('click', e => e.preventDefault());
        a.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true})); a.remove();
      };
      click('https://www.zinzino.com/?email=private@example.invalid');
      click('https://www.zinzino.com/?email=private@example.invalid');
      click('mailto:connect@themindfulmatrixhealth.com');
      click('/library/how-to-read-a-supplement-label.html?private=health');
      return payloads;
    }""")
    assert [p["action"] for p in payloads] == ["page_view", "manufacturer_click", "contact_click", "education_click"], payloads
    assert not any(word in json.dumps(payloads) for word in ["private", "@", "https", "?", "q=", "health"])
    context.close()
    return {"mocked_only": True, "duplicate_bindings_and_clicks_suppressed": True, "payloads": payloads}


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    baseline_root = ROOT.parent / "BioCare-editorial-hero-review"
    actual_tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=baseline_root).strip()
    expected_tree = subprocess.check_output(["git", "rev-parse", BASELINE + "^{tree}"], cwd=ROOT).strip()
    assert actual_tree == expected_tree, "Baseline worktree must match exact released tree"
    assert not subprocess.check_output(["git", "diff", "--name-only"], cwd=baseline_root).strip()
    current_server, base = serve(ROOT)
    old_server, old_base = serve(baseline_root)
    results, zoom = [], []
    fingerprint = hashlib.sha256(b''.join(daily_audit.build_bytes(ROOT / path) for path in
        sorted([p or 'index.html' for p in audited_page_paths(ROOT)] +
               daily_audit.asset_paths(ROOT, audited_page_paths(ROOT))))).hexdigest()
    checkpoint = OUTPUT / 'hero-checkpoint.json'
    resume = '--resume-hero' in sys.argv
    if resume:
        saved = json.loads(checkpoint.read_text(encoding='utf-8'))
        assert saved['fingerprint'] == fingerprint and len(saved['cases']) == 32
        results = saved['cases']
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(channel="chrome")
            for width, height in ([] if resume else SIZES):
                for dpr in (1, 2):
                    for motion in ("reduce", "no-preference"):
                        context = browser.new_context(viewport={"width": width, "height": height},
                                                      device_scale_factor=dpr, reduced_motion=motion)
                        page, old = context.new_page(), context.new_page()
                        settled(page, base)
                        settled(old, old_base)
                        current, before = inspect_hero(page), inspect_hero(old)
                        assert current == before, {"width": width, "dpr": dpr, "motion": motion, "before": before, "current": current}
                        assert not current["overflow"]
                        pixel_equal = None
                        changed_pixels = None
                        max_channel_difference = None
                        mean_channel_difference = None
                        if dpr == 1 and motion == "reduce" and (width, height) in MAIN_SIZES:
                            page.bring_to_front()
                            page.evaluate("document.querySelector('.hero-product__cutout img').decode()")
                            page.wait_for_timeout(300)
                            after_png = page.screenshot(path=OUTPUT / f"home-after-{width}.png")
                            old.bring_to_front()
                            old.evaluate("document.querySelector('.hero-product__cutout img').decode()")
                            old.wait_for_timeout(300)
                            before_png = old.screenshot(path=OUTPUT / f"home-before-{width}.png")
                            pixel_equal = after_png == before_png
                            diff = ImageChops.difference(Image.open(io.BytesIO(after_png)).convert('RGB'),
                                                         Image.open(io.BytesIO(before_png)).convert('RGB'))
                            changed_pixels = sum(pixel != (0,0,0) for pixel in diff.get_flattened_data())
                            max_channel_difference = max(high for low, high in diff.getextrema())
                            mean_channel_difference = sum(sum(pixel) for pixel in diff.get_flattened_data()) / (width*height*3)
                            # Pixel equality is diagnostic, not the release gate:
                            # composited canvas/gradients vary across Chrome tabs.
                            # Exact geometry and selected source are asserted above;
                            # before/after captures also require human visual review.
                        results.append({"width": width, "dpr": dpr, "motion": motion,
                                        "geometry_and_source_identical": True, "first_screen_png_identical": pixel_equal,
                                        "changed_pixels": changed_pixels,"max_channel_difference":max_channel_difference,
                                        "mean_channel_difference":mean_channel_difference})
                        context.close()
                print(f"Hero preservation checks passed at {width}px", flush=True)
            checkpoint.write_text(json.dumps({'fingerprint':fingerprint,'cases':results},indent=2)+'\n',encoding='utf-8')
            for width, height in MAIN_SIZES:
                context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
                page = context.new_page()
                for path, name in [("about.html", "about"), ("privacy.html", "privacy"),
                                   ("know-your-number.html", "journey"), ("products/balance-basic-kit.html", "kit")]:
                    settled(page, base + path)
                    page.screenshot(path=OUTPUT / f"{name}-after-{width}.png", full_page=True, animations="disabled")
                    if path == "know-your-number.html":
                        # A section crop omits fixed navigation/skip overlays only
                        # during capture, not from the actual website.
                        page.locator("#purchase-options").screenshot(path=OUTPUT / f"purchase-options-{width}.png",
                            style=".site-header,.mobile-dock,.skip-link{visibility:hidden!important}")
                    if name in ("journey", "kit"):
                        old = context.new_page()
                        settled(old, old_base + path)
                        old.screenshot(path=OUTPUT / f"{name}-before-{width}.png", full_page=True, animations="disabled")
                        old.close()
                        page.bring_to_front()
                    page.add_style_tag(content="html { font-size: 200% !important; }")
                    assert not page.evaluate("document.documentElement.scrollWidth > innerWidth"), f"200% text overflow: {path} {width}"
                    zoom.append({"path": path, "width": width, "text_size_200_percent_no_overflow": True})
                context.close()
            prototype = prototype_checks(browser, base)
            measurement = measurement_check(browser, base)
            browser.close()
        audit = daily_audit.audit_site(ROOT, base, "review-candidate")
        (OUTPUT / "local-parity.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
        assert audit["overall_status"] == "HEALTHY", audit
        pages = audited_page_paths(ROOT)
        def hashes():
            return {path: hashlib.sha256(daily_audit.build_bytes(ROOT / (path or "index.html"))).hexdigest() for path in pages}
        before = hashes()
        subprocess.run([sys.executable, "scripts/build.py"], cwd=ROOT, check=True)
        assert before == hashes(), "Non-deterministic public build"
        summary = {"baseline": BASELINE, "hero_cases": results, "text_zoom_cases": zoom,
                   "signup_prototype_cases": prototype, "measurement_mock": measurement,
                   "public_pages": len(pages), "local_parity_assets": audit["referenced_live_assets"],
                   "deterministic_build": True}
        (OUTPUT / "review-qa.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({key: len(value) if isinstance(value, list) else value for key, value in summary.items()}), flush=True)
        if "--full-browser" in sys.argv:
            subprocess.run([sys.executable, "scripts/browser_audit.py", "--root", str(ROOT), "--base-url", base,
                            "--browser-channel", "chrome", "--output-dir", str(OUTPUT / "browser")], cwd=ROOT, check=True)
    finally:
        for server in (current_server, old_server):
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    main()
