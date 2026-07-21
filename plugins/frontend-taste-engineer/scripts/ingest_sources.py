#!/usr/bin/env python3
"""Create a reviewable ingestion queue and report without promoting knowledge."""

from __future__ import annotations

import argparse
from pathlib import Path

from source_pipeline import INGESTION_ROOT, fingerprint, load_registry, now, validate_registry, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", action="append", default=[], help="Limit the queue to one or more source IDs")
    parser.add_argument("--out", type=Path, default=INGESTION_ROOT / "reports" / "ingestion.json")
    args = parser.parse_args()
    registry = load_registry()
    errors = validate_registry(registry)
    if errors:
        for error in errors:
            print(error)
        return 1
    wanted = set(args.source)
    selected = []
    for source in registry["sources"]:
        should_queue = bool(
            source.get("ingestion_status") in {"queued", "failed"}
            or source.get("stability") == "stale"
            or source.get("manual_approval") and source.get("ingestion_status") in {"partially-ingested", "inaccessible"}
            or source.get("id") in wanted
        )
        if wanted and source.get("id") not in wanted:
            should_queue = False
        if should_queue:
            selected.append(source)
    results = [{
        "source_id": source["id"],
        "event": "manual-reingestion-request" if source["id"] in wanted else "review-current-ingestion-state",
        "status": source["ingestion_status"],
        "accessible_revision": source["accessible_revision"],
        "evidence_consulted": source["files_or_sections_consulted"],
        "next_action": "review candidate evidence; do not promote automatically",
    } for source in selected]
    report = {
        "schema_version": 1,
        "generated_at": now(),
        "registry_fingerprint": fingerprint(registry),
        "selected_sources": [source["id"] for source in selected],
        "results": results,
        "promotion_behavior": "candidate-only; human-reviewed promotion required",
    }
    write_json(args.out, report)
    write_json(INGESTION_ROOT / "queues" / "current.json", {"schema_version": 1, "generated_at": report["generated_at"], "events": results})
    print(f"queued={len(selected)} report={args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
