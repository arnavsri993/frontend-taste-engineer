from __future__ import annotations

import sys
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PLUGIN_ROOT / "evals" / "copy"))
from copy_quality import audit_copy  # noqa: E402


class CopyQualityTests(unittest.TestCase):
    def test_internal_build_narration_is_flagged(self) -> None:
        copy = (
            "Development preview with mocked connectors and no agent endpoint. "
            "Competition results are not shown because none were supplied."
        )

        findings = audit_copy(copy)["findings"]

        self.assertTrue(any(row["code"] == "internal-build-narration" for row in findings))

    def test_user_relevant_consequence_is_not_build_narration(self) -> None:
        copy = "Submitting this form does not confirm eligibility; the agency will review it and send a decision."

        findings = audit_copy(copy)["findings"]

        self.assertFalse(any(row["code"] == "internal-build-narration" for row in findings))

    def test_dense_interface_copy_is_flagged_for_review(self) -> None:
        copy = (
            "This workspace provides a comprehensive and thoughtfully organized collection of tools that can help "
            "every member of your team understand project activity, coordinate their daily work, review important "
            "updates, discover useful information, and make better decisions without needing to switch between "
            "multiple separate applications."
        )

        report = audit_copy(copy)
        codes = {row["code"] for row in report["findings"]}

        self.assertIn("dense-interface-copy", codes)
        self.assertIn("long-interface-sentence", codes)
        self.assertGreater(report["metrics"]["max_block_words"], 40)

    def test_short_specific_interface_copy_stays_clear(self) -> None:
        copy = "Review project activity and assign the next step."

        findings = audit_copy(copy)["findings"]

        self.assertFalse(any(row["code"] in {"dense-interface-copy", "long-interface-sentence"} for row in findings))


if __name__ == "__main__":
    unittest.main()
