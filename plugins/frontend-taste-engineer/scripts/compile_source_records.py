#!/usr/bin/env python3
"""Compile reviewed source-derived records into a deterministic derivative index."""

from __future__ import annotations

import argparse
from pathlib import Path

from source_pipeline import INGESTION_ROOT, fingerprint, iter_source_records, load_registry, now, validate_registry, validate_source_records, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=INGESTION_ROOT / "compiled" / "source-records.json")
    args = parser.parse_args()
    registry = load_registry()
    errors = validate_registry(registry)
    records = list(iter_source_records())
    errors.extend(validate_source_records(records, {item["id"] for item in registry["sources"]}))
    if errors:
        for error in errors:
            print(error)
        return 1
    payload = {
        "schema_version": 1,
        "generated_at": now(),
        "registry_fingerprint": fingerprint(registry),
        "record_count": len(records),
        "records": [item for _, item in sorted(records, key=lambda pair: pair[1]["id"])],
    }
    write_json(args.out, payload)
    print(f"records={len(records)} output={args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
