"""Prevent asymmetric compliance comparisons as public Academy surfaces expand."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from audit_learning_candidate import baseline_paths


class LearningAuditBaselineTests(unittest.TestCase):
    def test_all_public_copy_surfaces_are_included(self):
        expected = ['learning.html','partners.html','testing.html','content/partner-learning.json',
                    'content/compliance/codex-production-gate.txt','library/example.html',
                    'social/disclosure.md','scripts/compliance_engine.py','scripts/validate_compliance.py']
        self.assertEqual(baseline_paths(expected), sorted(expected))

    def test_private_records_and_media_are_excluded(self):
        self.assertEqual(baseline_paths(['_private/course.html','_review/notes.json',
                                        'assets/video.mp4','content/large-image.png','scripts/build.py']), [])
