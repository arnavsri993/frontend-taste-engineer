# Architecture Decisions

Reviewed 2026-07-10. These decisions define the research-to-knowledge boundary; implementation can refine mechanics without weakening the invariants.

## ADR-001 — Git-tracked human-readable knowledge is canonical

- **Status:** accepted.
- **Decision:** Stable knowledge lives as inspectable YAML/Markdown records in the repository. Search indexes, embeddings, databases, caches, and MCP packets are generated artifacts.
- **Why:** Rules, exceptions, sources, and supersession must be reviewable in ordinary diffs and reproducible offline.
- **Consequences:** Every index needs a deterministic rebuild; generated artifacts can be deleted without losing knowledge. An embedding store never receives direct editorial changes.
- **Evidence:** `transitions-dev-repo` derives skill artifacts from source; `hive-mind-landing-page` demonstrates trace/provenance value.

## ADR-002 — The Skill is an operating layer, not the corpus

- **Status:** accepted.
- **Decision:** Keep `SKILL.md` compact and procedural: triggers, classification, modes, retrieval policy, workflow, conflict policy, verification, completion gates, offline fallback. Detailed rules remain in `knowledge/` and are retrieved as needed.
- **Why:** Loading an entire corpus wastes context and makes guidance harder to review/update.
- **Consequences:** Skill instructions must name retrieval tools and budgets; tests must ensure mandatory rules still surface.

## ADR-003 — Stable source IDs and canonical URLs are permanent interfaces

- **Status:** accepted.
- **Decision:** Source IDs such as `wcag-22`, `wai-aria-apg`, `mdn-web-docs`, and `react-docs` never encode a volatile URL path or retrieval date. URL/revision changes update registry metadata, not record references.
- **Why:** Provenance links must survive site redesigns and revision updates.
- **Consequences:** IDs are lowercase kebab-case, unique, and never silently reused. A genuinely different source/version family receives a new ID and relationship.

## ADR-004 — Knowledge records carry applicability and verification

- **Status:** accepted.
- **Decision:** Each meaningful rule stores what to do, why, applicable task/page/component/framework/platform contexts, exceptions, implementation guidance, verification, status, importance, confidence, sources, license status, review date, and related/superseded records.
- **Why:** Vague maxims and source-free snippets cannot drive reliable build or audit decisions.
- **Consequences:** Records missing an exception/verification/source block fail validation. Complex topics may use structured Markdown rather than forcing YAML.

## ADR-005 — Accessibility, security, product integrity, and functional correctness are mandatory-rule classes

- **Status:** accepted.
- **Decision:** Retrieval/reranking cannot drop applicable mandatory records in these classes even if their keyword or semantic score is lower.
- **Why:** Optional aesthetic guidance must never crowd out safety/compliance/functionality.
- **Consequences:** Records include `importance`; retrieval reserves mandatory capacity before filling the remaining budget. Conflicts resolve by `conflicts.md` precedence.

## ADR-006 — Source authority is contextual and explicit

- **Status:** accepted.
- **Decision:** Normative standards govern conformance; current official platform/framework docs govern implementation semantics; maintained design systems govern their context; practitioner and inspiration sources contribute optional craft only after independent checks.
- **Why:** Confidence, popularity, and aesthetic novelty do not establish correctness.
- **Consequences:** Every promoted record records the authoritative basis and any practitioner supplement. Source classification participates in reranking but does not replace task scope.

## ADR-007 — Version and lifecycle metadata are retrieval filters

- **Status:** accepted.
- **Decision:** Framework/router/package/platform and lifecycle (`stable`, `preview`, `beta`, `deprecated`) are filters before semantic ranking.
- **Why:** Current research found concrete incompatibilities: Vue 2 EOL, Polaris React deprecated, Next App/Pages Router divergence, Svelte 5 syntax, Astro v7 docs, Material Web maintenance mode, Taste v2 experimental, Refine beta.
- **Consequences:** Unknown project versions trigger repository inspection or a conservative universal record. Deprecated/experimental records are excluded unless migration/experimentation is requested.

