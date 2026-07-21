#!/usr/bin/env python3
"""Deterministic review signals for frontend copy and contrastive pairs."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any


GENERIC_PHRASES = (
    "unlock your potential", "transform the way", "built for the future", "elevate your workflow",
    "seamless experience", "powerful, intuitive", "next-generation", "cutting-edge",
    "future-ready", "game-changing", "world-class", "reimagined", "designed for everyone",
)
TRANSITIONS = ("additionally", "furthermore", "moreover", "thus", "therefore", "consequently", "overall", "as a result", "for instance", "in conclusion")
BUREAUCRATIC = ("in relation to", "with regard to", "in the process of", "due to the fact that", "in order to", "has the ability to", "it is important to note that", "it should be understood that")
VAGUE_CTAS = {"get started", "learn more", "explore", "discover", "unlock", "transform", "continue"}
FACT_RE = re.compile(r"(?:https?://\S+|\b\d{1,2}:\d{2}\s*(?:a\.m\.|p\.m\.)?|\$\d+(?:\.\d+)?|\b\d+(?:\.\d+)?%|\b\d[\d,]*(?:\.\d+)?\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,\s*\d{4})?)", re.I)
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def facts(text: str) -> list[str]:
    return list(dict.fromkeys(match.group(0).rstrip(".,;)") for match in FACT_RE.finditer(text)))


def sentences(text: str) -> list[str]:
    return [part.strip() for part in SENTENCE_RE.split(re.sub(r"\s+", " ", text.strip())) if part.strip()]


def audit_copy(text: str, *, source_text: str = "", cta_labels: list[str] | None = None) -> dict[str, Any]:
    lower = text.lower()
    sentence_rows = sentences(text)
    openings = [" ".join(re.findall(r"[a-z0-9']+", row.lower())[:3]) for row in sentence_rows]
    opening_counts = Counter(openings)
    lengths = [len(re.findall(r"\b\w+\b", row)) for row in sentence_rows]
    source_facts = set(facts(source_text)) if source_text else set()
    candidate_facts = set(facts(text))
    findings = []
    for phrase in GENERIC_PHRASES:
        if phrase in lower:
            findings.append({"code": "generic-abstraction", "evidence": phrase, "severity": "medium"})
    for phrase in BUREAUCRATIC:
        if phrase in lower:
            findings.append({"code": "bureaucratic-padding", "evidence": phrase, "severity": "medium"})
    transition_counts = {term: len(re.findall(rf"\b{re.escape(term)}\b", lower)) for term in TRANSITIONS}
    for term, count in transition_counts.items():
        if count >= 2:
            findings.append({"code": "transition-overuse", "evidence": term, "count": count, "severity": "medium"})
    for opening, count in opening_counts.items():
        if opening and count >= 3:
            findings.append({"code": "repeated-sentence-opening", "evidence": opening, "count": count, "severity": "low"})
    if lengths and len(lengths) >= 5 and max(lengths) - min(lengths) <= 5:
        findings.append({"code": "sentence-length-monotony", "evidence": {"min": min(lengths), "max": max(lengths)}, "severity": "low"})
    if source_text:
        missing = sorted(source_facts - candidate_facts)
        introduced = sorted(candidate_facts - source_facts)
        if missing:
            findings.append({"code": "factual-anchor-omission", "evidence": missing, "severity": "high"})
        if introduced:
            findings.append({"code": "unsupported-factual-anchor", "evidence": introduced, "severity": "high"})
    vague = sorted(label for label in (cta_labels or []) if label.strip().lower() in VAGUE_CTAS)
    if vague:
        findings.append({"code": "vague-cta", "evidence": vague, "severity": "medium"})
    return {
        "passed": not any(row["severity"] == "high" for row in findings),
        "findings": findings,
        "metrics": {
            "words": len(re.findall(r"\b\w+\b", text)),
            "sentences": len(sentence_rows),
            "transition_counts": transition_counts,
            "source_fact_count": len(source_facts),
            "candidate_fact_count": len(candidate_facts),
        },
        "limitation": "Heuristics are review signals, not proof of authorship, quality, truth, or detector performance.",
    }
