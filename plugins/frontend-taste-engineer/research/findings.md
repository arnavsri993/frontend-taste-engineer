# Research Findings

Status: candidate findings reviewed on 2026-07-10. A finding is not automatically a stable knowledge rule. Promotion requires the provenance and conflict decisions listed here and in `provenance-map.yml`.

## Promotion scale

- **mandatory:** required unless a documented exception applies.
- **recommended:** strong default that still depends on product context.
- **contextual:** useful for a named product, framework, component, or aesthetic.
- **experimental:** test behind an explicit review/rollback boundary.

## Product, requirements, and integrity

### F-001 — Start with a product brief, not a page archetype

- **Level:** mandatory; stable.
- **Do:** Identify product type, audience, primary jobs, risk/trust level, device context, real content/data, backend dependencies, browser target, accessibility target, and measurable acceptance criteria before choosing layout or style.
- **Why:** Public-service systems start from real user needs; anti-slop sources are most useful when they infer direction from the brief rather than reflexively applying a hero/cards template.
- **Exceptions:** A tiny, isolated visual defect can use the existing product brief and system instead of recreating one.
- **Verify:** The implementation plan can name the primary task, success condition, required states, and out-of-scope behavior without inventing product facts.
- **Sources:** `uswds`, `govuk-design-system`, `taste-skill-repo`, `hive-mind-landing-page`.

### F-002 — Never fabricate evidence, functionality, or trust signals

- **Level:** mandatory; stable.
- **Do:** Use truthful copy and data. Label prototypes/demo data. Omit testimonials, metrics, integrations, security claims, prices, compliance badges, and product screenshots that are not supplied or verified.
- **Why:** Misleading interface content damages trust and can create legal/security risk; structured data and metadata must describe real content.
- **Exceptions:** Clearly marked fictional fixtures are acceptable in a development-only environment.
- **Verify:** Every factual claim has a supplied source; every control either works, is clearly disabled/unavailable, or is explicitly marked as a prototype.
- **Sources:** `google-search-docs`, `uswds`, `taste-skill-repo`, `hive-mind-landing-page`.

### F-003 — Audit an existing frontend before redesigning it

- **Level:** mandatory; stable.
- **Do:** Inventory routes, working interactions, state/data ownership, design tokens, dependencies, accessibility failures, responsive behavior, console errors, and high-value architecture before editing.
- **Why:** Aesthetic rewrites routinely regress functioning systems and erase useful constraints.
- **Exceptions:** None for redesigns; emergency remediation can narrow the audit to the incident surface.
- **Verify:** The plan explicitly lists what will be preserved, changed, and intentionally deferred, with before/after evidence.
- **Sources:** `taste-skill-site`, `taste-skill-repo`, `hive-mind-landing-page`, `playwright-docs`.

### F-004 — Define completion as tested behavior, not generated code

- **Level:** mandatory; stable.
- **Do:** Gate completion on real states, keyboard behavior, responsive checks, error/loading/empty paths, build/type/lint status, console state, accessibility review, and any performance budget in scope.
- **Why:** A generated page can look complete while controls, validation, mobile layout, and failure recovery remain absent.
- **Exceptions:** Report unrun checks honestly when tools or environments are unavailable.
- **Verify:** The handoff separates passed, failed, not-run, and manually inspected checks.
- **Sources:** `hive-mind-landing-page`, `taste-skill-repo`, `playwright-docs`, `wcag-22`.

## Information architecture and content

### F-005 — Preserve task and navigation state in URLs when users need to return or share

- **Level:** recommended; stable.
- **Do:** Put durable route, filter, sort, pagination, and selected-resource state in URLs when deep links, reload, history, or collaboration matter.
- **Why:** Browser history and shareable context are part of expected web behavior.
- **Exceptions:** Sensitive values, short-lived secrets, or excessively large state must not be placed in URLs.
- **Verify:** Reload, copy/paste, Back, Forward, and permission-changed cases preserve or safely recover the logical view.
- **Sources:** `whatwg-html`, `nextjs-docs`, `svelte-docs`, `astro-docs`.

### F-006 — Use labels that describe the destination or action

