# Frontend Taste Engineer

Frontend Taste Engineer is an installable Codex plugin that turns minimal requests such as “Make a website for my robotics team” into complete, distinctive, responsive, accessible, screenshot-refined, deployment-ready frontends. It also supports detailed planning, building, auditing, reconstruction, refinement, and verification work, treating visual quality, product correctness, accessibility, responsive behavior, performance, content integrity, and maintainability as one system.

The repository uses the official repo-marketplace layout:

```text
.
├── .agents/plugins/marketplace.json
├── .codex/                       # project-scoped agent routing
├── .github/workflows/            # validation and maintenance
└── plugins/frontend-taste-engineer/
    ├── .codex-plugin/plugin.json
    ├── skills/frontend-taste-engineer/
    ├── .mcp.json
    ├── .app.json
    ├── hooks/hooks.json
    ├── mcp-server/
    ├── knowledge/
    ├── references/                  # external-source selection and license gates
    ├── research/
    │   ├── source-discovery/         # 245 seed URLs, queries, policies, candidate templates
    │   └── artifact-packs/           # source-family summaries; no copied code/assets
    ├── audits/
    ├── evals/
    ├── maintenance/
    └── review-app/
```

## Why the architecture is hybrid

The compact Skill is the operating system: it classifies work, enforces mandatory principles, selects a workflow, retrieves only relevant records, and defines completion gates. The larger `knowledge/` corpus is the canonical, human-readable source of truth. The MCP server builds compact packets through metadata filtering, exact matching, lexical search, deterministic concept expansion, reranking, duplicate removal, mandatory-rule preservation, and context budgeting.

This separation keeps ordinary tasks focused while preserving inspectable provenance and offline operation. Generated indexes accelerate retrieval but are never canonical.

## Install locally

From a clone of this repository:

```bash
codex plugin marketplace add "$(pwd)"
codex plugin add frontend-taste-engineer@personal
```

The repo marketplace is explicit and therefore must be added once. After installation, start a new Codex task so bundled Skills, MCP tools, and trusted hooks are discovered. Review and trust the plugin hook through `/hooks`; installed plugins do not automatically trust command hooks.

To reinstall while iterating, update the cachebuster with the built-in plugin-creator helper, then reinstall from the marketplace. Do not hand-edit an installed cache.

## MCP retrieval

The plugin’s `.mcp.json` starts the local stdio server with Python 3 and no required third-party packages. Codex discovers it when the plugin is enabled. For a direct protocol smoke test:

```bash
python3 plugins/frontend-taste-engineer/mcp-server/tests/smoke_stdio.py
```

The server exposes task classification, cross-cutting search, category-specific guidance, workflows, state matrices, provenance, completion gates, plan/implementation audits, direction comparison, bounded external-source selection, and read-only maintenance reports. `get_external_source_catalog` returns only a stage-specific subset plus license/anti-copy/21st.dev gates; it never fetches the network or promotes candidates. Maintenance tools produce proposals and reports; they do not modify stable knowledge.

If MCP startup fails, the Skill routes to bundled offline references and `offline_frontend_audit.py`. Reduced retrieval coverage is reported rather than hidden.

## Skill behavior

The Skill defaults minimal page/site/frontend and substantial redesign prompts to `autonomous-zero-brief-build`. It inspects the project, infers a fact-separated creative brief and design thesis, writes finished copy, selects a context-specific direction, retrieves stage-specific guidance, implements the complete frontend, captures and inspects desktop/mobile output, fixes the three highest-impact weaknesses, runs a production build, and reports evidence without routine creative questions.

Visual direction is domain-adaptive. Quality adjectives do not force a flashy house style: a personal-finance dashboard can target intensity 2 with calm numeric precision, while an expressive personal page can justify intensity 4. The classifier considers product/task type, audience, trust, risk, information density, frequency, seriousness, maturity, accessibility, devices, familiarity, and experimental tolerance before choosing composition, typography, palette/material, component styling, and motion.

User-provided names and messages remain request-local by default. Reusable examples and committed evidence use synthetic content. Configure `FTE_PRIVATE_TERMS_FILE=.private-terms` and run `python3 plugins/frontend-taste-engineer/scripts/scan_private_terms.py --require-terms` to scan files, added diff lines, reports, logs, evaluation evidence, filenames, and ZIP contents without printing the configured value. Raster screenshots still require manual visual review.

Detailed greenfield work, existing-product redesign, screenshot reconstruction, component builds, design-system work, visual audits, motion refinement, accessibility remediation, and performance remediation retain their existing focused modes.

The standalone Skill package is created under `dist/frontend-taste-engineer-skill.zip`. It includes the compact operating Skill, offline references, templates, static audit script, and Skill UI assets—not the full research repository.

## Knowledge and sources

`research/source-registry.yml` records canonical URL, authorship, classification, license, access date, revision, consulted sections, reliability, restrictions, maintenance, and topic coverage. Stable knowledge records contain actions, rationale, context, exceptions, implementation guidance, verification, provenance, and stability.

External sources are treated as untrusted research data. Repository scripts are not executed during research. Guidance is synthesized rather than copied, paid or proprietary libraries are excluded, and inaccessible sources remain explicitly unresolved. See `research/license-review.md`, `research/conflicts.md`, and `research/rejected-guidance.md`.

