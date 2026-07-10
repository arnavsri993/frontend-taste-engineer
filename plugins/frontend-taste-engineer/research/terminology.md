# Canonical Terminology

Reviewed 2026-07-10. Use these terms consistently in skills, knowledge records, MCP results, audits, and evals.

## Knowledge and provenance

### Source classification

- **core:** authoritative, broadly applicable material suitable for baseline rules after review (for example WCAG, APG, MDN, web.dev, public-service systems, OWASP).
- **specialized:** authoritative or high-quality guidance for a named framework, platform, product domain, or component system.
- **experimental:** promising but explicitly beta, preview, unstable, rapidly changing, or insufficiently validated.
- **inspiration-only:** useful for visual exploration or vocabulary; not authoritative enough for implementation or compliance rules.
- **rejected:** reviewed and not accepted in its current form.
- **inaccessible:** substantive content could not be verified.
- **deprecated:** superseded or no longer maintained for new work.

### Rule status

- **stable:** source-backed, conflict-reviewed, and suitable for production retrieval within its recorded scope.
- **candidate:** researched but awaiting promotion review/evaluation.
- **experimental:** may be tried behind explicit testing/rollback; never silently presented as stable.
- **deprecated:** retained for migration/history but excluded from ordinary retrieval.
- **superseded:** replaced by a named record; preserve the link for traceability.

### Importance

- **mandatory:** required unless a record’s explicit exception applies. Usually grounded in accessibility, security, product integrity, functional correctness, or an explicit acceptance criterion.
- **recommended:** strong default; product/system context can justify another choice.
- **contextual:** useful only for named conditions, page types, frameworks, components, or aesthetics.

### Confidence

- **high:** multiple authoritative/primary sources agree, or one normative source directly governs the claim.
- **medium:** credible primary or practitioner support with context/implementation uncertainty.
- **low:** incomplete evidence, a single opinionated source, or a rapidly changing claim. Low-confidence items do not become mandatory.

### Evidence language

- **verified:** directly observed in the cited accessible source or test output.
- **reported:** asserted by a source about its own behavior; not independently reproduced here.
- **inferred:** reasoned from verified facts and labeled as such.
- **unresolved:** evidence was unavailable or conflicting; no content is invented.

### Canonical corpus

The human-readable, version-controlled knowledge records in Git. Generated search indexes, embeddings, databases, caches, reports, and MCP packets are derived artifacts and are not canonical.

### Knowledge packet

A compact MCP response containing only relevant records, mandatory rules, provenance, exceptions, and verification steps within a context budget. It is not a whole-document dump.

### Provenance

The chain from a knowledge record to stable source IDs, canonical URLs, revisions/access dates, license status, conflict decisions, and later supersession. A link alone is not complete provenance.

## Product and design

### Product brief

A concise statement of audience, jobs/tasks, content/data, trust/risk, device context, required functionality/states, dependencies, constraints, and acceptance criteria. It precedes visual direction.

### Design thesis

One product-specific sentence that explains the intended experience and the few visual/interaction levers used to express it. It is more concrete than a mood word and less prescriptive than a finished mockup.

### Art direction

The intentional coordination of imagery, typography, composition, color, and motion for a specific message/context. It does not mean direct imitation of a reference brand.

### Visual reference

An image or site used to identify qualities such as density, hierarchy, crop, rhythm, or motion. A reference is not automatically licensed, authoritative, or an implementation specification.

### Anti-slop

A quality-control practice that detects reflexive templates, arbitrary decoration, fake content/functionality, missing states, weak hierarchy, and unsupported claims. It is not a fixed aesthetic and does not prohibit patterns universally.

### Honest functionality

The property that every visible action, data point, state, and claim either works/exists as presented or is clearly identified as unavailable, disabled with reason, demo data, or prototype behavior.

### Fidelity

Measured similarity along named dimensions—hierarchy, typography, spacing, color, imagery/crop, and interaction—at a specified viewport/state. “Pixel perfect” is not used without a comparison artifact and tolerance.

### Affordance

Perceptible information suggesting how an element can be used. An affordance can be visual, semantic, textual, spatial, or behavioral; it is not synonymous with decoration.

## Design systems and components

### Design system

