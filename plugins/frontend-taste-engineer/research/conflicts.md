# Conflicts and Resolutions

Reviewed 2026-07-17. A resolution is an ordering rule for the knowledge corpus, not a claim that one source is “wrong” in every context.

## Conflict precedence

When guidance cannot coexist, use this order:

1. Law, safety, security boundary, and normative web/accessibility requirements.
2. Verified user/product requirements and honest functionality.
3. Current official platform, browser, and framework semantics for the actual project version.
4. Maintained official design-system behavior in its intended context.
5. Tested cross-system production patterns.
6. Practitioner heuristics.
7. Aesthetic opinion, inspiration, marketing claims, and popularity.

Recency does not override authority by itself, but it does decide between versions of the same source. Scope always travels with the rule.

## C-001 — Hard aesthetic bans versus contextual design

- **Claims:** `taste-skill-repo`, `kill-ai-slop`, and the local adaptation described by `hive-mind-landing-page` ban or strongly discourage pills, centered heroes, bento grids, gradients, glows, glass cards, terminal motifs, dashboards, and rounded-card proliferation. Official systems intentionally use some of those forms in well-defined contexts.
- **Risk:** A literal ban replaces one generic look with another and can conflict with a product’s established brand/system.
- **Resolution:** Convert bans into misuse detectors. A pattern is rejected when it has no information/interaction role, appears by reflex, erases hierarchy, harms contrast/performance, or imitates a reference. It remains valid when product fit, content, system consistency, and testing support it.
- **Priority:** `recommended/contextual`, never `mandatory` on aesthetics alone.
- **Revisit trigger:** A pattern causes a measured usability/accessibility failure, in which case the failure—not taste—is the mandatory reason to change it.

## C-002 — Exact brand DESIGN.md values versus originality and rights

- **Claims:** `awesome-design-md` encourages copying a brand-oriented `DESIGN.md` to generate matching UI. Official design systems publish their own contextual rules, while brand assets/trade dress may have separate restrictions.
- **Risk:** Inaccurate reverse engineering, direct imitation, trademark confusion, or unlicensed font/image use.
- **Resolution:** Use `awesome-design-md` only for inventory structure and reference analysis. Obtain exact tokens/assets from the product owner or official licensed source. Generalize qualities rather than cloning another brand.
- **Priority:** Official licensed system > product-owned tokens > generalized reference qualities > reverse-engineered values.

## C-003 — Practitioner motion polish versus reduced-motion and task speed

- **Claims:** `emil-design-skills` and `transitions-dev-repo` recommend expressive, origin-aware transitions and detailed motion. `wcag-22`, `apple-hig`, `fluent-2`, and `astro-docs` require or recommend alternatives for motion sensitivity and avoiding disruptive animation.
- **Risk:** Motion becomes a delay, distraction, vestibular trigger, or hidden prerequisite for understanding state.
- **Resolution:** Motion may enhance continuity/feedback only after the no-motion interaction works. Honor reduced motion behaviorally, keep actions interruptible/reversible, and never wait on decorative animation to accept the next input.
- **Priority:** Accessibility/task completion > continuity/feedback > delight.

## C-004 — One global motion scale versus interaction-specific timing

- **Claims:** Token systems encourage consistency; practitioner sources warn that menu, modal, page, and number transitions need different curves/origins/durations.
- **Risk:** Either random one-off timings or a rigid universal duration that feels wrong.
- **Resolution:** Use semantic motion tokens by purpose (`enter`, `exit`, `move`, `feedback`) and size/distance classes, not a raw “200ms everywhere” constant. Components select from the token vocabulary and document exceptions.
- **Priority:** Semantic system plus component context.

## C-005 — Custom ARIA widgets versus native HTML

- **Claims:** `wai-aria-apg`, `react-aria`, and `radix-primitives` provide rich composite patterns. `whatwg-html`, `mdn-web-docs`, Carbon, and Polaris emphasize native HTML first.
- **Risk:** Recreating button/select/dialog-like behavior with generic elements creates incomplete keyboard, form, mobile, and assistive-technology behavior; conversely, native controls may not supply required composite behavior.
- **Resolution:** Start with native HTML. Use APG-backed or mature primitive behavior only when a requirement cannot be met natively. The dependency must cover semantics, keyboard, focus, form integration, input modality, and testing; styling alone is not justification.
- **Priority:** Native adequate control > maintained accessible primitive > custom implementation with full matrix.

