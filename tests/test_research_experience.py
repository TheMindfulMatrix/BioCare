"""The review redesign preserves facts and progressively enhances navigation."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ResearchExperienceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = (ROOT / 'index.html').read_text(encoding='utf-8')
        cls.script = (ROOT / 'assets/js/experience.js').read_text(encoding='utf-8')
        cls.site = json.loads((ROOT / 'content/site.json').read_text(encoding='utf-8'))['site']

    def test_paths_have_static_content_and_unique_controls(self):
        self.assertIn('data-path-controls hidden', self.home)
        for key in ('learn', 'measure', 'explore'):
            self.assertEqual(1, self.home.count(f'id="path-{key}"'))
            self.assertEqual(1, self.home.count(f'data-path-choice="{key}"'))
            self.assertRegex(self.home, f'aria-controls="path-{key}"')
            panel = re.search(r'<section[^>]+data-path-panel="' + key + r'"[^>]*>', self.home).group()
            self.assertNotIn('hidden', panel)

    def test_functional_navigation_has_no_motion_or_tracking_dependency(self):
        for forbidden in ('matchMedia', 'localStorage', 'sessionStorage', 'fetch(', 'XMLHttpRequest', 'document.cookie', 'eval('):
            self.assertNotIn(forbidden, self.script)
        self.assertIn("setAttribute('aria-pressed'", self.script)
        self.assertIn('panel.hidden =', self.script)
        self.assertLess(len(self.script.encode()), 3000)

    def test_commercial_disclosure_is_not_collapsed(self):
        hero = self.home.split('data-home-stage="matrix"')[0]
        details = re.findall(r'<details\b[\s\S]*?</details>', hero)
        disclosure = self.site['affiliateSourceDisclosure']
        self.assertIn(disclosure, hero)
        self.assertTrue(all(disclosure not in item for item in details))
        self.assertIn('id="hero-affiliate-disclosure"', hero)

    def test_home_preview_does_not_remove_guides_from_library(self):
        library = json.loads((ROOT / 'content/library.json').read_text(encoding='utf-8'))
        count = sum(item['status'] == 'published' for item in library['articles'])
        self.assertEqual(min(3, count), self.home.count('data-library-article'))
        self.assertEqual(count, (ROOT / 'library.html').read_text(encoding='utf-8').count('data-library-article'))

    def test_library_search_precedes_secondary_categories(self):
        library = (ROOT / 'library.html').read_text(encoding='utf-8')
        self.assertLess(library.index('data-library-controls'), library.index('id="categories"'))

    def test_review_and_competitor_material_are_not_published(self):
        sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
        self.assertNotIn('_review', sitemap)
        self.assertNotIn('benchmark', sitemap)
        self.assertNotIn('https://seed.com', self.home)
        self.assertEqual('https://themindfulmatrixhealth.com/', self.site['metadata']['canonicalBaseUrl'])

    def test_catalog_sync_does_not_scroll_or_skip_document_entry(self):
        script = (ROOT / 'assets/js/enhancements.js').read_text(encoding='utf-8')
        sync = script.split('function syncControls()')[1].split('function chipLabel')[0]
        self.assertNotIn('scrollIntoView', sync)
        self.assertNotIn('.focus(', sync)
        self.assertIn('rail.scrollLeft', sync)


if __name__ == '__main__':
    unittest.main()
