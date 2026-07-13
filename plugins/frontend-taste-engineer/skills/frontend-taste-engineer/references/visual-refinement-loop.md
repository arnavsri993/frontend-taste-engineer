# Visual refinement loop

Run this loop for every substantial autonomous build. Do not substitute source inspection for rendered inspection. For paid/client work, this loop is a completion gate—see `premium-quality-bar.md`.

## First capture

1. Run the application in its real development or preview mode.
2. Capture at least one meaningful desktop viewport and one meaningful mobile viewport. Include a short viewport or intermediate boundary when the composition is at risk.
3. Exercise the primary interaction before capturing any state-dependent view.
4. Record viewport, route, state, command/tool, and artifact path.

Keep real user names/messages in local project evidence only. Commit screenshots or traces only when the fixture is synthetic or publication was explicitly approved.

## Inspect

Compare the result against the design thesis and inspect:

- Brand test: without the logo wordmark, could this still be any startup’s page?
- First viewport: one composition, not a module dump (no unjustified stats/cards/badges).
- Reject list: Inter/Roboto identity, purple gradients, centered three-card heroes, glow/glass stacks, pill forests, fake proof, scroll-reveal-everything.
- Composition and reading sequence.
- Hierarchy and primary-message dominance.
- Typography, measure, wrapping, and loading behavior.
- Spacing rhythm, alignment, density, edge treatment, and the role of each major empty region.
- Color, contrast, materials, imagery, and icon consistency.
- Copy specificity (audience + outcome) and section necessity.
- Motion: ≤3 roles, purpose, interruption, repetition, reduced motion—not every section animating in.
- Mobile recomposition, short viewports, overflow, and touch targets.
- Focus visibility, keyboard path, console errors, and broken controls.

Name the three weaknesses with the largest effect on product fit, comprehension, character, or task completion. Prefer structural/identity issues over tiny polish.

## Refine and recapture

Implement all three fixes, rerun relevant checks, and capture the same viewports/states again. Inspect the revised output.

If the brand test still fails or the page still matches the default AI cluster, run a **second** refine pass focused only on:

1. Type/material identity
2. First viewport composition
3. Removal of generic chrome

Continue only when another change has meaningful value; stop when remaining issues are low impact or a real limitation blocks progress.

Examples of high-impact fixes: changing a generic centered composition, strengthening brand-level type, replacing vacant scale with content-led rhythm, repairing mobile hierarchy, rewriting weak headlines/CTAs, correcting type scale/measure, removing unjustified chrome, making a dead control real, adding one missing intentional focal/state motion role, or deleting scroll-reveal-everywhere.

## Evidence rules

- Never claim screenshot review when no rendered image was opened and inspected.
- Preserve before/after artifacts or record why only the final capture is retained.
- Record failed captures and runtime limitations.
- A build log does not prove visual quality; a screenshot does not prove keyboard or application behavior.
- Do not mark complete without the refine gate (and second pass when still generic).
