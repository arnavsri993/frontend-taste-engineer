# Source-derived design and copy migration v1

## Release

Plugin `0.4.0`, 2026-07-21.

## What changed

The plugin no longer treats a fixed-size source list or a hardcoded visual recipe classifier as the design engine. Reviewed source observations now live in canonical JSON under `knowledge/source-derived/`, with separate design and copy records. Retrieval combines those records with core UX, accessibility, responsive, integrity, and verification guidance before a visual or content direction is locked.

The source registry now separates manual approval, ingestion status, authority, stability, allowed use, and license status. A source can therefore be credible but inspiration-only, accessible but not approved, or ingested while still blocked from copying. Legacy classification remains compatibility metadata, not the primary promotion decision.

## Pipeline

1. `scripts/ingest_sources.py` creates a candidate-only queue and report. It cannot write canonical knowledge.
2. Human-reviewed records are authored in `knowledge/source-derived/design.json` or `copy.json`.
3. `scripts/compile_source_records.py` validates and compiles derivative retrieval data under `ingestion/compiled/`.
4. `scripts/generate_source_coverage.py` reports records per source/category, zero-record sources, stale gaps, and honest zero usage counters until artifact-backed usage is imported.
5. `scripts/validate_all.py` validates source dimensions, schemas, canonical records, compiled reports, all 21 copy pairs, and Codex-only packaging.

Stable knowledge promotion still requires a candidate branch and human-reviewed pull request. Monitoring and ingestion tooling remain report-only against stable knowledge.

## Runtime workflow

1. Inspect the repository and running product.
2. Classify product constraints only. Palette, typography, composition, material, component styling, visual intensity, and finished direction remain unset.
3. Ask one bounded clarification batch of at most four questions when needed; honor `use_judgment` or noninteractive execution.
4. Retrieve a diversified evidence packet with reserved capacity for a small mandatory safety kernel.
5. Generate two or three materially different candidate directions, compare them, and record applied/rejected evidence.
6. Lock `DESIGN.md` and `CONTENT.md`, then implement and verify.

## Copy evaluation

All 21 supplied AI/Grubby pairs are preserved exactly as a contrastive benchmark. Grubby output is not treated as gold truth. Annotations record which version is stronger for frontend use, why, what factual or structural drift occurred, and the best revision strategy. Deterministic copy audits flag generic abstractions, vague calls to action, transition/opening monotony, and factual-anchor drift; they do not claim authorship or detector accuracy.

## Distribution

The Apps SDK declaration and empty `.app.json` were removed. The standalone Skill packaging command and ZIP were removed. The supported artifact is the full Codex plugin, which contains the Skill and MCP server. Start a new Codex task after installing an updated plugin so the MCP surface is reloaded.

## Compatibility

- Source catalog count is dynamic; validators retain only the original 245-source minimum safety floor.
- Existing stable core records remain valid.
- The MCP server version is `0.4.0`; plugin cachebuster metadata may be newer.
- Consumers relying on removed creative-profile styling fields must switch to constraints plus `generate_candidate_directions`.
