# Monthly source discovery

1. Start from explicit coverage gaps and the queries in `../research/source-discovery/discovery-queries.yml`.
2. Preview with `python3 scripts/discover_frontend_sources.py --dry-run --max-results 50`; authorize network mode only for public text discovery.
3. Search standards, vendor/framework docs, maintained implementation sources, original case studies, and source families relevant to the current gap.
4. Record candidates with every required source field plus score evidence, security signals, maintenance, accessibility/performance implications, license, duplication, and trend/aesthetic risk.
5. Classify as `core`, `specialized`, `experimental`, `inspiration-only`, `inaccessible`, `unresolved`, or `rejected`. Core is reserved for authoritative standards/platform docs.
6. Write candidate YAML/Markdown under `../research/source-discovery/candidates/YYYY-MM/`. Do not modify stable knowledge.
7. Apply `../research/source-discovery/promotion-policy.md`, license review, evaluation, and reviewed PR promotion.
