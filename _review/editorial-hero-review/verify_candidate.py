"""Compare the candidate with the exact baseline, then audit the local build."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import hashlib
import json
import subprocess
import sys

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts import daily_audit
from scripts.site_paths import audited_page_paths

BASELINE = "02727eaa7e47f250b91ffef115fc1bb742b60422"
OUTPUT = ROOT / "_preview/editorial-hero-review"
DESKTOP = "assets/product-cutouts/hero/balance-test-basic-kit-650.webp"
OLD = "assets/product-cutouts/zinzino-v6/balance-test-basic-kit-910465.webp"
BASELINE_HTML = subprocess.check_output(["git", "show", f"{BASELINE}:index.html"], cwd=ROOT)


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path == "/?baseline-review=1":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(BASELINE_HTML)))
            self.end_headers()
            self.wfile.write(BASELINE_HTML)
        else:
            path = Path(self.translate_path(self.path))
            if path.is_file() and path.suffix in {".html", ".css", ".js", ".json", ".svg", ".xml", ".txt"}:
                # Simulate Git's LF-normalized Linux/Pages artifact, not this
                # Windows checkout's CRLF text storage. Binary assets are raw.
                body = path.read_bytes().replace(b"\r\n", b"\n")
                self.send_response(200)
                self.send_header("Content-Type", self.guess_type(str(path)))
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                super().do_GET()


def inspect(page):
    return page.evaluate("""() => {
      const img = document.querySelector('.hero-product__cutout img');
      return {source: new URL(img.currentSrc).pathname.substring(1),
        natural: [img.naturalWidth,img.naturalHeight],
        overflow: document.documentElement.scrollWidth > innerWidth,
        geometry: Object.fromEntries(['.hero-product__cutout img','.home-hero__content',
          '.hero-product__caption','.hero-product__tap'].map(s => {
            const r = document.querySelector(s).getBoundingClientRect();
            return [s,[r.x,r.y,r.width,r.height]];
          }))};
    }""")


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1",0), partial(Handler,directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}/"
    results, errors = [], []
    resume = "--resume-after-source-checks" in sys.argv
    if resume:
        saved = json.loads((OUTPUT/"responsive-source-checks.json").read_text(encoding="utf-8"))
        results, errors = saved["cases"], saved["errors"]
        assert len(results) == 32 and not errors
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(channel="chrome",headless=True)
            for width,height in ([] if resume else [(375,812),(390,844),(768,1024),(896,1024),(1024,900),(1199,900),(1200,900),(1440,900)]):
                for dpr in [1,2]:
                    for motion in ["reduce","no-preference"]:
                        context=browser.new_context(viewport={"width":width,"height":height},
                            device_scale_factor=dpr,reduced_motion=motion)
                        page=context.new_page()
                        requests=[]
                        page.on("request",lambda r: requests.append(r.url))
                        page.on("pageerror",lambda e: errors.append(str(e)))
                        page.on("console",lambda m: errors.append(m.text) if m.type in {"error","warning"} else None)
                        page.goto(base,wait_until="networkidle")
                        page.evaluate("document.fonts.ready")
                        current=inspect(page)
                        assert current["source"] == (DESKTOP if width >= 1200 else OLD), current
                        assert not current["overflow"]
                        if width < 1200:
                            assert not any(DESKTOP in url for url in requests), requests
                        result={"width":width,"height":height,"dpr":dpr,"motion":motion,"candidate":current}
                        if motion=="reduce":
                            old=context.new_page()
                            old.goto(base+"?baseline-review=1",wait_until="networkidle")
                            old.evaluate("document.fonts.ready")
                            baseline=inspect(old)
                            assert current["geometry"] == baseline["geometry"], (current,baseline)
                            result["baseline_geometry_identical"]=True
                            if dpr==1 and width in [375,390,768,1440]:
                                page.bring_to_front()
                                candidate_png=page.screenshot(path=str(OUTPUT/f"candidate-{width}.png"), animations="disabled")
                                old.bring_to_front()
                                baseline_png=old.screenshot(path=str(OUTPUT/f"baseline-{width}.png"), animations="disabled")
                                result["screenshot_pixel_encoding_identical"]=candidate_png==baseline_png
                                if width < 1200:
                                    assert candidate_png==baseline_png, f"Unexpected smaller-screen visual change: {width}"
                            old.close()
                        results.append(result)
                        context.close()
                print(f"Hero source/layout checks passed at {width}px", flush=True)
            browser.close()
        assert not errors, errors
        (OUTPUT/"responsive-source-checks.json").write_text(json.dumps({"cases":results,"errors":errors},indent=2)+"\n",encoding="utf-8")
        audit=daily_audit.audit_site(ROOT,base,"uncommitted-review-candidate")
        (OUTPUT/"local-parity.json").write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")
        assert audit["overall_status"]=="HEALTHY", {key:audit[key] for key in ["coverage_errors","page_regressions","broken_live_assets"]}
        pages=audited_page_paths(ROOT)
        other=[path or "index.html" for path in pages if path]
        unchanged=[]
        for path in other+["assets/data/search-index.json","sitemap.xml","robots.txt"]:
            baseline=subprocess.check_output(["git","show",f"{BASELINE}:{path}"],cwd=ROOT)
            assert baseline==daily_audit.build_bytes(ROOT/path), path
            unchanged.append(path)
        before={path:hashlib.sha256(daily_audit.build_bytes(ROOT/(path or "index.html"))).hexdigest() for path in pages}
        subprocess.run([sys.executable,"scripts/build.py"],cwd=ROOT,check=True)
        after={path:hashlib.sha256(daily_audit.build_bytes(ROOT/(path or "index.html"))).hexdigest() for path in pages}
        assert before==after
        boundary={"baseline":BASELINE,"unchanged_other_pages":len(other),"unchanged_supporting_outputs":3,
            "public_page_count":len(pages),"deterministic_public_build":True,"source_selection_cases":len(results),
            "geometry_comparisons":sum(r.get("baseline_geometry_identical",False) for r in results),
            "local_parity_assets":audit["referenced_live_assets"]}
        (OUTPUT/"candidate-boundary.json").write_text(json.dumps(boundary,indent=2)+"\n",encoding="utf-8")
        print(json.dumps(boundary),flush=True)
        subprocess.run([sys.executable,"scripts/browser_audit.py","--root",str(ROOT),"--base-url",base,
            "--browser-channel","chrome","--output-dir",str(OUTPUT/"browser")],cwd=ROOT,check=True)
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