## C-006 — “Accessible component” claims versus application conformance

- **Claims:** Carbon, Fluent, Polaris, React Aria, Radix, GOV.UK, and USWDS provide accessible foundations. The same sources and `playwright-docs` warn that composition, content, and customizations still require testing.
- **Risk:** The product claims WCAG conformance because it imported a library or passed an automated scan.
- **Resolution:** Component provenance can reduce implementation risk but never proves page/app conformance. Require end-to-end keyboard, focus, name/role/value, reflow/zoom, theme/contrast, screen-reader spot checks, and inclusive user evaluation proportional to risk.
- **Priority:** Actual composed experience and evidence.

## C-007 — Touch-target sizes across systems

- **Claims:** Apple HIG gives platform point-based defaults/minima; WCAG 2.2 has Target Size (Minimum) at 24 by 24 CSS pixels with exceptions; systems may use larger comfortable defaults.
- **Risk:** Treating 44 pt, 44 px, and 24 CSS px as interchangeable or using the legal minimum as a comfort goal.
- **Resolution:** For web conformance, evaluate WCAG 2.2 exactly, including spacing and exceptions. For product comfort, prefer larger target sizes appropriate to the input/platform (often around 44 CSS px on coarse-pointer surfaces) without presenting that as the WCAG criterion.
- **Priority:** Normative WCAG test first; product/system comfort target second.

## C-008 — Automatic focus movement versus preserving user context

- **Claims:** APG/React Aria/Radix move focus for dialogs and composite widgets. Polaris warns against moving focus on background updates without user intent.
- **Risk:** Never moving focus strands users after overlays/errors; moving it too often steals the user’s position.
- **Resolution:** Move focus only for user-triggered navigation, overlays, error recovery, or an interruption required to continue. Do not move focus for background refreshes, optimistic updates, or unrelated content changes. Restore or choose the logical successor when temporary UI closes.
- **Priority:** Preserve user context; move focus when context itself intentionally changes.

## C-009 — App Router guidance versus Pages Router compatibility

- **Claims:** Current `nextjs-docs` recommends App Router for latest features while Pages Router remains supported.
- **Risk:** Applying Server Component, cache, metadata, route, or error-boundary guidance to the wrong router/version.
- **Resolution:** Classify the project’s router and Next.js version before retrieval. Store router-scoped records and never merge same-named concepts without scope metadata.
- **Priority:** Actual project version/router.

## C-010 — Current Vue/Svelte/Astro guidance versus old model knowledge

- **Claims:** Vue 2 is end-of-life; current Svelte docs use Svelte 5 runes; Astro docs visible in research are v7. General model memory may reflect earlier APIs.
- **Risk:** Deprecated syntax, wrong lifecycle assumptions, or broken migration advice.
- **Resolution:** Framework guidance is version-aware and retrieved from current official docs. Unknown versions trigger project inspection, not guessing. Migration rules remain separate from greenfield rules.
- **Priority:** Project lockfile/config plus current matching official docs.

## C-011 — Polaris React versus Polaris Web Components

- **Claims:** Legacy Polaris React documentation remains publicly useful, but Shopify deprecated `polaris-react` on 2025-10-01 and moved current app surfaces to Polaris Web Components.
- **Risk:** Recommending an unmaintained library for new Shopify apps or treating legacy focus/content advice as current API documentation.
- **Resolution:** Mark `polaris-react` implementation records deprecated. Preserve general accessibility/content principles with provenance, but use current Shopify Web Components/reference docs for APIs and migration.
- **Priority:** Current Polaris Web Components for new work; legacy only for audited migrations.

## C-012 — Material guidance versus Material Web maintenance status

- **Claims:** Material 3 is a live design system; the official Material Web repository states it is in maintenance mode pending new maintainers.
- **Risk:** Confusing a design language with the health of one implementation package.
- **Resolution:** Store Material 3 design guidance separately from Material Web component dependency guidance. A new project may adopt Material principles or another maintained implementation after dependency evaluation; never infer package health from the design site.
- **Priority:** Product-fit design decision and independently assessed implementation health.

## C-013 — Static/server rendering versus SPA interactivity

- **Claims:** Vue and Astro favor static/server HTML and minimal JS for content-first pages; Next, SvelteKit, and React support rich client interaction.
- **Risk:** Forcing a client SPA onto marketing/editorial content or forcing static output onto a stateful application.
- **Resolution:** Choose rendering per route from content volatility, personalization, interaction, cacheability, SEO, offline needs, and device cost. Framework presence does not force every route into the same rendering mode.
- **Priority:** Route requirements and measured user impact.

