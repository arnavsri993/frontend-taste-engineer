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

## Stability

- `stable`: suitable for default behavior.
- `specialized`: use only in matching context.
- `experimental`: label and validate; never displace mandatory stable guidance silently.
- `inspiration-only`: use to form questions or directions, not as correctness authority.
- `deprecated` or `rejected`: do not retrieve as advice; expose only for provenance/conflict review.

## Failure behavior

On timeout, malformed data, or missing index, retry once with a smaller lexical-only query. Then use the offline references, disclose reduced coverage, and continue. Never weaken mandatory checks because retrieval failed.
