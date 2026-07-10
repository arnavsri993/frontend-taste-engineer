# License and Attribution Review

Checked 2026-07-10. This is an engineering provenance review, not legal advice. The corpus should summarize and link by default. Copying source prose, code, tokens, examples, fonts, icons, screenshots, or brand assets requires item-level confirmation even when a repository has a permissive root license.

## Status vocabulary

- `summarized`: ideas may be paraphrased with source IDs/links; no substantial copying.
- `adaptable-with-notice`: license permits adaptation when the stated notice/attribution/share-alike obligations are met.
- `link-only`: proprietary, brand-limited, or insufficiently clear for copying.
- `unresolved`: do not copy until license scope is verified.

## Supplied sources

| ID | Verified or stated license | Corpus status | Required handling and restrictions |
|---|---|---|---|
| `hive-mind-landing-page` | MIT for original code/prompts/docs/custom skill/generated assets; README says third-party skills keep upstream licenses | `summarized`; code only `adaptable-with-notice` | Retain MIT notice for substantial copies. Do not assume linked/adapted third-party skill rights transfer. Generated assets may still contain model/service usage constraints not reviewed here. |
| `emil-design-skills` | MIT | `summarized`; skill text/code `adaptable-with-notice` | Retain copyright/license notice. Attribute Emil Kowalski for adapted practitioner guidance. Avoid copying long skill text when a source-backed summary is enough. |
| `awesome-design-md` | MIT repository | `summarized`; schema `adaptable-with-notice`; brand entries `link-only` | MIT cannot grant rights in third-party marks, visual identity, fonts, images, or independently copyrighted site expression. Never imply referenced brand endorsement. |
| `transitions-refine-page` | Terms say Refine is MIT, copyright 2026 Jakub Antalik / Transitions.dev | `summarized`; Refine code `adaptable-with-notice` | Preserve MIT notice. Also preserve beta/no-warranty context and user responsibility for agent credits/changes when describing workflow. |
| `transitions-dev-repo` | Refine clearly MIT; no root repository license visible | `unresolved` for non-Refine files | Summarize/link transition principles. Do not vendor showcase CSS, generated skill files, or templates until repository-wide scope is explicit. |
| `motionsites` | Unknown | `link-only` / `unresolved` | Do not copy prompts, screenshots, assets, catalog text, or templates. Homepage/terms were not accessible enough to establish rights. |
| `monokern-x-post` | Unknown; platform terms apply | `unresolved` | No content was accessible. Do not quote, reproduce media, or infer permission. |
| `taste-skill-site` | Site license not stated; linked repository MIT | `summarized` for public claims; site assets `link-only` | Do not apply the repository MIT license to website copy, screenshots, supporter identities, or logos without evidence. |
| `taste-skill-repo` | MIT | `summarized`; repository files `adaptable-with-notice` | Retain MIT notice for substantial copies. Prefer generalized, exception-aware records over copying model-control text. |

## Standards, web references, and testing/security sources

| ID | License / terms | Corpus status | Handling |
|---|---|---|---|
| `wcag-22` | W3C document use rules and notices | `summarized` | Link to the normative criterion and avoid changing its meaning. Short identifiers/titles are used for reference; do not reproduce large normative sections. |
| `wai-aria-apg` | W3C document/software terms; example scope can vary | `summarized` | Prefer pattern summaries and links. If adapting example code, retain the applicable W3C notices and test the result. |
| `mdn-web-docs` | Prose CC-BY-SA 2.5 or later unless noted; code samples CC0; Mozilla marks/look-and-feel excluded | `summarized`; prose adaptation carries attribution/share-alike | Attribute “Mozilla Contributors” plus material when reusing prose. Keep CC-BY-SA obligations out of newly written original summaries by paraphrasing from multiple primary sources. Code samples may be reused under CC0. |
| `webdev` | Google Developers content generally CC-BY 4.0; code generally Apache-2.0 unless noted | `summarized`; copied samples `adaptable-with-notice` | Verify page footer, attribute prose, preserve Apache notice for substantial samples, and separate Chrome-specific claims. |
| `w3c-i18n` | W3C document terms | `summarized` | Link/attribute; quick tips are explicitly incomplete. |
| `owasp-cheat-sheets` | CC-BY-SA 4.0 | `summarized`; adaptations require attribution/share-alike | Avoid verbatim bulk copying. Derived shareable prose from a single cheat sheet may trigger share-alike; maintain explicit source attribution. |
| `google-search-docs` | Google Developers terms; samples generally Apache-2.0 unless noted | `summarized` | Attribute copied content/samples under applicable terms; do not imply ranking guarantees. |
| `playwright-docs` | Playwright repository Apache-2.0 | `summarized`; examples `adaptable-with-notice` | Retain Apache notice for substantial copied code; generated tests written for this plugin should be original. |
| `whatwg-html` | Specification text CC-BY 4.0 under WHATWG terms; embedded code can differ | `summarized` | Reference algorithms/semantics, avoid reproducing large specification text, and preserve attribution for copied passages. |

## Framework documentation