- **Level:** mandatory; stable.
- **Do:** Prefer specific verbs/nouns over vague labels such as “Click here,” “Learn more,” or icon-only actions without accessible names.
- **Why:** Clear labels reduce errors, improve scanning, help voice input, and create useful accessible names.
- **Exceptions:** A conventional icon may remain visually unlabeled when space is constrained, but it still needs an accessible name and often a discoverable tooltip.
- **Verify:** Links/actions remain distinguishable out of surrounding context and by accessible-name inspection.
- **Sources:** `primer-design-system`, `atlassian-design-system`, `wai-aria-apg`, `wcag-22`.

### F-007 — Write state messages that explain what happened and what to do next

- **Level:** mandatory; stable.
- **Do:** Error, warning, success, empty, offline, stale, and permission messages must name the condition, preserve user work where possible, and offer a concrete recovery action.
- **Why:** Tone alone or color alone cannot communicate operational state.
- **Exceptions:** Pure progress indicators may use concise labels, but completion/failure still needs an explicit outcome.
- **Verify:** Remove color/iconography and confirm the text still communicates state and recovery.
- **Sources:** `atlassian-design-system`, `govuk-design-system`, `uswds`, `wcag-22`.

### F-008 — Stress-test content before locking layout

- **Level:** recommended; stable.
- **Do:** Test long names, long translated strings, empty values, multiline labels, large numbers, dates/currency, RTL, and real validation messages.
- **Why:** Placeholder copy hides overflow, hierarchy, and localization failures.
- **Exceptions:** None for reusable components; one-off art-directed pages can document intentional clipping only for decorative content.
- **Verify:** No essential content clips, overlaps, becomes ambiguous, or changes source order at supported zoom/breakpoints.
- **Sources:** `w3c-i18n`, `polaris`, `uswds`, `mdn-web-docs`.

## Visual direction and design systems

### F-009 — State one design thesis and prove it through a few controlled levers

- **Level:** recommended; contextual.
- **Do:** Describe a product-appropriate visual thesis in one sentence, then express it through hierarchy, typography, composition, color/surface strategy, imagery, and motion—without adding every fashionable effect.
- **Why:** The strongest supplied example used a specific editorial thesis rather than a generic SaaS assembly.
- **Exceptions:** Mature products should usually evolve their existing thesis instead of replacing it.
- **Verify:** A reviewer can point to repeated, coherent decisions; removing decoration does not erase product hierarchy or usability.
- **Sources:** `hive-mind-landing-page`, `taste-skill-repo`, `apple-hig`, `awesome-design-md` (schema only).

### F-010 — Treat references as evidence of qualities, not as templates to clone

- **Level:** mandatory; stable.
- **Do:** Annotate what a reference contributes—density, rhythm, type contrast, motion behavior, or information structure—and recombine those qualities with the product’s own content and brand.
- **Why:** Brand-extracted DESIGN.md collections are not authoritative licenses to reproduce visual identity.
- **Exceptions:** Authorized implementation of a company’s own design system may use its exact tokens/assets under applicable terms.
- **Verify:** The result has independent content, hierarchy, assets, and token choices; provenance and asset licenses are documented.
- **Sources:** `awesome-design-md`, `apple-hig`, `material-3`, `primer-design-system`.

### F-011 — Choose a design-system strategy before adding components

- **Level:** mandatory; stable.
- **Do:** Decide among an existing product system, a platform/industry system, accessible headless primitives, or a small custom token layer. Record why it fits product, framework, accessibility, performance, and maintenance constraints.
- **Why:** Mixing systems ad hoc creates inconsistent semantics, styling, keyboard behavior, and dependencies.
- **Exceptions:** Incremental migration may temporarily bridge systems with an explicit deprecation plan.
- **Verify:** Every component maps to one source of behavior and one token vocabulary; duplicate primitives and uncontrolled variants are absent.
- **Sources:** `fluent-2`, `carbon-design-system`, `react-aria`, `radix-primitives`, `taste-skill-site`.

### F-012 — Use primitive tokens and semantic aliases as separate layers

- **Level:** recommended; stable.
- **Do:** Store raw palette/spacing/type values separately from role-based tokens such as `text-danger`, `surface-raised`, or `motion-enter-fast`.
- **Why:** Semantic aliases allow theme, high-contrast, brand, and density changes without rewriting component CSS.
- **Exceptions:** A tiny one-page artifact may use a smaller token set; repeated magic values still need consolidation.
- **Verify:** Components refer primarily to semantic roles; light/dark/high-contrast changes do not require editing component internals.
- **Sources:** `fluent-2`, `uswds`, `carbon-design-system`, `spectrum-design-system`.

