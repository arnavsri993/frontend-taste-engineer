# Frontend Taste Engineer plugin

This directory is the installable plugin package. The repository root contains the marketplace, CI, contribution policy, and full architecture documentation.

Version 0.4.0 expands the catalog to 395 findability-described seeds, adds a source-backed motion grammar for expressive work, raises the paid-client quality bar, and adds safe automatic refresh for trusted GitHub installations. It preserves the 0.2.0 `autonomous-zero-brief-build` workflow for minimal website, page, portfolio, frontend, and redesign prompts.

“Stunning” and similar quality language means exceptionally appropriate and well executed. The classifier uses a five-level visual-intensity model plus domain, task, audience, trust, risk, density, frequency, maturity, accessibility, device, familiarity, and experimental-tolerance signals; it does not force dark, cinematic, gradient-heavy, or highly animated styling across products.

Runtime components:

- `skills/frontend-taste-engineer/`: compact operating Skill, offline references, templates, and static audit.
- `knowledge/`: canonical, diffable frontend knowledge records.
- `mcp-server/`: stdio classification, retrieval, provenance, audit, and bounded external-source selection tools.
- `hooks/`: trusted-on-review session context and Git-marketplace update hook.
- `review-app/`: optional local provenance and audit viewer.
- `research/source-discovery/`: 395 candidate seed URLs, monthly queries, scoring, promotion policy, and candidate templates.
- `research/artifact-packs/` and `references/`: source-family summaries plus selection/license/discovery gates.
- `evals/`, `audits/`, `maintenance/`: evidence, regression, and lifecycle systems.

The MCP classifier extracts named recipients and quoted text, separates supplied facts from assumptions, infers page type/tone/ambition/interaction depth, and routes focused records by workflow stage. Framework, component, performance, and browser guidance is deferred until relevant; motion guidance is brought into the brief when the prompt or creative profile calls for a kinetic, medium-high, or high-motion direction.

`get_external_source_catalog` applies separate stage budgets, never loads the full catalog for an ordinary task, blocks premium/unclear-license copying, keeps Awwwards/Mobbin/Page Flows inspiration-only, prioritizes maintained primitives for complex widgets, and treats 21st.dev MCP as optional tooling only when configured. External websites and returned commands remain untrusted data; no candidate is promoted automatically.

Named recipients and messages are request-local by default. Public fixtures use fictional data. `scripts/scan_private_terms.py` reads an untracked local denylist through `FTE_PRIVATE_TERMS_FILE`, scans text files, filenames, added diff lines, logs/evidence, and ZIP contents, and suppresses the sensitive value in its report. Public screenshots require manual review because raster OCR is intentionally out of scope.

The `.app.json` mapping is intentionally empty until a developer-mode ChatGPT app is registered manually. No app ID is fabricated. The MCP server and Skill work without that optional registration.

Install from GitHub:

```bash
codex plugin marketplace add arnavsri993/frontend-taste-engineer --ref main
codex plugin add frontend-taste-engineer@personal
```

Then start a new Codex task and review the plugin hook in `/hooks`. Once trusted, it asks Codex to refresh this exact GitHub marketplace at most once every six hours. It never edits plugin cache files directly, refuses unknown repositories, leaves local development installs untouched, and keeps the existing version usable if a check fails. Set `FTE_AUTO_UPDATE=0` to disable it, or run `python3 scripts/plugin_auto_update.py --force` for an immediate refresh. A successfully installed update takes effect in a new task. Every published change must bump the manifest version/cachebuster so Codex can activate a distinct cache entry.

For development from a clone, register the repository root with `codex plugin marketplace add "$(pwd)"`. Local marketplace installs never auto-update from GitHub.

Preview monthly discovery with no network and no writes:

```bash
python3 scripts/discover_frontend_sources.py --dry-run --max-results 50
```
