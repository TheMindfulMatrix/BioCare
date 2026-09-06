"""Capture our own candidate/baseline and make a local, non-public review gallery."""
from pathlib import Path
from datetime import datetime,timezone
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
SHOTS=HERE/'screenshots'

def measure(page):
    return page.evaluate("""() => ({
        documentBytes: performance.getEntriesByType('navigation')[0].decodedBodySize,
        resources: performance.getEntriesByType('resource').map(r => ({path:new URL(r.name).pathname,
            decodedBodyBytes:r.decodedBodySize, kind:r.initiatorType})),
        scrollY,
        imagesLoaded:[...document.images].filter(i => i.complete && i.naturalWidth).length
    })""")

def main():
    SHOTS.mkdir(exist_ok=True)
    measurements=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='chrome')
        for width,height,label in [(1440,1000,'desktop'),(768,1024,'tablet'),(390,1100,'mobile'),(375,1000,'mobile375')]:
            context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
            page=context.new_page()
            page.goto('http://127.0.0.1:8772/',wait_until='networkidle')
            page.evaluate('document.fonts.ready')
            page.screenshot(path=SHOTS/f'home-{label}.jpg',quality=88)
            measurements.append({'version':'candidate','width':width,**measure(page)})
            if width==1440:
                for selector,name in [('#matrix-entry','navigator'),('.core-four-feature','collection'),('#shelf','universe')]:
                    page.locator(selector).scroll_into_view_if_needed()
                    page.wait_for_timeout(200)
                    page.locator(selector).screenshot(path=SHOTS/f'{name}.jpg',quality=88,style='.site-header,.mobile-dock{visibility:hidden!important}')
                for route,name in [('shop.html','products'),('library.html','library'),('evidence.html','evidence'),('products/balance-basic-kit.html','product-record')]:
                    page.set_viewport_size({'width':1440,'height':1100})
                    page.goto('http://127.0.0.1:8772/'+route,wait_until='networkidle')
                    page.screenshot(path=SHOTS/f'{name}.jpg',quality=88)
            context.close()
            if width in (1440,390):
                context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
                page=context.new_page()
                page.goto('http://127.0.0.1:8773/',wait_until='networkidle')
                page.evaluate('document.fonts.ready')
                page.screenshot(path=SHOTS/f'before-{label}.jpg',quality=88)
                measurements.append({'version':'baseline','width':width,**measure(page)})
                context.close()
        browser.close()
    payload={'checked_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Fresh isolated Chrome contexts on loopback; default network; first viewport only. Decoded resource bytes, not production transfer size, field Core Web Vitals, or an A/B experiment.',
        'measurements':measurements}
    (HERE/'local-payload-comparison.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'screenshots':len(list(SHOTS.glob('*.jpg'))),'total_bytes':sum(x.stat().st_size for x in SHOTS.glob('*.jpg'))}))

if __name__=='__main__':main()
