#!/usr/bin/env python3
"""Parse and contrastively annotate the preserved Grubby evaluation pairs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from copy_quality import audit_copy, facts


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT / "grubby-ai-humanized-pairs.txt"
DEFAULT_OUTPUT = ROOT / "grubby-pair-annotations.json"
PAIR_RE = re.compile(
    r"PAIR\s+(?P<number>\d+)\s+OF\s+\d+\nID:\s*(?P<id>[^\n]+)\nTITLE:\s*(?P<title>[^\n]+)\n\nAI TEXT\n-+\n(?P<ai>.*?)\n\nHUMANIZED TEXT\n-+\n(?P<humanized>.*?)(?=\n={20,}\n(?:PAIR\s+\d+\s+OF|\Z))",
    re.S,
)

CURATED_NOTES = {
    "academic-urban-shade-equity": "The rewrite implies 240 sensors in each tract rather than 240 across the study and weakens the private-garden and route-dependence distinctions.",
    "academic-remote-work-learning": "The rewrite omits the event-definition method and several access mechanisms, then compresses causal limitations.",
    "academic-retrieval-practice": "The rewrite drops design detail and shifts cautious classroom associations toward broader effectiveness claims.",
    "academic-right-to-repair": "The rewrite removes policy distinctions and implementation qualifications that make the market-access argument precise.",
    "academic-community-flood-mapping": "The rewrite repeats conclusions, introduces awkward causality, and blurs when citizen reports are appropriate evidence.",
    "academic-libraries-social-infrastructure": "The rewrite inherits a source sentence defect, omits several observed staff tasks, and changes the proposed measures.",
    "academic-sleep-regularity": "The rewrite turns a cautious association into a proven impact and drops structural and clinical qualifications.",
    "academic-circular-procurement": "The rewrite reduces lifecycle and procurement detail and makes the evidence less operationally useful.",
    "academic-archives-public-memory": "The rewrite flattens the distinction between community authority, archival selection, and public-memory claims.",
    "academic-algorithmic-decision-support": "The rewrite removes accountability boundaries and weakens the difference between decision support and automated authority.",
    "academic-edge-computing-public-services": "The rewrite loses technical and public-service constraints while increasing generalized certainty.",
    "academic-soil-microbial-restoration": "The rewrite says sequencing detected active populations, reversing the source warning that dormant organisms may also be detected.",
    "academic-language-access-administration": "The rewrite changes the program framing, applicant goal, and administrative-burden emphasis.",
    "professional-four-day-pilot-memo": "The rewrite changes schedule mechanics, department descriptions, outage impact, and the promised recommendation date from October 9 to August 24.",
    "professional-release-incident-review": "The rewrite compresses detection and review roles, changes operational detail, and obscures why independent capacity review failed.",
    "journalistic-night-bakery": "The rewrite introduces impossible sunrise timing, changes delivery timing and dough handling, and removes observed scene detail and voice.",
    "marketing-fieldnote-launch": "The rewrite changes the fictional agency example, drops downstream task detail, and turns a measured trial invitation into a stronger outcome implication.",
    "reflective-moving-cities": "The rewrite invents April 15 and new friends, changes street and delivery details, and repeats the emotional conclusion.",
    "email-community-garden": "The rewrite reallocates who brings food, changes the library reservation from pending to confirmed, and removes access and child-safety detail.",
    "social-casual-dinner-hosting": "The rewrite changes who found the mango and where, flattens jokes, and adds awkward or contradictory sentences.",
    "fiction-bellweather-borrowed-time": "The rewrite introduces grammar errors, removes causal and atmospheric detail, and weakens the final image while preserving the basic plot.",
}

GRAMMAR_PATTERNS = {
    "included of": re.compile(r"\bincluded of\b", re.I),
    "it was always been": re.compile(r"\bit was always been\b", re.I),
    "slid the lock open the door": re.compile(r"\bslid the lock open the door\b", re.I),
    "as-clause fragment": re.compile(r"(?:^|[.!?]\s+)As the [^.?!]+[.!?]", re.I),
    "double-spaced punctuation": re.compile(r"[.!?]\s{2,}"),
}


def parse(text: str) -> list[dict[str, object]]:
    rows = []
    for match in PAIR_RE.finditer(text.strip() + "\n====================\n"):
        rows.append({
            "pair_number": int(match.group("number")),
            "pair_id": match.group("id").strip(),
            "title": match.group("title").strip(),
            "ai_text": match.group("ai").strip(),
            "humanized_text": match.group("humanized").strip(),
        })
    return rows


def annotate(row: dict[str, object]) -> dict[str, object]:
    ai = str(row["ai_text"])
    humanized = str(row["humanized_text"])
    ai_facts = set(facts(ai))
    humanized_facts = set(facts(humanized))
    grammar = [name for name, pattern in GRAMMAR_PATTERNS.items() if pattern.search(humanized)]
    ai_audit = audit_copy(ai)
    human_audit = audit_copy(humanized, source_text=ai)
    return {
        "pair_number": row["pair_number"],
        "pair_id": row["pair_id"],
        "title": row["title"],
        "annotation": "ai-stronger",
        "factual_differences": {
            "omitted_anchors": sorted(ai_facts - humanized_facts),
            "introduced_anchors": sorted(humanized_facts - ai_facts),
            "curated_observation": CURATED_NOTES[str(row["pair_id"])],
        },
        "grammatical_errors": grammar,
        "omitted_details": sorted(ai_facts - humanized_facts),
        "introduced_details": sorted(humanized_facts - ai_facts),
        "style_strengths": {
            "ai": ["specific structure", "controlled qualification", "stronger sentence rhythm"],
            "humanized": ["occasionally shorter local phrasing"],
        },
        "style_weaknesses": {
            "ai": [finding["code"] for finding in ai_audit["findings"]],
            "humanized": sorted(set([finding["code"] for finding in human_audit["findings"]] + grammar + ["mechanical expansion", "repetition or flattened voice"])),
        },
        "best_revision_strategy": "Start from the AI version, preserve every verified fact and qualification, then edit only for audience fit, concision, natural rhythm, and interface-specific hierarchy; do not imitate the humanized version's drift.",
        "evaluation_target": "A revision better than both supplied versions, with exact factual anchors and no mechanical-humanization artifacts.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    rows = parse(args.input.read_text(encoding="utf-8"))
    if len(rows) != 21 or [row["pair_number"] for row in rows] != list(range(1, 22)):
        raise SystemExit(f"Expected 21 ordered pairs, found {len(rows)}")
    annotations = [annotate(row) for row in rows]
    result = {
        "schema_version": 1,
        "dataset": args.input.name,
        "pair_count": len(rows),
        "preservation": "AI and humanized texts remain exact in the source file; annotations do not rewrite raw output.",
        "ground_truth_policy": "The humanized side is not a gold label.",
        "annotation_counts": {label: sum(item["annotation"] == label for item in annotations) for label in ("ai-stronger", "humanized-stronger", "mixed", "both-require-revision")},
        "annotations": annotations,
    }
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"pair_count": len(rows), "annotation_counts": result["annotation_counts"], "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
