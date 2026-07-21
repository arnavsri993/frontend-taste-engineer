#!/usr/bin/env python3
"""Generate source coverage and usage reports from canonical reviewed data."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from source_pipeline import INGESTION_ROOT, iter_source_records, load_registry, now, validate_registry, validate_source_records, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coverage-out", type=Path, default=INGESTION_ROOT / "reports" / "source-coverage.json")
    parser.add_argument("--usage-out", type=Path, default=INGESTION_ROOT / "source-usage.json")
    parser.add_argument("--retrieval-results", type=Path, default=INGESTION_ROOT.parent / "evals" / "results" / "retrieval.json")
    args = parser.parse_args()
    registry = load_registry()
    records = list(iter_source_records())
    errors = validate_registry(registry)
    errors.extend(validate_source_records(records, {item["id"] for item in registry["sources"]}))
    if errors:
        for error in errors:
            print(error)
        return 1
    by_source = Counter(item["source_id"] for _, item in records)
    by_category = Counter(item["topic"] for _, item in records)
    statuses = Counter(item["ingestion_status"] for item in registry["sources"])
    retrieval_counts: Counter[str] = Counter()
    if args.retrieval_results.exists():
        results = json.loads(args.retrieval_results.read_text(encoding="utf-8"))
        for case in results.get("cases") or []:
            for record in (((case.get("variants") or {}).get("hybrid") or {}).get("evidence") or {}).get("records", []):
                if record.get("source_id"):
                    retrieval_counts[record["source_id"]] += 1
        # Current retrieval results retain IDs in retrieved_ids rather than
        # entire packets; resolve those IDs against canonical source records.
        source_by_record = {item["id"]: item["source_id"] for _, item in records}
        for case in results.get("cases") or []:
            retrieved = (((case.get("variants") or {}).get("hybrid") or {}).get("evidence") or {}).get("retrieved_ids") or []
            for record_id in retrieved:
                if record_id in source_by_record:
                    retrieval_counts[source_by_record[record_id]] += 1
    source_rows = []
    for source in registry["sources"]:
        source_rows.append({
            "source_id": source["id"],
            "records_generated": by_source[source["id"]],
            "retrieval_count": retrieval_counts[source["id"]],
            "applied_count": 0,
            "rejected_count": 0,
            "last_retrieved_at": now() if retrieval_counts[source["id"]] else "",
            "last_applied_at": "",
            "last_ingested_revision": source["last_checked_revision"],
            "categories": sorted({item["topic"] for _, item in records if item["source_id"] == source["id"]}),
        })
    write_json(args.usage_out, {"schema_version": 1, "generated_at": now(), "sources": source_rows})
    conceptual_coverage = set(by_category)
    if "information-architecture-content" in conceptual_coverage:
        conceptual_coverage.add("copy")
    if "components-states-forms" in conceptual_coverage:
        conceptual_coverage.add("components")
    coverage = {
        "schema_version": 1,
        "generated_at": now(),
        "source_counts": {"total": len(registry["sources"]), **dict(sorted(statuses.items()))},
        "records_per_source": dict(sorted(by_source.items())),
        "records_per_category": dict(sorted(by_category.items())),
        "sources_without_records": sorted(item["id"] for item in registry["sources"] if not by_source[item["id"]]),
        "sources_never_retrieved": sorted(item["id"] for item in registry["sources"] if not retrieval_counts[item["id"]]),
        "sources_retrieved_never_applied": sorted(source for source, count in retrieval_counts.items() if count),
        "heavily_overrepresented_sources": sorted(source for source, count in by_source.items() if count > 6),
        "stale_records": sorted(item["id"] for _, item in records if item.get("status") == "deprecated"),
        "gaps": sorted({"copy", "typography", "layout", "motion", "components", "responsive"} - conceptual_coverage),
        "note": "Retrieval counts come from artifact-backed hybrid evaluation results. Applied/rejected counts remain zero until DESIGN/CONTENT usage ledgers are imported.",
    }
    write_json(args.coverage_out, coverage)
    print(f"sources={len(registry['sources'])} records={len(records)} coverage={args.coverage_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
