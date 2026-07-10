# Audit outputs

This directory is reserved for generated review evidence. Committed schemas are
stable; timestamped or project-specific findings should normally stay out of
release packages.

Generate paired reports with, for example:

```bash
python3 scripts/run_frontend_audit.py ./path/to/frontend \
  --json-out audits/frontend.json --md-out audits/frontend.md
python3 scripts/check_accessibility.py ./path/to/frontend \
  --json-out audits/accessibility.json --md-out audits/accessibility.md
python3 scripts/check_performance.py ./path/to/frontend \
  --json-out audits/performance.json --md-out audits/performance.md
```

Static findings identify candidate defects and review risks. They do not prove
runtime accessibility, visual quality, functional completion, browser support,
or measured performance. Record those checks separately with commands,
viewports, artifacts, and observed outcomes.

