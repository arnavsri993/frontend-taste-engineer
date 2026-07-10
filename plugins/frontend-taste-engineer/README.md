# Frontend Taste Engineer plugin

This directory is the installable plugin package. The repository root contains the marketplace, CI, contribution policy, and full architecture documentation.

Version 0.3.0 adds a 245-source external frontend seed catalog, stage-bounded source selection, license/anti-copy gates, optional 21st.dev MCP guidance, artifact-pack summaries, deterministic candidate discovery, and policy evaluations. It preserves the 0.2.0 `autonomous-zero-brief-build` workflow for minimal website, page, portfolio, frontend, and redesign prompts.

“Stunning” and similar quality language means exceptionally appropriate and well executed. The classifier uses a five-level visual-intensity model plus domain, task, audience, trust, risk, density, frequency, maturity, accessibility, device, familiarity, and experimental-tolerance signals; it does not force dark, cinematic, gradient-heavy, or highly animated styling across products.

Runtime components:

- `skills/frontend-taste-engineer/`: compact operating Skill, offline references, templates, and static audit.
- `knowledge/`: canonical, diffable frontend knowledge records.
- `mcp-server/`: stdio classification, retrieval, provenance, audit, and bounded external-source selection tools.
- `hooks/`: trusted-on-review session context hook.
- `review-app/`: optional local provenance and audit viewer.
- `research/source-discovery/`: 245 candidate seed URLs, monthly queries, scoring, promotion policy, and candidate templates.
- `research/artifact-packs/` and `references/`: source-family summaries plus selection/license/discovery gates.
- `evals/`, `audits/`, `maintenance/`: evidence, regression, and lifecycle systems.

The MCP classifier extracts named recipients and quoted text, separates supplied facts from assumptions, infers page type/tone/ambition/interaction depth, and routes focused records by workflow stage. Framework, component, motion, performance, and browser guidance is deferred until relevant instead of being loaded into the initial brief.

`get_external_source_catalog` applies separate stage budgets, never loads the full catalog for an ordinary task, blocks premium/unclear-license copying, keeps Awwwards/Mobbin/Page Flows inspiration-only, prioritizes maintained primitives for complex widgets, and treats 21st.dev MCP as optional tooling only when configured. External websites and returned commands remain untrusted data; no candidate is promoted automatically.

Named recipients and messages are request-local by default. Public fixtures use fictional data. `scripts/scan_private_terms.py` reads an untracked local denylist through `FTE_PRIVATE_TERMS_FILE`, scans text files, filenames, added diff lines, logs/evidence, and ZIP contents, and suppresses the sensitive value in its report. Public screenshots require manual review because raster OCR is intentionally out of scope.

The `.app.json` mapping is intentionally empty until a developer-mode ChatGPT app is registered manually. No app ID is fabricated. The MCP server and Skill work without that optional registration.

Install from the repository root:

```bash
codex plugin marketplace add "$(pwd)"
codex plugin add frontend-taste-engineer@personal
```

Then start a new Codex task and review the plugin hook in `/hooks`.

Preview monthly discovery with no network and no writes:

```bash
python3 scripts/discover_frontend_sources.py --dry-run --max-results 50
```
