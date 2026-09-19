"""Release boundaries for public trust pages and non-public growth foundations."""
import json
import unittest
from pathlib import Path

from scripts import build, site_paths
from scripts.compliance_engine import ComplianceEngine

ROOT = Path(__file__).resolve().parents[1]


class GrowthFoundationsTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'content/site.json').read_text(encoding='utf-8'))
        self.data['growth'] = json.loads((ROOT / 'content/growth.json').read_text(encoding='utf-8'))
        self.data['catalog'] = json.loads((ROOT / 'content/catalog.json').read_text(encoding='utf-8'))
        self.data['products'] = self.data['catalog']['products']
        self.data['featuredProductId'] = self.data['catalog']['featuredProductId']

    def test_new_pages_are_in_canonical_inventory(self):
        paths = site_paths.audited_page_paths(ROOT)
        self.assertIn('about.html', paths)
        self.assertIn('privacy.html', paths)
        self.assertEqual(len(paths), 88)

    def test_footer_reaches_contact_and_privacy_from_nested_pages(self):
        html = build.shared_footer_markup(self.data, prefix='../')
        for value in ['../about.html','../privacy.html','mailto:connect@themindfulmatrixhealth.com']:
            self.assertIn(value, html)

    def test_contact_has_no_data_collection_form(self):
        html=(ROOT/'about.html').read_text(encoding='utf-8')
        self.assertIn('Gavin Reidel',html)
        self.assertNotIn('type="email"',html)
        self.assertIn('Please do not send medical records',html)

    def test_current_privacy_notice_matches_inert_integrations(self):
        self.assertFalse(self.data['growth']['integrations']['analyticsEnabled'])
        self.assertFalse(self.data['growth']['integrations']['newsletterEnabled'])
        html=(ROOT/'privacy.html').read_text(encoding='utf-8')
        self.assertIn('Analytics off',html)
        self.assertIn('Newsletter signup off',html)
        self.assertIn('Google Fonts',html)
        self.assertIn('GitHub Pages',html)

    def test_boolean_flip_cannot_silently_activate_services(self):
        for flag in ['analyticsEnabled','newsletterEnabled']:
            self.data['growth']['integrations'][flag]=True
            with self.assertRaisesRegex(ValueError,'activation review'):
                build.build_growth_pages(self.data)
            self.data['growth']['integrations'][flag]=False

    def test_public_pages_do_not_load_measurement_or_signup(self):
        for path in site_paths.audited_page_paths(ROOT):
            html=(ROOT/(path or 'index.html')).read_text(encoding='utf-8')
            self.assertNotIn('growth-measurement.js',html,path)
            self.assertNotIn('data-signup-preview',html,path)
            self.assertNotIn('_review/growth',html,path)

    def test_purchase_options_use_canonical_product_records(self):
        html=build.growth_purchase_options(self.data)
        for product_id in self.data['growth']['journey']['productIds']:
            product=next(p for p in self.data['products'] if p['id']==product_id)
            self.assertIn(build.price_markup(product),html)
            self.assertIn(f'products/{product_id}.html',html)
        self.assertIn('id="shelf-affiliate-disclosure"',html)
        self.assertIn('New York',html)
        self.assertIn('recurring monthly charge',html)

    def test_canonical_price_change_reaches_comparison(self):
        product=next(p for p in self.data['products'] if p['id']=='balance-basic-kit')
        product['price']['start_price']=129
        self.assertIn('$129',build.growth_purchase_options(self.data))

    def test_new_source_and_generated_pages_are_compliance_scanned(self):
        paths={p.relative_to(ROOT).as_posix() for p in ComplianceEngine().audit_paths()}
        for path in ['content/growth.json','about.html','privacy.html','know-your-number.html']:
            self.assertIn(path,paths)

    def test_false_success_subscription_cannot_be_published(self):
        html=(ROOT/'_review/growth-trust-conversion/email/signup-preview.html').read_text(encoding='utf-8')
        self.assertIn('NON-PUBLIC PROTOTYPE',html)
        self.assertIn('noindex,nofollow',html)
        self.assertNotIn(' checked',html)
        self.assertNotIn('name="email"',html)
        self.assertIn('onsubmit="return false"',html)
        js=(ROOT/'_review/growth-trust-conversion/email/signup-preview.js').read_text(encoding='utf-8')
        self.assertNotRegex(js,r'fetch\(|sendBeacon|localStorage|sessionStorage')
        self.assertIn('reader@example.invalid',js)

    def test_editorial_material_stays_out_of_public_discovery(self):
        for path in ['sitemap.xml','assets/data/search-index.json','library.html']:
            html=(ROOT/path).read_text(encoding='utf-8')
            self.assertNotIn('K2_REVIEW_ADDENDUM',html)
            self.assertNotIn('LABEL_CHECKLIST',html)
            self.assertNotIn('_review/growth-trust-conversion',html)

    def test_ci_packaging_includes_public_pages_not_private_prototype(self):
        yaml=(ROOT/'.github/workflows/validate.yml').read_text(encoding='utf-8')
        artifact=yaml.split('name: biocare-static-preview',1)[1]
        self.assertIn('about.html',artifact)
        self.assertIn('privacy.html',artifact)
        self.assertIn('products/',artifact)
        self.assertNotIn('_review/',artifact)

    def test_private_review_keeps_jekyll_exclusion_boundary(self):
        # The current Pages source is a Jekyll branch build. An alternate
        # publication pipeline needs explicit review, not a quiet bypass.
        self.assertFalse((ROOT/'.nojekyll').exists())
        config = (ROOT/'_config.yml').read_text(encoding='utf-8')
        self.assertIn('exclude:', config)
        for folder in ('_review', '_private', '_preview'):
            self.assertIn('  - ' + folder, config)
        self.assertNotIn('include:', config)
        self.assertFalse((ROOT/'_config.toml').exists())
        self.assertTrue((ROOT/'_review/growth-trust-conversion').is_dir())

    def test_purchase_comparison_backlink_is_limited_to_test_formats(self):
        for product in self.data['products']:
            if product.get('commercial_status') != 'active':
                continue
            html=(ROOT/f"products/{product['id']}.html").read_text(encoding='utf-8')
            self.assertEqual('class="section-warm growth-purchase-help"' in html,
                             product['id'] in self.data['growth']['journey']['productIds'])

    def test_no_measurement_runtime_dependency(self):
        js=(ROOT/'assets/js/growth-measurement.js').read_text(encoding='utf-8')
        self.assertNotRegex(js,r'fetch\(|sendBeacon|XMLHttpRequest|localStorage|sessionStorage|document\.cookie')

    def test_visible_focus_is_not_box_shadow_only(self):
        css=(ROOT/'assets/css/growth.css').read_text(encoding='utf-8')
        self.assertIn('forced-colors: active',css)
        self.assertIn('outline: 3px solid Highlight',css)

    def test_light_purchase_cards_override_dark_price_supporting_text(self):
        css=(ROOT/'assets/css/growth.css').read_text(encoding='utf-8')
        self.assertIn('.growth-purchase-card .product-price small { color: var(--section-muted)',css)
        self.assertIn('.growth-purchase-card .product-price__source { color: #20533d',css)
        self.assertEqual(build.growth_purchase_options(self.data).count('data-affiliate-disclosure'),1)


if __name__ == '__main__':
    unittest.main()