A governed collection of foundations/tokens, components, patterns, content guidance, accessibility behavior, documentation, tooling, releases, and contribution/deprecation practices. A component library alone is not a complete design system.

### Primitive token

A context-free raw value such as a color, length, font family, radius, or duration. Example: `blue-600`.

### Semantic token / alias token

A role-based name resolved from primitive tokens, such as `text-danger`, `surface-raised`, or `motion-enter-fast`. Components prefer semantic tokens so themes and system changes do not require internal rewrites.

### Component

A reusable interface unit with anatomy, semantics, states, input behavior, responsive behavior, accessibility contract, API, and tests.

### Primitive component

A low-level behavioral or structural component intended to be composed and styled, such as an accessible dialog or popover primitive. “Primitive” does not mean universally safe without labels/integration/testing.

### Pattern

A reusable solution to a user/task problem involving multiple elements or steps, such as address entry, filter/results, or destructive confirmation. A pattern includes context and content, not just component anatomy.

### Variant

A deliberate, documented alternative for a recurring use case. A one-off style patch is not automatically a variant.

### Escape hatch

A constrained way to handle a legitimate case outside standard variants without forking or weakening the system. Escape hatches require rationale and should not become the default customization path.

### Controlled / uncontrolled component

- **controlled:** the parent owns the state/value and updates it through callbacks.
- **uncontrolled:** the component owns initial/current state, while exposing appropriate events/defaults.

These are API/state-ownership terms, not quality rankings.

### Native HTML first

Use platform elements and behavior when they meet the requirement before recreating them with generic elements and ARIA. ARIA supplements missing semantics; it does not recreate all native behavior automatically.

## States and interaction

### State matrix

The explicit set of applicable component/product states and combinations, including visual treatment, semantics, keyboard/pointer/touch behavior, content, and transitions. States that cannot occur are marked not applicable rather than silently omitted.

### `focus` versus `focus-visible`

- **focus:** the element currently receives keyboard/input events.
- **focus-visible:** a styling heuristic indicating that a visible focus indicator should be shown (commonly for keyboard-like navigation).

Never remove focus indication without an equally visible alternative.

### Disabled versus read-only

- **disabled:** unavailable for interaction and often removed from focus/form submission; use only when that behavior is intended and the reason is discoverable.
- **read-only:** value remains available for reading/selection/focus in many controls but cannot be edited.

### Selected / checked / pressed

- **selected:** current item in a selection model (for example tab/listbox option).
- **checked:** boolean or mixed state for checkbox/radio/switch-like controls.
- **pressed:** toggle-button state or momentary active feedback, depending on semantics.

Do not interchange ARIA states based only on visual appearance.

### Modal

An interaction mode in which content outside the dialog is unavailable until the modal is dismissed/completed. Visual overlay alone does not make a surface modal; focus, semantics, and background interaction must match.

### Focus restoration

Returning focus after temporary UI closes to the logical trigger or successor, so keyboard and assistive-technology users keep their place.

### Optimistic state

UI that provisionally shows a successful mutation before authoritative confirmation. It must define pending, failure, retry/rollback, duplicate-action, and stale-data behavior.

### Stale state

Data known or suspected to be older than the authoritative source. It differs from loading (no current result) and offline (network unavailable).

### Interruptible / reversible motion

- **interruptible:** responds correctly when new input occurs before an animation finishes.
- **reversible:** transitions coherently when state reverses, without jumping through an artificial end state.

### Reduced motion

An alternate behavior honoring user preference by removing/replacing problematic travel, zoom, parallax, blur/depth, repetitive, or vestibular motion while preserving information and task flow. It is not merely “duration: 0” everywhere.

## Responsive and platform terms

### Responsive design

Layout/content/interaction adapt to available space, zoom, text size, input mode, orientation, and user preferences. It is broader than “mobile and desktop screenshots.”

### Adaptive design

Selection among distinct presentations or behaviors for known contexts/platforms. Responsive and adaptive techniques can coexist.

### Intrinsic layout

Layout driven by content and available space using platform sizing behavior (`min-content`, `max-content`, wrapping, grid/flex constraints) rather than fixed device dimensions.

### Breakpoint

A condition at which content or interaction requires restructuring. Name by purpose or token, not by assumed device brand.

