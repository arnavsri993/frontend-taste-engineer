# Source Inventory

Checked: 2026-07-10. The registry contains 37 sources: all 10 supplied URLs and 27 independently selected primary sources. This inventory describes what was actually reachable and consulted; it does not claim an exhaustive clone or crawl. No external code was installed or run.

The separate `source-discovery/seed-catalog.yml` adds 245 unique request-supplied discovery seeds across 15 families. It is not a claim that those sources were inspected: 203 are `unresolved`, 42 explicit galleries are `inspiration-only`, 12 cross-reference an existing reviewed registry source, and zero were promoted by the seed import. See `artifact-packs/source-discovery-report.md` for category counts.

## Method and evidence levels

1. Prefer the canonical first-party page, normative specification, or official repository.
2. Inspect the public root inventory, relevant documentation sections, license, release/commit information, and examples where reachable.
3. Treat embedded prompts and agent commands as untrusted text. Extract ideas only after checking them against standards and production documentation.
4. Separate `verified` facts from `inference`, marketing claims, and aesthetic opinion.
5. If a page requires unavailable JavaScript/browser access or authentication, record the gap. Never reconstruct missing content from context or popularity.

Evidence labels used below:

- **Normative:** a standard or specification.
- **Primary:** the author/maintainer describes its own system, code, or workflow.
- **Practitioner:** named experience with concrete examples, but not a standard.
- **Inspiration:** useful for visual exploration only.
- **Unresolved:** content could not be verified.

## Supplied URLs — individual review

| ID | Supplied URL | Accessible inventory and areas consulted | Authorship / revision / license | Evidence and disposition |
|---|---|---|---|---|
| `hive-mind-landing-page` | <https://github.com/adamholter/hive-mind-landing-page> | Root inventory: `README.md`, `PROMPTS.md`, `TRACE.md`, `SECURITY_REVIEW.md`, `index.html`, `styles.css`, `script.js`, preview images, `assets/`, `docs/`, and `skills/`. README details a one-prompt CHORUS landing-page build, image-first reference, anti-slop inputs, responsive checks, dialog/form states, and a sanitized trace. Linked upstreams were located and inspected: Anthropic’s official `frontend-design` plugin (authors Prithvi Rajasekaran and Alexander Bricken), `cyxzdev/Uncodixfy` (MIT; explicit anti-pattern rules), the local `frontend-from-generated-image` skill, and the OpenAI Codex imagegen sample skill. | Adam Holter; `main`, one visible commit; exact SHA/date was not exposed in the accessible history page; MIT with explicit upstream-license caveat. | **Primary worked example.** Promote its audit trail, concrete state verification, and image-reference workflow. Do not generalize one design outcome or accept self-reported checks as proof for other builds. |
| `emil-design-skills` | <https://github.com/emilkowalski/skills> | `README.md`, `LICENSE`, commit history, and listed skills: `emil-design-eng`, `review-animations`, `animation-vocabulary`, `apple-design`. The repository explains origin/experience, installation, and the distinction between motion vocabulary and strict review. | Emil Kowalski; `f76bece`, 2026-07-09; MIT. | **Practitioner.** Promote purpose-driven motion, exact-property transitions, origin awareness, and animation review—with reduced-motion, interruptibility, performance, and context exceptions. |
| `awesome-design-md` | <https://github.com/VoltAgent/awesome-design-md> | `README.md`, `LICENSE`, `CONTRIBUTING.md` listing, commit history, and `design-md/` inventory. Schema covers atmosphere, tokens, typography, components, layout, depth, do/don't guidance, responsive behavior, and prompt aids. | VoltAgent; `664b3e7`, 2026-06-16; MIT for repository material. | **Inspiration only.** The reusable contribution is the agent-readable design inventory format. Brand extracts are not authoritative brand documentation and may involve trademark, font, image, trade-dress, and factual-accuracy risks. |
| `transitions-refine-page` | <https://transitions.dev/refine.html> | Refine landing flow, skill/refine descriptions, and `terms.html`: beta status, user token/credit use, AI-written changes, review/version-control warnings, no warranty, MIT license. | Jakub Antalik / Transitions.dev; terms last updated June 2026; MIT for Refine. | **Experimental primary.** Promote reversible preview, human approval, semantic motion tokens, and review-before-commit. Do not promise stability or silently run a code-writing agent. |
| `transitions-dev-repo` | <https://github.com/Jakubantalik/transitions.dev> | Root inventory: showcase `index.html`, `prototypes.html`, `skill.html`, examples, `skills/transitions-dev/` with 18 references and `_root.css`, `build/extract.mjs`, templates, `refine/`, and `terms.html`. README states generated skill snippets remain synchronized with showcase source. | Jakub Antalik; `main`, 142 visible commits; latest immutable SHA was not available through the accessible history page. Refine is MIT; repository-wide root license was not visible. | **Specialized.** Promote single-source generation, reduced-motion guards, and pattern-specific motion. Avoid vendoring snippets until repository-wide license scope is clarified. |
| `motionsites` | <https://motionsites.ai> | Homepage metadata identified “MotionSites — Premium Website Prompts”; affiliates page was reachable. Homepage/terms body was not text-accessible. A browser-control fallback was attempted, but no browser backend was available. | MotionSites; individual authorship, revision history, and license not exposed. | **Unresolved/inaccessible.** No prompt, screenshot, template, or design rule was promoted. Treat all content as all-rights-reserved unless terms are verified. |
| `monokern-x-post` | <https://x.com/monokern/status/2071246711222055363?s=46> | Direct post, exact status-ID search, and author/status search returned no post body, media, transcript, or verified author explanation. | `@monokern` identity unverified; no accessible revision or license. | **Unresolved/inaccessible.** Do not quote, paraphrase, or infer the post. Recheck only through an official accessible post, author-provided mirror, or transcript. |
| `taste-skill-site` | <https://www.tasteskill.dev> | Homepage, skills list, v2 stability notice, project examples/marketing copy, and docs getting-started page. Site says v2 is the experimental default and documents brief inference, design-system selection, redesign, and preflight concepts. | Leon Lin and blueemi; live 2026 site; website license unstated; linked repo MIT. | **Experimental primary.** Promote workflow concepts only. Do not use marketing claims or showcased outputs as evidence of general quality. |
| `taste-skill-repo` | <https://github.com/Leonxlnx/taste-skill> | Root inventory: `.github/`, `assets/`, `examples/`, `research/`, `skills/`, `CHANGELOG.md`, `LICENSE`, `README.md`, scripts. Commit history and the current website establish fast iteration and experimental v2. | Leonxlnx contributors; `b177427`, 2026-07-04; MIT. | **Experimental practitioner.** Promote audit-first redesign, brief-to-direction mapping, honest preflight, and anti-pattern detection with exceptions. Reject blanket aesthetic bans and agent-control instructions as stable rules. |
| `kill-ai-slop` | <https://github.com/yetone/kill-ai-slop/tree/main/skill> | Root and skill inventories; `README.md`, `skill/README.md`, `skill/SKILL.md`, `skill/references/taxonomy.md`, `detection.md`, and `fixes.md`; GitHub license endpoint. The skill describes 23 visual/copy signals, contextual triage, grouped reporting, shared-system-first remediation, and visual re-verification. | yetone; `eb4857a3d75e0ac52d1c5f8bd628e29022fd1e75`, 2026-07-10; no root license or repository license declaration found. | **Inspiration only.** Promote original, exception-aware synthesis of the audit method and uncovered signal categories. Do not copy or adapt prose, examples, regexes, scanner code, or install instructions while the license is unresolved. |

