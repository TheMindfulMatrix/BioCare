"""Review-only screenshots and targeted usability checks against loopback.

Uses the repository's Playwright 1.55.0 test dependency and installed Chrome.
No checkout submissions, production writes, tracking, or persistent profiles.
"""
from pathlib import Path
import argparse
import json
import re
import runpy
import sys

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.browser_audit import tablet_hero_checks

VIEWPORTS = {1440: 900, 768: 1024, 390: 844, 375: 812}
ROUTES = {'home':'', 'products':'shop.html', 'library':'library.html',
          'evidence':'evidence.html', 'core-four':'core-four.html',
          'product-record':'products/balance-basic-kit.html',
          'guide':'library/how-to-read-a-health-study.html',
          'journey':'know-your-number.html', 'about':'about.html', 'privacy':'privacy.html'}
CONTRAST = runpy.run_path(str(ROOT / '_review/growth-trust-conversion/check_accessibility.py'))['CONTRAST']
CONTRAST = re.sub(r"  const selectors = [\s\S]*?;\n", "  const selectors = 'main h1,main h2,main h3,main h4,main p,main a,main button,main label,main summary,main dt,main dd';\n", CONTRAST, count=1)


def reveal(page):
    height = page.evaluate('document.documentElement.scrollHeight')
    for y in range(0, height, 700):
        page.evaluate('(y) => window.scrollTo(0,y)', y)
        page.wait_for_timeout(35)
    page.evaluate('window.scrollTo(0,0)')
    page.wait_for_timeout(150)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', default='http://127.0.0.1:8772/')
    parser.add_argument('--output-dir', type=Path, default=ROOT / '_preview/research-led-experience/review')
    parser.add_argument('--screenshots-only', action='store_true')
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(channel='chrome')
        for width,height in VIEWPORTS.items():
            context=browser.new_context(viewport={'width':width,'height':height}, reduced_motion='reduce')
            page=context.new_page()
            for name,path in ROUTES.items():
                page.goto(args.base_url + path,wait_until='networkidle')
                page.evaluate('document.fonts.ready')
                reveal(page)
                page.screenshot(path=args.output_dir / f'{name}-{width}.png',full_page=True)
                if name=='home':
                    page.screenshot(path=args.output_dir / f'home-opening-{width}.png')
                    for selector,label in [('#matrix-entry','navigator'),('.core-four-feature','collection'),('#shelf','universe')]:
                        page.locator(selector).screenshot(path=args.output_dir / f'{label}-{width}.png',style='.site-header,.mobile-dock{visibility:hidden!important}')
                if args.screenshots_only:
                    continue
                contrasts=page.evaluate(CONTRAST)
                page.keyboard.press('Tab')
                skip = page.locator('.skip-link').evaluate('el => el === document.activeElement')
                page.keyboard.press('Enter')
                skip_target = page.locator(page.locator('.skip-link').get_attribute('href')).evaluate('el => el === document.activeElement')
                primary=page.locator('main .button').first
                primary.focus()
                focus=primary.evaluate("el => { const s=getComputedStyle(el); return (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth)>=2) || s.boxShadow !== 'none'; }")
                hero = tablet_hero_checks(page) if name=='home' else None
                page.add_style_tag(content='html{font-size:200%!important}')
                zoom_overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth')
                heading_clipped=page.evaluate("""() => {
                    const heading = document.querySelector('main h1');
                    const walker = document.createTreeWalker(heading, NodeFilter.SHOW_TEXT);
                    const rectangles=[]; let node;
                    while ((node=walker.nextNode())) {
                        if (!node.textContent.trim()) continue;
                        const range=document.createRange(); range.selectNodeContents(node);
                        rectangles.push(...range.getClientRects());
                    }
                    return rectangles.some(rect => rect.left < -1 || rect.right > innerWidth+1);
                }""")
                overflow_elements=page.evaluate("() => [...document.querySelectorAll('main *')].filter(el => el.getClientRects().length && el.getBoundingClientRect().right > innerWidth+1).slice(0,10).map(el => ({tag:el.tagName,cls:el.className,text:el.textContent.slice(0,50)}))") if zoom_overflow else []
                results.append({'page':path or 'index.html','width':width,'skip_link':skip and skip_target,'focus_visible':focus,'hero':hero,
                    'text_200_percent_no_overflow':not zoom_overflow,'heading_200_percent_not_clipped':not heading_clipped,'overflow_elements':overflow_elements,
                    'contrast_checked':len(contrasts),'contrast_failures':[c for c in contrasts if c['passes'] is False],
                    'contrast_manual_review':sum(c['skipped'] is not None for c in contrasts)})
                (args.output_dir/'review-qa-checkpoint.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
            context.close()
            print(f'Review captures/checks complete at {width}px',flush=True)
        no_js=[]
        context=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
        page=context.new_page()
        for path in ['', 'shop.html','library.html','evidence.html','products/balance-basic-kit.html']:
            response=page.goto(args.base_url+path,wait_until='networkidle')
            checks={'http_200':response.status==200,'main_visible':page.locator('main').is_visible(),
                    'navigation_present':page.locator('a[href$="library.html"]').count()>0}
            if not path:
                checks['all_paths_visible']=page.locator('[data-path-panel]:visible').count()==3
                checks['enhancement_controls_hidden']=not page.locator('[data-path-controls]').is_visible()
                checks['disclosure_visible']=page.locator('#hero-affiliate-disclosure').is_visible()
            no_js.append({'page':path or 'index.html','checks':checks})
        context.close()
        browser.close()
    payload={'scope':'Targeted usability basics, not a WCAG certification; gradients/images require visual review.', 'cases':results,'no_js':no_js}
    (args.output_dir/'review-qa.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    failures=[r for r in results if not r['skip_link'] or not r['focus_visible'] or not r['text_200_percent_no_overflow'] or not r['heading_200_percent_not_clipped'] or r['contrast_failures'] or (r['hero'] and not all(r['hero'].values()))]
    print(json.dumps({'cases':len(results),'cases_with_findings':len(failures),'no_js':no_js}))
    if failures or any(not value for row in no_js for value in row['checks'].values()):
        raise SystemExit(1)


if __name__=='__main__':
    main()