### Container query

A style condition based on a containing element’s dimensions/style rather than the viewport. It is useful for reusable components embedded in different layouts.

### Reflow

Content’s ability to reorganize without loss or two-dimensional scrolling at the WCAG-defined zoom/viewport conditions, subject to legitimate exceptions such as data tables/maps.

### Progressive enhancement

Deliver a usable semantic core, then add optional styles/behavior when platform support and scripts are available. It is a resilience strategy, not an instruction that every app work fully without JavaScript.

### Feature detection

Test whether a required browser capability exists; do not infer support solely from user-agent strings.

## Rendering and performance

### CSR, SSR, SSG/prerendering

- **client-side rendering (CSR):** the browser constructs substantial UI from client JavaScript.
- **server-side rendering (SSR):** a server renders HTML for a request.
- **static site generation / prerendering (SSG):** HTML is produced before requests, usually at build time.

These can coexist per route or component. None guarantees performance/accessibility without measurement and correct behavior.

### Hydration

Client JavaScript attaches behavior/state to server- or statically-rendered HTML. Hydration cost and mismatch/failure states must be considered.

### Island

An independently interactive or dynamic region inside predominantly static/server-rendered content. Astro distinguishes client islands and server islands; do not generalize its exact API to other frameworks.

### Streaming

Sending/rendering parts of a response progressively. A streaming fallback must be meaningful, stable, and accessible; streaming does not remove error/loading-state design.

### Performance budget

A measurable limit for an artifact or user journey (for example JavaScript bytes, image weight, LCP/INP/CLS threshold, or interaction latency) with a measurement environment and regression policy.

### Core Web Vitals

The current stable web.dev/Chrome field metrics at review time:

- **LCP (Largest Contentful Paint):** loading/perceived main-content render.
- **INP (Interaction to Next Paint):** responsiveness across interactions.
- **CLS (Cumulative Layout Shift):** unexpected visual instability.

Threshold claims include the metric lifecycle, percentile, device/field source, and review date.

### Perceived performance

How responsive/available the product feels. Useful feedback, progressive content, and stable skeletons can improve perception but do not excuse slow objective performance or deceptive progress.

## Accessibility and testing

### Accessible

Usable by people with a broad range of abilities and assistive technologies in the stated context. Avoid claiming a whole product is “accessible” without scope/evidence.

### WCAG conformance

A formal claim that the complete page/process satisfies all applicable success criteria at a named WCAG version/level and conformance requirements. A library, component, or automated scan alone cannot establish it.

### Automated accessibility test

Machine-detectable checks for a subset of issues. Results are regression evidence, not a substitute for manual evaluation or user testing.

### Screen-reader spot check

A documented manual pass over representative tasks and states with a named screen reader/browser/platform. It is not a full assistive-technology conformance matrix.

### Visual regression

Comparison against a reviewed baseline for unintended visual change. It needs stable data/fonts/environment and should not approve inaccessible content merely because it matches.

### ARIA snapshot

A serialized representation of the accessibility tree used for structural assertions. It complements, but does not replace, interaction and assistive-technology testing.

### Completion gate status

- **passed:** evidence observed.
- **failed:** requirement not met.
- **not-run:** check was applicable but unavailable; reason recorded.
- **not-applicable:** check does not apply; rationale recorded.

“Not-run” is never silently converted to “passed.”

## Security, privacy, and trust

### Trust boundary

A point where data/code changes owner, privilege, or validation domain: user input, URL, CMS content, API data, upload, third-party script/embed, or server response.

### Sanitization versus escaping

- **escaping/encoding:** represent data safely for a specific output context.
- **sanitization:** remove/disallow unsafe structure from content intended to contain markup.

They are not interchangeable; use proven context-appropriate mechanisms.

### Content Security Policy (CSP)

A browser policy restricting executable/loadable resources. CSP is defense in depth against XSS, not a substitute for safe rendering and input handling.

### Honest metadata

Titles, structured data, social cards, canonical links, and robot directives that accurately describe visible, available content without fabricated ratings/reviews/claims.

### Dark pattern / deceptive pattern

An interaction that manipulates or obscures user choice, cost, consent, cancellation, privacy, or consequences. Visual polish does not mitigate deception.
