#!/usr/bin/env python3
"""Deterministic helpers for the source-derived knowledge pipeline."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping
from urllib.parse import urlsplit, urlunsplit


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = PLUGIN_ROOT / "research" / "source-registry.json"
SOURCE_DERIVED_ROOT = PLUGIN_ROOT / "knowledge" / "source-derived"
INGESTION_ROOT = PLUGIN_ROOT / "ingestion"

INGESTION_STATUSES = {"queued", "ingested", "partially-ingested", "inaccessible", "failed", "superseded", "rejected"}
AUTHORITIES = {"standard", "platform", "official-documentation", "official-design-system", "maintainer", "practitioner", "community", "commercial-gallery", "unknown"}
STABILITIES = {"stable", "active", "experimental", "stale", "archived", "unknown"}
ALLOWED_USES = {"rules-and-guidance", "implementation-reference", "adaptation-with-license-review", "inspiration-only", "link-only", "blocked"}
RECORD_TYPES = {"visual-observation", "interaction-observation", "implementation-observation", "copy-observation"}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def fingerprint(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def canonical_url(raw: str) -> str:
    parsed = urlsplit(raw.strip())
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        raise ValueError(f"Invalid public URL: {raw!r}")
    if parsed.username or parsed.password:
        raise ValueError("Credentials are prohibited in source URLs")
    host = parsed.hostname.lower().rstrip(".")
    port = f":{parsed.port}" if parsed.port else ""
    path = "/".join(part for part in parsed.path.split("/") if part)
    path = f"/{path}" if path else ""
    return urlunsplit((parsed.scheme.lower(), host + port, path.rstrip("/"), parsed.query, ""))


def load_registry() -> dict[str, Any]:
    value = read_json(REGISTRY_PATH)
    if not isinstance(value, Mapping) or not isinstance(value.get("sources"), list):
        raise ValueError("source-registry.json must contain a sources array")
    return dict(value)


def validate_registry(registry: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    urls: set[str] = set()
    required = {
        "id", "name", "canonical_url", "supplied_url", "source_type", "manual_approval",
        "ingestion_status", "authority", "stability", "allowed_use", "license_status",
        "accessible_revision", "last_checked_revision", "topics_contributed",
        "files_or_sections_consulted", "reliability_assessment", "maintenance_status",
        "copying_or_adaptation_restrictions", "related_sources", "notes",
    }
    for item in registry.get("sources") or []:
        if not isinstance(item, Mapping):
            errors.append("Registry source is not an object")
            continue
        source_id = str(item.get("id") or "")
        missing = sorted(required - set(item))
        if missing:
            errors.append(f"{source_id or '<unknown>'}: missing {', '.join(missing)}")
        if source_id in ids:
            errors.append(f"Duplicate source id: {source_id}")
        ids.add(source_id)
        try:
            url = canonical_url(str(item.get("canonical_url") or ""))
        except ValueError as exc:
            errors.append(f"{source_id}: {exc}")
            url = ""
        if url in urls:
            errors.append(f"Duplicate canonical URL: {url}")
        urls.add(url)
        if item.get("ingestion_status") not in INGESTION_STATUSES:
            errors.append(f"{source_id}: invalid ingestion_status")
        if item.get("authority") not in AUTHORITIES:
            errors.append(f"{source_id}: invalid authority")
        if item.get("stability") not in STABILITIES:
            errors.append(f"{source_id}: invalid stability")
        if item.get("allowed_use") not in ALLOWED_USES:
            errors.append(f"{source_id}: invalid allowed_use")
    return errors


def iter_source_records() -> Iterable[tuple[Path, dict[str, Any]]]:
    for path in sorted(SOURCE_DERIVED_ROOT.glob("*.json")):
        value = read_json(path)
        if not isinstance(value, list):
            raise ValueError(f"{path} must contain an array")
        for item in value:
            if isinstance(item, Mapping):
                yield path, dict(item)


def validate_source_records(records: Iterable[tuple[Path, Mapping[str, Any]]], registry_ids: set[str]) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    required = {"id", "record_type", "source_id", "source_url", "topic", "principle", "observations", "implementation", "exceptions", "verification", "confidence", "allowed_use", "license_status", "last_reviewed"}
    for path, item in records:
        record_id = str(item.get("id") or "")
        missing = sorted(required - set(item))
        if missing:
            errors.append(f"{path.name}:{record_id}: missing {', '.join(missing)}")
        if record_id in ids:
            errors.append(f"Duplicate source-derived record id: {record_id}")
        ids.add(record_id)
        if item.get("source_id") not in registry_ids:
            errors.append(f"{record_id}: unknown source_id {item.get('source_id')}")
        if item.get("record_type") not in RECORD_TYPES:
            errors.append(f"{record_id}: invalid record_type")
        for field in ("observations", "implementation", "exceptions", "verification"):
            if not isinstance(item.get(field), list) or not item.get(field):
                errors.append(f"{record_id}: {field} must be a non-empty array")
    return errors


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
