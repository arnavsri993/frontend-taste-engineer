from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SERVER = Path(__file__).resolve().parents[1] / "server.py"
SPEC = importlib.util.spec_from_file_location("fte_server", SERVER)
assert SPEC and SPEC.loader
server = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = server
SPEC.loader.exec_module(server)


RECORDS = [
    {
        "id": "dialog.focus-restoration",
        "title": "Restore dialog focus",
        "topic": "accessibility",
        "subtopic": "focus-management",
        "status": "stable",
        "importance": "mandatory",
        "confidence": "high",
        "task_types": ["component-build"],
        "components": ["dialog"],
        "frameworks": ["universal"],
        "principle": "Return focus to the trigger or a logical target after a modal dialog closes.",
        "rationale": "Keyboard users otherwise lose their place.",
        "implementation": ["Capture the logical trigger", "Restore focus after teardown"],
        "verification": ["Open and close with a keyboard", "Test when the trigger is removed"],
        "sources": ["wai-dialog-pattern"],
        "license_status": "summarized",
    },
    {
        "id": "motion.reduced-motion",
        "title": "Honor reduced motion",
        "topic": "motion",
        "status": "stable",
        "importance": "mandatory",
        "principle": "Provide a reduced-motion treatment that removes nonessential movement.",
        "rationale": "Motion can cause discomfort.",
        "implementation": ["Use prefers-reduced-motion"],
        "verification": ["Test the reduced motion preference"],
        "sources": ["wcag-motion"],
        "license_status": "summarized",
    },
    {
        "id": "visual.purple-gradient",
        "title": "Use gradients only with product rationale",
        "topic": "anti-patterns",
        "status": "stable",
        "importance": "recommended",
        "principle": "Do not use a purple gradient as a reflexive substitute for a product-specific visual direction.",
        "rationale": "Repeated defaults make products interchangeable.",
        "implementation": ["Define a design thesis first"],
        "verification": ["Trace each visual choice to the brief"],
        "sources": ["internal-synthesis"],
        "license_status": "original",
    },
]


class EngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "records.json").write_text(json.dumps(RECORDS), encoding="utf-8")
        self.engine = server.RetrievalEngine(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_preserves_dotted_exact_identifier(self) -> None:
        packet = self.engine.search("dialog.focus-restoration", budget_records=1)
        self.assertEqual(packet["records"][0]["id"], "dialog.focus-restoration")
        self.assertIn("exact-id", packet["records"][0]["retrieval"]["reasons"])

    def test_hybrid_expansion_and_metadata(self) -> None:
        packet = self.engine.search(
            "modal keyboard focus",
            {"topics": ["accessibility"], "components": ["dialog"]},
            budget_records=3,
        )
        self.assertEqual(packet["records"][0]["id"], "dialog.focus-restoration")
        self.assertEqual(packet["summary"]["mandatory_returned"], 1)

    def test_dedupe_and_context_budget(self) -> None:
        duplicate = dict(RECORDS[0], id="dialog.same-principle")
        (self.root / "more.json").write_text(json.dumps([duplicate]), encoding="utf-8")
        engine = server.RetrievalEngine(self.root)
        packet = engine.search("dialog focus", budget_records=4, context_budget=300)
        principles = [item["principle"] for item in packet["records"]]
        self.assertEqual(len(principles), len(set(principles)))
        self.assertLessEqual(packet["summary"]["estimated_context_tokens"], 300)

    def test_offline_fallback_is_explicit(self) -> None:
        empty = self.root / "empty"
        empty.mkdir()
        engine = server.RetrievalEngine(empty)
        packet = engine.search("responsive keyboard states")
        self.assertTrue(packet["summary"]["offline_fallback"])
        self.assertGreater(len(packet["records"]), 0)

    def test_audit_reports_missing_evidence(self) -> None:
        report = server.call_tool(self.engine, "audit_frontend_plan", {"plan": "Build a clean page."})
        ids = {item["id"] for item in report["findings"]}
        self.assertIn("keyboard-focus", ids)
        self.assertIn("verification-evidence", ids)

    def test_maintenance_tools_do_not_write(self) -> None:
        before = sorted(path.read_bytes() for path in self.root.iterdir())
        report = server.call_tool(self.engine, "generate_coverage_report", {})
        after = sorted(path.read_bytes() for path in self.root.iterdir())
        self.assertEqual(before, after)
        self.assertFalse(report["stable_knowledge_modified"])

    def test_entire_declared_tool_surface_is_callable(self) -> None:
        special = {
            "classify_frontend_task": {"task": "Build an accessible responsive dialog"},
            "get_workflow": {"stage": "implementation", "task": "dialog"},
            "get_component_state_matrix": {"component": "dialog"},
            "get_source_provenance": {"id": "dialog.focus-restoration"},
            "audit_frontend_plan": {"plan": "keyboard focus responsive states performance evidence"},
            "audit_frontend_implementation": {"implementation": "keyboard focus responsive states performance evidence"},
            "compare_design_directions": {"context": "serious enterprise", "directions": ["quiet system", "playful brand"]},
            "propose_knowledge_update": {"proposal": "candidate rule"},
        }
        for tool in server.TOOLS:
            with self.subTest(tool=tool["name"]):
                result = server.call_tool(self.engine, tool["name"], special.get(tool["name"], {"query": "accessible responsive dialog keyboard"}))
                self.assertIsInstance(result, dict)


class StdioIntegrationTests(unittest.TestCase):
    def test_initialize_list_and_call(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "records.json").write_text(json.dumps(RECORDS), encoding="utf-8")
            proc = subprocess.Popen(
                [sys.executable, str(SERVER), "--knowledge-dir", str(root)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            assert proc.stdin and proc.stdout
            messages = [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": server.PROTOCOL_VERSION, "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}},
                {"jsonrpc": "2.0", "method": "notifications/initialized"},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
                {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "search_frontend_guidance", "arguments": {"query": "dialog keyboard", "budget_records": 2}}},
            ]
            for message in messages:
                proc.stdin.write(json.dumps(message) + "\n")
            proc.stdin.close()
            responses = [json.loads(proc.stdout.readline()) for _ in range(3)]
            stderr = proc.stderr.read() if proc.stderr else ""
            proc.wait(timeout=5)
            proc.stdout.close()
            if proc.stderr:
                proc.stderr.close()
            self.assertEqual(proc.returncode, 0, stderr)
            self.assertEqual(responses[0]["result"]["serverInfo"]["name"], "frontend-taste-engineer")
            names = {item["name"] for item in responses[1]["result"]["tools"]}
            self.assertIn("classify_frontend_task", names)
            self.assertIn("generate_coverage_report", names)
            self.assertFalse(responses[2]["result"]["isError"])
            self.assertEqual(responses[2]["result"]["structuredContent"]["records"][0]["id"], "dialog.focus-restoration")


if __name__ == "__main__":
    unittest.main()
