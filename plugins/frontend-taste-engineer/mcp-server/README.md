# Frontend Taste Engineer MCP server

Version 0.3.0 adds bounded, stage-specific external-source selection with license, inspiration-only, optional 21st.dev MCP, anti-copy, and no-auto-promotion gates. The current unreleased update adds intentional-negative-space guidance plus early motion routing for explicitly kinetic and medium-high/high-motion autonomous briefs, while preserving deterministic `autonomous-zero-brief-build` classification and staged production-completion routing from 0.2.0.

`server.py` is a Python 3.9+ stdio MCP server with no third-party runtime
dependencies. It reads `../knowledge/**/*.json` at startup, builds an in-memory
index, and never writes to the corpus or uses the network.

Run it from any directory:

```bash
python3 mcp-server/server.py
python3 mcp-server/server.py --self-check
python3 -m unittest discover -s mcp-server/tests -v
```

Set `FTE_KNOWLEDGE_DIR` or pass `--knowledge-dir` to test a candidate corpus.
If no valid records are available, the server exposes a small, clearly marked
offline safety kernel. Parse failures appear in `corpus.parse_errors`; they are
never silently converted into invented records.

## Retrieval contract

The hybrid path classifies the task, applies metadata boosts/filters, honors
exact dotted record IDs, scores lexical evidence, adds a bounded deterministic
synonym expansion, reranks, deduplicates exact principles, reserves capacity for
relevant mandatory rules, and enforces both record and estimated-token budgets.
`strategy: "lexical"` disables synonym expansion for evaluation.

Packets include principle, rationale, implementation, verification, exceptions,
sources, license state, and inspectable retrieval reasons. Experimental records
remain labelled and rank below equally relevant stable/active records.

`get_external_source_catalog` reads the reviewable seed metadata without network access. Brief/planning/implementation/refinement/verification caps are 4/6/8/6/6 sources. Matching uses source cards (`summary`, `best_for`, `keywords`, topics, category) rather than bare names/URLs. The tool returns those descriptions plus artifact-pack paths, intended-use decisions, and the source-selection checklist; it never returns copied source contents or loads all 395 entries into an ordinary packet.

## Protocol and safety

The stdio transport uses one UTF-8 JSON-RPC object per line, as required by MCP
stdio. Supported methods are `initialize`, `ping`, `tools/list`, and
`tools/call`. All exposed tools are read-only. Maintenance tools only calculate
or describe reports; they do not spawn commands, access the network, or promote
candidate knowledge.
