# Autonomous zero-brief build

Use this reference only for `autonomous-zero-brief-build`.

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
4. Infer the creative profile. Separate supplied facts from assumptions.
5. Write a one-sentence design thesis and update `DESIGN.md`.
6. Retrieve brief-stage rules only. Defer framework, component, motion, performance, and browser packets until those stages.
7. Write complete copy and implement the full experience.
8. Make visible controls real; implement reachable states and honest backend boundaries.
9. Integrate semantics, keyboard/focus, reduced motion, responsive behavior, and metadata.
10. Run the interface and capture desktop and mobile output.
11. Inspect against the thesis, run the anti-slop review, fix the three largest weaknesses, and inspect revised captures.
12. Run the production build and applicable tests; verify routes, assets, console, links, and overflow.
13. Report the result and limitations concisely.

Do not stop after steps 3–6. A brief, plan, mockup, scaffold, or default starter is not completion.

## Question boundary

Infer and continue for style, palette, type, sections, imagery treatment, motion, cards, device support, framework choice, and other reversible decisions.

Pause only for:

- A required credential.
- Approval for an irreversible external action.
- A legally material fact.
- Directly contradictory requirements.
- A critical factual asset with no honest substitute.

When a factual asset is unavailable, omit it, use an explicitly creative abstraction, or expose a clear integration boundary. Never fabricate it.

## Verification

- `DESIGN.md` names the mode, facts, assumptions, profile, and thesis.
- The initial retrieval packet excludes deferred implementation/refinement topics.
- The page contains finished copy and no placeholder section.
- Controls and relevant failure/recovery states work.
- Desktop and mobile captures exist and were actually inspected.
- The top-three weakness list maps to implemented changes and revised captures.
- The production build and applicable checks ran, or the exact blocker is reported.
