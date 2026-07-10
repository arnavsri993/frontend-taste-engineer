# Design brief

## Operating mode and evidence

- Operating mode: autonomous-zero-brief-build applied as a substantial redesign of the existing local review interface.
- Build mode: redesign. Preserve the dependency-free static architecture, local artifact loading, read-only knowledge search, evaluation summary, and Python server; add a standalone production build and one-command localhost.
- Supplied facts: build a website that houses the skill, includes a button to GitHub, demonstrates what the skill can build, avoids excessive text, and feels more technical and modern.
- Inspected facts: the repository identifies Frontend Taste Engineer as an installable Codex plugin; its documented workflow includes classification, contextual direction, implementation, desktop/mobile screenshot refinement, and production verification. The Git remote is `https://github.com/arnavsri993/frontend-taste-engineer.git`.
- Creative assumptions: visitors are developers and first-time evaluators; the website should be both a public-facing showcase and a useful local inspection surface; a dark precision-instrument treatment better supports the revised technical direction.

## Product and user

- Product type: technical editorial marketing page plus read-only repository explorer.
- Primary user and job: a developer evaluating the plugin should understand its standard, see a tangible contextual-design demonstration, and reach the GitHub repository.
- Trust/risk level: normal, but claims must remain source-backed because the page presents developer tooling.
- Device and environment: mobile and desktop browsers; one-command localhost and a standalone static build that can be published without repository-relative runtime dependencies.
- Known constraints: no external framework, font, telemetry, backend, fabricated metrics, customers, testimonials, or live-generation behavior.
- Assumptions to verify: the local explorer paths continue loading through `serve.py`; the interactive specimen reflows and remains operable by keyboard; the GitHub destination resolves.

## Design thesis

Use a compact precision-runtime interface—dark grid, signal color, terse system labels, and one contrasting editorial voice—to move developers from command to live context shift to inspectable evidence without repeating the promise, while keeping GitHub primary and every interaction accessible, fast, and honest.

## Direction

- Composition: asymmetric opening with a four-step build signal; one large interactive specimen; provenance explorer; install close. The separate method and principle sections are removed because they repeated the same thesis.
- Typography: system sans for utility and hierarchy, system serif for authored contrast, monospace for process/evidence labels; no external font request.
- Color and surfaces: near-black technical canvas, cyan structure, acid-green state/action signal, and contextual light/dark specimen surfaces; borders and grid rhythm provide grouping before cards.
- Imagery/iconography: CSS-authored diagrams and existing brand geometry only; no stock imagery or unlicensed external assets.
- Motion: small hover/press feedback and instant specimen state transitions; full reduced-motion equivalence.
- Familiarity vs. originality: familiar navigation, links, buttons, search, and select controls inside a distinctive technical-editorial composition.
- Patterns intentionally avoided: generic centered hero, three-card feature parade, unsupported social proof, fake live generation, purple glow/glass, oversized empty first viewport, and decorative dashboard metrics.

## System

- Existing system to preserve or extend: vanilla HTML/CSS/JavaScript, `serve.py`, generated knowledge index, source registry, and eval result files. `build.py` snapshots only the public read-only evidence required by the showcase into an ignored `dist/` artifact.
- Tokens and component strategy: role-based colors, one squared geometry family, native links/buttons/input/select, a pressed-button mode group, and progressive enhancement.
- Responsive strategy: preserve DOM reading order; collapse at content failure points around 1080, 820, and 560 pixels; recompose the specimen and explorer rather than shrinking them.
- Accessibility target: semantic landmarks/headings, skip link, keyboard-complete controls, visible focus, 44-pixel targets, live status where state changes, non-color selection cues, forced-colors support, and reduced motion.
- Performance budget: no third-party runtime, no external fonts, no raster media, one local stylesheet, one small local script, and useful semantic content before JavaScript executes.

## States and acceptance criteria

- Specimen: default editorial, selected/pressed context, hover, focus-visible, active, rapid repeated switching, and reduced-motion states.
- Artifact explorer: loading, loaded, unavailable, matching, empty filter, and filtered states.
- Clipboard: idle, loading, success, failure/recovery, and disabled-during-write states. Clipboard failure must not claim success.
- Acceptance: all GitHub actions use the verified remote; source-visible page copy is reduced below 200 words before dynamic corpus results; the specimen is explicitly labeled local; existing records and evaluation data load from the standalone build; no horizontal overflow at mobile and desktop widths; production server returns all assets at the site root; keyboard order follows source order; desktop and mobile screenshots are inspected and refined.

## Rendered refinement

- Desktop/mobile captures: current pass inspected the deployed-root opening and specimen at 1440 × 1000 and 390 × 844.
- Three highest-impact weaknesses: the original page repeated its thesis across six sections and 474 source-visible words; the light paper/workbench treatment read as editorial before technical; the rule explorer required exact substring order.
- Fixes implemented: reduced source-visible copy to 186 words and four sections, removed the duplicate method/principle surfaces, replaced the surrounding system with a compact dark precision-runtime direction, preserved contextual specimen art direction, and changed search to match every entered term regardless of order.
- Revised captures and remaining limitations: desktop document height fell from 5,652 to 3,672 pixels and mobile from 7,568 to 4,660 pixels; both named viewports retain zero horizontal overflow. The GitHub action, local specimen state, 78 canonical rules, new concise-copy rule, flexible rule search, source/eval artifacts, and copy action remain live. Visible focus was observed, but the browser harness did not synthesize native button activation from Enter, so real-device keyboard activation, full screen-reader behavior, forced-colors rendering, and cross-browser behavior remain unverified.