### F-013 — Do not abstract before repeated needs are understood

- **Level:** recommended; stable.
- **Do:** Build the first concrete case cleanly, observe repeated anatomy/behavior, then extract a component with deliberate variants and escape hatches.
- **Why:** Premature abstraction produces ambiguous props, uncontrolled variants, and unusable universal cards/containers.
- **Exceptions:** Standards-backed primitives (button, dialog, field) already have well-known anatomy and can begin shared.
- **Verify:** Every variant has a named use case; no prop exists solely to patch one unexplained screen.
- **Sources:** `react-docs`, `radix-primitives`, `carbon-design-system`, `primer-design-system`.

## Layout, typography, and color

### F-014 — Build responsive behavior from content constraints, not device names

- **Level:** mandatory; stable.
- **Do:** Start with source order and the narrowest viable layout; add breakpoints or container queries when content or interaction stops working.
- **Why:** Fixed device categories miss text zoom, split views, embeds, foldables, and intermediate widths.
- **Exceptions:** Platform shells can have supported hardware classes, but components should still tolerate their actual container.
- **Verify:** Test between breakpoints, at zoom/text enlargement, in short viewports, and with long content.
- **Sources:** `webdev`, `mdn-web-docs`, `polaris`, `wcag-22`, `uswds`.

### F-015 — Keep DOM/source order meaningful when visual layout changes

- **Level:** mandatory; stable.
- **Do:** Ensure reading, focus, and task order remain logical without CSS positioning; do not reorder essential content only for a desktop composition.
- **Why:** Screen readers and keyboard users follow DOM/focus order, not an art-directed grid.
- **Exceptions:** Decorative media can move independently when it has no semantic or focus role.
- **Verify:** Disable CSS, navigate by keyboard, and inspect the accessibility tree at mobile and desktop layouts.
- **Sources:** `wcag-22`, `webdev`, `mdn-web-docs`.

### F-016 — Make typography resilient before making it distinctive

- **Level:** mandatory; stable.
- **Do:** Set readable size/line-height/measure, support text scaling, choose fallback metrics, reserve font space, and cover required scripts before adding expressive pairings or fluid scales.
- **Why:** Typography establishes hierarchy but can also cause layout shift, clipping, and inaccessible small/thin text.
- **Exceptions:** Display type can be more expressive when not used for dense or essential body content.
- **Verify:** Test font failure, slow loading, 200% text, multiple scripts, long headings, and cumulative layout shift.
- **Sources:** `apple-hig`, `webdev`, `mdn-web-docs`, `w3c-i18n`.

### F-017 — Encode color by role and pair it with non-color information

- **Level:** mandatory; stable.
- **Do:** Use semantic roles for text/surface/state/data; meet applicable contrast; add text, icon shape, pattern, or position so color is not the only signal.
- **Why:** Color perception varies, and theme changes can invalidate raw hex assumptions.
- **Exceptions:** Decorative color with no information content.
- **Verify:** Contrast checks in every theme/state, grayscale/color-vision simulation, forced-colors mode, and background-image extremes.
- **Sources:** `wcag-22`, `spectrum-design-system`, `carbon-design-system`, `fluent-2`.

### F-018 — Elevation, blur, glow, radius, and gradients need a job

- **Level:** recommended; contextual.
- **Do:** Use surface effects to convey hierarchy, separation, focus, brand, or spatial relation; remove effects that merely decorate every container.
- **Why:** AI-generated interfaces overuse cards, glass, glows, and pills, flattening hierarchy through uniform emphasis.
- **Exceptions:** An art-directed campaign may use a stronger motif when performance, contrast, and content clarity still pass.
- **Verify:** Explain each effect’s information role; disable it and determine whether meaning becomes worse or simply less trendy.
- **Sources:** `taste-skill-repo`, `hive-mind-landing-page`, `fluent-2`, `material-3`.

## Components, states, and forms

### F-019 — Prefer native HTML before ARIA or custom interaction

