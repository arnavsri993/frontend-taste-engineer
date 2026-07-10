#!/usr/bin/env python3
"""Evidence-oriented retrieval and frontend-evaluation harness."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Mapping, Sequence


EVAL_ROOT = Path(__file__).resolve().parent
PLUGIN_ROOT = EVAL_ROOT.parent
SERVER_PATH = PLUGIN_ROOT / "mcp-server" / "server.py"


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
    budget = 10
    if variant == "baseline":
        packet = {"records": [], "summary": {"estimated_context_tokens": 0, "mandatory_returned": 0}}
    elif variant == "static-skill":
        result = static_packets(str(case["brief"]), budget)
        packet = {"records": result, "summary": {"estimated_context_tokens": SERVER.estimate_tokens(result), "mandatory_returned": sum(item.get("importance") == "mandatory" for item in result)}}
    else:
        filters = {
            "task_types": [case.get("task_type")],
            "statuses": ["stable", "active", "experimental"],
        }
        packet = engine.search(
            str(case["brief"]), filters,
            budget_records=budget,
            context_budget=int(case.get("context_budget") or 4200),
            strategy="lexical" if variant == "lexical" else "hybrid",
        )
    elapsed = (time.perf_counter_ns() - started) / 1_000_000.0
    packet["observed_latency_ms"] = round(elapsed, 3)
    return packet


def score_retrieval(case: Mapping[str, Any], packet: Mapping[str, Any]) -> dict[str, Any]:
    records = list(packet.get("records") or [])
    expected_topics = set(case["expected_topics"])
    expected_terms = list(case["expected_terms"])
    mandatory_terms = list(case["mandatory_terms"])
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
        "evidence": {
            "retrieved_ids": [record.get("id") for record in records],
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


def retrieval_eval(args: argparse.Namespace) -> dict[str, Any]:
    cases = load_cases(Path(args.cases))
    engine = SERVER.RetrievalEngine(Path(args.knowledge_dir))
    variants = ["baseline", "static-skill", "lexical", "hybrid"]
    case_rows = []
    grouped: dict[str, list[dict[str, Any]]] = {variant: [] for variant in variants}
    for case in cases:
        variant_rows = {}
        for variant in variants:
            packet = retrieve_variant(engine, case, variant)
            score = score_retrieval(case, packet)
            grouped[variant].append(score)
            variant_rows[variant] = score
        case_rows.append({"id": case["id"], "name": case["name"], "variants": variant_rows})
    aggregates = {variant: aggregate(rows) for variant, rows in grouped.items()}
    hybrid = aggregates["hybrid"]
    lexical = aggregates["lexical"]
    gates = {
        "mandatory_rule_recall": hybrid["mandatory_rule_recall"] >= float(args.min_mandatory_recall),
        "duplicate_rate": hybrid["duplicate_rate"] <= float(args.max_duplicate_rate),
        "context_budget": all(row["context_tokens"] <= int(case.get("context_budget") or 4200) for row, case in zip(grouped["hybrid"], cases)),
        "provenance_correctness": hybrid["provenance_correctness"] >= float(args.min_provenance),
        "hybrid_not_below_lexical": hybrid["quality_score"] + 0.001 >= lexical["quality_score"],
        "latency": hybrid["latency_p95_ms"] <= float(args.max_p95_latency_ms),
    }
    return {
        "schema_version": 1,
        "evaluation": "retrieval",
        "passed": all(gates.values()),
        "summary": {"errors": sum(not value for value in gates.values()), "warnings": 0},
        "cases": case_rows,
        "aggregates": aggregates,
        "gates": gates,
        "thresholds": {
            "min_mandatory_recall": args.min_mandatory_recall,
            "max_duplicate_rate": args.max_duplicate_rate,
            "min_provenance": args.min_provenance,
            "max_p95_latency_ms": args.max_p95_latency_ms,
        },
        "corpus": engine.info,
        "methodology": {
            "baseline": "No plugin guidance.",
            "static-skill": "Small offline mandatory kernel, capped at five records.",
            "lexical": "Canonical corpus with metadata and exact/keyword scoring; synonym expansion disabled.",
            "hybrid": "Canonical corpus with classification, metadata, exact/lexical scoring, deterministic synonym expansion, reranking, dedupe, mandatory preservation, and budgets.",
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
    cases = load_cases(Path(args.cases))
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
    else:
        lines.extend([f"Scored cases: {value.get('scored_cases', 0)} / {value.get('case_count', 0)}", "", value.get("integrity_rule", "")])
    lines.extend(["", "## Case status", ""])
    for case in value.get("cases", []):
        if "variants" in case:
            score = case["variants"]["hybrid"]["quality_score"]
            lines.append(f"- `{case['id']}` — hybrid quality {score:.3f}")
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
    parser.add_argument("--json-out", "--output", type=Path, default=EVAL_ROOT / "results" / "retrieval.json")
    parser.add_argument("--md-out", type=Path, default=EVAL_ROOT / "results" / "retrieval.md")
    parser.add_argument("--min-mandatory-recall", type=float, default=0.45)
    parser.add_argument("--max-duplicate-rate", type=float, default=0.10)
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
