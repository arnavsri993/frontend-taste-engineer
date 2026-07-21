# Frontend Taste Engineer — Marketing Site Design

## Product summary

Frontend Taste Engineer is an installable Codex plugin that expands minimal frontend requests into complete, context-aware, responsive, accessible, screenshot-refined, deployment-ready implementations. It combines a compact operating Skill, a local MCP retrieval server, a canonical knowledge corpus, and a dynamically maintained, safely gated source catalog. No credentials, analytics, or telemetry are required for core operation.

## Audience

Frontend engineers, design engineers, and Codex users who need production-quality frontends from short prompts—not wireframes, templates, or plausible first drafts.

## Site goals

1. Explain what the plugin does with repository-accurate claims.
2. Demonstrate context-adaptive taste through an interactive workflow preview.
3. Make installation and validation commands copyable.
4. Build trust through honest limitations and architecture transparency.
5. Deploy cleanly to Vercel.

## Information architecture

Single long-form homepage with anchor navigation:

Navigation → Hero → Taste Lab (demo) → Problem → Capabilities → Workflow → Context-adaptive taste → Architecture → Safe sources → Supported work → Starter prompts → Install → Limitations → FAQ → CTA/Footer

## Design thesis

**Measured taste as engineering discipline** — the site reads like a calibration instrument: editorial precision, inspection overlays, and structured data surfaces that make deliberate visual decisions legible rather than decorative.

## Color

- **Ink** `#0F1A1A` — primary text, structural lines
- **Paper** `#F7F5F0` — warm off-white background
- **Teal** `#0B6E69` — brand foundation (from plugin.json)
- **Mint accent** `#C8F0A0` — restrained chartreuse for highlights and calibration marks
- **Warm gold** `#FFCF70` — secondary accent from logo calibration dot
- **Neutral grays** `#5C6B6A`, `#D4DCD9`, `#E8EDEB` — supporting UI

## Typography

- **Display/headings**: `"Instrument Serif", Georgia, serif` — editorial, measured
- **Body/UI**: `"IBM Plex Sans", system-ui, sans-serif` — precise, readable
- **Mono/terminal**: `"IBM Plex Mono", ui-monospace, monospace` — commands, data, annotations

## Layout

- Max content width 72rem with generous horizontal padding
- Section rhythm: 5–8rem vertical spacing on desktop, 3–5rem mobile
- Grid overlays and measurement marks as subtle background motifs
- Browser-frame containers for demo previews
- No identical card grids; varied section layouts (comparison tables, calibration scales, process diagrams, matrices)

## Imagery

- Plugin logo and icon from repository assets
- SVG-based inspection overlays, annotation lines, calibration scales
- Miniature responsive previews built in CSS (no stock photography)

## Motion

- CSS transitions for hover, focus, and stage transitions
- `prefers-reduced-motion`: disable stage auto-advance and reduce transitions
- Demo stage progression uses timed steps with manual override

## Accessibility

- Semantic landmarks (`header`, `nav`, `main`, `footer`)
- Logical heading hierarchy (single h1)
- Visible `:focus-visible` rings in teal
- Keyboard-operable demo controls and copy buttons
- FAQ accordions with `aria-expanded`
- 4.5:1+ contrast on body text
- 44px minimum tap targets on mobile
- No horizontal overflow at 320px

## Content integrity rules

- No invented user counts, testimonials, benchmarks, or integrations
- Demo labeled "Interactive workflow preview" — not real generation
- Plugin version read from plugin.json at build time
- MIT license and no-analytics claim only where repository confirms