- **Level:** mandatory; stable.
- **Do:** Use native links, buttons, inputs, selects, details, headings, landmarks, and form semantics whenever they meet the requirement.
- **Why:** Native elements include semantics, keyboard behavior, form integration, and broad assistive-technology support that generic elements do not.
- **Exceptions:** A custom composite widget may require ARIA/APG behavior after proving native controls cannot meet the interaction.
- **Verify:** Inspect computed role/name/value, keyboard behavior, form submission, high contrast, and mobile inputs.
- **Sources:** `whatwg-html`, `wai-aria-apg`, `mdn-web-docs`, `polaris`.

### F-020 — Every reusable component needs an explicit state matrix

- **Level:** mandatory; stable.
- **Do:** Define relevant default, hover, focus-visible, active/pressed, selected/checked/indeterminate, disabled, read-only, loading, empty, error, warning, success, offline, stale, saving/saved, permission-denied, and destructive/undo states.
- **Why:** Missing state behavior is a frequent source of fake completeness and accessibility regressions.
- **Exceptions:** Omit states that cannot occur, but record that decision.
- **Verify:** Component tests or stories exercise every applicable state, including combinations and theme/responsive variants.
- **Sources:** `carbon-design-system`, `primer-design-system`, `react-aria`, `taste-skill-repo`.

### F-021 — Dialogs must manage focus as a workflow, not only as a trap

- **Level:** mandatory; stable.
- **Do:** Give a dialog a name; move focus to a sensible element on open; contain keyboard focus while modal; support expected dismissal; restore focus to the trigger or a logical successor on close.
- **Why:** Without restoration, keyboard and screen-reader users lose context; destructive dialogs may need a safe initial focus target.
- **Exceptions:** If the trigger is removed or navigation completes, focus the next logical destination instead.
- **Verify:** Open/close by keyboard, Escape, visible action, pointer, and after trigger removal; test when desktop dialog becomes a mobile drawer.
- **Sources:** `wai-aria-apg`, `radix-primitives`, `react-aria`, `polaris`.

### F-022 — Tooltips are supplementary, not a container for required information

- **Level:** mandatory; stable.
- **Do:** Keep essential labels/instructions visible or programmatically associated; use tooltips only for concise supplemental explanation, accessible on keyboard and pointer.
- **Why:** Hover is unavailable to many touch, keyboard, and assistive-technology users.
- **Exceptions:** Familiar icon buttons may use an accessible name plus tooltip for sighted discoverability.
- **Verify:** Complete the task without hover; ensure focus and dismissal behavior do not obscure other content.
- **Sources:** `primer-design-system`, `wcag-22`, `wai-aria-apg`.

### F-023 — Dragging requires an equivalent non-drag path

- **Level:** mandatory; stable.
- **Do:** Provide visible controls, menus, or forms to accomplish every drag outcome, announce the result, and support repeated operations.
- **Why:** Pointer dragging excludes keyboard, switch, voice, and some motor-impaired users.
- **Exceptions:** None for task-critical outcomes.
- **Verify:** Complete the entire workflow with keyboard only and without precise pointer gestures.
- **Sources:** `wcag-22`, `atlassian-design-system`, `apple-hig`.

### F-024 — Form errors must be associated, summarized when useful, and recoverable

- **Level:** mandatory; stable.
- **Do:** Keep user input, identify fields in error, connect messages programmatically, move/announce focus intentionally after submission, and show server/general errors without erasing field errors.
- **Why:** Color-only or transient validation leaves users unsure what failed and can destroy work.
- **Exceptions:** Inline-only feedback is sufficient for a single simple field when it is immediately announced and visible.
- **Verify:** Submit empty, malformed, expired, duplicate, offline, server-failed, and double-submit paths with keyboard and screen reader.
- **Sources:** `govuk-design-system`, `polaris`, `wcag-22`, `react-aria`.

### F-025 — Disabled is not a substitute for explaining unavailable actions

- **Level:** recommended; stable.
- **Do:** Prefer an enabled action that explains missing prerequisites, or pair disabled controls with persistent contextual guidance. Use read-only when values should remain discoverable/selectable.
- **Why:** Disabled controls often disappear from the focus order and provide no reason or recovery path.
- **Exceptions:** A temporarily disabled submit during an in-flight request can prevent duplicates when progress remains announced and failure recovers.
- **Verify:** Keyboard and screen-reader users can discover why the action is unavailable and how to enable it.
- **Sources:** `wcag-22`, `carbon-design-system`, `atlassian-design-system`.