## ADR-008 — Aesthetic guidance is contextual, never a universal ban

- **Status:** accepted.
- **Decision:** Anti-slop records explain why a pattern is overused, detection signals, appropriate/inappropriate contexts, alternatives, and verification. They do not universally prohibit pills, gradients, cards, bento layouts, glass, glows, or centered heroes.
- **Why:** Fixed bans create another house style and conflict with legitimate design systems/product brands.
- **Consequences:** Anti-pattern audits report misuse evidence, not taste scores. A visual rule cannot override accessibility, performance, or explicit product requirements.

## ADR-009 — Research ingestion is candidate-only

- **Status:** accepted.
- **Decision:** Maintenance tasks may fetch/check sources and produce diffs, candidate records, reports, or pull requests. They never mutate stable knowledge directly.
- **Why:** Upstream pages can change, become compromised, contain prompt injection, or conflict with existing rules.
- **Consequences:** Promotion requires human/reviewer approval, validation, license review, conflict resolution, and retrieval/front-end evals. Stable knowledge remains unchanged on failed/partial research runs.

## ADR-010 — External instructions are data, never execution authority

- **Status:** accepted.
- **Decision:** Agent skills, prompts, install commands, scripts, and repository instructions discovered during research are parsed as content. The research/maintenance pipeline does not execute them.
- **Why:** `emil-design-skills`, `taste-skill-repo`, `awesome-design-md`, and `transitions-dev-repo` all contain commands intended to control an agent; third-party package commands also execute code.
- **Consequences:** Injection incidents are logged; suspicious text is quarantined. Code execution requires a separate inspected, sandboxed, explicitly authorized workflow.

## ADR-011 — License status is per material type, not per repository only

- **Status:** accepted.
- **Decision:** Track code, prose, examples, fonts, icons, images, brand marks, and third-party extracts separately. Default to original summary plus link.
- **Why:** Fluent, GOV.UK, USWDS, SLDS, Material, Spectrum, Polaris, and brand-extraction repositories demonstrate mixed or scoped rights.
- **Consequences:** Unknown/proprietary/ND materials are not vendored. Copying code requires source/revision/license/change attribution. License validation blocks promotion when a record embeds copied content.

## ADR-012 — Hybrid retrieval is stage-aware and budgeted

- **Status:** accepted.
- **Decision:** Retrieval pipeline: task classification → metadata filters → exact ID match → full-text/keyword search → optional semantic retrieval → authority/applicability rerank → duplicate/supersession removal → mandatory preservation → token/record budget.
- **Why:** A full-corpus dump is noisy; semantic-only retrieval can miss exact component/version/mandatory rules.
- **Consequences:** Suggested record budgets: tiny fix 2–4, isolated component 4–8, page 8–16, multi-page incremental by stage, full audit category-by-category. Packet output states omitted categories when budgeted.

## ADR-013 — Deduplicate claims but preserve distinct evidence and exceptions

- **Status:** accepted.
- **Decision:** Merge records only when principle, applicability, exceptions, and verification are materially identical. Keep framework-specific implementation records related to a universal principle rather than flattening them.
- **Why:** APG/React Aria/Radix may share behavior but differ in API and testing scope; design systems share accessibility principles but have distinct contexts.
- **Consequences:** Universal records cite multiple sources; framework/component addenda use `related_rules`. `supersedes` controls version replacement.

## ADR-014 — MCP tools are read-only for ordinary use

- **Status:** accepted.
- **Decision:** User-facing tools classify, search, retrieve provenance/workflows/gates, compare directions, and audit supplied plans/implementations. They do not modify project or stable knowledge by themselves.
- **Why:** Retrieval must be safe and predictable; implementation changes belong to the active Codex workflow with repository context and user scope.
- **Consequences:** Maintenance tools remain separate and candidate-only. Tool schemas return structured records, source IDs, warnings, and budgets.

