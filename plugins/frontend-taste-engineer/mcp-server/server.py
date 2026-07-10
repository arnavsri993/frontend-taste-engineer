#!/usr/bin/env python3
"""Dependency-free MCP stdio server for Frontend Taste Engineer.

The server deliberately treats ``knowledge/`` JSON as immutable input.  It never
writes the corpus and never uses the network.  Retrieval is deterministic so an
evaluation result can be reproduced from a Git revision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence


PROTOCOL_VERSION = "2024-11-05"
SERVER_VERSION = "0.1.0"
DEFAULT_RECORD_BUDGET = 8
DEFAULT_CONTEXT_BUDGET = 3200
MAX_RECORD_BUDGET = 32
MAX_CONTEXT_BUDGET = 12000

WORD_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
SPACE_RE = re.compile(r"\s+")


SYNONYMS: dict[str, tuple[str, ...]] = {
    "a11y": ("accessibility", "keyboard", "focus", "screen-reader"),
    "accessibility": ("a11y", "keyboard", "focus", "semantic", "aria"),
    "animate": ("animation", "motion", "transition"),
    "animation": ("motion", "transition", "easing", "reduced-motion"),
    "auth": ("authentication", "sign-in", "login"),
    "button": ("action", "control", "press"),
    "checkout": ("payment", "form", "commerce"),
    "color": ("contrast", "palette", "surface"),
    "dashboard": ("data", "table", "chart", "application-shell"),
    "dialog": ("modal", "focus-trap", "focus-restoration"),
    "error": ("failure", "recovery", "validation"),
    "fast": ("performance", "latency", "core-web-vitals"),
    "form": ("input", "validation", "error", "submission"),
    "internationalization": ("i18n", "localization", "rtl"),
    "landing": ("marketing", "conversion", "hero"),
    "mobile": ("responsive", "touch", "small-viewport"),
    "performance": ("core-web-vitals", "bundle", "rendering", "images"),
    "redesign": ("audit", "refactor", "preserve", "regression"),
    "responsive": ("mobile", "reflow", "breakpoint", "container-query"),
    "rtl": ("internationalization", "localization", "bidirectional"),
    "screenshot": ("reconstruction", "reference", "visual-comparison"),
    "security": ("xss", "sanitization", "trust", "privacy"),
    "states": ("loading", "empty", "error", "disabled", "success"),
    "table": ("grid", "sorting", "filtering", "pagination", "data"),
    "type": ("typography", "font", "line-height"),
    "ux": ("usability", "interaction", "information-architecture"),
}


CLASSIFICATION_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("screenshot-reconstruction", ("screenshot", "reconstruct", "pixel match", "reference image")),
    ("accessibility-audit", ("accessibility audit", "a11y", "wcag", "screen reader")),
    ("performance-remediation", ("performance", "lcp", "inp", "cls", "bundle", "slow")),
    ("motion-refinement", ("motion", "animation", "transition", "easing", "spring")),
    ("design-system", ("design system", "tokens", "component library", "theming")),
    ("component-build", ("component", "dialog", "button", "combobox", "table", "form")),
    ("existing-redesign", ("redesign", "modernize", "existing", "legacy", "ugly")),
    ("visual-audit", ("audit", "review", "critique", "find issues")),
    ("greenfield-build", ("build", "create", "landing page", "website", "application")),
)

FRAMEWORKS = (
    "react", "next.js", "nextjs", "vue", "nuxt", "svelte", "sveltekit",
    "astro", "tailwind", "web-components", "html", "css", "javascript", "typescript",
)
COMPONENTS = (
    "accordion", "alert", "banner", "breadcrumb", "button", "calendar", "card",
    "carousel", "chart", "checkbox", "combobox", "dialog", "drawer", "editor",
    "file-upload", "form", "input", "link", "menu", "navigation", "pagination",
    "popover", "radio", "search", "select", "sidebar", "slider", "switch", "table",
    "tabs", "textarea", "toast", "tooltip",
)
PAGE_TYPES = {
    "marketing": ("landing", "marketing", "campaign", "pricing"),
    "product-interface": ("dashboard", "settings", "saas", "application", "internal tool"),
    "public-service": ("public service", "government", "benefits", "application form"),
    "editorial": ("editorial", "article", "publication", "news"),
    "ecommerce": ("ecommerce", "commerce", "checkout", "cart", "product page"),
}

TOPIC_ALIASES: dict[str, tuple[str, ...]] = {
    "design-direction": ("visual-direction", "art-direction", "product", "anti-patterns"),
    "design-system": ("design-systems", "tokens", "components"),
    "component": ("components", "forms", "states", "components-states-forms"),
    "layout": ("layout", "composition", "responsive"),
    "typography": ("typography",),
    "color": ("color", "surfaces", "contrast"),
    "motion": ("motion", "interaction", "animation"),
    "responsive": ("responsive", "layout", "browser"),
    "accessibility": ("accessibility", "forms", "components"),
    "content": ("content", "product-writing", "localization", "information-architecture-content"),
    "framework": ("frameworks", "code-architecture", "frameworks-code-architecture"),
    "performance": ("performance",),
    "browser": ("browser", "browsers", "progressive-enhancement"),
    "security": ("security", "privacy", "trust", "security-privacy-trust"),
    "testing": ("testing", "verification", "testing-deployment"),
    "anti-patterns": ("anti-patterns", "anti-slop-integrity", "integrity", "visual-direction"),
    "examples": ("examples",),
}

WORKFLOW_TOPICS: dict[str, tuple[str, ...]] = {
    "brief": ("product", "information-architecture", "content", "visual-direction"),
    "planning": ("design-systems", "layout", "typography", "components", "responsive"),
    "implementation": ("frameworks", "components", "states", "accessibility", "browser"),
    "refinement": ("visual-direction", "motion", "content", "images", "responsive"),
    "verification": ("testing", "accessibility", "performance", "completion", "integrity"),
}

TASK_TYPE_ALIASES: dict[str, tuple[str, ...]] = {
    "greenfield-build": ("greenfield-build", "greenfield"),
    "existing-redesign": ("existing-redesign", "redesign"),
    "component-build": ("component-build", "component"),
    "design-system": ("design-system",),
    "visual-audit": ("visual-audit", "audit"),
    "accessibility-audit": ("accessibility-audit", "audit"),
    "performance-remediation": ("performance-remediation", "audit"),
    "motion-refinement": ("motion-refinement", "component"),
    "screenshot-reconstruction": ("screenshot-reconstruction", "reconstruction"),
}

FALLBACK_RECORDS: tuple[dict[str, Any], ...] = (
    {
        "id": "offline-native-semantics",
        "title": "Prefer native semantics before ARIA",
        "topic": "accessibility",
        "subtopic": "semantics",
        "status": "stable",
        "importance": "mandatory",
        "confidence": "high",
        "principle": "Use the native HTML element whose behavior matches the interaction before adding ARIA or custom keyboard logic.",
        "rationale": "Native controls preserve established keyboard, focus, form, and assistive-technology behavior.",
        "implementation": ["Choose semantic HTML first", "Add ARIA only to express semantics absent from HTML"],
        "verification": ["Complete the flow with a keyboard", "Inspect accessible names and roles"],
        "sources": ["offline-safety-kernel"],
        "license_status": "original-summary",
        "task_types": ["component-build", "greenfield-build", "existing-redesign"],
    },
    {
        "id": "offline-state-completeness",
        "title": "Implement real interface states",
        "topic": "states",
        "subtopic": "completion",
        "status": "stable",
        "importance": "mandatory",
        "confidence": "high",
        "principle": "Implement and verify loading, empty, error, success, disabled, and permission-dependent states that the product can reach.",
        "rationale": "A polished happy path is not a complete product flow.",
        "implementation": ["Map reachable states before implementation", "Provide recovery for failures"],
        "verification": ["Force every reachable state", "Verify controls do not become dead ends"],
        "sources": ["offline-safety-kernel"],
        "license_status": "original-summary",
        "task_types": ["greenfield-build", "component-build", "existing-redesign"],
    },
    {
        "id": "offline-honest-verification",
        "title": "Report only verification that ran",
        "topic": "testing",
        "subtopic": "integrity",
        "status": "stable",
        "importance": "mandatory",
        "confidence": "high",
        "principle": "Distinguish executed checks from recommendations and never claim visual, accessibility, performance, or browser verification that did not run.",
        "rationale": "False confidence hides product risk and prevents useful follow-up.",
        "implementation": ["Record commands, viewports, and outcomes", "Label skipped checks and reasons"],
        "verification": ["Match every completion claim to evidence"],
        "sources": ["offline-safety-kernel"],
        "license_status": "original-summary",
        "task_types": ["visual-audit", "accessibility-audit", "performance-remediation", "greenfield-build"],
    },
    {
        "id": "offline-responsive-reflow",
        "title": "Verify reflow between named breakpoints",
        "topic": "responsive",
        "subtopic": "reflow",
        "status": "stable",
        "importance": "mandatory",
        "confidence": "high",
        "principle": "Choose breakpoints from content pressure and test narrow, intermediate, wide, zoomed, and short-viewport layouts for clipping and inaccessible controls.",
        "rationale": "Named device widths miss the failures that occur between breakpoints and under text enlargement.",
        "implementation": ["Use intrinsic sizing where possible", "Avoid hiding required actions to make layouts fit"],
        "verification": ["Sweep viewport widths", "Check 200 percent zoom and long localized content"],
        "sources": ["offline-safety-kernel"],
        "license_status": "original-summary",
        "task_types": ["greenfield-build", "existing-redesign", "screenshot-reconstruction"],
    },
    {
        "id": "offline-preserve-functionality",
        "title": "Audit before redesigning",
        "topic": "code-architecture",
        "subtopic": "redesign",
        "status": "stable",
        "importance": "mandatory",
        "confidence": "high",
        "principle": "Before a redesign, inventory existing behavior and preserve useful architecture, data flow, and user capability unless evidence supports a change.",
        "rationale": "A visual improvement that removes functionality or creates regressions is a failed redesign.",
        "implementation": ["Create a before-state inventory", "Prefer targeted changes over an unmeasured rewrite"],
        "verification": ["Run regression checks against the inventory"],
        "sources": ["offline-safety-kernel"],
        "license_status": "original-summary",
        "task_types": ["existing-redesign", "visual-audit"],
    },
)


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        return " ".join(f"{k} {_text(v)}" for k, v in value.items())
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return " ".join(_text(v) for v in value)
    return str(value)


def tokenize(value: Any) -> tuple[str, ...]:
    return tuple(WORD_RE.findall(_text(value).lower().replace("_", "-")))


def _slug(value: Any) -> str:
    return "-".join(tokenize(value))


def _record_id(value: Any) -> str:
    """Normalize case without discarding the corpus' dotted ID namespace."""
    candidate = str(value or "").strip().lower().replace("_", "-")
    candidate = re.sub(r"[^a-z0-9.-]+", "-", candidate)
    candidate = re.sub(r"-+", "-", candidate).strip("-.")
    return candidate


