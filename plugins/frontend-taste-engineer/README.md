# Frontend Taste Engineer plugin

This directory is the installable plugin package. The repository root contains the marketplace, CI, contribution policy, and full architecture documentation.

Runtime components:

- `skills/frontend-taste-engineer/`: compact operating Skill, offline references, templates, and static audit.
- `knowledge/`: canonical, diffable frontend knowledge records.
- `mcp-server/`: stdio classification, retrieval, provenance, and audit tools.
- `hooks/`: trusted-on-review session context hook.
- `review-app/`: optional local provenance and audit viewer.
- `research/`, `evals/`, `audits/`, `maintenance/`: evidence, regression, and lifecycle systems.

The `.app.json` mapping is intentionally empty until a developer-mode ChatGPT app is registered manually. No app ID is fabricated. The MCP server and Skill work without that optional registration.

Install from the repository root:

```bash
codex plugin marketplace add "$(pwd)"
codex plugin add frontend-taste-engineer@personal
```

Then start a new Codex task and review the plugin hook in `/hooks`.
