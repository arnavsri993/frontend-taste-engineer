# Evaluations

`cases.json` contains 16 heterogeneous frontend tasks. Retrieval evaluation
compares no-plugin baseline, compact static Skill kernel, lexical retrieval, and
hybrid retrieval. It reports precision, recall, mandatory-rule recall, duplicate
rate, irrelevant-token rate, provenance correctness, observed latency, context
size, and stable/experimental ordering with retrieved IDs as evidence.

```bash
python3 evals/run_retrieval_evals.py
python3 evals/run_frontend_evals.py
```

Both stable entrypoints write deterministic-structure JSON and Markdown to
`evals/results/`. Retrieval selection and relevance scoring are deterministic
for a fixed corpus; measured wall-clock latency is necessarily observational.

The frontend runner uses a 16-part product/visual/technical rubric. It refuses
to score a case unless every criterion has a 0–5 score backed by a concrete
artifact or executed-command observation. This preserves the central integrity
rule: an unevaluated frontend is marked `not-run`, never assigned a flattering
synthetic score.

No evaluator uses the network, installs dependencies, mutates stable knowledge,
or executes code from researched sources.
