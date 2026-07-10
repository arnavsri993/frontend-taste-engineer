# Deterministic tooling

All tools use Python 3.9+ standard library only. They do not fetch URLs,
install packages, run researched repositories, or alter `knowledge/`. Commands
that can create an index, ZIP, report, or screenshot support `--dry-run` (report
wrappers are already safe and only write to an explicit output path).

Stable workflow entrypoints:

```bash
python3 scripts/validate_all.py
python3 scripts/check_source_freshness.py --output audits/freshness.json
python3 scripts/generate_coverage_report.py --output audits/coverage.json
python3 scripts/license_report.py --output audits/licenses.json
FTE_PRIVATE_TERMS_FILE=.private-terms python3 scripts/scan_private_terms.py --require-terms
python3 scripts/generate_index.py --dry-run
python3 scripts/evaluate_retrieval.py
python3 scripts/package_skill.py --dry-run
python3 scripts/package_plugin.py --dry-run
```

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
edits. Freshness reports unknown revisions offline and never invents upstream
state. Packaging uses sorted paths and fixed ZIP timestamps for reproducibility;
generated evaluation results and caches are excluded from plugin packages.

The private-term scanner reads an untracked newline-delimited denylist, scans
ordinary files, filenames, added Git diff lines, logs/evidence, and ZIP entries,
and reports only file/line locations plus term fingerprints. It does not echo
the term or OCR raster screenshots.
