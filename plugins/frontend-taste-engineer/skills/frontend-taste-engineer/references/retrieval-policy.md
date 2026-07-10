# Retrieval policy

## Packet construction

1. Classify task mode, size, page type, components, framework, platform, stage, and risk.
2. Apply exact identifier matches and metadata filters first.
3. Rank lexical matches, then use deterministic concept expansion or semantic retrieval only when it improves recall.
4. Rerank by importance, stability, context match, source reliability, and verification usefulness.
5. Deduplicate equivalent principles while preserving the strongest provenance.
6. Insert applicable mandatory rules even when their lexical score is lower.
7. Enforce the stage budget and return compact fields: action, rationale, exceptions, implementation, verification, provenance.

## Budgets

- Tiny fix: 2–4 records.
- Component: 4–8.
- Page: 8–16, split by stage.
- Multi-page: incremental per route or component family.
- Audit: one category at a time.

External source selection has separate stage caps: brief 4, planning 6, implementation 8, refinement 6, verification 6. Retrieve artifact-pack summaries or matching sources only; never load the complete seed catalog for an ordinary task.

## External source routing

- Brief: inspiration catalogs, section-pattern catalogs, and page-type summaries; no code.
- Planning: shadcn/ui, Tailwind blocks, official design-system docs, and source-fit matrices.
- Implementation: native HTML first, then maintained primitives such as Radix, React Aria, Ariakit, Headless UI, Ark UI, or Floating UI; use configured 21st.dev MCP only as optional discovery/install tooling.
- Refinement: expressive component/motion catalogs and inspiration galleries for direction, not copied expression.
- Verification: authoritative accessibility/platform guidance plus license, anti-copy, anti-slop, performance, and reduced-motion review.

Before external use, verify product fit, exact license/intended use, attribution and entitlement, dependency/security risk, accessibility and states, responsive/localization behavior, motion/canvas/WebGL cost, originality/brand-copy risk, safer primitives, stability, public-artifact permission, and the post-integration test plan. Unknown license blocks copying/adaptation. `inspiration-only` permits generalized observations only. OpenAI Build Week and other corporate/product/event marketing pages are not pullable catalogs.

## Stability

- `stable`: suitable for default behavior.
- `specialized`: use only in matching context.
- `experimental`: label and validate; never displace mandatory stable guidance silently.
- `inspiration-only`: use to form questions or directions, not as correctness authority.
- `deprecated` or `rejected`: do not retrieve as advice; expose only for provenance/conflict review.

## Failure behavior

On timeout, malformed data, or missing index, retry once with a smaller lexical-only query. Then use the offline references, disclose reduced coverage, and continue. Never weaken mandatory checks because retrieval failed.
