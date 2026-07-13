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
4. Infer the creative profile. Separate supplied facts from assumptions.
5. Write a one-sentence design thesis and update `DESIGN.md` with the **full visual system lock**: density profile, type pair/scale, spacing, color roles, material, first-viewport composition, ≤3 motion roles, avoid-list, and “Why this is not generic.”
6. Retrieve brief-stage rules only. Defer framework, component, performance, and browser packets until those stages. Catalog/template/motion-library pulls happen **only after** step 5. If motion intensity is medium-high/high or the prompt is explicitly kinetic, retrieve motion with `get_motion_guidance` and thesis-derived catalog queries from `pull-motion-and-elements.md`.
7. Write complete copy (text-only outline → finished page copy) and implement the full experience from the locked system—not from a template skin.
8. Make visible controls real; implement reachable states and honest backend boundaries.
9. Integrate semantics, keyboard/focus, reduced motion, responsive behavior, and metadata.
10. Run the interface and capture desktop and mobile output.
11. Inspect against the thesis and reject list, fix the three largest weaknesses, and inspect revised captures. If the brand test still fails or the AI cluster remains, run a second identity/first-viewport pass.
12. Run the production build and applicable tests; verify routes, assets, console, links, and overflow.
13. Report the result, **Why this is not generic**, and limitations concisely.

Do not stop after steps 3–6. A brief, plan, mockup, scaffold, or default starter is not completion. Starting from Magic UI / Aceternity / a SaaS template before the system lock is a process failure—restart from step 5.

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

- `DESIGN.md` names the mode, facts, assumptions, profile, thesis, system lock, and “why this is not generic.”
- The initial retrieval packet excludes deferred implementation topics; motion/catalog pulls occur only after the system lock (early only when kinetic / medium-high/high).
- Non-static builds name at most three motion roles and use thesis-derived catalog queries.
- The page contains finished copy and no placeholder section.
- First viewport obeys brand + one headline + one support + one CTA group + one visual plane.
- Controls and relevant failure/recovery states work.
- Desktop and mobile captures exist and were actually inspected; three weaknesses were fixed and recaptured.
- The production build and applicable checks ran, or the exact blocker is reported.