| ID | License / terms | Corpus status | Handling |
|---|---|---|---|
| `react-docs` | Documentation CC-BY 4.0; React software MIT | `summarized`; code/docs adaptable with their respective notices | Attribute React documentation for copied prose; retain MIT for software. Keep examples version-scoped. |
| `nextjs-docs` | Next.js repository, including bundled docs, MIT | `summarized`; code `adaptable-with-notice` | Retain MIT notice for substantial copies; keep App/Pages Router and version scope. |
| `vue-docs` | MIT | `summarized`; `adaptable-with-notice` | Retain MIT notice for substantial copies and identify Vue 3. |
| `svelte-docs` | Svelte projects MIT; documentation-repository scope should be checked for verbatim copying | `summarized` | Link and paraphrase; retain applicable MIT notice for code. |
| `astro-docs` | MIT | `summarized`; `adaptable-with-notice` | Retain MIT notice for substantial copies; record Astro major version. |

## Design systems and component libraries

| ID | License / terms | Corpus status | Handling |
|---|---|---|---|
| `apple-hig` | Proprietary Apple Developer documentation; Apple Design Resources use a separate limited license | `link-only` plus original summary | Do not redistribute design resources, SF Symbols/assets, screenshots, or lengthy text. Do not imply Apple endorsement. Translate principles to web rather than copy. |
| `material-3` | Material Web Apache-2.0; Material site and brand assets subject to Google terms | `summarized`; open-source code `adaptable-with-notice`; assets `link-only` | Retain Apache notice for code. Do not reuse Google marks/assets or treat “open-source design system” as blanket permission for brand expression. |
| `fluent-2` | Fluent UI code MIT; font/icon assets may have separate license | `summarized`; code `adaptable-with-notice`; branded assets conditional | Retain MIT notice. Inspect asset package license; do not assume all Microsoft fonts/icons are generally reusable. |
| `carbon-design-system` | Apache-2.0 | `summarized`; code `adaptable-with-notice` | Preserve Apache license and NOTICE obligations where applicable. IBM marks remain separate. |
| `polaris` | Legacy `polaris-react` MIT; current CDN Web Components/Shopify docs under Shopify terms | Current docs `summarized`; legacy code `adaptable-with-notice`; CDN code `link/use-as-documented` | Do not assume legacy MIT covers current hosted components. Shopify marks/admin appearance are context-bound. |
| `primer-design-system` | Primer React MIT; GitHub brand assets/marks separate | `summarized`; code `adaptable-with-notice`; brand assets `link-only` | Retain MIT notice; do not reuse GitHub trademarks or imply affiliation. |
| `govuk-design-system` | GOV.UK Frontend code MIT; Crown content generally Open Government Licence v3.0 with exceptions | `summarized`; code/content adaptable with attribution/notice | Retain MIT for code; follow OGL attribution for content; never use GOV.UK crown/branding to imply official status. |
| `uswds` | Most work worldwide public domain/CC0; LICENSE.md identifies exceptions and third-party portions | `summarized`; copy only after exception review | CC0 does not waive third-party rights or authorize seals/logos. Review the exact asset in `LICENSE.md`; do not imply government affiliation. |
| `spectrum-design-system` | React Spectrum Apache-2.0; Spectrum site and Adobe brand assets under Adobe terms | `summarized`; code `adaptable-with-notice`; assets `link-only` | Retain Apache notice for code; do not copy Adobe marks, screenshots, or proprietary design resources. |
| `react-aria` | Apache-2.0 | `summarized`; code `adaptable-with-notice` | Preserve Apache/NOTICE obligations for substantial copied code. |
| `radix-primitives` | MIT, copyright WorkOS | `summarized`; code `adaptable-with-notice` | Retain MIT notice for substantial copies. Preview API status is not a license issue but must remain in provenance. |
| `atlassian-design-system` | Public docs subject to Atlassian terms; package licenses vary | `summarized`; package-by-package review | Do not copy internal-only material, marks, fonts, or assets. Check each Atlaskit/package license before code reuse. |
| `lightning-design-system` | Source BSD-3-Clause; icons/images CC-BY-ND 4.0 | `summarized`; source `adaptable-with-notice`; icons/images no-derivatives | Preserve BSD notice/non-endorsement. Attribute icons/images and do not alter them; avoid Salesforce marks outside authorized contexts. |

## Rules for the knowledge corpus

1. Every promoted record stores source IDs, a `license_status`, and `last_reviewed`.
2. Original summaries are preferred over copied text. No record should be a lightly edited reproduction of one source.
3. Code examples should be newly authored from the principle and verified, or explicitly tagged with source/license/notice.
4. Exact brand tokens, fonts, icons, logos, screenshots, illustrations, templates, testimonials, and product copy are excluded unless supplied by the user with usage rights or covered by a verified license.
5. MIT/BSD/Apache apply to covered code/documentation, not automatically to trademarks or every third-party asset in the repository.
6. CC-BY/CC-BY-SA/OGL reuse requires attribution; share-alike implications must be reviewed before distributing adapted prose.
7. CC-BY-ND assets may be redistributed only under their terms and not adapted; the default plugin policy is not to vendor them.
8. Unknown, proprietary, or inaccessible sources are `link-only` or `unresolved`.
9. Provenance links are informational and do not imply endorsement by source organizations.

## Attribution template for a copied code example

```text
Adapted from: <source name and canonical URL>
Source revision: <tag or commit/date>
License: <SPDX identifier or exact terms link>
Changes: <concise description>
```

For ordinary knowledge records, use source IDs and original paraphrase rather than this copied-code template.
