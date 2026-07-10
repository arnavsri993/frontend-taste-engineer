# Unresolved Sources and Access Gaps

Checked 2026-07-10. Nothing in this file is promoted to stable knowledge until the stated evidence is obtained.

## U-001 — Supplied X post

- **URL:** <https://x.com/monokern/status/2071246711222055363?s=46>
- **Registry ID:** `monokern-x-post`
- **Attempted:** direct open; canonical URL without tracking query; exact status-ID search; `site:x.com` author/status search; search for an author-provided transcript or mirror.
- **Result:** no body text, media, timestamp, thread context, verified identity, official mirror, or transcript was accessible.
- **What is not known:** every substantive claim, visual, link, and authorship detail.
- **Resolution needed:** a publicly accessible X rendering, author-owned mirror, or user-provided screenshot/transcript with provenance.
- **Current action:** exclude entirely; do not paraphrase from status ID or surrounding project themes.
- **Priority:** high because the URL was explicitly supplied; blocked by access.

## U-002 — MotionSites substantive catalog and terms

- **URL:** <https://motionsites.ai>
- **Registry ID:** `motionsites`
- **Attempted:** direct homepage and `/terms` open; web search restricted to the domain; public affiliates page; browser-control fallback.
- **Result:** text crawler exposed only title metadata on the homepage and a small affiliates page. No browser backend was available (`agent.browsers.list()` returned none), so visual/DOM inspection could not continue.
- **What is not known:** prompt contents, example authorship, source provenance, revision dates, product claims, terms, and license.
- **Resolution needed:** an accessible `llms.txt`, HTML/Markdown export, public catalog pages, terms page, or a working browser surface.
- **Current action:** classify inaccessible and inspiration-only; copy nothing.
- **Priority:** high because the URL was explicitly supplied; blocked by rendering/access.

## U-003 — Transitions.dev repository-wide license scope

- **URL:** <https://github.com/Jakubantalik/transitions.dev>
- **Registry ID:** `transitions-dev-repo`
- **Known:** `terms.html` clearly states that Refine is MIT and includes the license text.
- **Gap:** no root `LICENSE` appeared in the public root inventory. It is therefore unclear whether the showcase, transition snippets, generated skill references, build templates, and all other directories are covered by the same MIT grant.
- **Resolution needed:** maintainer clarification or a root/per-directory license that explicitly covers those materials.
- **Current action:** summarize verified principles and link; do not vendor snippets outside the clearly licensed Refine scope.
- **Priority:** medium; no blocker for summarized guidance.

## U-004 — Exact immutable revision for CHORUS repository

- **URL:** <https://github.com/adamholter/hive-mind-landing-page>
- **Registry ID:** `hive-mind-landing-page`
- **Known:** public page showed `main`, one commit, root inventory, and MIT license.
- **Gap:** the accessible commit-history route returned a cache miss, so the latest SHA/date could not be captured.
- **Resolution needed:** accessible history/API, a release/tag, or maintainer-provided commit permalink.
- **Current action:** record `main@2026-07-10`; avoid claiming an exact SHA.
- **Priority:** low; content/repository identity is otherwise verified.

## U-005 — Exact immutable revision for Transitions.dev

- **URL:** <https://github.com/Jakubantalik/transitions.dev>
- **Registry ID:** `transitions-dev-repo`
- **Known:** public page showed 142 commits, file inventory, README, and June 2026 terms.
- **Gap:** accessible history route failed, so no latest SHA/date was captured.
- **Resolution needed:** accessible commit page/API or a release/tag.
- **Current action:** record `main@2026-07-10` and the explicit terms date.
- **Priority:** low/medium because the project is active and beta-adjacent.

## U-006 — Material 3 page bodies

- **URL:** <https://m3.material.io/>
- **Registry ID:** `material-3`
- **Attempted:** homepage, accessible-design URL, motion URL, domain searches, and official Material Web repository.
- **Result:** M3 pages returned “This website requires JavaScript.” Material Web source/README/license were accessible and say the implementation is in maintenance mode.
- **What remains partial:** detailed current M3 component/foundation wording and page-level revision metadata.
- **Resolution needed:** accessible browser, official static/Markdown export, or current official repository containing the docs.
- **Current action:** use only high-level first-party metadata and the inspectable official repository; no hidden page wording is inferred.
- **Priority:** medium; Material is included but not treated as a normative corpus source.

