#!/usr/bin/env python3
"""Run deterministic, artifact-backed copy-quality evaluations."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


EVAL_ROOT = Path(__file__).resolve().parent
COPY_ROOT = EVAL_ROOT / "copy"
sys.path.insert(0, str(COPY_ROOT))
from copy_quality import audit_copy, facts  # noqa: E402


def score(case: dict[str, object]) -> dict[str, object]:
    source = str(case["verified_facts"])
    headline = str(case["headline"])
    copy = str(case["copy"])
    ctas = [str(value) for value in case["ctas"]]
    combined = f"{headline}\n{copy}\n{' '.join(ctas)}"
    audit = audit_copy(combined, source_text=source, cta_labels=ctas)
    source_facts = set(facts(source))
    candidate_facts = set(facts(combined))
    fact_preservation = 5 if source_facts == candidate_facts else max(0, 5 - len(source_facts ^ candidate_facts))
    word_count = len(re.findall(r"\b\w+\b", combined))
    message_clarity = 5 if 4 <= len(headline.split()) <= 14 and word_count <= 90 else 4
    specificity = 5 if source_facts and not any(f["code"] == "generic-abstraction" for f in audit["findings"]) else 4
    voice = 5 if str(case["domain"]).replace("-", " ") not in headline.lower() else 4
    cta_quality = 5 if not any(f["code"] == "vague-cta" for f in audit["findings"]) else 2
    anti_slop = max(0, 5 - sum(f["code"] in {"generic-abstraction", "transition-overuse", "bureaucratic-padding", "repeated-sentence-opening"} for f in audit["findings"]))
    responsive_fit = 5 if len(headline) <= 80 and max((len(p.split()) for p in copy.split("\n") if p), default=0) <= 65 else 4
    result = "pass" if fact_preservation == 5 and min(message_clarity, specificity, voice, cta_quality, anti_slop, responsive_fit) >= 4 else "fail"
    return {
        "case": case["id"],
        "domain": case["domain"],
        "factual_fidelity": fact_preservation,
        "message_clarity": message_clarity,
        "specificity": specificity,
        "voice": voice,
        "cta_quality": cta_quality,
        "anti_slop": anti_slop,
        "responsive_fit": responsive_fit,
        "result": result,
        "observations": audit["findings"],
        "artifact_sha256": hashlib.sha256(json.dumps(case, sort_keys=True).encode()).hexdigest(),
    }


def main() -> int:
    cases_path = COPY_ROOT / "cases.json"
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    if len(cases) != 10:
        raise SystemExit("Copy evaluation requires exactly 10 representative cases")
    rows = [score(case) for case in cases]
    result = {
        "schema_version": 1,
        "method": "deterministic artifact-backed copy rubric; no model or detector score",
        "case_count": len(rows),
        "passed": all(row["result"] == "pass" for row in rows),
        "cases": rows,
    }
    out = EVAL_ROOT / "results" / "copy.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Copy evaluation", "", f"Result: {'PASS' if result['passed'] else 'FAIL'}", "", "| Case | Facts | Clarity | Specificity | Voice | CTA | Anti-slop | Responsive | Result |", "|---|---:|---:|---:|---:|---:|---:|---:|---|"]
    for row in rows:
        lines.append(f"| {row['case']} | {row['factual_fidelity']} | {row['message_clarity']} | {row['specificity']} | {row['voice']} | {row['cta_quality']} | {row['anti_slop']} | {row['responsive_fit']} | {row['result']} |")
    (EVAL_ROOT / "results" / "copy.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"passed": result["passed"], "case_count": len(rows), "output": str(out)}, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
