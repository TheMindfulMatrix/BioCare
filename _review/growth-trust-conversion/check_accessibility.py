"""Targeted accessibility checks, not a WCAG conformance certification."""
from pathlib import Path
import json
import sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "_preview/growth/final/accessibility.json"
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8767/"

CONTRAST = r"""() => {
  const rgb = value => value.match(/[\d.]+/g).map(Number);
  const luminance = color => color.slice(0,3).map(v => {
    v /= 255; return v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4;
  }).reduce((s,v,i) => s + v * [.2126,.7152,.0722][i],0);
  const selectors = '.growth-hero h1,.growth-lede,.growth-contact-card p,.growth-contact-card h2,' +
    '.growth-heading,.growth-card p,.growth-card h3,.growth-card__number,.growth-prose p,' +
    '.growth-prose h2,.growth-faq summary,.growth-purchase-card h3,.growth-purchase-card p,' +
    '.growth-status,.growth-checklist li,.growth-text-link,.growth-page .button,.growth-section .button,' +
    '.growth-purchase-card .product-price small,.growth-purchase-card .product-price__source,.growth-purchase-disclosure';
  return [...document.querySelectorAll(selectors)].filter(el => el.getClientRects().length).map(el => {
    const style = getComputedStyle(el), fg = rgb(style.color);
    let node=el, bg=[0,0,0,0], skipped=null;
    while(node && bg[3] < .999) {
      const s=getComputedStyle(node), c=rgb(s.backgroundColor), alpha=c[3] ?? 1;
      if(s.backgroundImage !== 'none' && bg[3] < .999) skipped='background image/gradient';
      const a=bg[3] + alpha*(1-bg[3]);
      bg=[0,1,2].map(i => a ? (bg[i]*bg[3]+c[i]*alpha*(1-bg[3]))/a : 0).concat(a);
      if(Number(s.opacity) < 1) skipped='ancestor opacity';
      node=node.parentElement;
    }
    if(bg[3] < .999) skipped='unresolved background';
    const a=luminance(fg), b=luminance(bg), ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);
    const size=parseFloat(style.fontSize), weight=parseInt(style.fontWeight,10);
    const required=size >= 24 || (size >= 18.66 && weight >= 700) ? 3 : 4.5;
    return {text:el.textContent.trim().slice(0,85), ratio, required, skipped,
      fontSize:size, passes:skipped ? null : ratio >= required};
  });
}"""


def main():
    results=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(channel="chrome")
        for width,height in [(1440,900),(768,1024),(390,844),(375,812)]:
            context=browser.new_context(viewport={"width":width,"height":height},reduced_motion="reduce")
            page=context.new_page()
            for path in ["about.html","privacy.html","know-your-number.html"]:
                page.goto(BASE+path,wait_until="networkidle")
                page.screenshot(path=OUTPUT.parent / f"{path.removesuffix('.html')}-firstscreen-{width}.png")
                page.keyboard.press("Tab")
                assert page.locator('.skip-link').evaluate('el => el === document.activeElement')
                page.keyboard.press("Enter")
                assert page.locator('#main-content').evaluate('el => el === document.activeElement')
                contrasts=page.evaluate(CONTRAST)
                assert contrasts and all(item['passes'] is not False for item in contrasts), {"path":path,"width":width,"failures":[c for c in contrasts if c['passes'] is False]}
                link=page.locator('main .button').first
                link.focus()
                focused=link.evaluate("el => { const s=getComputedStyle(el);return {outline:s.outlineStyle,width:parseFloat(s.outlineWidth),height:el.getBoundingClientRect().height};}")
                assert focused['outline'] != 'none' and focused['width'] >= 2 and focused['height'] >= 44, focused
                page.emulate_media(forced_colors="active")
                assert link.evaluate('el => parseFloat(getComputedStyle(el).outlineWidth)') >= 3
                page.emulate_media(forced_colors="none")
                results.append({"path":path,"width":width,"skip_link":True,"keyboard_focus":True,
                                "forced_colors_focus":True,"primary_button_minimum_44px":True,"contrast":contrasts})
            context.close()
        context=browser.new_context(java_script_enabled=False,viewport={"width":390,"height":844})
        page=context.new_page()
        for path in ['about.html','privacy.html','know-your-number.html','products/balance-test.html']:
            response=page.goto(BASE+path)
            assert response.status == 200
            assert page.locator('main').is_visible()
            assert page.locator('a[href$="about.html"]').count() > 0
        context.close()
        journeys=[]
        for motion in ('reduce','no-preference'):
            context=browser.new_context(viewport={'width':390,'height':844},reduced_motion=motion)
            page=context.new_page()
            for product in ('balance-test','balance-basic-kit'):
                page.goto(BASE+'know-your-number.html',wait_until='networkidle')
                page.locator(f'#purchase-options a[href="products/{product}.html"]').click()
                page.wait_for_url('**/products/'+product+'.html')
                official=page.locator('main a[rel*="sponsored"]').first
                assert official.get_attribute('href').startswith('https://www.zinzino.com/'), official.get_attribute('href')
                page.locator('.growth-purchase-help a').click()
                page.wait_for_url('**/know-your-number.html#purchase-options')
                journeys.append({'motion':motion,'product':product,'comparison_round_trip':True,
                                 'official_destination_present':True,'purchase_placed':False})
            context.close()
        browser.close()
    OUTPUT.write_text(json.dumps({"cases":results,"no_js_static_routes":4,
                                 "journey_checks":journeys,
                                 "scope":"targeted basics, not a full accessibility certification"},indent=2)+"\n",encoding="utf-8")
    print(f'{len(results)} targeted accessibility cases passed; 4 no-JS static routes and 4 purchase-comparison round trips passed')


if __name__=='__main__':
    main()
