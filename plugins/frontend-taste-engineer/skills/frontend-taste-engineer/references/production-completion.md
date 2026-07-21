# Production completion

An autonomous build is complete only when it is a finished, deployable frontend rather than plausible source code. For paid/client work, also satisfy `premium-quality-bar.md`.

## Required outcome

- Complete semantic page structure and finished copy.
- Coherent tokens, typography, color/material, composition, imagery, and motion locked after diversified evidence retrieval and candidate comparison.
- First viewport as one composition with a hero-level brand signal.
- Functional visible controls and honest integration boundaries.
- Relevant default, hover, focus, active, disabled, loading, empty, error, success, offline, permission, saving, and recovery states.
- Responsive layouts that survive narrow, intermediate, wide, short, zoomed, and long-content conditions.
- Keyboard operation, visible focus, accessible names, non-color cues, contrast, errors, and reduced-motion support.
- Truthful route metadata and no placeholder content, dead actions, fake evidence, or unsupported claims.
- A credible **Why this is not generic** line the author would say to a paying client.

## Production checks

Run the project's applicable type, lint, unit/component/integration/end-to-end, and production build commands. Verify production routes and asset paths rather than only development mode.

Inspect:

- Desktop and mobile output after the refinement pass (and second pass if still generic).
- Console errors and warnings caused by the change.
- Broken links and missing assets.
- Horizontal overflow and clipped required content.
- Keyboard path and focus visibility.
- Reduced-motion behavior.
- Metadata and document structure.
- Performance implications of images, fonts, JavaScript, and animation.
- Private-term scan results for tracked files, added diffs, evidence, logs, and package archives when request-local content exists.

Do not claim screen-reader, cross-browser, accessibility, or performance results that were not observed. Mark them unverified and name the next check.

## Backend boundary

If a backend is absent, choose one:

- A complete local-only interaction whose scope is obvious.
- A real existing link, mail, or navigation action.
- An explicit integration boundary with no false success state.

Never pretend a form submitted, an account was created, data was saved, or an external service responded.

## Completion report

Lead with the user-visible result. Then state:

1. Visual direction (thesis, density profile, type pair) and functional scope.
2. **Why this is not generic.**
3. Motion roles or “static by intent.”
4. Production build and test results.
5. Screenshot viewports, three weaknesses fixed, and whether a second pass ran.
6. Material accessibility/responsive/state evidence.
7. Remaining limitations or unverified areas.

Keep the report concise. Internal assumptions and routine process belong in `DESIGN.md` or evidence artifacts, not a long user-facing narrative.

If you cannot write a credible “why this is not generic” line, the work is not complete.
