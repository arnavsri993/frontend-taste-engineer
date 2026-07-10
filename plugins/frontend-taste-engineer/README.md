# Frontend Taste Engineer plugin

This directory is the installable plugin package. The repository root contains the marketplace, CI, contribution policy, and full architecture documentation.

Version 0.2.0 adds `autonomous-zero-brief-build`: a minimal request to make a website, page, landing page, portfolio, frontend, or substantial redesign now triggers brief inference, original copy, context-specific art direction, complete implementation, desktop/mobile screenshot inspection, a top-three refinement pass, production verification, and a concise evidence report without routine creative questions.

“Stunning” and similar quality language means exceptionally appropriate and well executed. The classifier uses a five-level visual-intensity model plus domain, task, audience, trust, risk, density, frequency, maturity, accessibility, device, familiarity, and experimental-tolerance signals; it does not force dark, cinematic, gradient-heavy, or highly animated styling across products.

Runtime components:

- `skills/frontend-taste-engineer/`: compact operating Skill, offline references, templates, and static audit.
- `knowledge/`: canonical, diffable frontend knowledge records.
- `mcp-server/`: stdio classification, retrieval, provenance, and audit tools.
- `hooks/`: trusted-on-review session context hook.
- `review-app/`: optional local provenance and audit viewer.
- `research/`, `evals/`, `audits/`, `maintenance/`: evidence, regression, and lifecycle systems.

The MCP classifier extracts named recipients and quoted text, separates supplied facts from assumptions, infers page type/tone/ambition/interaction depth, and routes focused records by workflow stage. Framework, component, motion, performance, and browser guidance is deferred until relevant instead of being loaded into the initial brief.

Named recipients and messages are request-local by default. Public fixtures use fictional data. `scripts/scan_private_terms.py` reads an untracked local denylist through `FTE_PRIVATE_TERMS_FILE`, scans text files, filenames, added diff lines, logs/evidence, and ZIP contents, and suppresses the sensitive value in its report. Public screenshots require manual review because raster OCR is intentionally out of scope.

The `.app.json` mapping is intentionally empty until a developer-mode ChatGPT app is registered manually. No app ID is fabricated. The MCP server and Skill work without that optional registration.

Install from the repository root:

```bash
codex plugin marketplace add "$(pwd)"
codex plugin add frontend-taste-engineer@personal
```

Then start a new Codex task and review the plugin hook in `/hooks`.
