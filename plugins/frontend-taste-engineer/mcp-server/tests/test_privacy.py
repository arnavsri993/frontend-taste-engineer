from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


TOOLING = Path(__file__).resolve().parents[2] / "scripts" / "tooling_core.py"
SPEC = importlib.util.spec_from_file_location("fte_tooling_privacy_tests", TOOLING)
assert SPEC and SPEC.loader
tooling = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = tooling
SPEC.loader.exec_module(tooling)


class PrivacyScannerTests(unittest.TestCase):
    def args(self, root: Path, terms: Path) -> argparse.Namespace:
        return argparse.Namespace(target=str(root), terms_file=terms, require_terms=True, max_file_bytes=1_000_000)

    def test_private_term_is_detected_without_echoing_value(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            private_value = "PRIVATE_FIXTURE_TERM"
            terms = root / ".private-terms"
            terms.write_text(private_value + "\n", encoding="utf-8")
            (root / "report.log").write_text(f"prefix {private_value} suffix\n", encoding="utf-8")
            report = tooling.privacy_scan(self.args(root, terms))
            encoded = json.dumps(report.value())
            self.assertFalse(report.passed)
            self.assertNotIn(private_value, encoded)
            self.assertEqual(report.details["matches"], 1)

    def test_private_term_is_detected_inside_package_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            private_value = "ARCHIVE_PRIVATE_FIXTURE"
            terms = root / ".private-terms"
            terms.write_text(private_value + "\n", encoding="utf-8")
            package = root / "plugin.zip"
            with zipfile.ZipFile(package, "w") as archive:
                archive.writestr("evidence/result.txt", f"synthetic {private_value} content")
            report = tooling.privacy_scan(self.args(root, terms))
            encoded = json.dumps(report.value())
            self.assertFalse(report.passed)
            self.assertNotIn(private_value, encoded)
            self.assertEqual(report.details["archives_scanned"], 1)
            self.assertGreaterEqual(report.details["matches"], 1)

    def test_clean_tree_passes_with_configured_terms(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            terms = root / ".private-terms"
            terms.write_text("UNUSED_PRIVATE_FIXTURE\n", encoding="utf-8")
            (root / "public.md").write_text("Synthetic public evaluation content.\n", encoding="utf-8")
            report = tooling.privacy_scan(self.args(root, terms))
            self.assertTrue(report.passed)
            self.assertEqual(report.details["matches"], 0)


if __name__ == "__main__":
    unittest.main()
