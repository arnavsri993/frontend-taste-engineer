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
REQUIRED_SOURCE_FIELDS = (
    "id", "name", "author_or_organization", "canonical_url", "supplied_url",
    "source_type", "classification", "license", "accessible_revision",
    "last_checked_revision", "topics_contributed", "files_or_sections_consulted",
    "reliability_assessment", "maintenance_status",
    "copying_or_adaptation_restrictions", "related_sources", "notes",
)
REQUIRED_SOURCE_DIMENSIONS = (
    "manual_approval", "ingestion_status", "authority", "stability", "allowed_use", "license_status",
)
SOURCE_CLASSIFICATIONS = {
    "core", "specialized", "experimental", "inspiration-only",
    "inaccessible", "unresolved", "rejected",
}
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


def _load_source_pipeline():
    path = PLUGIN_ROOT / "scripts" / "source_pipeline.py"
    spec = importlib.util.spec_from_file_location("fte_source_pipeline_tooling", path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load source pipeline module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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
    registry_path = PLUGIN_ROOT / "research" / "source-registry.json"
    registry_value = load_json(registry_path, report)
    source_ids = [
        str(item.get("id"))
        for item in (registry_value.get("sources") if isinstance(registry_value, Mapping) else []) or []
        if isinstance(item, Mapping) and item.get("id")
    ]
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


def _registry_source_entries(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, Mapping) or not isinstance(value.get("sources"), list):
        return []
    return [dict(item) for item in value["sources"] if isinstance(item, Mapping)]


def _effective_seed_entries(value: Mapping[str, Any], report: Report) -> list[dict[str, Any]]:
    defaults = dict(value.get("entry_defaults") or {})
    entries: list[dict[str, Any]] = []
    for category in value.get("categories") or []:
        if not isinstance(category, Mapping):
            report.error("invalid-seed-category", "Every seed category must be an object.")
            continue
        category_id = str(category.get("id") or "")
        category_defaults = dict(category.get("defaults") or {})
        for source in category.get("sources") or []:
            if not isinstance(source, Mapping):
                report.error("invalid-seed-source", "Every seed source must be an object.", category=category_id)
                continue
            entries.append({**defaults, **category_defaults, **source, "category": category_id})
    return entries


def validate_source_catalogs(_: argparse.Namespace) -> Report:
    report = Report("external-source-catalog-validation")
    registry_path = PLUGIN_ROOT / "research" / "source-registry.json"
    registry_value = load_json(registry_path, report)
    registry = _registry_source_entries(registry_value)
    registry_ids: set[str] = set()
    registry_urls: set[str] = set()
    for entry in registry:
        source_id = entry.get("id", "")
        missing = [field for field in REQUIRED_SOURCE_FIELDS if field not in entry]
        if missing:
            report.error("registry-source-fields", "Registry source lacks required fields.", id=source_id, missing=missing)
        missing_dimensions = [field for field in REQUIRED_SOURCE_DIMENSIONS if field not in entry]
        if missing_dimensions:
            report.error("registry-source-dimensions", "Registry source lacks separated approval, ingestion, authority, stability, allowed-use, or license dimensions.", id=source_id, missing=missing_dimensions)
        if source_id in registry_ids:
            report.error("duplicate-registry-id", "Registry source ID is duplicated.", id=source_id)
        registry_ids.add(source_id)
        canonical_url = entry.get("canonical_url", "")
        if canonical_url in registry_urls:
            report.error("duplicate-registry-url", "Registry canonical URL is duplicated.", id=source_id, canonical_url=canonical_url)
        registry_urls.add(canonical_url)
        classification = entry.get("classification")
        if classification not in SOURCE_CLASSIFICATIONS:
            report.error("registry-classification", "Registry source has an invalid classification.", id=source_id, classification=classification)
        if classification == "core":
            authority = f"{entry.get('author_or_organization', '')} {entry.get('source_type', '')}".lower()
            allowed = ("standard", "platform", "w3c", "whatwg", "mozilla", "chrome team", "browser-vendor")
            if not any(term in authority for term in allowed):
                report.error("core-authority", "Core is reserved for authoritative standards and platform documentation.", id=source_id)
        for field_name in ("canonical_url", "supplied_url"):
            if not re.fullmatch(r"https?://\S+", entry.get(field_name, "")):
                report.error("registry-url", "Registry URL must be absolute HTTP(S).", id=source_id, field=field_name)

    discovery_root = PLUGIN_ROOT / "research" / "source-discovery"
    seed_path = discovery_root / "seed-catalog.json"
    query_path = discovery_root / "discovery-queries.json"
    seed = load_json(seed_path, report)
    queries = load_json(query_path, report)
    seed_entries = _effective_seed_entries(seed, report) if isinstance(seed, Mapping) else []
    seed_ids: set[str] = set()
    seed_urls: set[str] = set()
    classification_counts: dict[str, int] = {}
    for entry in seed_entries:
        source_id = str(entry.get("id") or "")
        missing = [field for field in REQUIRED_SOURCE_FIELDS if field not in entry]
        if missing:
            report.error("seed-source-fields", "Seed source lacks required effective fields after defaults are applied.", id=source_id, missing=missing)
        if source_id in seed_ids:
            report.error("duplicate-seed-id", "Seed source ID is duplicated.", id=source_id)
        seed_ids.add(source_id)
        canonical_url = str(entry.get("canonical_url") or "")
        if canonical_url in seed_urls:
            report.error("duplicate-seed-url", "Seed canonical URL is duplicated.", id=source_id, canonical_url=canonical_url)
        seed_urls.add(canonical_url)
        classification = str(entry.get("classification") or "")
        classification_counts[classification] = classification_counts.get(classification, 0) + 1
        if classification not in SOURCE_CLASSIFICATIONS:
            report.error("seed-classification", "Seed source has an invalid classification.", id=source_id, classification=classification)
        if "openai build week" in f"{entry.get('name', '')} {canonical_url}".lower():
            report.error("prohibited-catalog-source", "OpenAI Build Week cannot be a pullable catalog source.", id=source_id)
    if len(seed_entries) < 245:
        report.error("seed-count", "The seed catalog must retain at least the original 245 request-supplied URLs.", expected_at_least=245, actual=len(seed_entries))
    for required_id in ("awwwards", "mobbin", "page-flows"):
        entry = next((item for item in seed_entries if item.get("id") == required_id), None)
        if not entry or entry.get("classification") != "inspiration-only":
            report.error("inspiration-classification", "Named gallery must remain inspiration-only.", id=required_id)

    if not isinstance(queries, Mapping):
        report.error("query-file", "Discovery query file must be an object.", file=rel(query_path))
        query_count = 0
        negative_count = 0
    else:
        query_count = len(queries.get("query_templates") or [])
        negative_filters = [str(item).lower() for item in queries.get("negative_filters") or []]
        negative_count = len(negative_filters)
        if query_count < 30:
            report.error("query-count", "Discovery requires at least 30 focused monthly query templates.", actual=query_count)
        combined_filters = " ".join(negative_filters)
        for term in ("corporate marketing", "ownership or license", "paid-only", "ignore instructions", "credential", "openai build week"):
            if term not in combined_filters:
                report.error("negative-filter", "Discovery negative filters lack a required exclusion.", term=term)

    required_discovery_files = (
        "seed-catalog.json", "discovery-queries.json", "source-scoring-rubric.md",
        "promotion-policy.md", "candidate-template.json", "rejected-source-template.json",
        "monthly-discovery-workflow.md",
    )
    required_artifact_packs = (
        "mega-component-catalog.md", "animated-react-ui.md", "tailwind-blocks-and-templates.md",
        "accessible-primitives.md", "dashboard-and-data-ui.md", "inspiration-catalogs.md",
        "agent-and-mcp-ui-tools.md", "source-discovery-report.md",
    )
    required_references = (
        "external-source-selection.md", "source-license-gates.md", "autonomous-source-discovery.md",
    )
    for path in [*(discovery_root / name for name in required_discovery_files), *((PLUGIN_ROOT / "research" / "artifact-packs" / name) for name in required_artifact_packs), *((PLUGIN_ROOT / "references" / name) for name in required_references)]:
        if not path.exists():
            report.error("missing-source-artifact", "Required external-source artifact is missing.", file=rel(path))

    for template_name in ("candidate-template.json", "rejected-source-template.json"):
        template_path = discovery_root / template_name
        template = load_json(template_path, report)
        if isinstance(template, Mapping):
            missing = [field for field in REQUIRED_SOURCE_FIELDS if field not in template]
            if missing:
                report.error("source-template-fields", "Source template lacks required fields.", file=rel(template_path), missing=missing)

    discovery_script = PLUGIN_ROOT / "scripts" / "discover_frontend_sources.py"
    command = [sys.executable, str(discovery_script), "--query-file", str(query_path), "--seed-file", str(seed_path), "--out-dir", str(Path(tempfile.gettempdir()) / "fte-source-validation"), "--max-results", "8", "--dry-run", "--as-of", "2026-07-10"]
    first = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    second = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if first.returncode != 0:
        report.error("discovery-dry-run", "Offline discovery dry-run failed.", stderr=first.stderr[-500:])
    elif first.stdout != second.stdout:
        report.error("discovery-nondeterministic", "Offline discovery output changed between identical runs.")
    else:
        try:
            dry_run_report = json.loads(first.stdout)
            if dry_run_report.get("network_used") or dry_run_report.get("stable_knowledge_modified") or dry_run_report.get("written"):
                report.error("discovery-dry-run-safety", "Dry-run must use no network, modify no stable knowledge, and write no files.")
        except json.JSONDecodeError as exc:
            report.error("discovery-dry-run-json", "Dry-run output is not valid JSON.", error=str(exc))

    report.details = {
        "registry_sources": len(registry),
        "seed_sources": len(seed_entries),
        "seed_classifications": dict(sorted(classification_counts.items())),
        "query_templates": query_count,
        "negative_filters": negative_count,
        "dry_run_deterministic": first.returncode == 0 and first.stdout == second.stdout,
        "network_used": False,
        "stable_knowledge_modified": False,
    }
    return report


def validate_source_architecture(_: argparse.Namespace) -> Report:
    report = Report("source-derived-architecture-validation")
    pipeline = _load_source_pipeline()
    try:
        registry = pipeline.load_registry()
        errors = list(pipeline.validate_registry(registry))
        source_records = list(pipeline.iter_source_records())
        errors.extend(pipeline.validate_source_records(source_records, {item["id"] for item in registry["sources"]}))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        report.error("source-pipeline-unreadable", str(exc))
        registry, source_records, errors = {"sources": []}, [], []
    for error in errors:
        report.error("source-pipeline-invalid", error)
    schema_root = PLUGIN_ROOT / "ingestion" / "schemas"
    required_schemas = (
        "source-record.schema.json", "source-derived-record.schema.json", "ingestion-report.schema.json",
        "source-usage.schema.json", "coverage-report.schema.json", "evaluation-manifest.schema.json",
    )
    for name in required_schemas:
        path = schema_root / name
        value = load_json(path, report)
        if isinstance(value, Mapping) and not value.get("$schema"):
            report.error("schema-dialect", "Schema must declare a JSON Schema dialect.", file=rel(path))
    for path in (
        PLUGIN_ROOT / "ingestion" / "compiled" / "source-records.json",
        PLUGIN_ROOT / "ingestion" / "reports" / "ingestion.json",
        PLUGIN_ROOT / "ingestion" / "reports" / "source-coverage.json",
        PLUGIN_ROOT / "ingestion" / "source-usage.json",
        PLUGIN_ROOT / "evals" / "copy" / "grubby-pair-annotations.json",
        PLUGIN_ROOT / "evals" / "results" / "copy.json",
    ):
        if not path.exists():
            report.error("generated-artifact-missing", "Required generated source/copy artifact is missing.", file=rel(path))
        else:
            load_json(path, report)
    annotations = load_json(PLUGIN_ROOT / "evals" / "copy" / "grubby-pair-annotations.json", report)
    pair_count = len(annotations.get("annotations") or []) if isinstance(annotations, Mapping) else 0
    if pair_count != 21:
        report.error("copy-pair-count", "The contrastive copy benchmark must preserve all 21 supplied pairs.", actual=pair_count)
    manifest = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json", report)
    if isinstance(manifest, Mapping) and "apps" in manifest:
        report.error("codex-only-apps", "Codex-only distribution must not declare an Apps SDK surface.")
    for path in (PLUGIN_ROOT / ".app.json", PLUGIN_ROOT / "scripts" / "package_skill.py", PLUGIN_ROOT / "dist" / "frontend-taste-engineer-skill.zip"):
        if path.exists():
            report.error("standalone-surface-present", "Codex-only distribution must not include Apps SDK or standalone Skill packaging.", file=rel(path))
    report.details = {
        "registry_sources": len(registry.get("sources") or []),
        "source_derived_records": len(source_records),
        "copy_pairs": pair_count,
        "codex_plugin_only": True,
    }
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


def _configured_private_terms(args: argparse.Namespace, report: Report) -> tuple[list[str], Path | None]:
    configured = getattr(args, "terms_file", None) or os.environ.get("FTE_PRIVATE_TERMS_FILE")
    if not configured:
        if bool(getattr(args, "require_terms", False)):
            report.error("private-terms-required", "No private-terms file was configured.")
        else:
            report.warn("private-terms-not-configured", "No private terms were configured; the privacy scan inspected no denylisted values.")
        return [], None
    path = Path(configured).expanduser().resolve()
    if not path.exists():
        report.error("private-terms-file-missing", "Configured private-terms file does not exist.", file=str(path))
        return [], path
    text = read_text(path)
    if text is None:
        report.error("private-terms-file-unreadable", "Configured private-terms file is not readable UTF-8 text.", file=str(path))
        return [], path
    terms = list(dict.fromkeys(line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")))
    if not terms:
        report.error("private-terms-empty", "Configured private-terms file contains no scan terms.", file=str(path))
    return terms, path


def _privacy_scan_files(root: Path, terms_path: Path | None) -> Iterable[Path]:
    excluded = {".git", "node_modules", "__pycache__", ".venv", "venv", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    if root.is_file():
        if not terms_path or root.resolve() != terms_path:
            yield root
        return
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in excluded for part in path.parts):
            continue
        if terms_path and path.resolve() == terms_path:
            continue
        yield path


def _private_term_metadata(term: str) -> dict[str, Any]:
    return {"term_fingerprint": hashlib.sha256(term.casefold().encode("utf-8")).hexdigest()[:12], "term_length": len(term)}


def _private_term_pattern(term: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![\w-]){re.escape(term)}(?![\w-])", re.IGNORECASE)


def _scan_private_text(report: Report, text: str, terms: Sequence[str], location: str) -> int:
    count = 0
    for term in terms:
        for match in _private_term_pattern(term).finditer(text):
            count += 1
            report.error(
                "private-term-match",
                "A configured private term appears in output; the value is suppressed.",
                file=location,
                line=text.count("\n", 0, match.start()) + 1,
                **_private_term_metadata(term),
            )
    return count


def _added_diff_text(root: Path, cached: bool) -> str:
    command = ["git", "-C", str(root), "diff", "--no-ext-diff", "--unified=0"]
    if cached:
        command.insert(4, "--cached")
    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if completed.returncode != 0:
        return ""
    return "\n".join(line[1:] for line in completed.stdout.splitlines() if line.startswith("+") and not line.startswith("+++"))


def privacy_scan(args: argparse.Namespace) -> Report:
    report = Report("private-term-privacy-scan")
    root = Path(getattr(args, "target", None) or PLUGIN_ROOT.parents[1]).resolve()
    terms, terms_path = _configured_private_terms(args, report)
    if not terms:
        report.details = {"target": str(root), "configured": bool(terms_path), "term_count": 0, "values_suppressed": True}
        return report
    maximum = int(getattr(args, "max_file_bytes", 5_000_000))
    files_scanned = 0
    archives_scanned = 0
    archive_entries = 0
    matches = 0
    image_files = 0
    for path in _privacy_scan_files(root, terms_path):
        relative = str(path.relative_to(root)) if root in path.parents else str(path)
        for term in terms:
            if _private_term_pattern(term).search(path.name):
                matches += 1
                report.error("private-term-filename", "A configured private term appears in a filename; the value is suppressed.", file=relative, **_private_term_metadata(term))
        if path.suffix.lower() == ".zip":
            archives_scanned += 1
            try:
                with zipfile.ZipFile(path) as archive:
                    for info in archive.infolist():
                        if info.is_dir() or info.file_size > maximum:
                            continue
                        archive_entries += 1
                        for term in terms:
                            if _private_term_pattern(term).search(info.filename):
                                matches += 1
                                report.error("private-term-archive-filename", "A configured private term appears in an archive filename; the value is suppressed.", file=f"{relative}!{info.filename}", **_private_term_metadata(term))
                        content = archive.read(info)
                        if b"\0" not in content[:4096]:
                            matches += _scan_private_text(report, content.decode("utf-8", errors="ignore"), terms, f"{relative}!{info.filename}")
            except (OSError, zipfile.BadZipFile) as exc:
                report.error("privacy-archive-unreadable", "Archive could not be inspected.", file=relative, error_type=exc.__class__.__name__)
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif"}:
            image_files += 1
            continue
        try:
            if path.stat().st_size > maximum:
                continue
            content = path.read_bytes()
        except OSError:
            continue
        if b"\0" in content[:4096]:
            continue
        files_scanned += 1
        matches += _scan_private_text(report, content.decode("utf-8", errors="ignore"), terms, relative)
    if (root / ".git").exists():
        matches += _scan_private_text(report, _added_diff_text(root, False), terms, "pending-diff:unstaged-added-lines")
        matches += _scan_private_text(report, _added_diff_text(root, True), terms, "pending-diff:staged-added-lines")
    report.details = {
        "target": str(root),
        "configured": True,
        "terms_file": str(terms_path) if terms_path else None,
        "term_count": len(terms),
        "term_fingerprints": [_private_term_metadata(term) for term in terms],
        "files_scanned": files_scanned,
        "archives_scanned": archives_scanned,
        "archive_entries_scanned": archive_entries,
        "matches": matches,
        "values_suppressed": True,
        "pending_added_diff_scanned": (root / ".git").exists(),
        "image_files_not_ocr_scanned": image_files,
        "limitation": "Raster images are inventoried but not OCR-scanned; inspect public screenshots visually before release.",
    }
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


def _zip_entries(root: Path) -> list[Path]:
    entries = []
    for path in sorted(root.rglob("*")):
        parts = path.relative_to(root).parts
        if not path.is_file() or any(part in PACKAGE_EXCLUDES for part in parts):
            continue
        if parts[:2] in {("audits", "generated"), ("evals", "artifacts")} or parts[:3] == ("evals", "evidence", "frontend-v1"):
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        if "results" in parts:
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


def package_plugin(args: argparse.Namespace) -> Report:
    report = Report("plugin-package")
    manifest = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
    version = str(manifest.get("version") or "unknown").split("+", 1)[0] if isinstance(manifest, Mapping) else "unknown"
    destination = Path(args.output or (PLUGIN_ROOT / "dist" / f"frontend-taste-engineer-plugin-{version}.zip"))
    entries = _zip_entries(PLUGIN_ROOT)
    count, digest = _deterministic_zip(PLUGIN_ROOT, destination, entries, args.dry_run)
    if not (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").exists():
        report.error("missing-manifest", "Cannot package without .codex-plugin/plugin.json.")
    report.details = {"source": str(PLUGIN_ROOT), "output": str(destination.resolve()), "dry_run": args.dry_run, "files": count, "content_sha256": digest}
    return report


CHECK_FUNCTIONS: tuple[Callable[[argparse.Namespace], Report], ...] = (
    validate_plugin, validate_skill, check_links, validate_refs, validate_provenance, validate_source_catalogs, validate_source_architecture,
    detect_duplicates, detect_contradictions, coverage_report, knowledge_depth, secret_scan, privacy_scan, license_report,
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
    command("validate-sources", "Validate reviewed and candidate external-source catalogs.", validate_source_catalogs)
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
    p = command("privacy-scan", "Scan files, added diffs, evidence, logs, and ZIP archives for locally configured private terms without printing the values.", privacy_scan)
    p.add_argument("--target", default=str(PLUGIN_ROOT.parents[1]))
    p.add_argument("--terms-file", type=Path)
    p.add_argument("--require-terms", action="store_true")
    p.add_argument("--max-file-bytes", type=int, default=5_000_000)
    command("licenses", "Inventory license evidence and dependency manifests.", license_report)
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