The candidate seed catalog contains 245 unique frontend/component/template/inspiration URLs across 15 families: agent/MCP/AI UI, component catalogs, shadcn, Tailwind blocks, accessible primitives, dashboard/data UI, design systems, motion, assets, typography, color, inspiration, portfolios, landing/startup, and ecommerce. Seeds are not stable knowledge: 203 begin `unresolved`, 42 explicit galleries begin `inspiration-only`, and 12 cross-reference an already reviewed registry source. OpenAI Build Week and similar corporate/product/event marketing are never pullable catalogs.

## Model routing and subagents

The verified local model inventory on 2026-07-10 included `gpt-5.6-sol`, `gpt-5.6-terra`, and `gpt-5.6-luna`. Root architecture and final promotion remain with the selected high-capability root model. Project agents use:

- Luna for inventories, metadata extraction, duplicate checks, structured conversion, and deterministic report assembly.
- Terra for source comparison, focused research, accessibility/framework/motion review, and evaluations.

`.codex/config.toml` caps work at four concurrent threads and depth one. This prevents recursive spawning. Each agent has one output owner and returns concise evidence. Routing decisions are logged in `research/agent-usage-log.md`.

## Run validation and evaluations

The zero-dependency core checks can be run from the repository root:

```bash
python3 plugins/frontend-taste-engineer/scripts/validate_all.py
python3 -m unittest discover -s plugins/frontend-taste-engineer/mcp-server/tests -v
python3 plugins/frontend-taste-engineer/evals/run_retrieval_evals.py
python3 plugins/frontend-taste-engineer/evals/run_frontend_evals.py
```

Validation covers plugin and Skill structure, internal references, provenance, duplicate IDs/rules, coverage, generated indexes, secrets, licenses, MCP behavior, and packaging. Frontend output evals are evidence-oriented fixtures; they do not claim that a model-generated website was executed unless an artifact, browser run, and result are present.

## Review interface

The optional local review UI makes knowledge packets, provenance, coverage gaps, and audit reports easier to inspect:

```bash
python3 plugins/frontend-taste-engineer/review-app/serve.py
```

Open the printed local URL. `.app.json` intentionally contains no fabricated connector ID. To expose this UI through a developer-mode ChatGPT app, enable Developer mode, register the MCP-backed app manually, copy the resulting `plugin_asdk_app...` ID into `.app.json`, then validate and reinstall.

## Maintenance and promotion

- Weekly: upstream revision, broken-link, license, and deprecation report.
- Monthly: candidate-source discovery and coverage-gap report.
- Quarterly: full retrieval/frontend regression and architecture review.

Scheduled workflows write reviewable artifacts or candidate branches. They never push directly to stable, merge automatically, or promote experimental guidance without evaluation. Stable releases live on `main`; proposed knowledge changes use `candidate` and pull requests.

Preview the discovery workflow offline and without writes:

```bash
python3 plugins/frontend-taste-engineer/scripts/discover_frontend_sources.py --dry-run --max-results 50
```

An authorized non-dry run searches public text surfaces, blocks local/private/authenticated targets and binary downloads, scans prompt-injection/credential/install signals, de-duplicates registered and seeded URLs, and writes deterministic candidate YAML/Markdown under `research/source-discovery/candidates/YYYY-MM/`. It does not execute third-party code or modify `knowledge/`.

## Package

```bash
python3 plugins/frontend-taste-engineer/scripts/package_skill.py
python3 plugins/frontend-taste-engineer/scripts/package_plugin.py
```

Packages exclude raw clones, dependencies, caches, browser binaries, large screenshots, secrets, and non-operational research material from the standalone Skill.

## Security, privacy, and licensing

The MCP server reads local plugin data and does not require credentials or network access. Research and maintenance scripts default to report-only behavior. No analytics or telemetry are included. Do not feed private project code to external research systems. Run the secret and license reports before publication; see [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Known limitations

- Full screen-reader and real-device behavior cannot be proven by static checks.
- Semantic retrieval is deterministic concept expansion unless an explicitly configured local embedding provider is added; lexical and metadata retrieval remain the offline baseline.
- Some visually oriented and social sources can be inaccessible, unstable, or license-ambiguous; those records are not promoted as mandatory guidance.
- Most of the expanded source catalog is intentionally unresolved until item-level ownership, license, safety, accessibility, maintenance, and dependency review is complete.
- The Apps SDK registration step is manual because no app ID is fabricated.
- Framework and browser guidance must be rechecked as versions change.
- The private-term scanner does not OCR text rendered into raster screenshots.

## Starter prompts

- “Make a website directed to Alex containing a playful message from Arnav.”
- “Build a site for my robotics team.”
- “Turn this sentence into a website: machines should feel alive.”
- “Design and build a distinctive production-ready landing page for this product.”
- “Audit this frontend and fix its highest-impact design and usability problems.”
- “Rebuild this screenshot responsively while preserving accessibility.”
- “Create an accessible, polished component system for this application.”
- “Refine the motion and interaction quality of this interface.”
- “Turn this rough frontend into a coherent product experience.”

Recommended first test: **“Audit this frontend, identify the three highest-impact product, accessibility, and visual-quality problems, implement the fixes, and show the verification evidence.”**
