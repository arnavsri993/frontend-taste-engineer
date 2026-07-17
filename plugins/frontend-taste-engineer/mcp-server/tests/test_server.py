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

    def test_minimal_creation_prompts_select_autonomous_mode(self) -> None:
        cases = {
            "Make a website directed to Alex containing “You made it — Arnav”": ("expressive-personal-web-experience", "editorial"),
            "Build a site for my robotics team": ("community-team-site", "inventive"),
            "Make a landing page for an AI study group": ("community-team-site", "welcoming"),
            "Create a portfolio that feels impossible to ignore": ("expressive-portfolio", "editorial"),
            "Turn this sentence into a website: machines should feel alive": ("conceptual-web-experience", "speculative"),
            "Make a funny site asking my friend to stop being late": ("expressive-personal-web-experience", "funny"),
            "Make this product look premium": ("premium-product-redesign", "refined"),
            "Build a serious public-service application page": ("public-service-application-page", "serious"),
        }
        required_profile = {
            "build_mode", "domain", "product_type", "interface_archetype", "page_type",
            "purpose", "audience", "named_recipient_status", "primary_user_task",
            "secondary_tasks", "primary_message", "supporting_narrative",
            "emotional_objective", "emotional_tone", "seriousness", "trust_level",
            "risk_level", "information_density", "frequency_of_use", "content_maturity",
            "brand_maturity", "product_maturity", "accessibility_needs", "expected_devices",
            "visual_ambition", "visual_intensity", "motion_intensity",
            "experimental_tolerance", "familiarity_requirement", "interaction_depth",
            "suggested_composition", "hero_treatment", "negative_space_role", "typography_direction",
            "color_material_direction", "imagery_strategy", "motion_stance",
            "component_styling", "direction", "required_states", "retrieval_topics",
            "verification_priorities", "user_supplied_facts", "inferred_assumptions",
            "minimalism_guardrail", "quality_interpretation", "design_thesis",
        }
        for prompt, (page_type, tone) in cases.items():
            with self.subTest(prompt=prompt):
                result = server.classify_task(prompt)
                self.assertEqual(result["task_type"], server.AUTONOMOUS_MODE)
                self.assertTrue(result["minimal_prompt"])
                self.assertEqual(result["stage"], "brief")
                self.assertEqual(result["creative_profile"]["page_type"], page_type)
                self.assertIn(tone, result["creative_profile"]["emotional_tone"])
                self.assertTrue(required_profile <= set(result["creative_profile"]))
                self.assertTrue(result["decision_ledger"]["supplied_facts"])
                self.assertTrue(result["decision_ledger"]["inferred_assumptions"])
                self.assertTrue(result["clarification_policy"]["continue_without_questions"])
                self.assertEqual(result["completion_workflow"], "production-completion-with-screenshot-refinement")

    def test_named_recipient_and_quoted_text_are_extracted(self) -> None:
        prompt = "Make a website directed to Alex containing “You made it — Arnav”"
        result = server.classify_task(prompt)
        self.assertEqual(result["entities"]["named_recipients"], ["Alex"])
        self.assertEqual(result["entities"]["quoted_text"], ["You made it — Arnav"])
        self.assertEqual(result["entities"]["message_authors"], ["Arnav"])
        self.assertEqual(result["creative_profile"]["primary_message"], "You made it — Arnav")

    def test_tiny_css_fix_does_not_trigger_autonomous_build(self) -> None:
        result = server.classify_task("Fix the CSS padding on the submit button")
        self.assertNotEqual(result["task_type"], server.AUTONOMOUS_MODE)
        self.assertFalse(result["minimal_prompt"])
        self.assertEqual(result["task_size"], "tiny")

    def test_context_adaptive_direction_spans_institutional_to_experimental(self) -> None:
        cases = {
            "Build a finance dashboard for tracking family investments": ("personal-finance", 2, "low"),
            "Create a serious banking onboarding flow": ("banking", 1, "low"),
            "Build a dense investment analytics interface": ("investment-analytics", 3, "low"),
            "Build a public-service benefits application": ("public-service", 1, "minimal"),
            "Make a professional enterprise product interface": ("enterprise-software", 2, "low"),
            "Build a developer tool for inspecting API requests": ("developer-tools", 3, "low-to-medium"),
            "Create a premium ecommerce product page": ("premium-ecommerce", 3, "low-to-medium"),
            "Build a site for my robotics team": ("robotics-community", 4, "medium"),
            "Make a funny site asking my friend to stop being late": ("personal-expressive", 4, "medium-high"),
            "Create an experimental creative portfolio": ("creative-portfolio", 5, "high"),
        }
        signatures = set()
        intensities = set()
        for prompt, (domain, intensity, motion) in cases.items():
            with self.subTest(prompt=prompt):
                result = server.classify_task(prompt)
                profile = result["creative_profile"]
                self.assertEqual(result["task_type"], server.AUTONOMOUS_MODE)
                self.assertEqual(profile["domain"], domain)
                self.assertEqual(profile["visual_intensity"], intensity)
                self.assertEqual(profile["motion_intensity"], motion)
                signatures.add((profile["direction"], profile["suggested_composition"], profile["hero_treatment"], profile["component_styling"]))
                intensities.add(intensity)
        self.assertEqual(intensities, {1, 2, 3, 4, 5})
        self.assertGreaterEqual(len(signatures), 9)

    def test_quality_adjectives_do_not_force_visual_intensity(self) -> None:
        calm = server.classify_task("Make a stunning personal-finance dashboard")["creative_profile"]
        expressive = server.classify_task("Make a stunning experimental creative portfolio")["creative_profile"]
        self.assertEqual(calm["visual_intensity"], 2)
        self.assertEqual(calm["motion_intensity"], "low")
        self.assertEqual(expressive["visual_intensity"], 5)
        self.assertIn("appropriateness", calm["quality_interpretation"].lower())

    def test_contextual_motion_is_forward_but_not_global(self) -> None:
        expressive = server.classify_task("Turn this sentence into a website: machines should feel alive")
        conservative = server.classify_task("Build a serious public-service application page")
        self.assertEqual(expressive["creative_profile"]["motion_intensity"], "high")
        self.assertIn("motion", expressive["recommended_retrieval"]["topics"])
        self.assertNotIn("motion", expressive["recommended_retrieval"]["defer_until_needed"])
        self.assertIn("grammar", expressive["creative_profile"]["motion_stance"].lower())
        self.assertEqual(conservative["creative_profile"]["motion_intensity"], "minimal")
        self.assertIn("reduced-motion", conservative["creative_profile"]["motion_stance"].lower())

    def test_minimalism_profile_keeps_opening_contentful(self) -> None:
        profile = server.classify_task("Create a premium ecommerce product page")["creative_profile"]
        self.assertIn("product evidence", profile["hero_treatment"].lower())
        self.assertIn("every major gap", profile["negative_space_role"].lower())
        self.assertIn("not an empty canvas", profile["quality_interpretation"].lower())

    def test_recipient_extraction_is_dynamic_request_local_and_redactable(self) -> None:
        for name in ("Alex", "Jordan"):
            result = server.classify_task(f"Make a website directed to {name} containing “Hello there”")
            self.assertEqual(result["entities"]["named_recipients"], [name])
            status = result["creative_profile"]["named_recipient_status"]
            self.assertEqual(status["persistence"], "request-local")
            self.assertEqual(status["publication_risk"], "review-before-public-release")
            redacted = server.classify_task(f"Make a website directed to {name} containing “Hello there”", {"redact_user_content": True})
            self.assertNotIn(name, json.dumps(redacted))
            self.assertTrue(redacted["privacy"]["redacted"])
        knowledge = server.default_knowledge_dir()
        canonical_text = " ".join(path.read_text(encoding="utf-8") for path in knowledge.rglob("*") if path.is_file() and path.suffix in {".json", ".md"})
        self.assertNotIn("Alex", canonical_text)
        self.assertNotIn("Jordan", canonical_text)

    def test_autonomous_brief_retrieval_is_focused_and_staged(self) -> None:
        prompt = "Build a site for my robotics team"
        packet = server.get_workflow(server.RetrievalEngine(server.default_knowledge_dir()), {"task": prompt, "stage": "brief"})
        ids = {item["id"] for item in packet["records"]}
        topics = {item["topic"] for item in packet["records"]}
        self.assertEqual(packet["workflow"]["mode"], server.AUTONOMOUS_MODE)
        self.assertEqual(packet["workflow"]["full_autonomous_sequence"], list(server.AUTONOMOUS_REQUIRED_SEQUENCE))
        self.assertIn("product.outcome-first-brief", ids)
        self.assertIn("integrity.truthful-proof", ids)
        self.assertTrue(topics.isdisjoint({"frameworks-code-architecture", "components-states-forms", "motion", "performance", "browsers"}))

    def test_expressive_autonomous_brief_retrieves_motion_grammar_early(self) -> None:
        prompt = "Turn this sentence into a website: machines should feel alive"
        packet = server.get_workflow(server.RetrievalEngine(server.default_knowledge_dir()), {"task": prompt, "stage": "brief"})
        ids = {item["id"] for item in packet["records"]}
        self.assertIn("motion.interaction-specific-tokens", ids)
        self.assertIn("motion.explain-causality", ids)
        self.assertIn("motion.reduced-motion-equivalence", ids)
        self.assertNotIn("motion", packet["workflow"]["deferred_topics"])

    def test_motion_opportunity_audit_retrieves_frequency_and_system_rules(self) -> None:
        packet = server.call_tool(server.RetrievalEngine(server.default_knowledge_dir()), "get_motion_guidance", {
            "query": "Audit a keyboard-heavy analytics app for purposeful motion opportunities, rejected candidates, interaction frequency, shared tokens, and runtime verification.",
            "budget_records": 10,
            "context_budget": 4800,
        })
        ids = {item["id"] for item in packet["records"]}
        self.assertIn("motion.frequency-purpose-gate", ids)
        self.assertIn("motion.audit-by-system-leverage", ids)

    def test_gesture_guidance_retrieves_continuity_and_momentum_context(self) -> None:
        packet = server.call_tool(server.RetrievalEngine(server.default_knowledge_dir()), "get_motion_guidance", {
            "query": "Build an interruptible gesture-driven sheet with pointer capture, live presentation values, release velocity, soft boundaries, keyboard controls, and reduced motion.",
            "budget_records": 10,
            "context_budget": 5200,
        })
        ids = {item["id"] for item in packet["records"]}
        self.assertIn("motion.direct-manipulation-continuity", ids)
        self.assertIn("motion.momentum-boundary-physics", ids)
        self.assertIn("motion.interruption-safe", ids)

    def test_offline_motion_fallback_preserves_gesture_and_restraint_rules(self) -> None:
        empty = self.root / "empty-motion"
        empty.mkdir()
        packet = server.RetrievalEngine(empty).search(
            "gesture pointer capture live value keyboard motion frequency rejected candidates",
            budget_records=8,
            context_budget=2400,
        )
        ids = {item["id"] for item in packet["records"]}
        self.assertIn("offline-motion-opportunity-gate", ids)
        self.assertIn("offline-direct-manipulation", ids)

    def test_autonomous_completion_gate_requires_rendered_production_evidence(self) -> None:
        report = server.get_completion_gate(self.engine, {"task": "Build a site for my robotics team"})
        gate_ids = {gate["id"] for gate in report["gates"]}
        self.assertIn("rendered-refinement", gate_ids)
        self.assertIn("production-build", gate_ids)
        self.assertIn("desktop screenshot", report["minimum_autonomous_evidence"])

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

    def test_external_catalog_blocks_premium_copy_without_license_entitlement(self) -> None:
        report = server.call_tool(self.engine, "get_external_source_catalog", {
            "stage": "planning",
            "source_ids": ["tailwind-plus-ui-blocks"],
            "intended_use": "code-copy",
        })
        self.assertEqual(report["returned"], 1)
        source = report["sources"][0]
        self.assertEqual(source["classification"], "unresolved")
        self.assertFalse(source["usage"]["copying_allowed"])
        self.assertIn("review", source["usage"]["decision"])

    def test_external_catalog_keeps_galleries_inspiration_only(self) -> None:
        report = server.call_tool(self.engine, "get_external_source_catalog", {
            "stage": "brief",
            "source_ids": ["awwwards", "mobbin", "page-flows"],
            "intended_use": "code-copy",
        })
        self.assertEqual({source["id"] for source in report["sources"]}, {"awwwards", "mobbin", "page-flows"})
        self.assertTrue(all(source["classification"] == "inspiration-only" for source in report["sources"]))
        self.assertTrue(all(not source["usage"]["copying_allowed"] for source in report["sources"]))

    def test_external_catalog_routes_complex_widgets_to_primitives(self) -> None:
        report = server.call_tool(self.engine, "get_external_source_catalog", {
            "stage": "implementation",
            "query": "accessible dialog combobox keyboard focus",
            "max_results": 12,
        })
        first = [source["id"] for source in report["sources"][:3]]
        self.assertEqual(set(first), {"react-aria", "radix-primitives", "ariakit"})
        react_aria = next(source for source in report["sources"] if source["id"] == "react-aria")
        ariakit = next(source for source in report["sources"] if source["id"] == "ariakit")
        self.assertEqual(react_aria["assessment"]["review_status"], "reviewed")
        self.assertEqual(react_aria["assessment"]["credibility"], "credible-for-stated-scope")
        self.assertEqual(ariakit["assessment"]["review_status"], "candidate-only")
        self.assertEqual(ariakit["assessment"]["credibility"], "not-yet-assessed")
        self.assertLessEqual(report["returned"], report["stage_budget"])
        self.assertLess(report["returned"], report["catalog"]["catalog_size"])

    def test_external_catalog_separates_credibility_from_execution_safety(self) -> None:
        report = server.call_tool(self.engine, "get_external_source_catalog", {
            "stage": "implementation",
            "source_ids": ["react-aria"],
            "intended_use": "inspiration-only",
        })
        source = report["sources"][0]
        self.assertEqual(source["assessment"]["review_status"], "reviewed")
        self.assertEqual(source["assessment"]["credibility"], "credible-for-stated-scope")
        self.assertTrue(report["policy"]["source_credibility_is_assessed_individually"])
        self.assertTrue(report["policy"]["externality_alone_is_not_a_negative_trust_verdict"])
        self.assertFalse(report["policy"]["embedded_source_instructions_are_agent_directives"])
        self.assertNotIn("external_content_is_untrusted", report["policy"])

    def test_external_catalog_uses_source_cards_for_findability(self) -> None:
        report = server.call_tool(self.engine, "get_external_source_catalog", {
            "stage": "refinement",
            "query": "animated marketing landing sections kinetic effects",
            "max_results": 6,
        })
        ids = [source["id"] for source in report["sources"]]
        self.assertTrue({"magic-ui", "aceternity-ui"} & set(ids))
        magic = next(source for source in report["sources"] if source["id"] == "magic-ui")
        self.assertIn("Animated React", magic["summary"])
        self.assertTrue(magic["best_for"])
        self.assertTrue(magic["keywords"])

    def test_external_catalog_treats_21st_mcp_as_optional_tooling(self) -> None:
        report = server.call_tool(self.engine, "get_external_source_catalog", {
            "stage": "implementation",
            "source_ids": ["21st-dev-mcp"],
            "tool_configured": False,
        })
        source = report["sources"][0]
        self.assertEqual(source["usage"]["decision"], "not-configured")
        self.assertFalse(report["policy"]["twenty_first_mcp_is_design_authority"])
        configured = server.call_tool(self.engine, "get_external_source_catalog", {
            "stage": "implementation",
            "source_ids": ["21st-dev-mcp"],
            "tool_configured": True,
        })
        self.assertNotEqual(configured["sources"][0]["usage"]["decision"], "not-configured")

    def test_external_catalog_excludes_build_week_and_never_promotes(self) -> None:
        report = server.call_tool(self.engine, "get_external_source_catalog", {
            "stage": "brief", "query": "component template inspiration", "max_results": 12,
        })
        self.assertFalse(report["policy"]["openai_build_week_catalog_allowed"])
        self.assertFalse(report["policy"]["automatic_promotion"])
        self.assertNotIn("build week", json.dumps(report).lower())

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
