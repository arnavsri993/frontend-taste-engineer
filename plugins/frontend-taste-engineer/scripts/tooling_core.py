#!/usr/bin/env python3
"""Shared deterministic maintenance tooling for Frontend Taste Engineer.

Only the standard library is required.  Network access and arbitrary project
execution are absent by default.  Every write-capable command supports
``--dry-run`` and refuses to write into the canonical ``knowledge/`` tree.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = PLUGIN_ROOT / "mcp-server" / "server.py"
TODAY = dt.date.today()
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)|!\[[^\]]*\]\(([^)]+)\)")
URL_RE = re.compile(r"https?://[^\s)>\]}'\"]+")
SECRET_PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\bgh[opusr]_[A-Za-z0-9_]{30,}\b"),
    "openai-key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "generic-secret": re.compile(r"(?i)\b(?:api[_-]?key|client[_-]?secret|access[_-]?token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}"),
}
SOURCE_SUFFIXES = {".html", ".htm", ".css", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro", ".md", ".json", ".yml", ".yaml", ".toml", ".py", ".sh"}
EXPECTED_TOPICS = (
    "accessibility", "anti-patterns", "browser", "code-architecture", "color",
    "components", "content", "design-systems", "forms", "frameworks", "images",
    "information-architecture", "internationalization", "layout", "motion",
    "performance", "product", "responsive", "security", "testing", "typography",
    "visual-direction",
)
COVERAGE_ALIASES = {
    "anti-patterns": {"anti-patterns", "anti-slop-integrity"},
    "browser": {"browser", "browsers"},
    "code-architecture": {"code-architecture", "frameworks-code-architecture"},
    "components": {"components", "components-states-forms"},
    "content": {"content", "information-architecture-content"},
    "forms": {"forms", "components-states-forms"},
    "frameworks": {"frameworks", "frameworks-code-architecture"},
    "images": {"images", "images-icons"},
    "information-architecture": {"information-architecture", "information-architecture-content"},
    "product": {"product", "product-requirements"},
    "security": {"security", "security-privacy-trust"},
    "testing": {"testing", "testing-deployment"},
}


def _load_server():
    spec = importlib.util.spec_from_file_location("fte_server_tooling", SERVER_PATH)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load MCP server module: {SERVER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SERVER = _load_server()


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PLUGIN_ROOT.resolve()))
    except ValueError:
        return str(path.resolve())


def iter_files(root: Path, suffixes: set[str] | None = None) -> Iterable[Path]:
    excluded = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
    if root.is_file():
        yield root
        return
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in excluded for part in path.parts):
            continue
        if suffixes is None or path.suffix.lower() in suffixes:
            yield path


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None


@dataclass
class Report:
    check: str
    passed: bool = True
    errors: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[dict[str, Any]] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def error(self, code: str, message: str, **evidence: Any) -> None:
        self.passed = False
        self.errors.append({"code": code, "message": message, **evidence})

    def warn(self, code: str, message: str, **evidence: Any) -> None:
        self.warnings.append({"code": code, "message": message, **evidence})

    def value(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "check": self.check,
            "passed": self.passed,
            "summary": {"errors": len(self.errors), "warnings": len(self.warnings)},
            "errors": self.errors,
            "warnings": self.warnings,
            "details": self.details,
        }


def report_markdown(value: Mapping[str, Any]) -> str:
    lines = [f"# {str(value.get('check', 'Report')).replace('-', ' ').title()}", ""]
    lines.append(f"**Result:** {'PASS' if value.get('passed') else 'FAIL'}")
    summary = value.get("summary") or {}
    if summary:
        lines.extend(["", f"Errors: {summary.get('errors', 0)} · Warnings: {summary.get('warnings', 0)}"])
    for heading, key in (("Errors", "errors"), ("Warnings", "warnings")):
        items = value.get(key) or []
        if items:
            lines.extend(["", f"## {heading}", ""])
            for item in items:
                location = item.get("file") or item.get("id") or ""
                suffix = f" (`{location}`)" if location else ""
                lines.append(f"- **{item.get('code', key)}**{suffix}: {item.get('message', '')}")
    details = value.get("details") or {}
    lines.extend(["", "## Details", "", "```json", json.dumps(details, indent=2, sort_keys=True, ensure_ascii=False), "```", ""])
    return "\n".join(lines)


def _safe_output(path: Path) -> None:
    resolved = path.resolve()
    knowledge = (PLUGIN_ROOT / "knowledge").resolve()
    if resolved == knowledge or knowledge in resolved.parents:
        raise ValueError("Generated output may not modify canonical knowledge/")


def emit(value: Mapping[str, Any], args: argparse.Namespace) -> int:
    encoded = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    json_out = getattr(args, "json_out", None)
    md_out = getattr(args, "md_out", None)
    dry_run = bool(getattr(args, "dry_run", False))
    writes: list[str] = []
    for output, content in ((json_out, encoded), (md_out, report_markdown(value))):
        if not output:
            continue
        path = Path(output)
        _safe_output(path)
        writes.append(str(path.resolve()))
        if not dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if not json_out:
        sys.stdout.write(encoded)
    elif dry_run:
        sys.stdout.write(json.dumps({"dry_run": True, "would_write": writes, "report": value}, indent=2, sort_keys=True) + "\n")
    return 0 if value.get("passed", True) else 1


def load_json(path: Path, report: Report | None = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        if report:
            report.error("invalid-json", str(exc), file=rel(path))
            return None
        raise


def records() -> tuple[list[Any], dict[str, Any]]:
    return SERVER.load_records(PLUGIN_ROOT / "knowledge")


def validate_plugin(_: argparse.Namespace) -> Report:
    report = Report("plugin-structure-validation")
    manifest = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
    if not manifest.exists():
        report.error("missing-manifest", "Required .codex-plugin/plugin.json is missing.", file=rel(manifest))
        return report
    extras = [path for path in manifest.parent.iterdir() if path.name != "plugin.json"]
    for path in extras:
        report.error("manifest-directory-extra", "Only plugin.json may be stored in .codex-plugin/.", file=rel(path))
    data = load_json(manifest, report)
    if not isinstance(data, Mapping):
        return report
    name = data.get("name")
    if name != PLUGIN_ROOT.name:
        report.error("name-mismatch", "Manifest name must equal the normalized plugin directory name.", expected=PLUGIN_ROOT.name, actual=name)
    version = str(data.get("version") or "")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        report.error("invalid-version", "Manifest version must be semantic version text.", actual=version)
    if "[TODO:" in json.dumps(data) or any(value == "" for value in (name, data.get("description"))):
        report.error("placeholder", "Manifest contains a TODO or empty required metadata.", file=rel(manifest))
    companion_checks = (("mcpServers", ".mcp.json"), ("apps", ".app.json"))
    for field_name, companion in companion_checks:
        if field_name in data and not (PLUGIN_ROOT / companion).exists():
            report.error("missing-companion", f"Manifest declares {field_name} but {companion} is missing.", file=companion)
    report.details = {"manifest": rel(manifest), "name": name, "version": version, "top_level_fields": sorted(data)}
    return report


def _frontmatter(text: str) -> Mapping[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("'\"")
    return result


def validate_skill(_: argparse.Namespace) -> Report:
    report = Report("skill-structure-validation")
    skill_dir = PLUGIN_ROOT / "skills" / "frontend-taste-engineer"
    path = skill_dir / "SKILL.md"
    text = read_text(path)
    if text is None:
        report.error("missing-skill", "Bundled SKILL.md is missing or unreadable.", file=rel(path))
        return report
    metadata = _frontmatter(text)
    if metadata.get("name") != "frontend-taste-engineer":
        report.error("skill-name", "Skill frontmatter name must be frontend-taste-engineer.", actual=metadata.get("name"))
    description = metadata.get("description", "")
    if len(description) < 40:
        report.error("skill-description", "Skill description must say what the skill does and when it triggers.")
    if "[TODO:" in text or "Structuring This Skill" in text:
        report.error("skill-placeholder", "SKILL.md still contains scaffold guidance or TODO placeholders.", file=rel(path))
    line_count = len(text.splitlines())
    if not 160 <= line_count <= 500:
        report.warn("skill-size", "Operating skill should remain compact (target roughly 200–450 lines).", lines=line_count)
    agent = skill_dir / "agents" / "openai.yaml"
    if not agent.exists():
        report.warn("missing-agent-metadata", "agents/openai.yaml is absent.", file=rel(agent))
    report.details = {"path": rel(path), "lines": line_count, "description_length": len(description)}
    return report


def check_links(args: argparse.Namespace) -> Report:
    root = Path(args.target).resolve() if args.target else PLUGIN_ROOT
    report = Report("broken-link-detection")
    checked = 0
    external: set[str] = set()
    anchors: dict[Path, set[str]] = {}
    for path in iter_files(root, {".md"}):
        text = read_text(path)
        if text is None:
            continue
        anchors[path] = {SERVER._slug(match.group(1)) for match in re.finditer(r"^#{1,6}\s+(.+)$", text, re.MULTILINE)}
    for path in iter_files(root, {".md", ".json", ".yml", ".yaml", ".toml"}):
        text = read_text(path)
        if text is None:
            continue
        links = []
        if path.suffix == ".md":
            links.extend((m.group(1) or m.group(2) or "").strip().strip("<>") for m in LINK_RE.finditer(text))
        links.extend(URL_RE.findall(text))
        for target in sorted(set(links)):
            if target.startswith(("http://", "https://")):
                external.add(target)
                continue
            if target.startswith(("#", "mailto:", "codex:", "app:")):
                continue
            checked += 1
            clean, _, fragment = target.partition("#")
            clean = clean.split("?", 1)[0]
            destination = (path.parent / clean).resolve() if clean else path.resolve()
            if not destination.exists():
                report.error("broken-local-link", "Referenced local path does not exist.", file=rel(path), target=target)
            elif fragment and destination.suffix == ".md":
                available = anchors.get(destination)
                if available is None:
                    dest_text = read_text(destination) or ""
                    available = {SERVER._slug(m.group(1)) for m in re.finditer(r"^#{1,6}\s+(.+)$", dest_text, re.MULTILINE)}
                if SERVER._slug(fragment) not in available:
                    report.error("broken-anchor", "Markdown anchor does not exist.", file=rel(path), target=target)
    report.details = {"root": str(root), "local_links_checked": checked, "external_links_not_fetched": len(external), "network_used": False}
    return report


def validate_refs(_: argparse.Namespace) -> Report:
    report = Report("internal-reference-validation")
    corpus, info = records()
    ids = {item.id for item in corpus}
    broken: list[dict[str, str]] = []
    for item in corpus:
        for target in item.related_rules:
            if target not in ids:
                broken.append({"id": item.id, "target": target})
    for item in broken:
        report.error("missing-related-rule", "related_rules references an unknown record ID.", **item)
    report.details = {"record_count": len(corpus), "references_checked": sum(len(item.related_rules) for item in corpus), "parse_errors": info["parse_errors"]}
    if info["parse_errors"]:
        report.error("corpus-parse", "One or more canonical JSON files could not be parsed.", count=len(info["parse_errors"]))
    return report


def check_freshness(args: argparse.Namespace) -> Report:
    report = Report("source-freshness-check")
    corpus, _ = records()
    maximum = int(args.max_age_days)
    stale = 0
    unknown = 0
    for item in corpus:
        if not item.last_reviewed:
            unknown += 1
            report.warn("missing-review-date", "Record has no last_reviewed date.", id=item.id)
            continue
        try:
            reviewed = dt.date.fromisoformat(item.last_reviewed[:10])
        except ValueError:
            report.error("invalid-review-date", "last_reviewed is not ISO YYYY-MM-DD.", id=item.id, value=item.last_reviewed)
            continue
        age = (TODAY - reviewed).days
        if age > maximum:
            stale += 1
            report.warn("stale-record", "Record exceeds the configured review age.", id=item.id, age_days=age, max_age_days=maximum)
    registry_path = PLUGIN_ROOT / "research" / "source-registry.yml"
    registry_text = read_text(registry_path) or ""
    source_ids = re.findall(r"^\s+- id:\s*([^\s#]+)", registry_text, re.MULTILINE)
    upstream = [
        {"source_id": source_id.strip("'\""), "status": "unknown-offline"}
        for source_id in source_ids
    ]
    if not source_ids:
        report.warn("source-registry-unavailable", "No parseable source IDs were found; upstream freshness is unknown offline.", file=rel(registry_path))
    report.details = {"record_count": len(corpus), "stale": stale, "unknown": unknown, "max_age_days": maximum, "as_of": TODAY.isoformat(), "network_used": False, "upstream_source_status": upstream, "upstream_note": "No remote request was made; current upstream revisions and license changes remain unknown until an explicitly authorized network audit."}
    return report


def validate_provenance(_: argparse.Namespace) -> Report:
    report = Report("provenance-validation")
    corpus, info = records()
    for item in corpus:
        if not item.sources:
            report.error("missing-source", "Meaningful guidance must identify at least one source.", id=item.id)
        if not item.license_status or item.license_status == "unknown":
            report.error("missing-license-status", "Record must identify its license/adaptation status.", id=item.id)
        if not item.rationale:
            report.warn("missing-rationale", "Record has no rationale.", id=item.id)
    report.details = {"record_count": len(corpus), "source_file_count": len(info["source_files"]), "fallback": info["fallback"]}
    return report


def _jaccard(a: set[str], b: set[str]) -> float:
    union = a | b
    return len(a & b) / len(union) if union else 1.0


def detect_duplicates(args: argparse.Namespace) -> Report:
    report = Report("duplicate-rule-detection")
    corpus, _ = records()
    threshold = float(args.threshold)
    pairs = []
    for idx, left in enumerate(corpus):
        a = set(SERVER.tokenize(left.principle))
        for right in corpus[idx + 1:]:
            b = set(SERVER.tokenize(right.principle))
            similarity = _jaccard(a, b)
            if similarity >= threshold:
                pairs.append({"left": left.id, "right": right.id, "similarity": round(similarity, 3), "exact": left.fingerprint == right.fingerprint})
    for pair in pairs:
        method = report.error if pair["exact"] else report.warn
        method("duplicate-rule", "Rules have highly overlapping principles; review for merge or explicit distinction.", **pair)
    report.details = {"record_count": len(corpus), "threshold": threshold, "candidate_pairs": len(pairs)}
    return report


NEGATIONS = {"not", "never", "avoid", "without", "no", "forbid", "prohibit", "mustn't", "don't"}


def detect_contradictions(args: argparse.Namespace) -> Report:
    report = Report("contradiction-heuristic")
    corpus, _ = records()
    threshold = float(args.threshold)
    candidates = []
    for idx, left in enumerate(corpus):
        left_terms = set(SERVER.tokenize(left.principle))
        left_neg = bool(left_terms & NEGATIONS)
        for right in corpus[idx + 1:]:
            if left.topic != right.topic:
                continue
            right_terms = set(SERVER.tokenize(right.principle))
            overlap = _jaccard(left_terms - NEGATIONS, right_terms - NEGATIONS)
            polarity_diff = left_neg != bool(right_terms & NEGATIONS)
            if polarity_diff and overlap >= threshold:
                candidates.append({"left": left.id, "right": right.id, "lexical_overlap": round(overlap, 3), "topic": left.topic})
    for item in candidates:
        report.warn("possible-contradiction", "Opposite polarity appears in highly overlapping rules; human context review is required.", **item)
    report.details = {"record_count": len(corpus), "threshold": threshold, "candidate_pairs": len(candidates), "heuristic_only": True}
    return report


def coverage_report(_: argparse.Namespace) -> Report:
    report = Report("knowledge-coverage-report")
    corpus, _ = records()
    counts: dict[str, int] = {}
    mandatory: dict[str, int] = {}
    for item in corpus:
        counts[item.topic] = counts.get(item.topic, 0) + 1
        if item.importance == "mandatory":
            mandatory[item.topic] = mandatory.get(item.topic, 0) + 1
    conceptual_counts = {
        topic: sum(counts.get(alias, 0) for alias in COVERAGE_ALIASES.get(topic, {topic}))
        for topic in EXPECTED_TOPICS
    }
    gaps = [topic for topic, count in conceptual_counts.items() if count == 0]
    for topic in gaps:
        report.warn("coverage-gap", "No canonical records were found for an expected lifecycle topic.", topic=topic)
    report.details = {"record_count": len(corpus), "topic_counts": dict(sorted(counts.items())), "conceptual_topic_counts": conceptual_counts, "mandatory_counts": dict(sorted(mandatory.items())), "expected_topics": list(EXPECTED_TOPICS), "gaps": gaps, "coverage_ratio": round((len(EXPECTED_TOPICS) - len(gaps)) / len(EXPECTED_TOPICS), 3)}
    return report


DEPTH_FIELDS = ("principle", "rationale", "implementation", "verification", "sources", "exceptions")


def knowledge_depth(args: argparse.Namespace) -> Report:
    report = Report("knowledge-depth-audit")
    corpus, _ = records()
    minimum = float(args.minimum_score)
    rows = []
    for item in corpus:
        values = {
            "principle": item.principle,
            "rationale": item.rationale,
            "implementation": item.implementation,
            "verification": item.verification,
            "sources": item.sources,
            "exceptions": item.exceptions,
        }
        present = [key for key, value in values.items() if value]
        score = len(present) / len(DEPTH_FIELDS)
        row = {"id": item.id, "score": round(score, 3), "missing": [key for key in DEPTH_FIELDS if key not in present]}
        rows.append(row)
        if score < minimum:
            report.warn("shallow-record", "Record lacks enough decision, exception, verification, or provenance depth.", **row)
    report.details = {"record_count": len(corpus), "minimum_score": minimum, "average_score": round(sum(row["score"] for row in rows) / max(1, len(rows)), 3), "records": rows}
    return report


def build_index(args: argparse.Namespace) -> Report:
    report = Report("knowledge-index-generation")
    corpus, info = records()
    entries = []
    for item in corpus:
        entries.append({
            "id": item.id,
            "title": item.title,
            "topic": item.topic,
            "subtopic": item.subtopic,
            "status": item.status,
            "importance": item.importance,
            "task_types": list(item.task_types),
            "components": list(item.components),
            "frameworks": list(item.frameworks),
            "sources": list(item.sources),
            "origin": item.origin,
            "fingerprint": item.fingerprint,
        })
    payload = {
        "schema_version": 1,
        "generator": "scripts/generate_index.py",
        "record_count": len(entries),
        "corpus_fingerprint": hashlib.sha256(json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "records": entries,
    }
    destination = Path(args.output or (PLUGIN_ROOT / "ingestion" / "knowledge-index.json"))
    _safe_output(destination)
    if not args.dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report.details = {"destination": str(destination.resolve()), "dry_run": args.dry_run, "record_count": len(entries), "corpus_fingerprint": payload["corpus_fingerprint"], "parse_errors": info["parse_errors"]}
    if info["parse_errors"]:
        report.error("corpus-parse", "Index is incomplete because canonical files failed to parse.", count=len(info["parse_errors"]))
    return report


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def frontend_audit(args: argparse.Namespace) -> Report:
    root = Path(args.target).resolve()
    report = Report("frontend-static-audit")
    files = list(iter_files(root, {".html", ".htm", ".css", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro"}))
    checks = (
        ("dead-link", "high", re.compile(r"(?:href=[\"']#(?:[\"'])|href=[\"']javascript:void\(0\))", re.I), "Replace placeholder navigation with a real destination or non-link control."),
        ("placeholder-copy", "high", re.compile(r"\b(?:lorem ipsum|todo:? copy|placeholder text|your company)\b", re.I), "Use product-specific content and identify unresolved copy explicitly."),
        ("fake-metric", "high", re.compile(r"\b(?:99\.9%|10k\+|trusted by thousands|industry-leading)\b", re.I), "Source the claim or remove it; do not fabricate product evidence."),
        ("focus-suppression", "critical", re.compile(r"(?:outline\s*:\s*(?:none|0)|focus[^\{]*\{[^}]*outline\s*:\s*(?:none|0))", re.I | re.S), "Provide a visible focus treatment with sufficient contrast."),
        ("transition-all", "medium", re.compile(r"transition(?:-property)?\s*:\s*all\b", re.I), "List the properties that should transition to avoid accidental layout or color animation."),
        ("viewport-lock", "medium", re.compile(r"(?:height|min-height)\s*:\s*100vh\b", re.I), "Account for dynamic mobile viewport units and short content/viewport behavior."),
        ("purple-gradient-reflex", "low", re.compile(r"(?:linear|radial)-gradient\([^)]*(?:purple|#(?:7c3aed|8b5cf6|a855f7))", re.I), "Verify the gradient follows the product design thesis rather than a default aesthetic."),
        ("pill-proliferation", "low", re.compile(r"border-radius\s*:\s*(?:9999?px|50rem|100%)", re.I), "Reserve pill geometry for controls or compact labels whose shape communicates a purpose."),
    )
    findings = []
    for path in files:
        text = read_text(path) or ""
        for check_id, severity, pattern, correction in checks:
            for match in list(pattern.finditer(text))[:10]:
                finding = {"id": check_id, "severity": severity, "file": str(path), "line": _line_number(text, match.start()), "evidence": hashlib.sha256(match.group(0).encode()).hexdigest()[:12], "correction": correction, "classification": "defect" if severity in {"critical", "high"} else "review"}
                findings.append(finding)
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    findings.sort(key=lambda item: (order[item["severity"]], item["file"], item["line"], item["id"]))
    for finding in findings:
        method = report.error if finding["severity"] == "critical" else report.warn
        method(finding["id"], finding["correction"], **{k: v for k, v in finding.items() if k not in {"id", "correction"}})
    report.details = {"target": str(root), "files_scanned": len(files), "finding_count": len(findings), "findings": findings, "limitations": ["Static heuristics do not replace browser, keyboard, assistive-technology, or design review.", "Evidence hashes avoid echoing possible sensitive source text."]}
    return report


def accessibility_audit(args: argparse.Namespace) -> Report:
    root = Path(args.target).resolve()
    report = Report("accessibility-static-check")
    files = list(iter_files(root, {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro", ".css"}))
    patterns = (
        ("image-alt", re.compile(r"<img\b(?![^>]*\balt\s*=)[^>]*>", re.I), "Images need an alt decision: useful text or alt=\"\" when decorative."),
        ("unnamed-button", re.compile(r"<button\b[^>]*>\s*(?:<[^>]+>\s*)*</button>", re.I | re.S), "Buttons require a persistent accessible name."),
        ("div-click", re.compile(r"<(?:div|span)\b[^>]*(?:onClick|@click|onclick)\s*=", re.I), "Use a native button/link or fully implement semantics and keyboard behavior."),
        ("positive-tabindex", re.compile(r"tabindex\s*=\s*[\"']?[1-9]", re.I), "Avoid positive tabindex; preserve a logical DOM order."),
        ("autofocus", re.compile(r"\bautofocus\b", re.I), "Verify autofocus does not steal context, scroll, or open a mobile keyboard unexpectedly."),
        ("focus-hidden", re.compile(r"outline\s*:\s*(?:none|0)", re.I), "Do not suppress focus without an equivalent visible treatment."),
    )
    count = 0
    for path in files:
        text = read_text(path) or ""
        for code, pattern, message in patterns:
            for match in list(pattern.finditer(text))[:20]:
                count += 1
                report.warn(code, message, file=str(path), line=_line_number(text, match.start()))
    report.details = {"target": str(root), "files_scanned": len(files), "candidate_findings": count, "network_used": False, "automated_runtime_audit": False, "required_manual_checks": ["keyboard primary flow", "visible focus", "accessible names and roles", "error announcement and focus", "200% zoom and reflow", "reduced motion", "screen-reader spot check"]}
    return report


def performance_audit(args: argparse.Namespace) -> Report:
    root = Path(args.target).resolve()
    report = Report("performance-static-check")
    assets = []
    total = 0
    for path in iter_files(root):
        try:
            size = path.stat().st_size
        except OSError:
            continue
        total += size
        if size >= int(args.large_asset_bytes):
            item = {"file": str(path), "bytes": size}
            assets.append(item)
            report.warn("large-asset", "Large asset requires delivery, compression, and loading-priority review.", **item)
    missing_image_dimensions = 0
    for path in iter_files(root, {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro"}):
        text = read_text(path) or ""
        for match in re.finditer(r"<img\b[^>]*>", text, re.I):
            tag = match.group(0).lower()
            if "width=" not in tag or "height=" not in tag:
                missing_image_dimensions += 1
                report.warn("image-dimensions", "Image lacks explicit width/height evidence; verify layout-shift prevention.", file=str(path), line=_line_number(text, match.start()))
    report.details = {"target": str(root), "total_bytes_scanned": total, "large_assets": assets, "images_without_both_dimensions": missing_image_dimensions, "runtime_measurement": False, "network_used": False, "next_step": "Measure the built product with the project's pinned browser/performance tooling."}
    return report


def responsive_capture(args: argparse.Namespace) -> Report:
    report = Report("responsive-screenshot-capture")
    viewports = []
    for value in args.viewport:
        match = re.fullmatch(r"(\d+)x(\d+)", value)
        if not match:
            report.error("invalid-viewport", "Viewport must use WIDTHxHEIGHT.", value=value)
            continue
        viewports.append((int(match.group(1)), int(match.group(2))))
    browser = next((shutil.which(name) for name in ("chromium", "chromium-browser", "google-chrome", "Google Chrome") if shutil.which(name)), None)
    url = str(args.url)
    local = url.startswith(("http://127.0.0.1", "http://localhost", "file://"))
    if not local and not args.allow_network:
        report.error("network-disabled", "Only localhost or file:// URLs are allowed without --allow-network.", url=url)
    output = Path(args.output_dir).resolve()
    captures = []
    for width, height in viewports:
        target = output / f"{width}x{height}.png"
        command = [browser or "<chromium-not-found>", "--headless", "--hide-scrollbars", "--disable-gpu", f"--window-size={width},{height}", f"--screenshot={target}", url]
        row = {"viewport": f"{width}x{height}", "output": str(target), "command": command, "status": "planned"}
        if args.execute and not args.dry_run and browser and report.passed:
            output.mkdir(parents=True, exist_ok=True)
            completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=int(args.timeout), check=False)
            row["status"] = "captured" if completed.returncode == 0 and target.exists() else "failed"
            row["returncode"] = completed.returncode
            if row["status"] == "failed":
                report.error("capture-failed", "Headless browser screenshot failed.", viewport=row["viewport"], returncode=completed.returncode, stderr=completed.stderr[-500:])
        elif args.execute and not browser:
            row["status"] = "skipped"
            report.warn("browser-unavailable", "No supported Chromium executable was found; no dependency was downloaded.")
        captures.append(row)
    report.details = {"url": url, "captures": captures, "dry_run": args.dry_run, "execute": args.execute, "network_allowed": bool(args.allow_network), "browser": browser}
    return report


def secret_scan(args: argparse.Namespace) -> Report:
    root = Path(args.target).resolve()
    report = Report("secret-scan")
    scanned = 0
    matches = 0
    for path in iter_files(root, SOURCE_SUFFIXES | {".env", ".txt"}):
        text = read_text(path)
        if text is None or len(text) > int(args.max_file_bytes):
            continue
        scanned += 1
        for name, pattern in SECRET_PATTERNS.items():
            for match in pattern.finditer(text):
                matches += 1
                report.error(name, "Potential secret material found; value suppressed. Review before packaging or commit.", file=str(path), line=_line_number(text, match.start()), fingerprint=hashlib.sha256(match.group(0).encode()).hexdigest()[:12])
    report.details = {"target": str(root), "files_scanned": scanned, "matches": matches, "values_suppressed": True}
    return report


def license_report(_: argparse.Namespace) -> Report:
    report = Report("license-report")
    license_files = [
        rel(path) for path in iter_files(PLUGIN_ROOT)
        if path.name.lower() in {"license", "license.md", "license.txt", "copying", "copying.md", "notice", "notice.md", "notice.txt"}
    ]
    corpus, _ = records()
    statuses: dict[str, int] = {}
    for item in corpus:
        statuses[item.license_status] = statuses.get(item.license_status, 0) + 1
        if item.license_status in {"", "unknown"}:
            report.error("unknown-record-license", "Knowledge record has unresolved license status.", id=item.id)
    dependencies = []
    for name in ("package.json", "requirements.txt", "pyproject.toml", "Cargo.toml"):
        for path in sorted(PLUGIN_ROOT.rglob(name)):
            if any(part in {"node_modules", ".git", ".venv"} for part in path.parts):
                continue
            dependencies.append(rel(path))
    report.details = {"root_license_files": license_files, "record_license_status_counts": dict(sorted(statuses.items())), "dependency_manifests": dependencies, "runtime_dependency_claim": "MCP and deterministic tooling use Python standard library only.", "network_used": False}
    if not license_files:
        report.error("missing-license", "No repository/plugin license file was found.")
    return report


PACKAGE_EXCLUDES = {".git", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache", ".DS_Store", "dist", "build"}


def _zip_entries(root: Path, *, skill_only: bool) -> list[Path]:
    entries = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in PACKAGE_EXCLUDES for part in path.relative_to(root).parts):
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        if not skill_only and "results" in path.relative_to(root).parts:
            continue
        entries.append(path)
    return entries


def _deterministic_zip(root: Path, destination: Path, entries: Sequence[Path], dry_run: bool) -> tuple[int, str]:
    digest = hashlib.sha256()
    for path in entries:
        archive = str(path.relative_to(root)).replace(os.sep, "/")
        digest.update(archive.encode() + b"\0" + path.read_bytes())
    if not dry_run:
        _safe_output(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive_file:
            for path in entries:
                archive = str(path.relative_to(root)).replace(os.sep, "/")
                info = zipfile.ZipInfo(archive, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o755 if os.access(path, os.X_OK) else 0o644) << 16
                archive_file.writestr(info, path.read_bytes())
    return len(entries), digest.hexdigest()


def package_skill(args: argparse.Namespace) -> Report:
    report = Report("skill-package")
    root = PLUGIN_ROOT / "skills" / "frontend-taste-engineer"
    destination = Path(args.output or (PLUGIN_ROOT / "dist" / "skill.zip"))
    entries = _zip_entries(root, skill_only=True)
    count, digest = _deterministic_zip(root, destination, entries, args.dry_run)
    if not (root / "SKILL.md").exists():
        report.error("missing-skill", "Cannot package without SKILL.md.", file=rel(root / "SKILL.md"))
    report.details = {"source": str(root), "output": str(destination.resolve()), "dry_run": args.dry_run, "files": count, "content_sha256": digest, "entries": [str(path.relative_to(root)) for path in entries]}
    return report


def package_plugin(args: argparse.Namespace) -> Report:
    report = Report("plugin-package")
    destination = Path(args.output or (PLUGIN_ROOT / "dist" / "frontend-taste-engineer-plugin-0.1.0.zip"))
    entries = _zip_entries(PLUGIN_ROOT, skill_only=False)
    count, digest = _deterministic_zip(PLUGIN_ROOT, destination, entries, args.dry_run)
    if not (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").exists():
        report.error("missing-manifest", "Cannot package without .codex-plugin/plugin.json.")
    report.details = {"source": str(PLUGIN_ROOT), "output": str(destination.resolve()), "dry_run": args.dry_run, "files": count, "content_sha256": digest}
    return report


CHECK_FUNCTIONS: tuple[Callable[[argparse.Namespace], Report], ...] = (
    validate_plugin, validate_skill, check_links, validate_refs, validate_provenance,
    detect_duplicates, detect_contradictions, coverage_report, knowledge_depth, secret_scan, license_report,
)


def validate_all(args: argparse.Namespace) -> Report:
    report = Report("complete-deterministic-validation")
    defaults = argparse.Namespace(
        target=str(PLUGIN_ROOT), threshold=0.78, minimum_score=0.66,
        max_file_bytes=2_000_000, max_age_days=370,
    )
    checks = []
    for function in CHECK_FUNCTIONS:
        result = function(defaults)
        value = result.value()
        checks.append(value)
        if not result.passed:
            report.error("subcheck-failed", f"{result.check} failed.", check=result.check, errors=len(result.errors))
        for warning in result.warnings:
            report.warnings.append({"code": "subcheck-warning", "message": f"{result.check}: {warning['message']}", "check": result.check})
    self_check = subprocess.run([sys.executable, str(SERVER_PATH), "--self-check"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if self_check.returncode != 0:
        report.error("mcp-self-check", "MCP server self-check failed.", stderr=self_check.stderr[-500:])
    report.details = {"checks": checks, "mcp_self_check": json.loads(self_check.stdout) if self_check.returncode == 0 else {"returncode": self_check.returncode}}
    return report


def add_report_options(parser: argparse.ArgumentParser, *, writes: bool = False) -> None:
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--md-out", type=Path)
    if writes:
        parser.add_argument("--dry-run", action="store_true")


def make_parser(default_command: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=default_command is None)

    def command(name: str, help_text: str, function: Callable[[argparse.Namespace], Report], *, writes: bool = False) -> argparse.ArgumentParser:
        p = sub.add_parser(name, help=help_text)
        p.set_defaults(function=function)
        add_report_options(p, writes=writes)
        return p

    command("validate-plugin", "Validate plugin structure and metadata.", validate_plugin)
    command("validate-skill", "Validate bundled skill structure.", validate_skill)
    p = command("check-links", "Check local links and inventory external URLs without fetching them.", check_links)
    p.add_argument("--target", default=str(PLUGIN_ROOT))
    command("validate-refs", "Validate related-rule references.", validate_refs)
    p = command("check-freshness", "Check record review dates without network access.", check_freshness)
    p.add_argument("--max-age-days", type=int, default=370)
    command("validate-provenance", "Validate source and license metadata.", validate_provenance)
    p = command("duplicates", "Find exact and near-duplicate principles.", detect_duplicates)
    p.add_argument("--threshold", type=float, default=0.78)
    p = command("contradictions", "Flag high-overlap rules with opposite polarity.", detect_contradictions)
    p.add_argument("--threshold", type=float, default=0.55)
    command("coverage", "Report topic coverage and gaps.", coverage_report)
    p = command("depth", "Audit record decision and verification depth.", knowledge_depth)
    p.add_argument("--minimum-score", type=float, default=0.66)
    p = command("index", "Generate a deterministic retrieval index outside knowledge/.", build_index, writes=True)
    p.add_argument("--output", type=Path)
    p = command("frontend-audit", "Run static frontend integrity and anti-slop heuristics.", frontend_audit)
    p.add_argument("target")
    p = command("accessibility", "Run dependency-free static accessibility checks.", accessibility_audit)
    p.add_argument("target")
    p = command("performance", "Run dependency-free static performance checks.", performance_audit)
    p.add_argument("target")
    p.add_argument("--large-asset-bytes", type=int, default=500_000)
    p = command("responsive-capture", "Plan or optionally run local Chromium responsive captures.", responsive_capture, writes=True)
    p.add_argument("url")
    p.add_argument("--viewport", action="append", default=["375x812", "768x1024", "1440x1000"])
    p.add_argument("--output-dir", type=Path, default=PLUGIN_ROOT / "audits" / "screenshots")
    p.add_argument("--execute", action="store_true")
    p.add_argument("--allow-network", action="store_true")
    p.add_argument("--timeout", type=int, default=30)
    p = command("secret-scan", "Scan text files for likely secrets without printing values.", secret_scan)
    p.add_argument("--target", default=str(PLUGIN_ROOT))
    p.add_argument("--max-file-bytes", type=int, default=2_000_000)
    command("licenses", "Inventory license evidence and dependency manifests.", license_report)
    p = command("package-skill", "Create a deterministic standalone skill.zip.", package_skill, writes=True)
    p.add_argument("--output", type=Path)
    p = command("package-plugin", "Create a deterministic plugin ZIP.", package_plugin, writes=True)
    p.add_argument("--output", type=Path)
    command("validate-all", "Run all read-only deterministic validation checks.", validate_all)
    if default_command:
        parser.set_defaults(_default_command=default_command)
    return parser


def main(argv: Sequence[str] | None = None, default_command: str | None = None) -> int:
    actual = list(argv if argv is not None else sys.argv[1:])
    if default_command:
        actual.insert(0, default_command)
    parser = make_parser(default_command)
    args = parser.parse_args(actual)
    try:
        result = args.function(args)
        return emit(result.value(), args)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        failure = Report(getattr(args, "command", default_command or "tool"), passed=False)
        failure.error("tool-failure", str(exc))
        return emit(failure.value(), args)


if __name__ == "__main__":
    raise SystemExit(main())
