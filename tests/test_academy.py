"""Static contracts, not a substitute for requested browser or screen-reader QA."""
from html.parser import HTMLParser
import json
from pathlib import Path
import unittest
from scripts.compliance_engine import ComplianceEngine, path_context

ROOT = Path(__file__).resolve().parents[1]


class Markup(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class AcademyTests(unittest.TestCase):
    def pages(self):
        for name in ('learning.html', 'partners.html'):
            text = (ROOT / name).read_text(encoding='utf-8')
            yield name, text, Markup(text).elements

    def test_runtime_and_styles_only_added_to_academy_pages(self):
        for _, text, _ in self.pages():
            self.assertIn('assets/js/academy.js?v=', text)
            self.assertIn('assets/css/academy.css?v=', text)
        for name in ('index.html', 'testing.html', 'library.html', 'shop.html'):
            self.assertNotIn('academy.js', (ROOT / name).read_text(encoding='utf-8'))

    def test_real_original_photography_has_responsive_variants(self):
        for _, text, elements in self.pages():
            images = [a for tag, a in elements if tag == 'img' and '/academy/' in a.get('src', '')]
            self.assertTrue(images)
            for image in images:
                self.assertIn('640w', image['srcset'])
                self.assertIn('1280w', image['srcset'])
                self.assertEqual(image['width'], '1280')
                self.assertEqual(image['height'], '853')
                self.assertIn('alt', image)
                self.assertTrue((ROOT / image['src']).is_file())
            self.assertIn('AI-generated illustrations', text)
            self.assertIn('not actual students, instructors or events', text)

    def test_all_three_static_lesson_panels_are_visible_without_javascript(self):
        for _, text, elements in self.pages():
            panels = [a for tag, a in elements if 'data-panel' in a]
            self.assertEqual([p['data-panel'] for p in panels], ['0', '1', '2'])
            self.assertTrue(all('hidden' not in p for p in panels))
            self.assertIn('<noscript>', text)
            self.assertIn('Read the answer', text)

    def test_label_associations_status_regions_and_native_controls(self):
        for _, text, elements in self.pages():
            ids = [a['id'] for _, a in elements if 'id' in a]
            self.assertEqual(len(ids), len(set(ids)))
            for tag, attrs in elements:
                if tag == 'label' and 'for' in attrs:
                    self.assertIn(attrs['for'], ids)
                if tag == 'button' and 'academy-button' in attrs.get('class', ''):
                    self.assertEqual(attrs.get('type'), 'button')
            self.assertEqual(sum(tag == 'fieldset' for tag, _ in elements), 1)
            self.assertEqual(sum(tag == 'progress' for tag, _ in elements), 1)
            self.assertIn('role="status"', text)
            self.assertIn('aria-live="polite"', text)

    def test_curriculum_counts_match_canonical_outlines(self):
        for (name, _, elements), content in zip(self.pages(), ['learning.json','partner-learning.json']):
            modules = json.loads((ROOT / 'content' / content).read_text())['modules']
            cards = [a for tag, a in elements if tag == 'details' and a.get('class') == 'academy-module']
            self.assertEqual(len(cards), len(modules), name)

    def test_commercial_plans_come_from_the_audited_partner_source(self):
        config = ROOT / 'content/partner-learning.json'
        self.assertIn(config, ComplianceEngine().audit_paths())
        self.assertEqual(path_context(config), 'MLM_RECRUITMENT')
        template = json.loads(config.read_text())['practice']['template']
        self.assertIn('benefit commercially', template)
        self.assertIn('No pressure', template)
        self.assertTrue(any('practice.template' in f.location for f in ComplianceEngine().scan_json(config)))

    def test_sample_config_and_every_selector_choice_are_consistent(self):
        for (name, text, elements), source in zip(self.pages(), ['learning.json','partner-learning.json']):
            copy = json.loads((ROOT / 'content' / source).read_text())['practice']
            for key in ('cues','actions','topics','formats'):
                for value in copy.get(key, {}):
                    self.assertTrue(any(tag == 'option' and a.get('value') == value for tag, a in elements), (name, key, value))
            self.assertIn('data-practice-copy', text)
            self.assertIn(json.dumps(copy, ensure_ascii=True).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026'), text)

    def test_images_remain_within_review_payload_budget(self):
        sizes = {p.name: p.stat().st_size for p in (ROOT / 'assets/images/academy').glob('*.webp')}
        self.assertEqual(len(sizes), 4)
        self.assertLess(sum(sizes.values()), 300000)
        self.assertTrue(all(size < 120000 for size in sizes.values()))

    def test_no_fake_video_or_sales_controls(self):
        for _, text, elements in self.pages():
            main = text.split('<main', 1)[1].split('</main>', 1)[0]
            # The existing global header has a real site-search form.
            self.assertFalse(any(tag in ('iframe','video','form') for tag, _ in Markup(main).elements))
            self.assertIn('Not available for purchase', text)
            self.assertIn('choices are not saved or sent', text)
            self.assertNotIn('Enroll now', text)
            self.assertNotIn('Watch lesson', text)


if __name__ == '__main__':
    unittest.main()