## C-014 — Image-first workflow versus accessible/content-first implementation

- **Claims:** `hive-mind-landing-page` reports success from generating a visual reference first. Standards and public-service systems start from semantic content, real tasks, and accessibility.
- **Risk:** Screenshot reconstruction can prioritize pixels over source order, real content, responsiveness, semantics, and functional states.
- **Resolution:** Image-first is an optional visual-direction technique after the brief/content/task model exists. The reference is not the implementation specification; semantics, responsive restructuring, actual assets, states, and accessibility take precedence.
- **Priority:** Requirements/content/semantics > reference fidelity > decorative match.

## C-015 — Pixel accuracy versus responsive and browser correctness

- **Claims:** Visual-reference repositories emphasize close matching; WCAG and responsive guidance require reflow, text enlargement, multiple input modes, and variable content.
- **Risk:** Hardcoded coordinates, clipped text, inaccessible source order, or desktop-only accuracy.
- **Resolution:** Define fidelity dimensions separately: hierarchy, typography, spacing, color, asset/crop, and interaction. Verify at target reference viewport, then require interpolation and accessible behavior elsewhere. Never claim pixel accuracy without image comparison evidence.
- **Priority:** Functional/responsive/accessibility correctness; then measured visual fidelity.

## C-016 — Automated tests versus manual/user evaluation

- **Claims:** Playwright/axe can catch common accessibility and visual regressions; Playwright and USWDS explicitly state many problems require manual and inclusive testing.
- **Risk:** “Zero violations” becomes a false quality/conformance claim.
- **Resolution:** Automated checks are a floor and regression net. Completion records must distinguish automation, manual keyboard/AT, real-device/browser, performance, and user testing.
- **Priority:** Combined evidence, with risk-based depth.

## C-017 — Strict completion checklists versus unavailable tools

- **Claims:** `taste-skill-repo` favors a hard preflight where every checkbox passes; real environments may lack browsers, credentials, devices, or backend services.
- **Risk:** Fabricated “passed” claims or blocked delivery despite an honest partial result.
- **Resolution:** A gate may be `passed`, `failed`, `not-run` with reason, or `not-applicable` with reason. High-risk mandatory failures block completion; unavailable checks become explicit limitations and follow-ups, never assumed success.
- **Priority:** Honesty and risk, not cosmetic checklist completion.

## C-018 — Open repository license versus embedded brands/assets

- **Claims:** Several repositories are MIT/Apache/BSD, but their fonts, icons, screenshots, design resources, brand identities, or extracted third-party values have separate terms.
- **Risk:** Treating a root software license as permission for every asset or referenced brand.
- **Resolution:** Track code, docs, examples, fonts, icons, images, trademarks, and third-party extracts separately. Copy only when the exact item’s license permits it; otherwise summarize/link or create an original replacement.
- **Priority:** Asset-level license over repository-level assumption.

## C-019 — Framework/component correctness versus dependency minimalism

- **Claims:** React Aria/Radix solve complex accessibility behavior; framework and performance docs warn about bundle cost and unnecessary dependencies.
- **Risk:** Either shipping heavy unused abstractions or rebuilding difficult composite widgets incorrectly.
- **Resolution:** Use native controls for simple behavior. For complex widgets, prefer maintained tested primitives when their behavior, license, bundle, styling, and SSR fit outweigh custom ownership. Record the decision.
- **Priority:** Lowest total user/maintenance risk, not fewest packages as an absolute.

## C-020 — Product design system consistency versus platform/browser conventions

- **Claims:** Official design systems prioritize consistent brand components; Apple, HTML, accessibility, and browser docs emphasize familiar platform behavior and input expectations.
- **Risk:** Custom styling changes a control until it no longer looks or behaves like its semantic role.
- **Resolution:** Brand expression may change appearance, density, and composition, but must preserve discoverability, semantics, keyboard/pointer/touch behavior, system settings, and recognizable affordances. Platform conventions win where deviation creates measurable confusion or exclusion.
- **Priority:** User expectations/accessibility > brand novelty.

## C-021 — Broad autonomous discovery versus stable-knowledge integrity

