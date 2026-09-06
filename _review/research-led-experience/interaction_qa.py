"""Exercise the live local discovery controls without buying or sending data."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright,expect

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
BASE='http://127.0.0.1:8772/'

def main():
    rows=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='chrome')
        for width,height in [(1440,900),(768,1024),(390,844),(375,812)]:
            for motion in ('reduce','no-preference'):
                context=browser.new_context(viewport={'width':width,'height':height},reduced_motion=motion)
                page=context.new_page()
                page.goto(BASE,wait_until='networkidle')
                page.locator('.experience-kit-details summary').click()
                assert page.locator('.experience-kit-details').get_attribute('open') is not None
                assert page.locator('#hero-affiliate-disclosure').is_visible()
                page.locator('.experience-kit-details summary').click()
                page.locator('[data-universe-manufacturer]').select_option('BioLimitless')
                page.locator('[data-universe-search]').fill('magnesium')
                expect(page.locator('[data-universe-results]')).to_have_text('Showing 2 of 45 active products.')
                assert set(page.locator('[data-product-universe]').get_attribute('data-universe-filter-ids').split(','))=={'biolimitless-magnesium-glycinate','biolimitless-bio-basics-core-four'}
                page.locator('[data-universe-search]').fill('zzznomatch')
                assert page.locator('[data-universe-empty]').is_visible()
                assert not page.locator('[data-product-universe]').is_visible()
                page.locator('[data-universe-reset]').click()
                expect(page.locator('[data-universe-results]')).to_have_text('Showing 45 of 45 active products.')
                page.locator('[data-universe-sort]').select_option('name')
                sorted_ids=page.locator('[data-product-universe]').get_attribute('data-universe-filter-ids').split(',')
                expected=page.locator('[data-universe-data]').evaluate("el => JSON.parse(el.textContent).sort((a,b)=>a.name.localeCompare(b.name)).map(p=>p.id)")
                assert sorted_ids==expected
                page.locator('[data-universe-reset]').click()
                first=page.locator('[data-universe-product]').get_attribute('data-universe-product')
                page.locator('[data-universe-step="1"]').click()
                assert page.locator('[data-universe-product]').get_attribute('data-universe-product')!=first
                intent=page.locator('[data-universe-intent]').first
                intent.focus()
                page.keyboard.press('ArrowRight')
                assert page.locator('[data-product-universe]').get_attribute('data-active-intent')!=intent.get_attribute('data-universe-intent')
                page.locator('.header-search input').fill('magnesium')
                page.locator('.header-search input').press('Enter')
                page.wait_for_url('**/explore.html?q=magnesium')
                expect(page.locator('.search-result').first).to_be_visible()
                page.locator('[data-search-mode="products"]').click()
                assert page.locator('.search-result').evaluate_all("items=>items.length>0&&items.every(i=>i.classList.contains('search-result--product'))")
                page.locator('[data-search-input]').fill('omega')
                page.locator('[data-search-form]').evaluate('form=>form.requestSubmit()')
                page.locator('[data-search-mode="learn"]').click()
                assert page.locator('.search-result').evaluate_all("items=>items.length>0&&items.every(i=>!i.classList.contains('search-result--product'))")
                page.goto(BASE+'shop.html',wait_until='networkidle')
                page.locator('[data-shop-filter-open]').click()
                page.locator('[name="filter-manufacturer"][value="BioLimitless"]').check()
                page.locator('[data-shop-filter-apply]').click()
                expect(page.locator('[data-shop-product]').first).to_be_visible()
                assert page.locator('[data-shop-product]').evaluate_all("items=>items.length>0&&items.every(i=>i.textContent.includes('BioLimitless'))")
                assert 'manufacturer=BioLimitless' in page.url
                page.locator('[data-shop-product] [data-product-open]').first.click()
                expect(page.locator('[data-product-inspector]')).to_be_visible()
                page.keyboard.press('Escape')
                expect(page.locator('[data-product-inspector]')).not_to_be_visible()
                # Escape restores URL state and then the dialog's close event
                # returns focus; wait for the actual browser lifecycle event.
                expect(page.locator('[data-product-open]:focus')).to_have_count(1)
                rows.append({'width':width,'motion':motion,'kit_details':True,'disclosure_visible':True,
                    'combined_universe_filter':True,'empty_state_and_reset':True,'universe_sort':True,
                    'next_product':True,'keyboard_intent':True,'header_search':True,'search_modes':True,
                    'catalog_filter_and_url':True,'inspector_escape_and_focus_return':True})
                context.close()
                print(f'Interaction suite passed at {width}, {motion}',flush=True)
        browser.close()
    (HERE/'interaction-qa.json').write_text(json.dumps({'cases':rows,'case_count':len(rows),'failures':0},indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