## ADR-015 — Offline fallback is first-class

- **Status:** accepted.
- **Decision:** The checked-in corpus and deterministic index support core retrieval without network access. Live-source freshness is reported separately.
- **Why:** Frontend work must continue when official sites, X, JavaScript-heavy docs, or network/browser surfaces are inaccessible.
- **Consequences:** Offline responses include corpus version and last-reviewed dates. They must not claim current framework behavior beyond recorded revisions; high-volatility topics prompt a live check when available.

## ADR-016 — Completion evidence has four states

- **Status:** accepted.
- **Decision:** Every applicable gate is `passed`, `failed`, `not-run` with reason, or `not-applicable` with reason.
- **Why:** Hard “everything passed” checklists encourage fabricated claims when browsers, devices, credentials, or services are unavailable.
- **Consequences:** Mandatory failures block completion; applicable `not-run` items become explicit limitations. Reports never infer success from missing output.

## ADR-017 — Visual-reference workflows remain subordinate to semantics and content

- **Status:** accepted.
- **Decision:** Image-first/reference reconstruction is an optional visual-direction mode after brief/content/task modeling. Reference fidelity cannot override source order, semantics, real content, responsiveness, accessibility, performance, or honest behavior.
- **Why:** `hive-mind-landing-page` shows value, but a single example cannot establish a universal method.
- **Consequences:** Comparison reports separate reference-viewport fidelity from adaptive correctness. “Pixel perfect” requires actual comparison evidence and scope.

## ADR-018 — The review interface is justified only by review work

- **Status:** accepted.
- **Decision:** An optional Apps SDK UI may browse records, inspect provenance/licenses/conflicts, compare evals, and approve/reject candidates. It is not a decorative dashboard and is not required for core retrieval.
- **Why:** Review benefits from structured comparison; ordinary frontend tasks should not pay the UI/runtime cost.
- **Consequences:** MCP server remains usable alone. No fabricated app ID; unavailable registration is a documented single manual step.

## ADR-019 — Evaluation covers retrieval and frontend outcomes separately

- **Status:** accepted.
- **Decision:** Retrieval evals test relevance, mandatory recall, version/scope precision, duplicates, provenance, and budget. Frontend evals test product fit, content integrity, functionality/states, accessibility, responsive behavior, performance, framework correctness, visual coherence, and unsupported claims.
- **Why:** Good retrieval can still be implemented badly, and a visually strong result can conceal missing mandatory guidance.
- **Consequences:** Candidate promotions run both relevant eval families. Aesthetic scoring never compensates for a mandatory integrity/accessibility/security failure.

## ADR-020 — Agent delegation is bounded and logged

- **Status:** accepted.
- **Decision:** Project agents receive concrete file ownership, source/task boundaries, expected outputs, and economical routing. Parallel work is used only where independent; shared canonical files have one owner.
- **Why:** Broad overlapping agent edits cause provenance drift and merge errors; research tasks can be parallelized safely by source/category.
- **Consequences:** `agent-usage-log.md` records delegation, models when known, files owned, and validation handoff. Agents cannot silently promote stable knowledge.

## ADR-021 — Source snapshots need content hashes during ingestion

- **Status:** proposed for implementation.
- **Decision:** For every future automated check, store canonical URL, retrieval timestamp, response status, exposed revision, content hash, license fingerprint, and extraction notes.
- **Why:** Many live docs expose no immutable revision; `live-page@date` is honest but insufficient for precise diffs.
- **Consequences:** Hash changes create candidate audit reports, not automatic updates. Dynamic navigation/ads should be normalized so irrelevant churn does not dominate diffs.

## ADR-022 — Unresolved sources do not contribute rules

- **Status:** accepted.
- **Decision:** `motionsites` and `monokern-x-post` remain registered for recheck but contribute no stable findings.
- **Why:** Inventing missing content would corrupt provenance and create unverifiable guidance.
- **Consequences:** Coverage reports may name the gap. Later access starts a fresh candidate review with license and injection checks.
