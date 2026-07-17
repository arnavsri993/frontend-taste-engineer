# Changelog

All notable changes follow semantic versioning and are recorded here.

## Unreleased

- Replaced the blanket external-source “untrusted” label with evidence-based per-source assessments. Candidate seeds now report not-yet-assessed; reviewed sources report scoped credibility, reliability evidence, and license status separately from the inspect-before-execution boundary. Refreshed `kill-ai-slop` at `2d21245d` while retaining its missing-license copy restriction.
- Refreshed the MIT-licensed `emilkowalski/skills` practitioner source and added contextual rules for motion opportunity gating, system-level audits, gesture continuity and physics, optical typography, and accessible translucent-material fallbacks, with retrieval and provenance coverage.

## 0.4.0 — 2026-07-16

- Added opt-out automatic updates for trusted GitHub marketplace installs. The rate-limited hook delegates refresh and atomic cache activation to Codex, rejects local and unknown sources, preserves the current version on failure, and reports when a new task is required.
- Raised the Skill to a paid-client quality bar: system lock before catalogs, first-viewport law, AI-cluster reject list, density profiles, ≤3 motion roles, mandatory screenshot refine, and required “Why this is not generic” proof.
- Expanded the external seed catalog from 245 to 395 sources with findability cards, including a large template/starter absorption pass; no seed or template was promoted to stable knowledge or vendored into the repo.

## 0.3.0 — 2026-07-10

- Added a 245-URL external frontend seed catalog across 15 source families and 34 monthly query templates.
- Added standard-library public-text discovery with private/authenticated/binary blocking, injection/credential/install detection, deterministic candidate reports, and no automatic stable promotion.
- Added full source-field validation, a 100-point scoring rubric, source classification/promotion/license policies, and seven source-family artifact packs.
- Added stage-bounded MCP source selection, premium/unclear-license copy blocking, maintained-primitive routing, inspiration-only galleries, and optional 21st.dev MCP handling.
- Added eight external-source policy eval fixtures and narrowed `core` to authoritative standards/platform documentation.
- Explicitly excluded OpenAI Build Week and similar corporate/product/event marketing from pullable source catalogs.

## 0.2.0 — 2026-07-10

- Added `autonomous-zero-brief-build` for minimal website, page, landing-page, portfolio, product-polish, and substantial redesign prompts.
- Added deterministic creative-profile classification with entity and quoted-text extraction, fact/assumption separation, prompt-specific tone/page inference, and strict clarification limits.
- Added domain-adaptive five-level visual intensity, motion/familiarity/experimental-tolerance inference, regulated/finance/enterprise/developer/ecommerce behavior, and anti-convergence evaluation gates.
- Added request-local recipient policy, classifier redaction, synthetic public fixtures, and configurable private-term scanning across files, diffs, evidence, logs, and package archives.
- Added staged minimal-prompt retrieval, focused Skill references, complete copy and implementation defaults, rendered desktop/mobile refinement, and production-completion gates.
- Added minimal-prompt unit/retrieval/classification evaluations and a synthetic one-line end-to-end evidence workflow.
- Updated plugin, MCP, packages, documentation, and canonical workflow metadata to 0.2.0.

## 0.1.0 — 2026-07-10

- Scaffolded the installable repo-marketplace plugin with `@plugin-creator`.
- Added the compact Frontend Taste Engineer operating Skill and standalone offline resources.
- Added a source-backed canonical knowledge corpus and research/provenance system.
- Added a dependency-light stdio MCP retrieval server with focused read-only tools.
- Added deterministic validation, audit, retrieval, packaging, and evaluation workflows.
- Added project-scoped Luna/Terra agent routing with four-thread, depth-one limits.
- Added recurring source and regression maintenance workflows.
- Added original plugin identity assets and a local review interface.

Known limitations are documented in the README and release validation report.