def _list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def estimate_tokens(value: Any) -> int:
    # Deliberately conservative, deterministic and tokenizer-independent.
    return max(1, (len(json.dumps(value, ensure_ascii=False, sort_keys=True)) + 3) // 4)


def _norm_string_list(value: Any) -> tuple[str, ...]:
    return tuple(dict.fromkeys(_slug(v) for v in _list(value) if _slug(v)))


def _iter_json_records(value: Any, origin: str) -> Iterator[dict[str, Any]]:
    if isinstance(value, list):
        for item in value:
            if isinstance(item, Mapping):
                yield dict(item, _origin=origin)
        return
    if not isinstance(value, Mapping):
        return
    for key in ("records", "rules", "guidance", "items"):
        if isinstance(value.get(key), list):
            for item in value[key]:
                if isinstance(item, Mapping):
                    yield dict(item, _origin=origin)
            return
    # Index and registry documents are metadata, not rules.
    if any(key in value for key in ("principle", "guidance", "recommendation")) and (
        "id" in value or "title" in value
    ):
        yield dict(value, _origin=origin)


@dataclass(frozen=True)
class Record:
    id: str
    title: str
    topic: str
    subtopic: str
    status: str
    importance: str
    confidence: str
    principle: str
    rationale: str
    applies_when: tuple[str, ...] = ()
    exceptions: tuple[str, ...] = ()
    implementation: tuple[str, ...] = ()
    verification: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()
    task_types: tuple[str, ...] = ()
    page_types: tuple[str, ...] = ()
    components: tuple[str, ...] = ()
    frameworks: tuple[str, ...] = ()
    platforms: tuple[str, ...] = ()
    related_rules: tuple[str, ...] = ()
    license_status: str = "unknown"
    last_reviewed: str = ""
    origin: str = ""
    extra: Mapping[str, Any] = field(default_factory=dict, compare=False, hash=False)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any], ordinal: int = 0) -> "Record":
        principle = str(data.get("principle") or data.get("guidance") or data.get("recommendation") or "").strip()
        title = str(data.get("title") or principle[:80] or f"Guidance {ordinal}").strip()
        rid = _record_id(data.get("id")) or _slug(title) or f"record-{ordinal:04d}"
        known = {f.name for f in cls.__dataclass_fields__.values()} | {"_origin", "guidance", "recommendation"}
        return cls(
            id=rid,
            title=title,
            topic=_slug(data.get("topic") or data.get("category") or "general"),
            subtopic=_slug(data.get("subtopic") or "general"),
            status=_slug(data.get("status") or "stable"),
            importance=_slug(data.get("importance") or "recommended"),
            confidence=_slug(data.get("confidence") or "medium"),
            principle=principle,
            rationale=str(data.get("rationale") or "").strip(),
            applies_when=tuple(str(v).strip() for v in _list(data.get("applies_when")) if str(v).strip()),
            exceptions=tuple(str(v).strip() for v in _list(data.get("exceptions")) if str(v).strip()),
            implementation=tuple(str(v).strip() for v in _list(data.get("implementation")) if str(v).strip()),
            verification=tuple(str(v).strip() for v in _list(data.get("verification")) if str(v).strip()),
            sources=tuple(str(v).strip() for v in _list(data.get("sources")) if str(v).strip()),
            task_types=_norm_string_list(data.get("task_types")),
            page_types=_norm_string_list(data.get("page_types")),
            components=_norm_string_list(data.get("components")),
            frameworks=_norm_string_list(data.get("frameworks")),
            platforms=_norm_string_list(data.get("platforms")),
            related_rules=tuple(dict.fromkeys(_record_id(v) for v in _list(data.get("related_rules")) if _record_id(v))),
            license_status=str(data.get("license_status") or "unknown"),
            last_reviewed=str(data.get("last_reviewed") or ""),
            origin=str(data.get("_origin") or ""),
            extra={k: v for k, v in data.items() if k not in known},
        )

    @property
    def searchable(self) -> str:
        return " ".join(
            [self.id, self.title, self.topic, self.subtopic, self.principle, self.rationale]
            + list(self.applies_when)
            + list(self.exceptions)
            + list(self.implementation)
            + list(self.verification)
            + list(self.task_types)
            + list(self.page_types)
            + list(self.components)
            + list(self.frameworks)
        ).lower()

    @property
    def fingerprint(self) -> str:
        normalized = " ".join(tokenize(self.principle or self.title))
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]

    def packet(self, score: float, reasons: Sequence[str]) -> dict[str, Any]:
        packet: dict[str, Any] = {
            "id": self.id,
            "title": self.title,
            "topic": self.topic,
            "subtopic": self.subtopic,
            "status": self.status,
            "importance": self.importance,
            "confidence": self.confidence,
            "principle": self.principle,
            "rationale": self.rationale,
            "implementation": list(self.implementation[:4]),
            "verification": list(self.verification[:4]),
            "exceptions": list(self.exceptions[:3]),
            "sources": list(self.sources),
            "license_status": self.license_status,
            "retrieval": {"score": round(score, 3), "reasons": list(reasons)},
        }
        return {key: value for key, value in packet.items() if value not in ("", [], None)}


