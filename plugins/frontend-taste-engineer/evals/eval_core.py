#!/usr/bin/env python3
"""Evidence-oriented retrieval and frontend-evaluation harness."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Mapping, Sequence


EVAL_ROOT = Path(__file__).resolve().parent
PLUGIN_ROOT = EVAL_ROOT.parent
SERVER_PATH = PLUGIN_ROOT / "mcp-server" / "server.py"
SKILL_PATH = PLUGIN_ROOT / "skills" / "frontend-taste-engineer" / "SKILL.md"
SKILL_AGENT_PATH = PLUGIN_ROOT / "skills" / "frontend-taste-engineer" / "agents" / "openai.yaml"
SOURCE_POLICY_CASES = EVAL_ROOT / "source-policy-cases.json"
SOURCE_DISCOVERY_SCRIPT = PLUGIN_ROOT / "scripts" / "discover_frontend_sources.py"


def _module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load module {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SERVER = _module(SERVER_PATH, "fte_server_evals")


def load_cases(path: Path) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list) or len(value) < 16:
        raise ValueError("Evaluation fixture must contain at least 16 cases")
    seen = set()
    for case in value:
        if not isinstance(case, dict) or not case.get("id") or case["id"] in seen:
            raise ValueError("Each evaluation case requires a unique ID")
        seen.add(case["id"])
        for field in ("brief", "expected_topics", "expected_terms", "mandatory_terms"):
            if not case.get(field):
                raise ValueError(f"{case['id']} lacks {field}")
        required_ids = case.get("required_record_ids", [])
        if required_ids and (not isinstance(required_ids, list) or not all(isinstance(value, str) and value for value in required_ids) or len(required_ids) != len(set(required_ids))):
            raise ValueError(f"{case['id']} has invalid required_record_ids")
        if "retrieval_only" in case and not isinstance(case["retrieval_only"], bool):
            raise ValueError(f"{case['id']} has invalid retrieval_only")
        if case.get("expected_mode") == SERVER.AUTONOMOUS_MODE:
            for field in ("expected_page_type", "expected_tone_terms", "expect_no_questions", "expect_production_completion"):
                if field not in case:
                    raise ValueError(f"{case['id']} lacks autonomous classification field {field}")
    return value


def tokens(value: Any) -> set[str]:
    return set(SERVER.tokenize(value))


def phrase_present(phrase: str, text: str) -> bool:
    normalized = " ".join(SERVER.tokenize(text))
    wanted = " ".join(SERVER.tokenize(phrase))
    return bool(wanted and (wanted in normalized or tokens(phrase) <= tokens(text)))


def percentile(values: Sequence[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    rank = max(0, min(len(ordered) - 1, math.ceil(p * len(ordered)) - 1))
    return ordered[rank]


def static_packets(query: str, budget: int) -> list[dict[str, Any]]:
    scored = []
    query_terms = tokens(query)
    for raw in SERVER.FALLBACK_RECORDS:
        record = SERVER.Record.from_dict(raw)
        overlap = len(query_terms & tokens(record.searchable))
        scored.append((overlap + (2 if record.importance == "mandatory" else 0), record))
    scored.sort(key=lambda item: (-item[0], item[1].id))
    return [record.packet(float(score), ["static-skill-kernel"]) for score, record in scored[: min(budget, 5)]]


def retrieve_variant(engine: Any, case: Mapping[str, Any], variant: str) -> dict[str, Any]:
    started = time.perf_counter_ns()
    autonomous = case.get("expected_mode") == SERVER.AUTONOMOUS_MODE
    budget = int(case.get("budget_records") or (11 if autonomous else 10))
    if variant == "baseline":
        packet = {"records": [], "summary": {"estimated_context_tokens": 0, "mandatory_returned": 0}}
    elif variant == "static-skill":
        result = static_packets(str(case["brief"]), budget)
        packet = {"records": result, "summary": {"estimated_context_tokens": SERVER.estimate_tokens(result), "mandatory_returned": sum(item.get("importance") == "mandatory" for item in result)}}
    else:
        filters = {
            "task_types": list(SERVER.TASK_TYPE_ALIASES.get(str(case.get("task_type")), (str(case.get("task_type")),))),
            "statuses": ["stable", "specialized", "experimental"],
        }
        if autonomous and variant == "hybrid":
            packet = SERVER.get_workflow(engine, {
                "task": str(case["brief"]),
                "stage": str(case.get("stage") or "brief"),
                "budget_records": budget,
                "context_budget": int(case.get("context_budget") or 4800),
                "strategy": "hybrid",
            })
        else:
            packet = engine.search(
                str(case["brief"]), filters,
                budget_records=budget,
                context_budget=int(case.get("context_budget") or 4200),
                strategy="lexical" if variant == "lexical" else "hybrid",
            )
    elapsed = (time.perf_counter_ns() - started) / 1_000_000.0
    packet["observed_latency_ms"] = round(elapsed, 3)
    return packet


PROFILE_FIELDS = {
    "build_mode", "domain", "product_type", "interface_archetype", "page_type",
    "purpose", "audience", "named_recipient_status", "primary_user_task",
    "secondary_tasks", "primary_message", "supporting_narrative", "emotional_objective",
    "emotional_tone", "seriousness", "trust_level", "risk_level",
    "information_density", "frequency_of_use", "content_maturity", "brand_maturity",
    "product_maturity", "accessibility_needs", "expected_devices", "visual_ambition",
    "visual_intensity", "motion_intensity", "experimental_tolerance",
    "familiarity_requirement", "interaction_depth", "suggested_composition",
    "hero_treatment", "negative_space_role", "typography_direction", "color_material_direction",
    "imagery_strategy", "motion_stance", "component_styling", "direction",
    "required_states", "retrieval_topics", "verification_priorities",
    "user_supplied_facts", "inferred_assumptions", "minimalism_guardrail", "quality_interpretation",
    "design_thesis",
}


def score_classification(case: Mapping[str, Any]) -> dict[str, Any] | None:
    expected_mode = case.get("expected_mode")
    if not expected_mode:
        return None
    result = SERVER.classify_task(str(case["brief"]), {"stage": case.get("stage")})
    profile = result.get("creative_profile") or {}
    ledger = result.get("decision_ledger") or {}
    entities = result.get("entities") or {}
    guardrails = set(result.get("copy_guardrails") or [])
    tone = set(profile.get("emotional_tone") or [])
    retrieval = result.get("recommended_retrieval") or {}
    expected_deferred = {"framework", "component", "motion", "performance", "browser"}
    if "motion" in set(retrieval.get("topics") or []):
        expected_deferred.remove("motion")
    checks = {
        "mode": result.get("task_type") == expected_mode,
        "minimal_prompt": bool(result.get("minimal_prompt")),
        "profile_complete": PROFILE_FIELDS <= set(profile) and all(profile.get(field) not in (None, "", []) for field in PROFILE_FIELDS),
        "page_type": profile.get("page_type") == case.get("expected_page_type"),
        "domain": not case.get("expected_domain") or profile.get("domain") == case.get("expected_domain"),
        "tone": set(case.get("expected_tone_terms") or []) <= tone,
        "visual_intensity": case.get("expected_visual_intensity") is None or profile.get("visual_intensity") == case.get("expected_visual_intensity"),
        "motion_intensity": not case.get("expected_motion_intensity") or profile.get("motion_intensity") == case.get("expected_motion_intensity"),
        "trust_level": not case.get("expected_trust_level") or profile.get("trust_level") == case.get("expected_trust_level"),
        "risk_level": not case.get("expected_risk_level") or profile.get("risk_level") == case.get("expected_risk_level"),
        "information_density": not case.get("expected_information_density") or profile.get("information_density") == case.get("expected_information_density"),
        "facts_and_assumptions": bool(ledger.get("supplied_facts")) and bool(ledger.get("inferred_assumptions")),
        "recipient": not case.get("expected_recipient") or case.get("expected_recipient") in (entities.get("named_recipients") or []),
        "quoted_text": not case.get("expected_quoted_text") or case.get("expected_quoted_text") in (entities.get("quoted_text") or []),
        "no_unnecessary_questions": not case.get("expect_no_questions") or bool((result.get("clarification_policy") or {}).get("continue_without_questions")),
        "no_invented_claims": {"no-fake-testimonials", "no-fake-metrics", "no-unsupported-claims"} <= guardrails,
        "staged_retrieval": bool(retrieval.get("record_ids")) and set(retrieval.get("defer_until_needed") or []) == expected_deferred,
        "production_completion": not case.get("expect_production_completion") or result.get("completion_workflow") == "production-completion-with-screenshot-refinement",
        "request_local_privacy": (result.get("privacy") or {}).get("user_supplied_names") == "request-local" and not (result.get("privacy") or {}).get("persist_to_plugin_knowledge", True),
    }
    return {
        "passed": all(checks.values()),
        "case_id": case.get("id"),
        "direction_diversity_case": bool(case.get("direction_diversity_case")),
        "checks": checks,
        "mode": result.get("task_type"),
        "page_type": profile.get("page_type"),
        "tone": profile.get("emotional_tone"),
        "entities": entities,
        "design_thesis": profile.get("design_thesis"),
        "direction_profile": {
            "domain": profile.get("domain"),
            "page_type": profile.get("page_type"),
            "visual_intensity": profile.get("visual_intensity"),
            "motion_intensity": profile.get("motion_intensity"),
            "tone": profile.get("emotional_tone"),
            "composition": profile.get("suggested_composition"),
            "hero": profile.get("hero_treatment"),
            "typography": profile.get("typography_direction"),
            "palette_material": profile.get("color_material_direction"),
            "components": profile.get("component_styling"),
            "direction": profile.get("direction"),
        },
    }


def skill_activation_evidence() -> dict[str, Any]:
    skill = SKILL_PATH.read_text(encoding="utf-8").lower()
    agent = SKILL_AGENT_PATH.read_text(encoding="utf-8").lower()
    triggers = (
        "make a website", "build a site", "build a landing page", "create a frontend",
        "turn this idea into a website", "make this page stunning", "redesign this frontend",
        "make this production-ready", "build a page addressed to someone", "create a visual web experience",
    )
    found = {trigger: trigger in skill for trigger in triggers}
    return {
        "passed": all(found.values()) and "allow_implicit_invocation: true" in agent,
        "trigger_phrases": found,
        "implicit_invocation": "allow_implicit_invocation: true" in agent,
        "skill": str(SKILL_PATH),
        "agent_metadata": str(SKILL_AGENT_PATH),
    }


def direction_diversity_evidence(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    selected = [row for row in rows if row.get("direction_diversity_case")]
    profiles = [row["direction_profile"] for row in selected]
    style_fields = ("palette_material", "typography", "composition", "hero", "components", "tone")
    unique_counts = {
        field: len({json.dumps(profile.get(field), sort_keys=True, ensure_ascii=False) for profile in profiles})
        for field in (*style_fields, "motion_intensity", "visual_intensity", "page_type", "direction")
    }
    unique_rates = {field: round(count / max(1, len(profiles)), 3) for field, count in unique_counts.items()}
    signatures = {
        json.dumps({field: profile.get(field) for field in (*style_fields, "motion_intensity", "visual_intensity", "page_type")}, sort_keys=True, ensure_ascii=False)
        for profile in profiles
    }
    similar_pairs = []
    for left_index, left in enumerate(selected):
        left_tokens = tokens(left["direction_profile"])
        for right in selected[left_index + 1:]:
            right_tokens = tokens(right["direction_profile"])
            union = left_tokens | right_tokens
            similarity = len(left_tokens & right_tokens) / len(union) if union else 1.0
            if similarity >= 0.78:
                similar_pairs.append({"left": left["case_id"], "right": right["case_id"], "similarity": round(similarity, 3)})
    intensity_levels = sorted({profile.get("visual_intensity") for profile in profiles if isinstance(profile.get("visual_intensity"), int)})
    motion_levels = sorted({str(profile.get("motion_intensity")) for profile in profiles})
    gates = {
        "case_coverage": len(selected) >= 10,
        "full_signature_uniqueness": len(signatures) / max(1, len(selected)) >= 0.9,
        "style_dimension_diversity": all(unique_rates[field] >= 0.65 for field in style_fields),
        "visual_intensity_range": set(intensity_levels) == {1, 2, 3, 4, 5},
        "motion_range": len(motion_levels) >= 4,
        "no_overly_similar_cross-domain_pairs": not similar_pairs,
    }
    return {
        "passed": all(gates.values()),
        "cases": len(selected),
        "gates": gates,
        "unique_counts": unique_counts,
        "unique_rates": unique_rates,
        "visual_intensity_levels": intensity_levels,
        "motion_levels": motion_levels,
        "overly_similar_pairs": similar_pairs,
        "profiles": [{"case_id": row["case_id"], **row["direction_profile"]} for row in selected],
    }


def score_retrieval(case: Mapping[str, Any], packet: Mapping[str, Any]) -> dict[str, Any]:
    records = list(packet.get("records") or [])
    expected_topics = set(case["expected_topics"])
    expected_terms = list(case["expected_terms"])
    mandatory_terms = list(case["mandatory_terms"])
    required_record_ids = list(case.get("required_record_ids") or [])
    relevant = []
    irrelevant_tokens = 0
    total_tokens = 0
    for record in records:
        text = json.dumps(record, ensure_ascii=False)
        is_relevant = record.get("topic") in expected_topics or any(phrase_present(term, text) for term in expected_terms)
        relevant.append(is_relevant)
        cost = SERVER.estimate_tokens(record)
        total_tokens += cost
        if not is_relevant:
            irrelevant_tokens += cost
    topics_found = {record.get("topic") for record in records}
    retrieved_ids = {str(record.get("id")) for record in records}
    missing_required_record_ids = [record_id for record_id in required_record_ids if record_id not in retrieved_ids]
    packet_text = json.dumps(records, ensure_ascii=False)
    recall_units = [topic in topics_found for topic in expected_topics] + [phrase_present(term, packet_text) for term in expected_terms]
    mandatory_units = [phrase_present(term, packet_text) for term in mandatory_terms]
    fingerprints = [hashlib.sha256(" ".join(SERVER.tokenize(record.get("principle", ""))).encode()).hexdigest() for record in records]
    duplicate_count = len(fingerprints) - len(set(fingerprints))
    provenance_valid = [bool(record.get("sources")) and bool(record.get("license_status")) for record in records]
    statuses = [record.get("status") for record in records]
    first_experimental = next((idx for idx, status in enumerate(statuses) if status in {"experimental", "inspiration-only"}), len(statuses))
    stable_after_experimental = any(status in {"stable", "active"} for status in statuses[first_experimental + 1:])
    precision = sum(relevant) / len(records) if records else 0.0
    recall = sum(recall_units) / len(recall_units) if recall_units else 1.0
    mandatory_recall = sum(mandatory_units) / len(mandatory_units) if mandatory_units else 1.0
    duplicate_rate = duplicate_count / len(records) if records else 0.0
    irrelevant_rate = irrelevant_tokens / total_tokens if total_tokens else 0.0
    provenance = sum(provenance_valid) / len(provenance_valid) if provenance_valid else 0.0
    quality = (
        0.24 * precision + 0.22 * recall + 0.28 * mandatory_recall
        + 0.12 * provenance + 0.07 * (1 - duplicate_rate)
        + 0.07 * (1 - irrelevant_rate)
    ) if records else 0.0
    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "mandatory_rule_recall": round(mandatory_recall, 3),
        "duplicate_rate": round(duplicate_rate, 3),
        "irrelevant_token_rate": round(irrelevant_rate, 3),
        "provenance_correctness": round(provenance, 3),
        "context_tokens": int(packet.get("summary", {}).get("estimated_context_tokens", total_tokens)),
        "latency_ms": float(packet.get("observed_latency_ms", 0.0)),
        "stable_experimental_separation": 0.0 if stable_after_experimental else 1.0,
        "quality_score": round(quality, 3),
        "missing_required_record_ids": missing_required_record_ids,
        "evidence": {
            "retrieved_ids": [record.get("id") for record in records],
            "required_record_ids": required_record_ids,
            "required_record_ids_found": [record_id for record_id in required_record_ids if record_id in retrieved_ids],
            "topics_found": sorted(topic for topic in topics_found if topic),
            "expected_terms_found": [term for term in expected_terms if phrase_present(term, packet_text)],
            "mandatory_terms_found": [term for term in mandatory_terms if phrase_present(term, packet_text)],
            "relevance_by_id": {str(record.get("id")): flag for record, flag in zip(records, relevant)},
        },
    }


def aggregate(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    metric_names = (
        "precision", "recall", "mandatory_rule_recall", "duplicate_rate",
        "irrelevant_token_rate", "provenance_correctness", "context_tokens",
        "stable_experimental_separation", "quality_score",
    )
    result = {name: round(statistics.fmean(float(row[name]) for row in rows), 3) for name in metric_names}
    latencies = [float(row["latency_ms"]) for row in rows]
    result.update({
        "latency_median_ms": round(statistics.median(latencies), 3),
        "latency_p95_ms": round(percentile(latencies, 0.95), 3),
        "cases": len(rows),
    })
    return result


def _path_value(value: Any, path: str) -> Any:
    current = value
    for part in path.split(".") if path else []:
        if not isinstance(current, Mapping) or part not in current:
            return None
        current = current[part]
    return current


def source_policy_evidence(path: Path) -> dict[str, Any]:
    fixtures = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for fixture in fixtures:
        kind = fixture.get("kind")
        arguments = dict(fixture.get("arguments") or {})
        execution_error = ""
        if kind == "mcp":
            result = SERVER.external_source_catalog(arguments)
        elif kind == "discovery-dry-run":
            with tempfile.TemporaryDirectory() as temp:
                command = [
                    sys.executable, str(SOURCE_DISCOVERY_SCRIPT), "--dry-run",
                    "--max-results", str(arguments.get("max_results") or 8),
                    "--as-of", str(arguments.get("as_of") or "2026-07-10"),
                    "--out-dir", str(Path(temp) / "candidates"),
                ]
                process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
                execution_error = process.stderr.strip() if process.returncode else ""
                result = json.loads(process.stdout) if process.returncode == 0 else {"returncode": process.returncode}
        else:
            result = {"error": f"unknown fixture kind: {kind}"}
            execution_error = str(result["error"])
        check_rows = []
        for check in fixture.get("checks") or []:
            check_type = check.get("type")
            expected = check.get("equals")
            actual: Any = None
            passed = False
            if check_type == "top-field":
                actual = _path_value(result, str(check.get("path") or ""))
                passed = actual == expected
            elif check_type == "source-field":
                source = next((item for item in result.get("sources", []) if item.get("id") == check.get("source_id")), None)
                actual = _path_value(source, str(check.get("path") or "")) if source else None
                passed = actual == expected
            elif check_type == "all-source-field":
                actual = [_path_value(item, str(check.get("path") or "")) for item in result.get("sources", [])]
                passed = bool(actual) and all(value == expected for value in actual)
            elif check_type == "source-prefix":
                actual = [item.get("id") for item in result.get("sources", [])[:len(expected or [])]]
                passed = actual == expected
            elif check_type == "budget-bounded":
                actual = {"returned": result.get("returned"), "stage_budget": result.get("stage_budget")}
                passed = isinstance(actual["returned"], int) and isinstance(actual["stage_budget"], int) and actual["returned"] <= actual["stage_budget"]
            elif check_type == "catalog-not-fully-loaded":
                actual = {"returned": result.get("returned"), "catalog_size": (result.get("catalog") or {}).get("catalog_size")}
                passed = isinstance(actual["returned"], int) and isinstance(actual["catalog_size"], int) and actual["returned"] < actual["catalog_size"]
            elif check_type == "json-excludes":
                needle = str(check.get("value") or "").lower()
                actual = needle
                passed = needle not in json.dumps(result, ensure_ascii=False).lower()
            check_rows.append({"type": check_type, "passed": passed, "expected": expected, "actual": actual})
        rows.append({
            "id": fixture.get("id"), "name": fixture.get("name"),
            "passed": not execution_error and bool(check_rows) and all(row["passed"] for row in check_rows),
            "execution_error": execution_error or None, "checks": check_rows,
        })
    return {
        "passed": bool(rows) and all(row["passed"] for row in rows),
        "cases": len(rows),
        "passed_cases": sum(row["passed"] for row in rows),
        "fixtures": str(path),
        "results": rows,
    }


def retrieval_eval(args: argparse.Namespace) -> dict[str, Any]:
    cases = load_cases(Path(args.cases))
    engine = SERVER.RetrievalEngine(Path(args.knowledge_dir))
    variants = ["baseline", "static-skill", "lexical", "hybrid"]
    case_rows = []
    classification_rows = []
    grouped: dict[str, list[dict[str, Any]]] = {variant: [] for variant in variants}
    for case in cases:
        variant_rows = {}
        for variant in variants:
            packet = retrieve_variant(engine, case, variant)
            score = score_retrieval(case, packet)
            grouped[variant].append(score)
            variant_rows[variant] = score
        classification = score_classification(case)
        if classification is not None:
            classification_rows.append(classification)
        case_rows.append({"id": case["id"], "name": case["name"], "variants": variant_rows, "classification": classification})
    aggregates = {variant: aggregate(rows) for variant, rows in grouped.items()}
    hybrid = aggregates["hybrid"]
    lexical = aggregates["lexical"]
    activation = skill_activation_evidence()
    direction_diversity = direction_diversity_evidence(classification_rows)
    source_policy = source_policy_evidence(Path(args.source_policy_cases))
    classification_checks = sorted({name for row in classification_rows for name in row["checks"]})
    classification_summary = {
        "cases": len(classification_rows),
        "passed_cases": sum(row["passed"] for row in classification_rows),
        "pass_rate": round(sum(row["passed"] for row in classification_rows) / max(1, len(classification_rows)), 3),
        "check_rates": {
            name: round(sum(bool(row["checks"].get(name)) for row in classification_rows) / max(1, len(classification_rows)), 3)
            for name in classification_checks
        },
    }
    gates = {
        "mandatory_rule_recall": hybrid["mandatory_rule_recall"] >= float(args.min_mandatory_recall),
        "duplicate_rate": hybrid["duplicate_rate"] <= float(args.max_duplicate_rate),
        "irrelevant_token_rate": hybrid["irrelevant_token_rate"] <= float(args.max_irrelevant_token_rate),
        "context_budget": all(row["context_tokens"] <= int(case.get("context_budget") or 4200) for row, case in zip(grouped["hybrid"], cases)),
        "provenance_correctness": hybrid["provenance_correctness"] >= float(args.min_provenance),
        "hybrid_not_below_lexical": hybrid["quality_score"] + 0.001 >= lexical["quality_score"],
        "latency": hybrid["latency_p95_ms"] <= float(args.max_p95_latency_ms),
        "minimal_prompt_skill_activation": activation["passed"],
        "minimal_prompt_classification": bool(classification_rows) and classification_summary["pass_rate"] == 1.0,
        "context_adaptive_direction_diversity": direction_diversity["passed"],
        "external_source_policy": source_policy["passed"],
        "required_record_ids": all(not row["missing_required_record_ids"] for row in grouped["hybrid"]),
    }
    return {
        "schema_version": 1,
        "evaluation": "retrieval",
        "passed": all(gates.values()),
        "summary": {"errors": sum(not value for value in gates.values()), "warnings": 0},
        "cases": case_rows,
        "aggregates": aggregates,
        "classification": classification_summary,
        "direction_diversity": direction_diversity,
        "skill_activation": activation,
        "source_policy": source_policy,
        "gates": gates,
        "thresholds": {
            "min_mandatory_recall": args.min_mandatory_recall,
            "max_duplicate_rate": args.max_duplicate_rate,
            "max_irrelevant_token_rate": args.max_irrelevant_token_rate,
            "min_provenance": args.min_provenance,
            "max_p95_latency_ms": args.max_p95_latency_ms,
        },
        "corpus": engine.info,
        "methodology": {
            "baseline": "No plugin guidance.",
            "static-skill": "Small offline mandatory kernel, capped at five records.",
            "lexical": "Canonical corpus with metadata and exact/keyword scoring; synonym expansion disabled.",
            "hybrid": "Canonical corpus with creative-profile classification, stage-specific autonomous routing, metadata, exact/lexical scoring, deterministic synonym expansion, reranking, dedupe, mandatory preservation, and budgets.",
            "latency_note": "Latency is observed wall time and therefore informational, while relevance scoring and selection are deterministic for a fixed corpus.",
        },
    }


RUBRIC = (
    "product_fit", "visual_hierarchy", "typography", "composition",
    "information_architecture", "interaction_quality", "state_completeness",
    "accessibility", "responsive_behavior", "performance", "content_quality",
    "originality", "maintainability", "reference_fidelity",
    "anti_generic_patterns", "functional_integrity",
)


def _valid_evidence(item: Any) -> bool:
    return isinstance(item, Mapping) and bool(item.get("observation")) and bool(item.get("artifact") or item.get("command")) and item.get("status") in {"pass", "fail", "partial"}


def frontend_eval(args: argparse.Namespace) -> dict[str, Any]:
    cases = [case for case in load_cases(Path(args.cases)) if not case.get("retrieval_only")]
    evidence_root = Path(args.evidence_dir)
    rows = []
    scored = 0
    for case in cases:
        path = evidence_root / f"{case['id']}.json"
        if not path.exists():
            rows.append({"id": case["id"], "name": case["name"], "status": "not-run", "reason": "No evidence manifest. Run the frontend task and record artifacts/commands before scoring.", "rubric": {criterion: None for criterion in RUBRIC}})
            continue
        value = json.loads(path.read_text(encoding="utf-8"))
        rubric = {}
        valid = True
        for criterion in RUBRIC:
            entry = value.get("rubric", {}).get(criterion)
            evidence = entry.get("evidence", []) if isinstance(entry, Mapping) else []
            score = entry.get("score") if isinstance(entry, Mapping) else None
            if not isinstance(score, (int, float)) or not 0 <= score <= 5 or not evidence or not all(_valid_evidence(item) for item in evidence):
                rubric[criterion] = {"score": None, "valid": False, "reason": "Requires a 0–5 score and artifact/command-backed observations."}
                valid = False
            else:
                rubric[criterion] = {"score": float(score), "valid": True, "evidence": evidence}
        overall = round(statistics.fmean(item["score"] for item in rubric.values() if item["score"] is not None), 3) if any(item["score"] is not None for item in rubric.values()) else None
        rows.append({"id": case["id"], "name": case["name"], "status": "scored" if valid else "invalid-evidence", "overall": overall, "rubric": rubric, "manifest": str(path)})
        if valid:
            scored += 1
    complete = scored == len(cases)
    return {
        "schema_version": 1,
        "evaluation": "frontend-output",
        "passed": complete,
        "summary": {"errors": 0 if complete else len(cases) - scored, "warnings": 0},
        "case_count": len(cases),
        "scored_cases": scored,
        "unscored_cases": len(cases) - scored,
        "cases": rows,
        "rubric": list(RUBRIC),
        "integrity_rule": "No score is accepted without a concrete artifact or executed-command observation. Missing evidence remains unscored, never inferred.",
        "next_step": "Place one evidence manifest per case under evals/evidence/ after executing real frontend outputs.",
    }


def markdown(value: Mapping[str, Any]) -> str:
    title = "Retrieval evaluation" if value.get("evaluation") == "retrieval" else "Frontend output evaluation"
    lines = [f"# {title}", "", f"**Result:** {'PASS' if value.get('passed') else 'INCOMPLETE/FAIL'}", ""]
    if value.get("aggregates"):
        lines.extend(["| Variant | Quality | Precision | Recall | Mandatory recall | Duplicates | Irrelevant tokens | Provenance | Context tokens | p95 ms |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"])
        for variant, row in value["aggregates"].items():
            lines.append(f"| {variant} | {row['quality_score']:.3f} | {row['precision']:.3f} | {row['recall']:.3f} | {row['mandatory_rule_recall']:.3f} | {row['duplicate_rate']:.3f} | {row['irrelevant_token_rate']:.3f} | {row['provenance_correctness']:.3f} | {row['context_tokens']:.0f} | {row['latency_p95_ms']:.3f} |")
        lines.extend(["", "## Gates", ""])
        lines.extend(f"- {'PASS' if passed else 'FAIL'} — {name}" for name, passed in value["gates"].items())
        classification = value.get("classification") or {}
        lines.extend([
            "", "## Minimal-prompt classification", "",
            f"Passed cases: {classification.get('passed_cases', 0)} / {classification.get('cases', 0)}",
            f"Skill activation: {'PASS' if (value.get('skill_activation') or {}).get('passed') else 'FAIL'}",
        ])
        diversity = value.get("direction_diversity") or {}
        lines.extend([
            "", "## Context-adaptive direction", "",
            f"Direction cases: {diversity.get('cases', 0)}",
            f"Diversity gate: {'PASS' if diversity.get('passed') else 'FAIL'}",
            f"Visual intensity levels: {', '.join(str(item) for item in diversity.get('visual_intensity_levels', []))}",
            f"Overly similar pairs: {len(diversity.get('overly_similar_pairs', []))}",
        ])
        source_policy = value.get("source_policy") or {}
        lines.extend([
            "", "## External source policy", "",
            f"Passed cases: {source_policy.get('passed_cases', 0)} / {source_policy.get('cases', 0)}",
        ])
    else:
        lines.extend([f"Scored cases: {value.get('scored_cases', 0)} / {value.get('case_count', 0)}", "", value.get("integrity_rule", "")])
    lines.extend(["", "## Case status", ""])
    for case in value.get("cases", []):
        if "variants" in case:
            score = case["variants"]["hybrid"]["quality_score"]
            classification = case.get("classification")
            suffix = f"; classification {'PASS' if classification.get('passed') else 'FAIL'} ({classification.get('mode')})" if classification else ""
            lines.append(f"- `{case['id']}` — hybrid quality {score:.3f}{suffix}")
        else:
            lines.append(f"- `{case['id']}` — {case['status']}")
    lines.append("")
    return "\n".join(lines)


def write_outputs(value: Mapping[str, Any], json_out: Path, md_out: Path) -> int:
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    md_out.write_text(markdown(value), encoding="utf-8")
    print(json.dumps({"passed": value.get("passed"), "json": str(json_out.resolve()), "markdown": str(md_out.resolve())}, indent=2, sort_keys=True))
    return 0 if value.get("passed") else 1


def retrieval_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run baseline/static/lexical/hybrid retrieval comparisons.")
    parser.add_argument("--cases", type=Path, default=EVAL_ROOT / "cases.json")
    parser.add_argument("--knowledge-dir", type=Path, default=PLUGIN_ROOT / "knowledge")
    parser.add_argument("--source-policy-cases", type=Path, default=SOURCE_POLICY_CASES)
    parser.add_argument("--json-out", "--output", type=Path, default=EVAL_ROOT / "results" / "retrieval.json")
    parser.add_argument("--md-out", type=Path, default=EVAL_ROOT / "results" / "retrieval.md")
    parser.add_argument("--min-mandatory-recall", type=float, default=0.45)
    parser.add_argument("--max-duplicate-rate", type=float, default=0.10)
    parser.add_argument("--max-irrelevant-token-rate", type=float, default=0.38)
    parser.add_argument("--min-provenance", type=float, default=0.95)
    parser.add_argument("--max-p95-latency-ms", type=float, default=100.0)
    return parser


def frontend_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score real frontend outputs only when evidence manifests exist.")
    parser.add_argument("--cases", type=Path, default=EVAL_ROOT / "cases.json")
    parser.add_argument("--evidence-dir", type=Path, default=EVAL_ROOT / "evidence")
    parser.add_argument("--json-out", "--output", type=Path, default=EVAL_ROOT / "results" / "frontend.json")
    parser.add_argument("--md-out", type=Path, default=EVAL_ROOT / "results" / "frontend.md")
    return parser


def retrieval_main(argv: Sequence[str] | None = None) -> int:
    args = retrieval_parser().parse_args(argv)
    return write_outputs(retrieval_eval(args), args.json_out, args.md_out)


def frontend_main(argv: Sequence[str] | None = None) -> int:
    args = frontend_parser().parse_args(argv)
    return write_outputs(frontend_eval(args), args.json_out, args.md_out)
