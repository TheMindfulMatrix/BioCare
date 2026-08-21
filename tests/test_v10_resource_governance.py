from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_private_resources.py"
OUTPUT = ROOT / "_private" / "test-resource-audit"


def load_audit_module():
    spec = importlib.util.spec_from_file_location("audit_private_resources", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PrivateResourceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = load_audit_module()

    def test_classification_defaults_restrictive(self) -> None:
        cases = {
            "CompensationPlan_USA_eng.txt": "EXCLUDED",
            "Zinzino-Marketing-rules-and-ethics-English.txt": "INTERNAL / PARTNER ONLY",
            "Omega3andpregnancy_US.txt": "RESEARCH / REFERENCE ONLY",
            "Key-properties-overview-BalanceOil-EN.txt": "ONE-TO-ONE ONLY",
        }
        for filename, expected in cases.items():
            with self.subTest(filename=filename):
                self.assertEqual(self.audit.classify(filename)[0], expected)

    def test_no_private_resource_is_automatically_public_eligible(self) -> None:
        for filename in (
            "Customer-Presentation-PDF-en-USA.txt",
            "Certificate-Informed-Sport-Zinzino-BalanceOil-plus.txt",
            "NCBI_Fish_OilDerived_Fatty_Acids_in_Pregnancy.txt",
        ):
            self.assertNotEqual(self.audit.classify(filename)[0], "PUBLIC WEBSITE ELIGIBLE")

    def test_audit_is_read_only_and_deterministic(self) -> None:
        shutil.rmtree(OUTPUT, ignore_errors=True)
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "private-library"
            docs = source / "docs"
            docs.mkdir(parents=True)
            (source / "README.md").write_text("Private; non-redistributable.\n", encoding="utf-8")
            (source / "INDEX.md").write_text("Reference-only science.\n", encoding="utf-8")
            filenames = {
                "CompensationPlan_USA_eng.txt": "Commission and career material.\n",
                "Zinzino-Marketing-rules-and-ethics-English.txt": "Independent Partner compliance policy.\n",
                "Omega3andpregnancy_US.txt": "Research references DOI 10.1000/example.\n",
                "Key-properties-overview-BalanceOil-EN.txt": "Manufacturer product information.\n",
            }
            manifest = []
            for filename, content in filenames.items():
                (docs / filename).write_text(content, encoding="utf-8")
                manifest.append(f"filelibrary/{Path(filename).stem}.pdf")
            (source / "_manifest.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
            subprocess.run(["git", "init", "-b", "master", str(source)], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(source), "config", "user.name", "V10 Test"], check=True)
            subprocess.run(["git", "-C", str(source), "config", "user.email", "v10@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(source), "add", "--", "README.md", "INDEX.md", "_manifest.txt", "docs"], check=True)
            subprocess.run(["git", "-C", str(source), "commit", "-m", "fixture"], check=True, capture_output=True)
            sha = subprocess.run(["git", "-C", str(source), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
            command = [
                sys.executable,
                str(SCRIPT),
                "--source-path",
                str(source),
                "--source-repo-sha",
                sha,
                "--output-dir",
                str(OUTPUT),
            ]
            subprocess.run(command, cwd=ROOT, check=True, capture_output=True)
            first = hashlib.sha256((OUTPUT / "resources.json").read_bytes()).hexdigest()
            subprocess.run(command, cwd=ROOT, check=True, capture_output=True)
            second = hashlib.sha256((OUTPUT / "resources.json").read_bytes()).hexdigest()
            payload = json.loads((OUTPUT / "resources.json").read_text(encoding="utf-8"))
            self.assertEqual(first, second)
            self.assertEqual(payload["resource_count"], 4)
            self.assertEqual(payload["classification_totals"]["PUBLIC WEBSITE ELIGIBLE"], 0)
            self.assertEqual(
                subprocess.run(["git", "-C", str(source), "status", "--porcelain"], check=True, capture_output=True, text=True).stdout,
                "",
            )
        shutil.rmtree(OUTPUT, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