def default_plugin_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_knowledge_dir() -> Path:
    configured = os.environ.get("FTE_KNOWLEDGE_DIR")
    return Path(configured).expanduser().resolve() if configured else default_plugin_root() / "knowledge"


def load_records(knowledge_dir: Path | str | None = None) -> tuple[list[Record], dict[str, Any]]:
    root = Path(knowledge_dir) if knowledge_dir is not None else default_knowledge_dir()
    raw: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    files: list[str] = []
    if root.exists():
        for path in sorted(root.rglob("*.json")):
            if path.name.endswith(".schema.json") or path.name in {"index.json", "coverage.json"}:
                continue
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
                relative = str(path.relative_to(root))
                extracted = list(_iter_json_records(value, relative))
                if extracted:
                    files.append(relative)
                    raw.extend(extracted)
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                errors.append({"file": str(path), "error": str(exc)})
    records: list[Record] = []
    seen: set[str] = set()
    for ordinal, data in enumerate(raw, 1):
        record = Record.from_dict(data, ordinal)
        if record.id in seen or not record.principle:
            continue
        seen.add(record.id)
        records.append(record)
    fallback = not records
    if fallback:
        records = [Record.from_dict(item, idx) for idx, item in enumerate(FALLBACK_RECORDS, 1)]
    records.sort(key=lambda r: r.id)
    return records, {
        "knowledge_dir": str(root.resolve()),
        "source_files": files,
        "parse_errors": errors,
        "fallback": fallback,
        "record_count": len(records),
        "offline": True,
    }