## Motion and interaction

### F-026 — Motion must communicate relationship, feedback, or continuity

- **Level:** recommended; stable.
- **Do:** Name the purpose before animating: show cause/effect, preserve spatial continuity, confirm input, or soften a state change.
- **Why:** Random entrance effects and perpetual motion consume attention and can cause discomfort.
- **Exceptions:** Brand/celebratory motion can add delight when optional, brief, and non-blocking.
- **Verify:** Remove the animation and ask what information is lost; test repeated interaction, interruption, reversal, and reduced motion.
- **Sources:** `emil-design-skills`, `transitions-dev-repo`, `apple-hig`, `fluent-2`.

### F-027 — Select easing, origin, and duration from the interaction

- **Level:** recommended; contextual.
- **Do:** Entering UI should respond immediately; exiting UI should not delay the next task; anchored surfaces should reveal their trigger relationship; duration should scale with distance/complexity, not one global number.
- **Why:** A menu, modal, number change, and page transition have different spatial and temporal semantics.
- **Exceptions:** System/platform animations may provide appropriate built-in timing.
- **Verify:** Compare fast repeat actions, slow devices, large/small travel, and input modalities; confirm no interaction waits on animation completion unnecessarily.
- **Sources:** `emil-design-skills`, `transitions-dev-repo`, `apple-hig`, `fluent-2`.

### F-028 — Reduced motion is a behavioral alternative, not only duration zero

- **Level:** mandatory; stable.
- **Do:** Honor `prefers-reduced-motion`; remove parallax, zoom, large spatial travel, blur/depth changes, and repetitive movement; preserve status and continuity with instant changes or restrained fades where appropriate.
- **Why:** Some motion causes distraction, nausea, or loss of orientation; the information must remain available.
- **Exceptions:** Essential motion should be rare and documented; provide an alternate representation whenever possible.
- **Verify:** Run the complete flow with reduced motion enabled and ensure no information, focus cue, or completion signal disappears.
- **Sources:** `wcag-22`, `apple-hig`, `fluent-2`, `astro-docs`, `transitions-dev-repo`.

### F-029 — Preview experimental motion as reversible overrides

- **Level:** recommended; experimental.
- **Do:** Keep prototype adjustments isolated, review diffs, use version control, and require explicit approval before committing generated changes.
- **Why:** Live tuning is valuable, but agent-written motion can be incorrect, costly, or destabilizing.
- **Exceptions:** Deterministic local token changes can skip an agent call when behavior is fully understood.
- **Verify:** Revert cleanly, review all changed properties, and run interaction/accessibility/performance checks before merge.
- **Sources:** `transitions-refine-page`, `hive-mind-landing-page`.

## Accessibility, responsive behavior, and browser support

### F-030 — Accessibility is integrated into every lifecycle stage

- **Level:** mandatory; stable.
- **Do:** Put accessibility targets in the brief, semantics in architecture, state/keyboard behavior in components, contrast/reflow in visual review, and manual plus automated checks in verification.
- **Why:** A final scan cannot repair structural, content, and interaction decisions cheaply or completely.
- **Exceptions:** None; depth scales with scope and risk.
- **Verify:** Each plan/build/review artifact has applicable accessibility requirements and evidence.
- **Sources:** `wcag-22`, `uswds`, `govuk-design-system`, `carbon-design-system`, `playwright-docs`.

### F-031 — Focus must remain visible, unobscured, and logically ordered

- **Level:** mandatory; stable.
- **Do:** Preserve a strong `:focus-visible` indicator, avoid sticky layers covering it, and keep focus movement tied to user intent or necessary interruption.
- **Why:** Removing focus outlines or programmatically moving focus on background updates makes the interface unusable for keyboard users.
- **Exceptions:** Programmatic focus after errors, overlays, in-page navigation, or route change is appropriate when it advances the user’s task.
- **Verify:** Keyboard every path at zoom, with sticky headers/drawers, validation, route changes, and overlays.
- **Sources:** `wcag-22`, `polaris`, `radix-primitives`, `wai-aria-apg`.

