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


if __name__ == "__main__":
    unittest.main()
