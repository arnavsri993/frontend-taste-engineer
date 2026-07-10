# Visual refinement loop

Run this loop for every substantial autonomous build. Do not substitute source inspection for rendered inspection.

## First capture

1. Run the application in its real development or preview mode.
2. Capture at least one meaningful desktop viewport and one meaningful mobile viewport. Include a short viewport or intermediate boundary when the composition is at risk.
3. Exercise the primary interaction before capturing any state-dependent view.
4. Record viewport, route, state, command/tool, and artifact path.

Keep real user names/messages in local project evidence only. Commit screenshots or traces only when the fixture is synthetic or publication was explicitly approved.

## Inspect

Compare the result against the design thesis and inspect:

- Composition and reading sequence.
- Hierarchy and primary-message dominance.
- Typography, measure, wrapping, and loading behavior.
- Spacing rhythm, alignment, density, and edge treatment.
- Color, contrast, materials, imagery, and icon consistency.
- Copy specificity and section necessity.
- Motion purpose, interruption, repetition, and reduced motion.
- Mobile recomposition, short viewports, overflow, and touch targets.
- Focus visibility, keyboard path, console errors, and broken controls.
- Generic generated patterns and visually disconnected sections.

Name the three weaknesses with the largest effect on product fit, comprehension, character, or task completion. Do not spend the pass on three tiny polish details while a structural issue remains.

## Refine and recapture

Implement all three fixes, rerun relevant checks, and capture the same viewports/states again. Inspect the revised output. Continue only when another change has meaningful value; stop when remaining issues are low impact or a real limitation blocks progress.

Examples of high-impact fixes include changing a generic centered composition, repairing mobile hierarchy, replacing weak copy, correcting type scale/measure, removing unjustified chrome, making a dead control real, or simplifying distracting motion.

## Evidence rules

- Never claim screenshot review when no rendered image was opened and inspected.
- Preserve before/after artifacts or record why only the final capture is retained.
- Record failed captures and runtime limitations.
- A build log does not prove visual quality; a screenshot does not prove keyboard or application behavior.
