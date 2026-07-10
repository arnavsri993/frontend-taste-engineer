# Ingestion and generated index

The Git-reviewed JSON under `../knowledge/` is canonical. Ingestion never
replaces that source of truth. `knowledge-index.json` is a deterministic,
disposable projection used for inspection and deployment checks.

```bash
python3 scripts/generate_index.py --dry-run
python3 scripts/generate_index.py
```

The generator reads every canonical JSON record, preserves dotted IDs, records
metadata and provenance, computes principle fingerprints, sorts by ID, and
hashes the complete entry list. It skips malformed records and returns a failing
report when parse errors exist. It performs no network requests and cannot write
inside `knowledge/`.

Research imports must be inspected, licensed, summarized, assigned stable IDs,
and reviewed before a human promotes them into canonical files. Never execute
scripts from researched repositories as part of ingestion.