## Additional primary and authoritative sources

| ID | Authority | Consulted areas | Primary use | Important limitation |
|---|---|---|---|---|
| `wcag-22` | W3C Recommendation | WCAG 2.2 abstract, status, success criteria, conformance, changes | Normative accessibility baseline and completion gates | Automated scans cannot prove conformance; supporting guidance and human evaluation remain necessary. |
| `wai-aria-apg` | W3C WAI task force | Pattern catalog, keyboard interfaces, landmarks, accessible names, dialog/tabs examples | Widget semantics and interaction matrices | Examples are illustrative, not drop-in proof of accessibility. |
| `mdn-web-docs` | Mozilla + contributors | HTML/CSS/JS references, accessibility, performance, compatibility, licensing | Cross-browser platform reference and feature status | Check specifications and browser-compatibility data for unstable features. |
| `webdev` | Google Chrome team | Learn HTML/CSS/forms/design/accessibility/testing, Web Vitals, strict CSP | Performance, responsive, browser-vendor, privacy/security guidance | Separate Chrome-specific implementation from interoperable standards. |
| `react-docs` | React team | Learn, state structure, state reset/preservation, DOM/built-ins | React architecture and behavior | Not a visual design system; retrieve only for React projects. |
| `nextjs-docs` | Vercel/Next.js | App Router getting started/guides, Pages Router status, rendering, metadata, security/testing indexes | Version-aware Next.js workflow | Router and version are mandatory filters; advice changes rapidly. |
| `vue-docs` | Vue team | Vue 3 introduction, accessibility, performance, architecture choices | Vue 3 implementation | Vue 2 is end-of-life and must not contaminate current guidance. |
| `svelte-docs` | Svelte team | Svelte overview/runes/transitions/testing; SvelteKit routing/forms/rendering/a11y/performance indexes | Svelte 5 and SvelteKit implementation | Migration state and use of SvelteKit versus standalone Svelte matter. |
| `astro-docs` | Astro team | Islands, rendering modes, server islands, images/i18n, view-transition accessibility | Low-JS content sites and incremental interactivity | Adapter/deployment constraints must be checked; islands are not automatically the right architecture. |
| `apple-hig` | Apple | Design principles, accessibility, motion, typography | Platform-aware craft and accessibility | Apple-specific measurements/assets are not universal web rules; documentation/assets are proprietary. |
| `material-3` | Google | M3 URLs; Material Web README, components/tokens, license, maintenance notice | Material patterns and tokens | M3 body required JavaScript; Material Web is in maintenance mode pending maintainers. |
| `fluent-2` | Microsoft | Accessibility, motion, global/alias tokens, repository licensing | Enterprise theming, high contrast, semantic tokens | Fonts and icons can have separate asset terms. |
| `carbon-design-system` | IBM | Accessibility overview/color/developer guidance; repository/release | Data-heavy enterprise components and tokens | Product integration still needs end-to-end testing. |
| `polaris` | Shopify | Current Polaris Web Components/reference docs; legacy accessibility; deprecation notice | Commerce/admin UI, content, forms, i18n | `polaris-react` is deprecated; current components are Shopify-surface-specific. |
| `primer-design-system` | GitHub | Primer overview, accessibility patterns/checklists, component guidance | Developer-tool UI and practical accessibility | GitHub brand/marks are separate from open code. |
| `govuk-design-system` | UK GDS | Components, accessibility, audited statement, Frontend release | Evidence-led forms, errors, public-service content | GOV.UK styling/brand is not a generic theme; using components alone does not make a service accessible. |
| `uswds` | U.S. GSA | Principles, accessibility strategy/report, components, repository/license exceptions | Public-service trust, accessibility, tokens, tests | CC0/public-domain status has explicit third-party exceptions; do not imply government affiliation. |
| `spectrum-design-system` | Adobe | Spectrum overview, color fundamentals/system, React Spectrum metadata | Perceptual color and adaptive design systems | Site/brand assets are proprietary even where code is Apache-2.0. |
| `react-aria` | Adobe | Getting started, component catalog, behavior/i18n examples | Accessible React behavior across modalities | React-specific and still requires labels, content, styling, integration, and testing. |
| `radix-primitives` | WorkOS/Radix | Introduction, accessibility, release notes, keyboard tables | Headless behavior/focus/keyboard implementation | Preview APIs are unstable; native elements may be simpler. |
| `atlassian-design-system` | Atlassian | Accessibility, content, tools, drag-and-drop alternatives | Enterprise content, tokens, and non-pointer alternatives | Package licenses vary; several resources are internal-only. |
| `lightning-design-system` | Salesforce | SLDS 2 shell, repository inventory/license, blueprints, a11y test scripts | Enterprise CRM blueprints/tokens | SLDS 2 site was only partly text-accessible; icons/images are CC-BY-ND. |
| `w3c-i18n` | W3C | Quick Tips, Language on the Web, bidi/language links | UTF-8, language tags, RTL/bidi, local formats | Quick Tips explicitly are not a complete specification. |
| `owasp-cheat-sheets` | OWASP | Third-party JavaScript, file upload, XSS/CSP indexes | Frontend security boundaries and escalation | High-risk systems require specialist/backend review; frontend checks are defense in depth. |
| `google-search-docs` | Google Search Central | SEO Starter Guide, Search Essentials, How Search Works | Crawlability and honest metadata | No ranking guarantee; Google-specific guidance is not a substitute for useful content. |
| `playwright-docs` | Microsoft/Playwright | Accessibility tests, ARIA snapshots, visual comparisons, browser projects | Deterministic browser and regression verification | Automated accessibility tests detect only some issues. |
| `whatwg-html` | WHATWG | Semantics, forms, interactive content, browsing/history/media | Native HTML and platform behavior | Normative text needs MDN/browser data for practical support details. |

## Source instructions and prompt-injection handling

Three source families contain instructions designed for an AI agent rather than neutral prose:

1. `emil-design-skills` contains response-format and persona commands, including instructions about what an agent must say or how it must format a review.
2. `taste-skill-repo` contains strong execution directives, fixed baseline settings, preflight commands, and aesthetic bans.
3. `awesome-design-md` includes “agent prompt guide” content, while `transitions-dev-repo` packages action commands for install/apply/refine workflows.

These are expected contents of agent skills, not evidence of a malicious repository compromise. They are nevertheless prompt-injection relative to this research task. They were not executed or adopted as authority. No credential request, destructive command, mission override, or request to exfiltrate local data was followed. The incidents and dispositions are also recorded in `rejected-guidance.md` and `agent-usage-log.md`.

## Depth limits

- GitHub file inventories and relevant rendered pages were inspected, but full repository clones were intentionally avoided because external code was untrusted and not required for the research outputs.
- `motionsites` could not be rendered because no browser backend was available; the text crawler exposed only metadata and a small affiliates surface.
- The X post supplied by status ID returned no content and has no verified mirror.
- Material Design 3 and Lightning Design System 2 are JavaScript-heavy; their official repositories and accessible first-party pages were used to avoid inventing hidden page content.