## U-007 — Lightning Design System 2 detailed page bodies

- **URL:** <https://www.lightningdesignsystem.com/>
- **Registry ID:** `lightning-design-system`
- **Attempted:** SLDS 2 landing page, accessibility URL, official repository, and old blueprint pages.
- **Result:** SLDS 2 exposed a rendered shell but little text to the crawler. The repository, licenses, a11y test commands, and old blueprint inventory were accessible.
- **What remains partial:** current SLDS 2 component/foundation wording and exact current site revision.
- **Resolution needed:** accessible browser/static docs or official current repository mapping.
- **Current action:** keep SLDS specialized and source general repository facts only; do not promote v1 wording as current.
- **Priority:** medium.

## U-008 — Current Polaris Web Components redistribution terms

- **URL:** <https://shopify.dev/docs/api/polaris/index>
- **Registry ID:** `polaris`
- **Known:** current web components/reference/migration guidance is accessible; legacy `polaris-react` is MIT and deprecated.
- **Gap:** the current CDN-delivered Web Components do not present a repository-wide open-source license in the consulted pages comparable to the legacy MIT repo.
- **Resolution needed:** explicit current component license/terms from Shopify.
- **Current action:** link/use through documented Shopify surfaces; do not vendor the CDN implementation or assume the legacy MIT license applies.
- **Priority:** medium for copying; none for summarized usage guidance.

## U-009 — MotionSites and Taste Skill website asset rights

- **URLs:** <https://motionsites.ai>, <https://www.tasteskill.dev/>
- **Registry IDs:** `motionsites`, `taste-skill-site`
- **Gap:** site-level image, screenshot, testimonial, and marketing-copy reuse terms were not stated in accessible pages.
- **Resolution needed:** explicit website terms/license or written permission.
- **Current action:** do not copy assets, testimonials, or long passages. Link to the MIT repository where applicable.
- **Priority:** low because no assets are needed for the corpus.

## U-010 — Live documentation without immutable revisions

- **Affected IDs:** `wai-aria-apg`, `mdn-web-docs`, `webdev`, `react-docs`, `vue-docs`, `svelte-docs`, `astro-docs`, `apple-hig`, `fluent-2`, `primer-design-system`, `spectrum-design-system`, `react-aria`, `radix-primitives`, `atlassian-design-system`, `w3c-i18n`, `owasp-cheat-sheets`, `google-search-docs`, `playwright-docs`, `whatwg-html`.
- **Gap:** many live sites expose page-level updated dates inconsistently and use living documentation rather than immutable releases.
- **Resolution needed:** ingestion should store retrieval timestamp, canonical URL, content hash, and—when exposed—repository SHA/release/version for every snapshot.
- **Current action:** registry says `live-page@2026-07-10` rather than inventing a version.
- **Priority:** high for the future ingestion pipeline; not a blocker for initial summarized research.

## U-011 — Expanded seed catalog item-level review

- **Inventory:** `source-discovery/seed-catalog.yml` contains 245 unique URLs; 12 cross-reference a reviewed registry source and 233 are not registered.
- **Known:** the URLs and requested category memberships; 42 explicit galleries are constrained to `inspiration-only`.
- **Gap:** the seed import did not verify ownership, public accessibility, immutable revisions, exact license/entitlement, asset scope, dependency/security posture, accessibility usefulness, or maintenance for each unregistered source.
- **Resolution needed:** run bounded discovery, inspect public docs/repository/package/license metadata, score observed evidence, and apply the promotion policy per source.
- **Current action:** 203 seed entries remain `unresolved`; 42 remain `inspiration-only`; copy/adapt/install nothing from seed metadata alone.
- **Priority:** incremental and coverage-driven. Do not review or retrieve the whole catalog for an ordinary frontend task.

## Recheck policy

- Recheck high-priority unresolved supplied sources weekly for the first month, then monthly.
- Recheck experimental sources (`taste-skill-*`, `transitions-*`) before promoting or updating any rule.
- Recheck framework/design-system sources at use time when the project version or package differs from the recorded revision.
- A newly accessible source enters candidate review; it never updates stable knowledge directly.
