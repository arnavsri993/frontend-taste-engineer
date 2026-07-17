# Deterministic tooling

All tools use Python 3.9+ standard library only. Network access is limited to
the explicit registered-source monitor and authorized candidate discovery;
neither installs packages, runs researched repositories, or alters
`knowledge/`. Commands that can create an index, ZIP, report, or screenshot
support `--dry-run` (report wrappers are already safe and only write to an
explicit output path).

Stable workflow entrypoints:

```bash
python3 scripts/validate_all.py
python3 scripts/check_source_freshness.py --output audits/freshness.json
python3 scripts/monitor_registered_sources.py --json-out audits/source-monitor.json --md-out audits/source-monitor.md
python3 scripts/generate_coverage_report.py --output audits/coverage.json
python3 scripts/license_report.py --output audits/licenses.json
FTE_PRIVATE_TERMS_FILE=.private-terms python3 scripts/scan_private_terms.py --require-terms
python3 scripts/generate_index.py --dry-run
python3 scripts/evaluate_retrieval.py
python3 scripts/discover_frontend_sources.py --dry-run --max-results 50
python3 scripts/expand_source_library.py
python3 scripts/absorb_templates.py
python3 scripts/enrich_source_cards.py --check
python3 scripts/package_skill.py --dry-run
python3 scripts/package_plugin.py --dry-run
python3 scripts/plugin_auto_update.py --status
```

`plugin_auto_update.py` is the only runtime maintenance script that may refresh an installed plugin. It accepts only the configured Git marketplace for `arnavsri993/frontend-taste-engineer`, delegates fetching and atomic cache activation to `codex plugin marketplace upgrade`, rate-limits checks, and never edits the plugin cache itself. Local marketplace installs and unknown Git origins are refused. Use `--force` for an immediate refresh or `FTE_AUTO_UPDATE=0` to disable the session hook.

`expand_source_library.py` and `absorb_templates.py` add curated discovery seeds with findability cards (libraries, kits, template catalogs, starters). `enrich_source_cards.py` rewrites seed/knowledge findability cards (`summary`, `best_for`, keywords) and regenerates `research/source-discovery/source-findability.md`. These scripts do not download templates, inspect upstream privately, or change licenses beyond explicit inspiration-only gallery/marketplace tags.
Focused checks cover plugin/Skill structure, local Markdown links, record
references, review dates, provenance, duplicate and contradiction candidates,
topic coverage, record depth, static frontend integrity, static accessibility,
static performance, secrets, configured private terms, and license evidence. Every report is JSON; pass
`--md-out PATH` for a human-readable companion.

`capture_responsive.py` is a safe plan by default. Add `--execute` only when a
local Chromium executable is already installed. Only localhost and `file://`
URLs are accepted unless `--allow-network` is explicit; the script never
downloads a browser.

Duplicate and contradiction outputs are triage heuristics, not automatic corpus
edits. The offline freshness report never invents upstream state. The explicit
registered-source monitor resolves public GitHub revision, license, archive, and
deprecation metadata or hashes bounded visible text from other public pages. It
blocks local/private destinations, executes no source code, retains no page
dumps, compares only a cached metadata baseline, and can request human review
without modifying stable knowledge. Packaging uses sorted paths and fixed ZIP
timestamps for reproducibility; generated evaluation results and caches are
excluded from plugin packages.

The private-term scanner reads an untracked newline-delimited denylist, scans
ordinary files, filenames, added Git diff lines, logs/evidence, and ZIP entries,
and reports only file/line locations plus term fingerprints. It does not echo
the term or OCR raster screenshots.

`discover_frontend_sources.py` is the other maintenance script with an optional public-network mode. `--dry-run` is offline, seed-backed, deterministic, and write-free. A non-dry run fetches bounded text content only, blocks private/authenticated destinations and binary assets, executes no page or package code, de-duplicates the registry and seeds, and writes candidate reports only under the selected candidate directory. It never modifies `knowledge/` or promotes a source.
