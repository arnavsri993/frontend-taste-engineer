# Frontend Taste Engineer knowledge corpus

This directory is the canonical, reviewable knowledge layer for the plugin. It is deliberately plain JSON plus narrowly scoped Markdown so standard-library readers, review UIs, MCP servers, tests, and Git diffs can consume the same source without a database or build step.

Start with `index.json`. It points to every record file, workflow, supporting artifact, guide, schema, and source entry. Consumers should not discover files by directory glob alone because future versions may retain migrations or archived material that is not canonical.

## Corpus shape

- `records/*.json` contains arrays of rule records validated by `rule.schema.json`.
- `workflows/*.json` turns rules into ordered, evidence-producing procedures.
- `component-state-matrix.json` defines states and checks for ten component archetypes.
- `completion-gates.json` defines production completion and waiver policy.
- `direction-comparison-rubric.json` and `guides/design-direction-comparison.md` make visual-direction decisions comparable without reducing taste to a score.
- `sources.json` is the corpus-facing source index and mirrors stable IDs from the authoritative `../research/source-registry.json`. Records contain those source IDs, never ad hoc URLs.
- `index.json` contains canonical paths and exact corpus counts for retrieval and review.

## Rule contract

`id` is the permanent primary key. Changing wording does not change an ID; a materially different rule receives a new ID and the old record points to it through `supersedes` or a migration. `related_rules` is non-directional context and must resolve to another canonical rule.

Every record separates:

- `status`: stability classification—`stable`, `specialized`, `experimental`, or `deprecated`;
- `importance`: enforcement—`mandatory`, `recommended`, or `contextual`;
- `confidence`: evidence confidence, independent from both stability and importance;
- applicability facets: tasks, pages, components, frameworks, and platforms;
- normative content: principle and rationale;
- decision content: applies-when, exceptions, implementation, and verification;
- cross-cutting review: accessibility, responsive, performance, and browser notes;
- provenance and lifecycle: source IDs, license status, introduction version, review date, relationships, and supersession.

Most cross-context platform, accessibility, and delivery rules are `stable`. Domain-bound rules are `specialized`. Trend-sensitive aesthetic detectors are `experimental` even when their importance is mandatory in a generated-work review. A status never weakens a mandatory rule when its stated context applies.

All `anti-slop-integrity` records also include `anti_pattern`: why generators overuse the pattern, detectable signals, legitimate and illegitimate contexts, alternatives, and explicit verification. These are contextual diagnostics rather than blanket bans.

## Retrieval guidance

1. Load `index.json` and the files in `record_files`.
2. Select by task, page, component, framework, and platform facets.
3. Apply `applies_when` and `exceptions` to the actual evidence.
4. Enforce applicable mandatory rules and completion gates.
5. Prefer stable rules; add specialized rules only when their scope matches; treat experimental rules as explicit review prompts.
6. Traverse `related_rules` when a decision crosses topics and `supersedes` when migrating old IDs.

Do not retrieve by title similarity alone. For example, a generic visual audit should load stable hierarchy and accessibility rules plus the anti-slop detectors, while a React server/client decision should additionally load specialized framework rules.

## Source and license policy

The corpus is newly authored synthesis. It does not reproduce long passages, code samples, icons, or assets from the upstream sources. `license_status` records this synthesis posture; `sources.json` identifies the evidence family and reminds implementers to check current upstream terms before copying anything beyond ideas and platform facts.

## Editing and review

Keep records in their topical file and preserve the file order in `index.json`. New records require a unique stable ID, all schema fields, at least one registered source, related-rule integrity, exact lifecycle values for the release, and an index count update. Prefer a new record over turning one rule into a bundle of loosely related requirements.

Before release, parse every JSON file with the language standard library, validate record shape, confirm source and relationship resolution, compare counts to `index.json`, and check that workflow, gate, matrix, rubric, and guide paths exist. A review should also ensure no placeholder or fabricated claim has entered the corpus itself.
