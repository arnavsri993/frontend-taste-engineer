# Plugin development rules

- Keep `.codex-plugin/` limited to `plugin.json`.
- Treat `knowledge/` as canonical and generated indexes as disposable.
- MCP tools are read-only against stable knowledge.
- Maintenance jobs may write reports or candidate artifacts, never stable rules.
- Preserve mandatory accessibility, integrity, and verification rules under context budgets.
- Use source IDs from `research/source-registry.yml`; unresolved or license-ambiguous material cannot support copied examples.
- Do not claim runtime, visual, accessibility, or performance verification from static analysis alone.
- Keep the standalone Skill compact and validate it independently from the plugin.
