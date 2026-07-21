# Frontend Taste Engineer plugin

This directory is the installable plugin package. The repository root contains the marketplace, CI, contribution policy, and full architecture documentation.

Version 0.4.0 migrates the plugin to source-derived design and copy retrieval. It separates source authority, stability, license, allowed use, and ingestion state; replaces fixed catalog-size assumptions with dynamic validation; adds candidate-only ingestion, compiled source records, coverage and usage reports; and retrieves diversified evidence before visual and content lock. The classifier now emits constraints rather than preselected styling, while candidate-direction, CONTENT-brief, copy-audit, and 21-pair contrastive copy evaluation complete the planning path.

“Stunning” and similar quality language means exceptionally appropriate and well executed. The classifier reports product, audience, task, trust, risk, density, familiarity, and motion-tolerance constraints; it does not select palette, typography, material, component styling, or a finished direction.

Runtime components:

- `skills/frontend-taste-engineer/`: compact operating Skill, offline references, templates, and static audit.
- `knowledge/`: canonical, diffable frontend knowledge records.
- `mcp-server/`: stdio classification, retrieval, provenance, audit, and bounded external-source selection tools.
- `hooks/`: trusted-on-review session context and opt-out GitHub marketplace update hook.
- `review-app/`: optional local frontend showcase and deployment example.
- `research/source-discovery/`: a dynamically counted candidate seed catalog, monthly queries, scoring, promotion policy, and candidate templates.
- `research/artifact-packs/` and `references/`: source-family summaries plus selection/license/discovery gates.
- `evals/`, `audits/`, `maintenance/`: evidence, regression, and lifecycle systems.

The MCP classifier extracts request-local entities, separates supplied facts from assumptions, reports constraints, and offers one bounded clarification batch. The brief workflow retrieves core UX, source-derived design, copy, responsive, accessibility, integrity, and verification evidence before generating and comparing two or three directions. Framework, component, performance, and browser guidance remains staged.

`get_external_source_catalog` applies separate stage budgets, never loads the full catalog for an ordinary task, blocks premium/unclear-license copying, keeps Awwwards/Mobbin/Page Flows inspiration-only, prioritizes maintained primitives for complex widgets, and treats 21st.dev MCP as optional tooling only when configured. It reports source-specific review status, credibility, reliability basis, and license status. Externality alone is not a negative trust verdict; embedded commands remain source content rather than agent directives, and no candidate is promoted automatically.

Named recipients and messages are request-local by default. Public fixtures use fictional data. `scripts/scan_private_terms.py` reads an untracked local denylist through `FTE_PRIVATE_TERMS_FILE`, scans text files, filenames, added diff lines, logs/evidence, and ZIP contents, and suppresses the sensitive value in its report. Public screenshots require manual review because raster OCR is intentionally out of scope.

This is a Codex plugin only. It packages the Skill and read-only MCP server; no Apps SDK surface or standalone Skill ZIP is distributed.

Install from the repository root:

```bash
codex plugin marketplace add "$(pwd)"
codex plugin add frontend-taste-engineer@personal
```

Then start a new Codex task and review the plugin hook in `/hooks`. The update hook is limited to the trusted `arnavsri993/frontend-taste-engineer` GitHub marketplace source, is rate-limited and configurable, and preserves the current cache on failure; local development installs and unknown origins are not auto-updated.

Preview monthly discovery with no network and no writes:

```bash
python3 scripts/discover_frontend_sources.py --dry-run --max-results 50
```

Run a targeted live registered-source check without changing the registry or knowledge:

```bash
python3 scripts/monitor_registered_sources.py \
  --source-id emil-design-skills \
  --json-out audits/generated/source-monitor.json \
  --md-out audits/generated/source-monitor.md
```

The scheduled weekly job checks all registered sources, compares public-text fingerprints with the prior run, uploads reports, and opens or refreshes one review issue when a revision, license/deprecation signal, content fingerprint, redirect, or availability state needs inspection. Reports retain public metadata and hashes only; promotion remains review-gated.
