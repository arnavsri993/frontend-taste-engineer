# Offline core rules

Load this file when the MCP server is unavailable or the work carries accessibility, security, or integrity risk.

## Product and integrity

- Identify the user, primary job, trust/risk level, device context, and true data/behavior before choosing visual patterns.
- Mark assumptions. Prefer reversible choices when requirements are unclear.
- Never invent metrics, customers, testimonials, integrations, screenshots, security guarantees, product behavior, or test results.
- Every visible control must work, be explicitly disabled with a reason, or be removed.
- Provide loading, empty, error, success, permission, offline/retry, destructive, and recovery states when the flow can reach them.

## Accessibility baseline

- Use semantic HTML and native controls before ARIA.
- Preserve logical source and focus order. Make focus visible and restore it after temporary overlays.
- Give every control a programmatic name; connect instructions and errors to the field.
- Support keyboard completion without traps. Provide Escape only where the interaction pattern expects it.
- Do not rely on color, position, hover, motion, or sound alone.
- Test text resizing, zoom/reflow, contrast, forced colors where relevant, and reduced motion.
- Automated checks supplement rather than replace keyboard and assistive-technology review.

## Responsive baseline

- Let content determine breakpoints. Test between breakpoints, not only at them.
- Preserve reading/task order when layout changes.
- Prevent horizontal overflow at narrow widths and 200% zoom.
- Use appropriate touch targets and spacing without making desktop layouts needlessly sparse.
- Account for long text, dynamic viewport units, virtual keyboards, safe areas, short viewports, and ultra-wide lines.

## Performance baseline

- Prefer the least client JavaScript and hydration that fulfills the interaction.
- Reserve image and font space, deliver appropriate sizes, and avoid decorative assets that dominate LCP.
- Limit font files/weights, third-party scripts, and animation work.
- Measure before claiming improvement. Distinguish lab checks from real-user data.

## Visual-quality baseline

- Write a design thesis before substantial styling.
- Use hierarchy, rhythm, composition, type, color, imagery, and motion to express product character.
- Treat minimalism as selective reduction, not blank scale: every major gap needs a hierarchy, grouping, pacing, focus, evidence, or boundary job.
- For a non-static direction, use a small motion grammar across focal, state, and feedback moments; preserve reduced-motion outcomes and never hide ordinary reading content behind generic reveals.
- Challenge generator defaults: centered hero, three cards, purple gradient, glow/glass, bento, pill, and rounded-card patterns require a product reason.
- Distinguish aesthetic preference from a usability or correctness defect.

## Engineering baseline

- Inspect and preserve useful architecture.
- Prefer composition over monolithic components and derived state over synchronized copies.
- Avoid new dependencies and abstractions without repeated need.
- Verify build, types, tests, console, URLs, assets, and failure paths proportionately.
