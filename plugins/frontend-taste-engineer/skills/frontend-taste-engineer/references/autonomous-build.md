# Autonomous zero-brief build

Use this reference only for `autonomous-zero-brief-build`. For paid/client quality, also obey `premium-quality-bar.md`.

## Trigger decision

Select the mode when all are true:

- The user asks to create or substantially redesign a website, site, page, landing page, frontend, portfolio, product presentation, or visual web experience.
- The prompt leaves major reversible product, content, or visual choices unspecified.
- The requested surface is at least a page, not a tiny correction or isolated component.

Examples include “Build a site for my robotics team,” “Turn this sentence into a website,” “Make this page stunning,” and “Make this product look premium.”

Do not select it for a padding/color/typo fix, a named component, audit-only work, screenshot reconstruction, or explicit accessibility, performance, or motion remediation. If a minimal prompt asks to redesign an existing page, keep this mode but set `build_mode` to `redesign` and preserve working behavior.

## Required sequence

1. Inspect repository structure, framework, routes, assets, dependencies, existing conventions, and the running product when available.
2. Decide new build versus redesign. Record what must be preserved.
3. Classify the exact prompt. Extract people, quoted text, products, groups, events, and concepts.
4. Classify constraints only. Separate supplied facts from assumptions; do not preselect visual styling.
5. Classify the site as a single document, multi-page site, or application. Map every proposed top-level navigation item to a real route, application state, or intentional in-page landmark before styling. Default distinct header destinations to same-tab routes with stable URLs. Do not invent thin pages to fill navigation.
6. Ask one batch of at most four questions if essential product information is missing. If the user says to use judgment or the run is noninteractive, record reversible defaults and continue.
7. Retrieve a diversified brief packet: core UX, source-derived design, copy, responsive, accessibility, integrity, and verification. Defer framework, component, performance, and browser packets until those stages.
8. Generate two or three materially different candidate directions, compare them, and record applied/rejected evidence.
9. Select one, then lock `DESIGN.md` and `CONTENT.md`, including the route/destination map. Write complete copy and implement the full experience from the locked system—not from a template skin.
10. Make visible controls real; implement reachable states and honest backend boundaries.
11. Integrate semantics, keyboard/focus, reduced motion, responsive behavior, route metadata, and direct-entry behavior.
12. Run the interface and capture desktop and mobile output.
13. Inspect against the thesis and reject list, fix the three largest weaknesses, and inspect revised captures. If the brand test still fails or the AI cluster remains, run a second identity/first-viewport pass.
14. Run the production build and applicable tests; verify direct routes, URL/history behavior, assets, console, links, and overflow.
15. Report the result, **Why this is not generic**, and limitations concisely.

Do not stop after steps 3–8. A brief, plan, mockup, scaffold, or default starter is not completion. Starting from Magic UI / Aceternity / a SaaS template without source retrieval, candidate comparison, and the implementation/license gate is a process failure.

## Question boundary

Offer one bounded clarification batch when essential context is missing. After that, infer and continue for style, palette, type, sections, imagery treatment, motion, cards, device support, framework choice, and other reversible decisions.

Pause only for:

- A required credential.
- Approval for an irreversible external action.
- A legally material fact.
- Directly contradictory requirements.
- A critical factual asset with no honest substitute.

When a factual asset is unavailable, omit it, use an explicitly creative abstraction, or expose a clear integration boundary. Never fabricate it.

## Verification

- `DESIGN.md` names constraints, candidate directions, retrieved/applied/rejected evidence, the selected thesis/system, and “why this is not generic”; `CONTENT.md` locks facts, hierarchy, site shape, route/destination map, actions, state copy, and responsive copy.
- The initial retrieval packet precedes direction lock and excludes deferred implementation topics.
- Non-static builds name at most three motion roles and use thesis-derived catalog queries.
- The page contains finished copy and no placeholder section.
- First viewport obeys brand + one headline + one support + one CTA group + one visual plane.
- Distinct top-level destinations use real same-tab routes by default; fragments are intentional single-document navigation or contextual tables of contents, and direct entry plus back/forward behavior works.
- Controls and relevant failure/recovery states work.
- Desktop and mobile captures exist and were actually inspected; three weaknesses were fixed and recaptured.
- The production build and applicable checks ran, or the exact blocker is reported.