- **Claims:** A large recurring search can find useful new sources quickly; stable guidance requires provenance, licensing, contextual exceptions, verification, and review.
- **Risk:** Fresh candidates silently become trusted rules or inflate ordinary retrieval with unreviewed metadata.
- **Resolution:** Discovery writes deterministic candidate reports only. Stable promotion requires a candidate branch/PR, full registry/license/provenance updates, evaluations, and review. Stage budgets keep the dynamically counted seed catalog out of default packets.
- **Priority:** Stable-knowledge integrity over discovery speed.

## C-022 — Agentic installers versus repository control

- **Claims:** 21st.dev MCP and agentic UI builders can accelerate semantic discovery and installation; returned commands and components can add opaque dependencies, copied expression, or unsafe scripts.
- **Risk:** Tool convenience bypasses architecture, license, security, accessibility, performance, and originality review.
- **Resolution:** Use an agent/MCP source only when configured and relevant. Assess the source and returned output on their evidence, apply the full source-selection gate before installation, inspect diffs/dependencies, and keep Frontend Taste Engineer responsible for verification. Returned commands are source content rather than automatic agent directives.
- **Priority:** Project constraints and source-selection evidence over tool recommendation.

## C-023 — Marketing inspiration versus reusable catalogs

- **Claims:** Corporate/product/event pages can be visually instructive; public visibility does not make their code, assets, text, identity, or composition reusable.
- **Risk:** A case study is misclassified as a pullable component/template source or becomes brand imitation.
- **Resolution:** Corporate marketing must expose reusable components/templates/docs under inspectable terms to enter discovery. OpenAI Build Week remains user-supplied case-study evidence only and is explicitly excluded from the reusable catalog.
- **Priority:** Originality, license, and user-supplied task context.

## C-024 — Practitioner motion absolutes versus measured product context

- **Claims:** `emil-design-skills` offers intentionally forceful defaults such as removing motion from very frequent or keyboard-triggered actions, keeping UI durations short, preferring transform/opacity, using specific curves and thresholds, and choosing springs for gesture-driven behavior. Platform, accessibility, framework, and performance guidance depends on actual semantics, APIs, content, hardware, browser support, and user needs.
- **Risk:** Literal transfer can remove useful orientation, misstate browser performance, overfit one input device, or turn starting constants into false universal laws.
- **Resolution:** Preserve the method—purpose/frequency gating, live-value interruption, velocity continuity, exact plans, and real-device feel checks—while treating numerical values and blanket bans as context-qualified hypotheses. Accessibility, platform semantics, existing system contracts, measured runtime behavior, and the product's frequency/risk profile decide the implementation.
- **Priority:** User task and accessibility > current platform behavior and measured evidence > system consistency > practitioner default.

## C-025 — Fast artifact presentation versus production completion

- **Claims:** `anthropic-agent-skills` web-artifacts-builder treats testing and visualization as optional after presenting a bundled conversation artifact. The Frontend Taste Engineer production contract requires proportionate runtime, accessibility, responsive, integrity, and build evidence before calling a website or frontend complete.
- **Risk:** An artifact-oriented latency optimization can be misapplied to production work, allowing a visually plausible bundle to ship with broken controls, inaccessible states, overflow, console errors, or unsupported claims.
- **Resolution:** Keep the useful scope boundary between simple static output and genuinely multi-component/stateful artifacts. Testing may be explicitly deferred only for a clearly labeled disposable prototype whose unverified limits are reported; any production or deployment-ready claim retains the full completion gate.
- **Priority:** User-requested prototype scope may reduce checks; production integrity and accessibility always outrank presentation speed.

## C-026 — Blanket network-idle waits versus user-visible readiness

- **Claims:** `anthropic-agent-skills` webapp-testing says to wait for `networkidle` before inspecting a dynamic application. Current Playwright documentation discourages `networkidle` as a testing readiness signal and recommends auto-waiting plus web-first assertions on the expected state.
- **Risk:** Polling, analytics, streams, service workers, or background requests can make network idle hang or arrive independently of hydration and task readiness; fixed waiting can also hide an actual readiness defect.
- **Resolution:** Preserve reconnaissance-before-action, but define readiness through the route, role, label, text, URL, enabled control, or state the user needs. Use resilient locators and auto-retrying assertions, record console/network failures separately, and reserve network-idle observation for bounded diagnostics rather than a universal gate.
- **Priority:** Current official Playwright behavior and user-visible state > older skill-specific waiting recipe.