### F-032 — Component-library accessibility is a starting point, not a product claim

- **Level:** mandatory; stable.
- **Do:** Test composed flows, labels/content, custom styling, focus order, and application state even when using Carbon, Polaris, Primer, USWDS, GOV.UK, React Aria, or Radix.
- **Why:** Accessible primitives can be assembled into an inaccessible page.
- **Exceptions:** None.
- **Verify:** Run keyboard/manual screen-reader spot checks, automated scans, zoom/reflow, touch, and user testing proportional to risk.
- **Sources:** `uswds`, `govuk-design-system`, `polaris`, `react-aria`, `radix-primitives`, `playwright-docs`.

### F-033 — Progressive enhancement protects core tasks

- **Level:** recommended; stable.
- **Do:** Deliver meaningful HTML and usable core navigation/forms before optional JavaScript; detect features and provide fallbacks for newer CSS/APIs.
- **Why:** Networks, scripts, browser features, and hydration can fail; HTML is the durable baseline.
- **Exceptions:** Highly interactive tools may require JavaScript, but must provide explicit loading/error/recovery states.
- **Verify:** Test with slow/failed scripts, unsupported features, offline/reconnect paths, and server-rendered markup.
- **Sources:** `whatwg-html`, `mdn-web-docs`, `webdev`, `astro-docs`, `uswds`.

## Performance and framework architecture

### F-034 — Choose rendering architecture from content and interaction needs

- **Level:** mandatory; stable.
- **Do:** Prefer static/server-rendered HTML for content-first pages; hydrate only interactive islands/boundaries; use client rendering where sustained app interactivity actually requires it.
- **Why:** Framework docs themselves warn that pure client SPAs can delay useful content and ship unnecessary JavaScript.
- **Exceptions:** Offline-first or highly stateful client applications may justify a larger client runtime after measuring tradeoffs.
- **Verify:** Record route rendering modes, JavaScript cost, hydration boundaries, cache behavior, and failure states.
- **Sources:** `vue-docs`, `nextjs-docs`, `svelte-docs`, `astro-docs`, `webdev`.

### F-035 — Performance claims require measured budgets and real-user context

- **Level:** mandatory; stable.
- **Do:** Define route/component budgets, measure LCP/INP/CLS and resource costs, inspect field data where available, and profile representative low-powered devices/networks.
- **Why:** “Fast” is not a build flag. Core Web Vitals measure distinct loading, responsiveness, and stability dimensions.
- **Exceptions:** Early prototypes can use provisional budgets but must not claim production performance.
- **Verify:** Report tool, environment, percentile/data source, thresholds, and regressions. Current “good” CWV thresholds are LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 at the 75th percentile.
- **Sources:** `webdev`, `mdn-web-docs`, `vue-docs`, `nextjs-docs`.

### F-036 — Images and fonts are layout, content, and performance decisions

- **Level:** mandatory; stable.
- **Do:** Provide dimensions/aspect ratio, responsive sources, correct priority/lazy loading, meaningful alt behavior, compression/format, font fallbacks, and limited required weights.
- **Why:** Media commonly dominates LCP and layout shift; decorative stock imagery can add cost without meaning.
- **Exceptions:** Pure decorative assets can have empty alternative text and lower priority.
- **Verify:** Test slow network, missing asset, narrow crop, high-density display, reduced data, and layout-shift traces.
- **Sources:** `webdev`, `mdn-web-docs`, `nextjs-docs`, `astro-docs`.

### F-037 — Add dependencies only for behavior worth owning

- **Level:** recommended; stable.
- **Do:** Check native platform capability, bundle/runtime cost, maintenance, license, accessibility, SSR/hydration, browser support, and replacement cost before adding a library.
- **Why:** Dependencies can solve complex behavior but also expand bundle size, attack surface, and upgrade burden.
- **Exceptions:** Mature tested primitives are often preferable to reimplementing complex composite widgets.
- **Verify:** The decision record explains the nontrivial behavior gained and includes a version/update plan.
- **Sources:** `vue-docs`, `radix-primitives`, `react-aria`, `owasp-cheat-sheets`.

## Security, privacy, SEO, and internationalization

### F-038 — Treat untrusted HTML, URLs, files, and third-party scripts as security boundaries

