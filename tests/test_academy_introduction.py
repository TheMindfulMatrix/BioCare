"""Public introduction must be useful without implying enrollment or leaking paid content."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class AcademyIntroductionTests(unittest.TestCase):
    def test_native_mobile_menu_does_not_depend_on_deferred_javascript(self):
        for name in ('learning.html','partners.html'):
            source=(ROOT/name).read_text(encoding='utf-8')
            self.assertIn('<details class="academy-native-menu">',source)
            self.assertIn('class="nav-links academy-desktop-links"',source)
            self.assertNotIn('class="nav-toggle"',source)
            self.assertEqual(source.count('id="primary-links"'),1)
    def test_both_introductions_include_fit_materials_and_honest_status(self):
        for name in ('learning.html','partners.html'):
            source=(ROOT/name).read_text(encoding='utf-8')
            for required in ('id="course-experience"','id="access-questions"','Three connected labs.','Content and learner review remain pending.','not open for enrollment','This page creates no student account.','protected lessons'):
                self.assertIn(required,source)
    def test_private_assets_prices_and_accounts_are_not_exposed(self):
        for name in ('learning.html','partners.html'):
            source=(ROOT/name).read_text(encoding='utf-8')
            for forbidden in ('127.0.0.1','review-app','complete-manuscript','-private-draft.json','19.99','39.99','checkout.stripe.com','data-packet','<video','<audio'):
                self.assertNotIn(forbidden,source)
            for path in ('testing.html','library.html','evidence.html','explore.html'):
                self.assertIn('href="'+path+'"',source)
    def test_network_marketing_is_explicit_and_sample_is_not_credential(self):
        source=(ROOT/'partners.html').read_text(encoding='utf-8')
        self.assertIn('independent network marketing with explicit Zinzino context',source)
        self.assertIn('not a professional credential',source)
        self.assertNotIn('<p>No. This is an original education project',source)
