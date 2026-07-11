# Evaluations

`cases.json` contains 34 heterogeneous frontend tasks, including two retrieval-only
motion/minimalism regressions and eight minimal
website/page prompts for autonomous classification and stage routing. Retrieval evaluation
compares no-plugin baseline, compact static Skill kernel, lexical retrieval, and
hybrid retrieval. It reports precision, recall, mandatory-rule recall, duplicate
rate, irrelevant-token rate, provenance correctness, observed latency, context
size, stable/experimental ordering, and per-case required canonical-record IDs as evidence.

`source-policy-cases.json` adds eight deterministic policy fixtures: premium/pro copy rejection, inspiration-only gallery handling, primitive routing for complex widgets, optional 21st.dev MCP behavior, Build Week exclusion, candidate reporting without promotion, unclear-license resolution, and stage-budget preservation. These cases run as a retrieval gate.

Minimal-prompt cases also score Skill trigger coverage, autonomous mode, profile
completeness, page type, tone, entity/quote extraction, fact/assumption
separation, no-question policy, copy-integrity guardrails, staged retrieval, and
production-completion selection. A tiny CSS-fix non-trigger is covered by the
MCP unit tests.

Ten marked direction-diversity cases cover personal finance, banking,
investment analytics, public service, enterprise software, developer tools,
premium ecommerce, robotics, a playful friend-directed page, and an
experimental portfolio. The evaluator gates palette/material, typography,
composition, hero treatment, component styling, tone, motion, and all five
visual-intensity levels against aesthetic convergence.

Recipient tests use fictional names, verify dynamic extraction and report
redaction, and assert that canonical knowledge remains recipient-agnostic.
Private real-project evidence stays local; public evaluation artifacts must be
synthetic and pass the configurable private-term scanner.

```bash
python3 evals/run_retrieval_evals.py
python3 evals/run_frontend_evals.py
python3 evals/run_autonomous_e2e.py
```

Both stable entrypoints write deterministic-structure JSON and Markdown to
`evals/results/`. Retrieval selection and relevance scoring are deterministic
for a fixed corpus; measured wall-clock latency is necessarily observational.

The frontend runner uses a 16-part product/visual/technical rubric. It refuses
to score a case unless every criterion has a 0–5 score backed by a concrete
artifact or executed-command observation. This preserves the central integrity
rule: an unevaluated frontend is marked `not-run`, never assigned a flattering
synthetic score.

The `minimal-alex-message` case is the release's synthetic end-to-end target.
Its evidence is accepted only after a fresh Codex task creates and runs the
fixture, captures desktop/mobile output, records refinement, and completes the
production build. The harness sends only the synthetic prompt; its pre-created
files provide build, preview, and Chrome capture infrastructure, not hidden
design direction.

No evaluator uses the network, installs dependencies, mutates stable knowledge,
or executes code from researched sources.