- **Level:** mandatory; stable.
- **Do:** Escape by context, sanitize only with proven libraries, validate protocols/destinations, constrain embeds, apply CSP as defense in depth, and send uploads to a server-side validation/scanning boundary.
- **Why:** Frontend rendering and CDN scripts can execute with user privileges; client validation cannot enforce authorization or file safety.
- **Exceptions:** Trusted compile-time content still needs a clear provenance boundary.
- **Verify:** Threat-model data sources/sinks, test malicious inputs, audit third-party scripts, and escalate high-risk flows to security specialists.
- **Sources:** `owasp-cheat-sheets`, `webdev`, `nextjs-docs`.

### F-039 — Metadata must be complete, unique, crawlable, and honest

- **Level:** mandatory for public pages; stable.
- **Do:** Supply useful title/description, canonical where needed, language/alternate metadata, crawlable internal links, social images, and valid structured data that matches visible content.
- **Why:** Metadata affects discovery and link previews, but fabricated markup is deceptive and can violate search policies.
- **Exceptions:** Authenticated/internal tools may intentionally block indexing and omit social metadata.
- **Verify:** Inspect rendered head, canonical/robots/sitemap behavior, social card, structured-data validation, and noindex boundaries.
- **Sources:** `google-search-docs`, `nextjs-docs`, `astro-docs`.

### F-040 — Internationalization affects data and layout, not only strings

- **Level:** mandatory when localization is in scope; stable.
- **Do:** Use UTF-8, BCP 47 language tags, locale-aware date/number/currency/plural formatting, logical CSS properties, RTL/bidi handling, script-capable fonts, translation-safe composition, and persistent locale routing.
- **Why:** Concatenated strings, fixed widths, physical left/right properties, and English-only forms fail beyond translation.
- **Exceptions:** A single-locale prototype may defer translation, but should not hard-code an architecture that blocks it when localization is a known requirement.
- **Verify:** Pseudo-localization, RTL, mixed-direction content, long strings, local inputs/names/addresses, sorting/search, and font coverage.
- **Sources:** `w3c-i18n`, `polaris`, `webdev`, `mdn-web-docs`.

## Verification and provenance

### F-041 — Combine automated, manual, and user-centered testing

- **Level:** mandatory; stable.
- **Do:** Use type/lint/unit/component/E2E/visual/a11y/performance automation, then keyboard, screen-reader spot checks, real-device/browser checks, content stress tests, and inclusive user testing proportional to risk.
- **Why:** Automated accessibility tools detect only a subset; snapshots can pass while workflows remain confusing or broken.
- **Exceptions:** Tiny changes may run a narrowed risk-based set, documented explicitly.
- **Verify:** Each acceptance criterion maps to evidence; failures and unrun checks are visible.
- **Sources:** `playwright-docs`, `wcag-22`, `uswds`, `govuk-design-system`.

### F-042 — Keep human-readable knowledge canonical and generated indexes disposable

- **Level:** mandatory; stable.
- **Do:** Store inspectable records in Git, derive search/embedding indexes deterministically, and include source IDs, review dates, stability, exceptions, and supersession metadata.
- **Why:** Retrieval indexes are difficult to review and can silently drift; source-backed records need normal diffs and reversible promotion.
- **Exceptions:** None; generated artifacts may be cached but never become the only source.
- **Verify:** Delete/rebuild the index and reproduce results from the repository; provenance lookup resolves every stable rule.
- **Sources:** `transitions-dev-repo` (generated skill from source), `hive-mind-landing-page` (trace/provenance), repository architecture decision.

### F-043 — Resolve conflicts by authority, scope, recency, and evidence

- **Level:** mandatory; stable.
- **Do:** Apply normative standards first for compliance, official platform/framework docs for implementation semantics, mature design systems for contextual patterns, and practitioner/inspiration sources for optional craft. Preserve the narrower context and newest verified version.
- **Why:** A confident aesthetic rule must not override accessibility, security, product integrity, or framework correctness.
- **Exceptions:** A documented product requirement may choose a different aesthetic, never a lower legal/safety baseline without explicit accountable review.
- **Verify:** Conflict records name competing claims, chosen resolution, exception, and revisit trigger.
- **Sources:** all registered sources; decision formalized in `architecture-decisions.md`.