def classify_task(text: str, context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    context = context or {}
    haystack = f"{text} {_text(context)}".lower()
    matches: list[tuple[int, str, list[str]]] = []
    for task_type, needles in CLASSIFICATION_RULES:
        evidence = [needle for needle in needles if needle in haystack]
        if evidence:
            matches.append((sum(2 if " " in needle else 1 for needle in evidence), task_type, evidence))
    matches.sort(key=lambda item: (-item[0], item[1]))
    task_type = matches[0][1] if matches else "greenfield-build"
    stage = str(context.get("stage") or "").strip().lower()
    if stage not in WORKFLOW_TOPICS:
        if any(word in haystack for word in ("audit", "verify", "test", "review")):
            stage = "verification"
        elif any(word in haystack for word in ("fix", "implement", "code", "build")):
            stage = "implementation"
        elif any(word in haystack for word in ("polish", "refine", "motion")):
            stage = "refinement"
        elif any(word in haystack for word in ("plan", "architecture", "system")):
            stage = "planning"
        else:
            stage = "brief"
    frameworks = []
    for framework in FRAMEWORKS:
        if framework in haystack:
            frameworks.append("next.js" if framework == "nextjs" else framework)
    components = [component for component in COMPONENTS if component.replace("-", " ") in haystack or component in haystack]
    page_types = [page_type for page_type, terms in PAGE_TYPES.items() if any(term in haystack for term in terms)]
    risk = "high" if any(term in haystack for term in ("payment", "health", "government", "authentication", "public service")) else "normal"
    confidence = min(0.98, 0.55 + (matches[0][0] * 0.08 if matches else 0.0))
    return {
        "task_type": task_type,
        "stage": stage,
        "page_types": page_types or [str(context.get("page_type") or "general")],
        "frameworks": list(dict.fromkeys(frameworks)),
        "components": list(dict.fromkeys(components)),
        "risk": risk,
        "confidence": round(confidence, 2),
        "evidence": matches[0][2] if matches else ["default-classification"],
        "recommended_budget": _recommended_budget(task_type, text),
    }


def _recommended_budget(task_type: str, text: str) -> dict[str, int]:
    if task_type in {"component-build", "motion-refinement"}:
        return {"records": 6, "context_tokens": 2400}
    if len(text) < 80 and any(word in text.lower() for word in ("fix", "color", "spacing", "copy")):
        return {"records": 4, "context_tokens": 1600}
    if task_type in {"visual-audit", "accessibility-audit", "performance-remediation"}:
        return {"records": 12, "context_tokens": 5000}
    return {"records": 10, "context_tokens": 4000}


@dataclass
class Scored:
    record: Record
    score: float
    reasons: list[str]


class RetrievalEngine:
    """In-memory deterministic hybrid retrieval over canonical records."""

    def __init__(self, knowledge_dir: Path | str | None = None) -> None:
        self.records, self.info = load_records(knowledge_dir)
        self.by_id = {record.id: record for record in self.records}
        self.document_frequency: dict[str, int] = {}
        self.record_tokens: dict[str, set[str]] = {}
        for record in self.records:
            tokens = set(tokenize(record.searchable))
            self.record_tokens[record.id] = tokens
            for token in tokens:
                self.document_frequency[token] = self.document_frequency.get(token, 0) + 1

    def _query_terms(self, query: str, semantic: bool) -> tuple[set[str], set[str]]:
        exact = set(tokenize(query))
        expanded: set[str] = set()
        if semantic:
            for term in sorted(exact):
                expanded.update(SYNONYMS.get(term, ()))
                if term.endswith("s"):
                    expanded.add(term[:-1])
        return exact, expanded - exact

    @staticmethod
    def _metadata(record: Record, filters: Mapping[str, Any]) -> tuple[float, list[str], bool]:
        score = 0.0
        reasons: list[str] = []
        hard_mismatch = False
        mappings = {
            "topics": (record.topic, record.subtopic),
            "task_types": record.task_types,
            "page_types": record.page_types,
            "components": record.components,
            "frameworks": record.frameworks,
            "platforms": record.platforms,
            "statuses": (record.status,),
            "importance": (record.importance,),
        }
        for key, record_values in mappings.items():
            wanted = set(_norm_string_list(filters.get(key)))
            if not wanted:
                continue
            values = set(record_values)
            if values & wanted or "universal" in values:
                score += 5.0 if key in {"topics", "components"} else 3.0
                reasons.append(f"metadata:{key}")
            elif key in {"statuses", "importance"}:
                hard_mismatch = True
            else:
                score -= 1.5
        return score, reasons, hard_mismatch

    def score_records(
        self,
        query: str,
        filters: Mapping[str, Any] | None = None,
        *,
        semantic: bool = True,
    ) -> list[Scored]:
        filters = filters or {}
        exact_terms, expanded_terms = self._query_terms(query, semantic)
        exact_id = _record_id(query)
        total = max(1, len(self.records))
        scored: list[Scored] = []
        for record in self.records:
            score, reasons, hard_mismatch = self._metadata(record, filters)
            if hard_mismatch:
                continue
            record_terms = self.record_tokens[record.id]
            exact_overlap = exact_terms & record_terms
            expansion_overlap = expanded_terms & record_terms
            if record.id == exact_id or record.id in {_record_id(v) for v in _list(filters.get("ids"))}:
                score += 100.0
                reasons.append("exact-id")
            if exact_overlap:
                weighted = sum(1.0 + (total / (1 + self.document_frequency.get(term, total))) for term in exact_overlap)
                score += min(18.0, weighted)
                reasons.append("lexical:" + ",".join(sorted(exact_overlap)[:8]))
            query_lower = query.lower().strip()
            if query_lower and query_lower in record.searchable:
                score += 8.0
                reasons.append("phrase")
            if expansion_overlap:
                score += min(6.0, len(expansion_overlap) * 1.1)
                reasons.append("semantic-expansion:" + ",".join(sorted(expansion_overlap)[:6]))
            if record.importance == "mandatory":
                score += 2.5
                reasons.append("mandatory-preservation")
            if record.status == "stable":
                score += 0.75
            elif record.status in {"experimental", "inspiration-only"}:
                score -= 0.5
            if record.confidence == "high":
                score += 0.25
            retrieval_evidence = any(
                reason != "mandatory-preservation" for reason in reasons
            )
            if score > 0 and retrieval_evidence:
                scored.append(Scored(record, score, reasons))
        return sorted(scored, key=lambda item: (-item.score, item.record.id))

    @staticmethod
    def _dedupe(scored: Iterable[Scored]) -> list[Scored]:
        seen_ids: set[str] = set()
        seen_fingerprints: set[str] = set()
        result: list[Scored] = []
        for item in scored:
            if item.record.id in seen_ids or item.record.fingerprint in seen_fingerprints:
                continue
            seen_ids.add(item.record.id)
            seen_fingerprints.add(item.record.fingerprint)
            result.append(item)
        return result

    def search(
        self,
        query: str,
        filters: Mapping[str, Any] | None = None,
        *,
        budget_records: int = DEFAULT_RECORD_BUDGET,
        context_budget: int = DEFAULT_CONTEXT_BUDGET,
        strategy: str = "hybrid",
    ) -> dict[str, Any]:
        started = time.perf_counter()
        budget_records = max(1, min(MAX_RECORD_BUDGET, int(budget_records)))
        context_budget = max(300, min(MAX_CONTEXT_BUDGET, int(context_budget)))
        semantic = strategy == "hybrid"
        scored = self._dedupe(self.score_records(query, filters, semantic=semantic))

        # Mandatory rules compete on relevance but receive reserved capacity.  A
        # generic mandatory rule is not injected when it has no query/metadata
        # evidence beyond the preservation boost.
        mandatory = [item for item in scored if item.record.importance == "mandatory" and item.score >= 3.0]
        normal = [item for item in scored if item.record.importance != "mandatory"]
        mandatory_slots = min(len(mandatory), max(1, (budget_records + 2) // 3))
        chosen = mandatory[:mandatory_slots]
        chosen_ids = {item.record.id for item in chosen}
        for item in sorted(scored, key=lambda entry: (-entry.score, entry.record.id)):
            if item.record.id in chosen_ids:
                continue
            chosen.append(item)
            chosen_ids.add(item.record.id)
            if len(chosen) >= budget_records:
                break
        chosen.sort(key=lambda item: (-item.score, item.record.id))

        packets: list[dict[str, Any]] = []
        used = 0
        truncated = False
        for item in chosen:
            packet = item.record.packet(item.score, item.reasons)
            cost = estimate_tokens(packet)
            if packets and used + cost > context_budget:
                truncated = True
                continue
            if not packets and cost > context_budget:
                # Preserve the rule while trimming explanatory arrays.
                packet.pop("implementation", None)
                packet.pop("verification", None)
                packet.pop("exceptions", None)
                cost = estimate_tokens(packet)
            packets.append(packet)
            used += cost
        elapsed = (time.perf_counter() - started) * 1000.0
        return {
            "query": query,
            "strategy": strategy,
            "filters": dict(filters or {}),
            "records": packets,
            "summary": {
                "returned": len(packets),
                "candidates": len(scored),
                "mandatory_returned": sum(1 for item in packets if item.get("importance") == "mandatory"),
                "estimated_context_tokens": used,
                "context_budget": context_budget,
                "truncated": truncated or len(packets) < min(len(chosen), budget_records),
                "latency_ms": round(elapsed, 3),
                "offline_fallback": bool(self.info.get("fallback")),
            },
            "corpus": self.info,
        }


def _filters_from_args(args: Mapping[str, Any], classification: Mapping[str, Any] | None = None) -> dict[str, Any]:
    filters = dict(args.get("filters") or {})
    for key in ("ids", "topics", "task_types", "page_types", "components", "frameworks", "platforms", "statuses", "importance"):
        if key in args and args[key] not in (None, "", []):
            filters[key] = args[key]
    if classification:
        filters.setdefault("task_types", list(TASK_TYPE_ALIASES.get(classification["task_type"], (classification["task_type"],))))
        filters.setdefault("page_types", classification.get("page_types", []))
        filters.setdefault("components", classification.get("components", []))
        filters.setdefault("frameworks", classification.get("frameworks", []))
    return filters


def _search_args(engine: RetrievalEngine, args: Mapping[str, Any], *, topic: str | None = None) -> dict[str, Any]:
    query = str(args.get("query") or args.get("context") or args.get("task") or topic or "frontend guidance")
    classification = classify_task(query, args)
    filters = _filters_from_args(args, classification)
    if topic:
        filters["topics"] = list(TOPIC_ALIASES.get(topic, (topic,)))
    recommended = classification["recommended_budget"]
    return engine.search(
        query,
        filters,
        budget_records=int(args.get("budget_records") or recommended["records"]),
        context_budget=int(args.get("context_budget") or recommended["context_tokens"]),
        strategy=str(args.get("strategy") or "hybrid"),
    )


def get_workflow(engine: RetrievalEngine, args: Mapping[str, Any]) -> dict[str, Any]:
    stage = _slug(args.get("stage") or classify_task(str(args.get("task") or args.get("context") or ""), args)["stage"])
    if stage not in WORKFLOW_TOPICS:
        stage = "planning"
    augmented = dict(args)
    augmented["topics"] = list(WORKFLOW_TOPICS[stage])
    packet = _search_args(engine, augmented)
    packet["workflow"] = {
        "stage": stage,
        "required_sequence": {
            "brief": ["inspect", "classify", "brief", "design-thesis"],
            "planning": ["inventory-system", "map-states", "retrieve", "plan"],
            "implementation": ["implement-behavior", "integrate-accessibility", "test-locally"],
            "refinement": ["capture", "compare", "correct-high-impact-gaps"],
            "verification": ["functional", "keyboard", "responsive", "accessibility", "performance", "report-evidence"],
        }[stage],
    }
    return packet


BASE_COMPONENT_STATES = (
    "default", "hover", "focus-visible", "active", "disabled", "loading",
    "empty", "error", "success", "offline", "permission-denied",
)


def get_state_matrix(engine: RetrievalEngine, args: Mapping[str, Any]) -> dict[str, Any]:
    component = _slug(args.get("component") or "component")
    packet = _search_args(engine, {**args, "components": [component], "query": f"{component} states keyboard touch responsive"}, topic="component")
    states = list(BASE_COMPONENT_STATES)
    if component in {"checkbox", "radio", "switch", "tabs"}:
        states.extend(["selected", "checked", "indeterminate"])
    if component in {"form", "input", "textarea", "select", "combobox"}:
        states.extend(["read-only", "invalid", "saving", "saved"])
    return {
        "component": component,
        "states": list(dict.fromkeys(states)),
        "interaction_checks": ["keyboard", "pointer", "touch", "screen-reader", "reduced-motion", "narrow-viewport"],
        "guidance": packet,
    }


def get_examples(engine: RetrievalEngine, args: Mapping[str, Any]) -> dict[str, Any]:
    query = str(args.get("query") or args.get("context") or "frontend implementation verification")
    packet = _search_args(engine, {**args, "query": query})
    return {
        "query": query,
        "examples": [
            {
                "rule_id": item["id"],
                "implementation": item.get("implementation", []),
                "verification": item.get("verification", []),
                "sources": item.get("sources", []),
            }
            for item in packet["records"]
            if item.get("implementation") or item.get("verification")
        ],
        "retrieval": packet["summary"],
        "corpus": packet["corpus"],
    }


COMPLETION_GATES = (
    ("functional", "Primary actions, navigation, and forms complete their real behavior; no dead controls."),
    ("state-complete", "Reachable loading, empty, error, success, offline, and permission states are implemented."),
    ("keyboard", "The primary flow works by keyboard with visible focus and logical focus movement."),
    ("responsive", "Narrow, intermediate, wide, short, zoomed, and long-content layouts do not lose information or actions."),
    ("accessibility", "Semantics, names, contrast, errors, motion preferences, and manual checks are evidenced."),
    ("performance", "The change respects explicit budgets or documents measured tradeoffs."),
    ("integrity", "Claims, metrics, testimonials, controls, and verification statements are real and evidenced."),
)


def get_completion_gate(engine: RetrievalEngine, args: Mapping[str, Any]) -> dict[str, Any]:
    context = str(args.get("context") or args.get("task") or "frontend completion verification")
    packet = _search_args(engine, {**args, "query": context, "importance": ["mandatory"]})
    return {
        "task": classify_task(context, args),
        "gates": [{"id": gate_id, "requirement": requirement, "status": "unverified"} for gate_id, requirement in COMPLETION_GATES],
        "mandatory_guidance": packet,
        "reporting_rule": "Mark a gate passed only with executed evidence; otherwise mark unverified or blocked.",
    }


AUDIT_CHECKS: tuple[tuple[str, str, str, tuple[str, ...], str], ...] = (
    ("functional-integrity", "critical", "Provide real behavior or explicitly label the element non-interactive.", ("button", "form", "link", "submit", "action"), "dead controls and real behavior"),
    ("state-completeness", "high", "Map and test reachable loading, empty, error, success, and permission states.", ("loading", "empty", "error", "success", "permission"), "reachable interface states"),
    ("keyboard-focus", "high", "Specify keyboard order, visible focus, overlay focus containment, and restoration.", ("keyboard", "focus", "escape", "tab"), "keyboard and focus behavior"),
    ("responsive-reflow", "high", "Test reflow across content-driven widths, zoom, long content, and short viewports.", ("responsive", "mobile", "zoom", "overflow", "viewport"), "responsive evidence"),
    ("content-integrity", "high", "Replace fabricated or placeholder claims with sourced content or honest placeholders.", ("content", "copy", "claim", "metric", "testimonial"), "content provenance and truth"),
    ("reduced-motion", "medium", "Define a reduced-motion behavior and test interrupted or repeated interactions.", ("reduced motion", "prefers-reduced-motion", "interrupt", "motion"), "motion preference"),
    ("performance-budget", "medium", "Name a relevant budget and record an executed measurement or the reason it was skipped.", ("performance", "bundle", "lcp", "inp", "cls", "budget"), "performance evidence"),
    ("verification-evidence", "high", "Record commands, viewports, observations, and failures; separate executed checks from recommendations.", ("tested", "verified", "screenshot", "axe", "lighthouse", "evidence"), "executed verification"),
)


def audit_payload(engine: RetrievalEngine, args: Mapping[str, Any], kind: str) -> dict[str, Any]:
    payload = args.get("plan") if kind == "plan" else args.get("implementation")
    if payload is None:
        payload = args.get("content") or args.get("context") or ""
    haystack = _text(payload).lower()
    findings: list[dict[str, Any]] = []
    for check_id, severity, correction, terms, evidence_name in AUDIT_CHECKS:
        found = [term for term in terms if term in haystack]
        if not found:
            findings.append({
                "id": check_id,
                "severity": severity,
                "finding": f"No evidence of {evidence_name} was found in the supplied {kind}.",
                "evidence": {"searched_terms": list(terms), "matched": []},
                "correction": correction,
                "classification": "defect-risk",
            })
    findings.sort(key=lambda item: ({"critical": 0, "high": 1, "medium": 2, "low": 3}[item["severity"]], item["id"]))
    query = " ".join(item["id"] for item in findings[:5]) or f"{kind} verification"
    return {
        "audit_kind": kind,
        "finding_count": len(findings),
        "findings": findings,
        "passed_signals": [check_id for check_id, _, _, terms, _ in AUDIT_CHECKS if any(term in haystack for term in terms)],
        "guidance": _search_args(engine, {**args, "query": query, "budget_records": min(10, max(4, len(findings)))}),
        "limitation": "This deterministic audit checks supplied evidence; it does not inspect a browser or execute product behavior.",
    }


def compare_directions(engine: RetrievalEngine, args: Mapping[str, Any]) -> dict[str, Any]:
    directions = args.get("directions") or []
    if isinstance(directions, Mapping):
        directions = [{"name": key, "description": value} for key, value in directions.items()]
    normalized = []
    context = str(args.get("context") or "")
    context_tokens = set(tokenize(context))
    for idx, item in enumerate(_list(directions), 1):
        if isinstance(item, str):
            item = {"name": f"direction-{idx}", "description": item}
        if not isinstance(item, Mapping):
            continue
        description = _text(item.get("description") or item)
        terms = set(tokenize(description))
        fit = len(terms & context_tokens)
        integrity = 2 - sum(term in terms for term in ("fake", "placeholder", "nonfunctional"))
        accessibility = sum(term in terms for term in ("accessible", "semantic", "contrast", "keyboard"))
        maintainability = sum(term in terms for term in ("tokens", "system", "reuse", "component"))
        originality = sum(term in terms for term in ("distinctive", "editorial", "art-direction", "brand"))
        score = fit * 2 + integrity * 2 + accessibility + maintainability + originality
        normalized.append({
            "name": str(item.get("name") or f"direction-{idx}"),
            "score": score,
            "evidence": {"product_fit_terms": sorted(terms & context_tokens), "integrity": integrity, "accessibility_signals": accessibility, "system_signals": maintainability, "originality_signals": originality},
            "tradeoffs": "Requires human review against product constraints and references; keyword evidence is not an aesthetic verdict.",
        })
    normalized.sort(key=lambda item: (-item["score"], item["name"]))
    return {
        "comparison": normalized,
        "recommended": normalized[0]["name"] if normalized else None,
        "guidance": _search_args(engine, {**args, "query": context or "compare product-appropriate design direction"}, topic="design-direction"),
    }


def provenance(engine: RetrievalEngine, args: Mapping[str, Any]) -> dict[str, Any]:
    ids = tuple(dict.fromkeys(_record_id(value) for value in _list(args.get("ids") or args.get("id")) if _record_id(value)))
    if not ids and args.get("query"):
        packet = engine.search(str(args["query"]), budget_records=int(args.get("budget_records") or 6))
        ids = tuple(item["id"] for item in packet["records"])
    records = []
    missing = []
    for rid in ids:
        record = engine.by_id.get(rid)
        if not record:
            missing.append(rid)
            continue
        records.append({
            "id": record.id,
            "title": record.title,
            "sources": list(record.sources),
            "license_status": record.license_status,
            "last_reviewed": record.last_reviewed or None,
            "origin": record.origin or None,
            "status": record.status,
            "confidence": record.confidence,
        })
    return {"records": records, "missing_ids": missing, "fallback": engine.info.get("fallback", False)}


def maintenance_report(engine: RetrievalEngine, tool: str, args: Mapping[str, Any]) -> dict[str, Any]:
    base = {
        "tool": tool,
        "mode": "read-only",
        "offline": True,
        "stable_knowledge_modified": False,
        "corpus": engine.info,
        "generated_at": "deterministic-runtime",
    }
    if tool == "check_registered_sources":
        missing = [record.id for record in engine.records if not record.sources]
        base["report"] = {"records_without_sources": missing, "passed": not missing}
    elif tool == "discover_candidate_sources":
        base["report"] = {
            "candidates": [],
            "network_attempted": False,
            "next_step": "Run the repository research workflow with explicit network access; review candidates before promotion.",
        }
    elif tool == "generate_source_audit":
        license_unknown = [record.id for record in engine.records if record.license_status in {"", "unknown"}]
        stale_unknown = [record.id for record in engine.records if not record.last_reviewed]
        base["report"] = {"unknown_license": license_unknown, "missing_review_date": stale_unknown}
    elif tool == "generate_coverage_report":
        counts: dict[str, int] = {}
        for record in engine.records:
            counts[record.topic] = counts.get(record.topic, 0) + 1
        base["report"] = {"topic_counts": dict(sorted(counts.items())), "record_count": len(engine.records)}
    elif tool == "propose_knowledge_update":
        base["report"] = {
            "proposal": args.get("proposal") or args.get("context") or "",
            "status": "candidate-only",
            "required_reviews": ["provenance", "license", "contradiction", "retrieval-eval", "human-promotion"],
        }
    elif tool in {"run_retrieval_evals", "run_frontend_evals"}:
        base["report"] = {
            "executed": False,
            "reason": "The MCP surface is read-only and does not spawn processes.",
            "command": "python3 evals/run_retrieval_evals.py" if tool == "run_retrieval_evals" else "python3 evals/run_frontend_evals.py",
        }
    return base


COMMON_SEARCH_SCHEMA = {
    "type": "object",
    "properties": {
        "query": {"type": "string"},
        "context": {"type": "string"},
        "budget_records": {"type": "integer", "minimum": 1, "maximum": MAX_RECORD_BUDGET},
        "context_budget": {"type": "integer", "minimum": 300, "maximum": MAX_CONTEXT_BUDGET},
        "strategy": {"type": "string", "enum": ["lexical", "hybrid"]},
        "filters": {"type": "object"},
        "task_types": {"type": "array", "items": {"type": "string"}},
        "page_types": {"type": "array", "items": {"type": "string"}},
        "components": {"type": "array", "items": {"type": "string"}},
        "frameworks": {"type": "array", "items": {"type": "string"}},
        "statuses": {"type": "array", "items": {"type": "string"}},
    },
    "additionalProperties": True,
}


def _tool(name: str, description: str, schema: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {"name": name, "description": description, "inputSchema": dict(schema or COMMON_SEARCH_SCHEMA)}


CATEGORY_TOOLS = {
    "get_design_direction_guidance": "design-direction",
    "get_design_system_guidance": "design-system",
    "get_component_guidance": "component",
    "get_layout_guidance": "layout",
    "get_typography_guidance": "typography",
    "get_color_guidance": "color",
    "get_motion_guidance": "motion",
    "get_responsive_guidance": "responsive",
    "get_accessibility_requirements": "accessibility",
    "get_content_guidance": "content",
    "get_framework_guidance": "framework",
    "get_performance_guidance": "performance",
    "get_browser_guidance": "browser",
    "get_security_guidance": "security",
    "get_testing_requirements": "testing",
    "get_anti_patterns": "anti-patterns",
    "get_examples": "examples",
}


TOOLS = [
    _tool("classify_frontend_task", "Classify a frontend task, workflow stage, page type, framework, components, risk, and retrieval budget.", {"type": "object", "properties": {"task": {"type": "string"}, "context": {"type": "object"}}, "required": ["task"]}),
    _tool("search_frontend_guidance", "Hybrid-search compact, source-backed frontend guidance with deterministic budgets."),
    _tool("get_workflow", "Retrieve stage-specific workflow guidance.", {"type": "object", "properties": {"stage": {"type": "string", "enum": list(WORKFLOW_TOPICS)}, "task": {"type": "string"}, "context_budget": {"type": "integer"}}}),
    *[_tool(name, f"Retrieve focused {topic.replace('-', ' ')} guidance.") for name, topic in CATEGORY_TOOLS.items()],
    _tool("get_component_state_matrix", "Return required component states and focused supporting guidance.", {"type": "object", "properties": {"component": {"type": "string"}, "context": {"type": "string"}}, "required": ["component"]}),
    _tool("get_source_provenance", "Inspect source, license, stability, and origin metadata for guidance IDs.", {"type": "object", "properties": {"id": {"type": "string"}, "ids": {"type": "array", "items": {"type": "string"}}, "query": {"type": "string"}}}),
    _tool("get_completion_gate", "Return evidence-oriented completion gates plus mandatory guidance."),
    _tool("audit_frontend_plan", "Audit a supplied plan for missing frontend product and verification evidence.", {"type": "object", "properties": {"plan": {}, "context": {"type": "string"}}, "required": ["plan"]}),
    _tool("audit_frontend_implementation", "Audit supplied implementation evidence without executing product code.", {"type": "object", "properties": {"implementation": {}, "context": {"type": "string"}}, "required": ["implementation"]}),
    _tool("compare_design_directions", "Compare design directions against explicit product context using inspectable evidence.", {"type": "object", "properties": {"context": {"type": "string"}, "directions": {}}, "required": ["directions"]}),
    *[_tool(name, "Generate a read-only, offline maintenance report; never modifies stable knowledge.") for name in (
        "check_registered_sources", "discover_candidate_sources", "generate_source_audit", "generate_coverage_report",
        "propose_knowledge_update", "run_retrieval_evals", "run_frontend_evals",
    )],
]


class ToolError(ValueError):
    pass


def call_tool(engine: RetrievalEngine, name: str, arguments: Mapping[str, Any] | None) -> dict[str, Any]:
    args = dict(arguments or {})
    if name == "classify_frontend_task":
        task = str(args.get("task") or "").strip()
        if not task:
            raise ToolError("classify_frontend_task requires a non-empty 'task'")
        return classify_task(task, args.get("context") if isinstance(args.get("context"), Mapping) else args)
    if name == "search_frontend_guidance":
        return _search_args(engine, args)
    if name == "get_workflow":
        return get_workflow(engine, args)
    if name == "get_examples":
        return get_examples(engine, args)
    if name in CATEGORY_TOOLS:
        return _search_args(engine, args, topic=CATEGORY_TOOLS[name])
    if name == "get_component_state_matrix":
        return get_state_matrix(engine, args)
    if name == "get_source_provenance":
        return provenance(engine, args)
    if name == "get_completion_gate":
        return get_completion_gate(engine, args)
    if name == "audit_frontend_plan":
        return audit_payload(engine, args, "plan")
    if name == "audit_frontend_implementation":
        return audit_payload(engine, args, "implementation")
    if name == "compare_design_directions":
        return compare_directions(engine, args)
    if name in {"check_registered_sources", "discover_candidate_sources", "generate_source_audit", "generate_coverage_report", "propose_knowledge_update", "run_retrieval_evals", "run_frontend_evals"}:
        return maintenance_report(engine, name, args)
    raise ToolError(f"Unknown tool: {name}")


def _response(request_id: Any, result: Any = None, error: Mapping[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {"jsonrpc": "2.0", "id": request_id}
    if error is not None:
        value["error"] = dict(error)
    else:
        value["result"] = result
    return value


def dispatch(engine: RetrievalEngine, message: Mapping[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")
    if request_id is None:
        return None
    if method == "initialize":
        requested = str((message.get("params") or {}).get("protocolVersion") or PROTOCOL_VERSION)
        return _response(request_id, {
            "protocolVersion": requested,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "frontend-taste-engineer", "version": SERVER_VERSION},
            "instructions": "Read-only, deterministic frontend guidance retrieval. Stable knowledge is never modified.",
        })
    if method == "ping":
        return _response(request_id, {})
    if method == "tools/list":
        return _response(request_id, {"tools": TOOLS})
    if method == "tools/call":
        params = message.get("params") or {}
        try:
            result = call_tool(engine, str(params.get("name") or ""), params.get("arguments") or {})
            encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            return _response(request_id, {"content": [{"type": "text", "text": encoded}], "structuredContent": result, "isError": False})
        except (ToolError, TypeError, ValueError) as exc:
            payload = {"error": str(exc), "type": exc.__class__.__name__}
            return _response(request_id, {"content": [{"type": "text", "text": json.dumps(payload, sort_keys=True)}], "structuredContent": payload, "isError": True})
    return _response(request_id, error={"code": -32601, "message": f"Method not found: {method}"})


def serve_stdio(engine: RetrievalEngine) -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
            if not isinstance(message, Mapping):
                raise ValueError("JSON-RPC message must be an object")
            response = dispatch(engine, message)
        except (json.JSONDecodeError, ValueError) as exc:
            response = _response(None, error={"code": -32700, "message": str(exc)})
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
            sys.stdout.flush()
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--knowledge-dir", type=Path, default=default_knowledge_dir())
    parser.add_argument("--self-check", action="store_true", help="Load the corpus and emit a deterministic health report.")
    args = parser.parse_args(argv)
    engine = RetrievalEngine(args.knowledge_dir)
    if args.self_check:
        report = {
            "ok": not engine.info["parse_errors"],
            "server_version": SERVER_VERSION,
            "tool_count": len(TOOLS),
            "corpus": engine.info,
            "mandatory_records": sum(record.importance == "mandatory" for record in engine.records),
        }
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["ok"] else 1
    return serve_stdio(engine)


if __name__ == "__main__":
    raise SystemExit(main())
