from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = PLUGIN_ROOT / "scripts" / "monitor_registered_sources.py"
SPEC = importlib.util.spec_from_file_location("fte_source_monitor", SCRIPT)
assert SPEC and SPEC.loader
monitor = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = monitor
SPEC.loader.exec_module(monitor)


class FakeClient:
    def __init__(self, responses: dict[str, monitor.Response]) -> None:
        self.responses = responses

    def fetch(self, url: str, *, github_api: bool = False) -> monitor.Response:
        return self.responses[url]


def response(url: str, value: object, content_type: str = "application/json") -> monitor.Response:
    body = json.dumps(value).encode() if content_type == "application/json" else str(value).encode()
    return monitor.Response(200, url, content_type, {}, body)


class SourceMonitorTests(unittest.TestCase):
    def test_registry_parser_reads_reviewed_sources(self) -> None:
        entries = monitor.parse_registry(monitor.DEFAULT_REGISTRY)
        ids = {entry["id"] for entry in entries}
        self.assertIn("emil-design-skills", ids)
        self.assertIn("wcag-22", ids)
        self.assertGreaterEqual(len(entries), 30)

    def test_github_revision_change_and_license_are_review_gated(self) -> None:
        source = {
            "id": "example",
            "canonical_url": "https://github.com/example/project",
            "classification": "specialized",
            "license": "MIT",
            "last_checked_revision": "1111111",
        }
        repo_url = "https://api.github.com/repos/example/project"
        commit_url = "https://api.github.com/repos/example/project/commits/main"
        client = FakeClient({
            repo_url: response(repo_url, {"default_branch": "main", "license": {"spdx_id": "Apache-2.0"}, "archived": False, "disabled": False}),
            commit_url: response(commit_url, {"sha": "2222222222222222222222222222222222222222", "commit": {"committer": {"date": "2026-07-17T12:00:00Z"}}}),
        })
        report = monitor.monitor_sources([source], client, as_of="2026-07-17")
        item = report["sources"][0]
        self.assertTrue(report["review_required"])
        self.assertIn("upstream-revision-changed", item["review_reasons"])
        self.assertIn("license-metadata-needs-review", item["review_reasons"])
        self.assertFalse(report["stable_knowledge_modified"])

    def test_public_text_fingerprint_uses_prior_report_without_storing_page(self) -> None:
        source = {
            "id": "docs",
            "canonical_url": "https://example.com/docs",
            "classification": "specialized",
            "license": "Documentation terms",
            "last_checked_revision": "live-page@2026-07-10",
        }
        page = monitor.Response(
            200,
            source["canonical_url"],
            "text/html",
            {"etag": '"v2"'},
            b"<main>Updated guidance</main><script>secret page noise</script>",
        )
        baseline = {"sources": [{"id": "docs", "content_sha256": "old"}]}
        report = monitor.monitor_sources([source], FakeClient({source["canonical_url"]: page}), baseline=baseline, as_of="2026-07-17")
        item = report["sources"][0]
        self.assertIn("public-content-changed", item["review_reasons"])
        self.assertNotIn("Updated guidance", json.dumps(report))
        self.assertNotIn("secret page noise", json.dumps(report))

    def test_reports_cannot_write_into_stable_knowledge(self) -> None:
        with self.assertRaises(monitor.MonitorError):
            monitor.safe_output(PLUGIN_ROOT / "knowledge" / "monitor.json")
        with tempfile.TemporaryDirectory() as temp:
            destination = monitor.safe_output(Path(temp) / "monitor.json")
            self.assertTrue(str(destination).endswith("monitor.json"))


if __name__ == "__main__":
    unittest.main()
