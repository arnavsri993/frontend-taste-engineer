# Design brief — Leonida Heat Ledger

## Operating mode and evidence

- Operating mode: `autonomous-zero-brief-build` inside the existing dependency-free review-app deployment shell.
- Task size: single-page promotional frontend replacement.
- Supplied fact: the user requested a frontend for GTA VI after syncing the latest Frontend Taste Engineer skill from GitHub.
- Verified current facts: Rockstar's official GTA VI page lists a November 19, 2026 release for PlayStation 5 and Xbox Series X|S, and describes Jason and Lucia in Vice City and across Leonida.
- Inspected project facts: `review-app/` is the repository's standalone deployable example; `website/` is the plugin marketing site and is not the product-demo target. The shell supports dependency-free HTML, CSS, JavaScript, a Python build, and SPA-style preview fallback.
- Integrity boundary: this is an unofficial fan-made interface concept. It does not use Rockstar or GTA logos, official screenshots, trailer frames, character likenesses, key art, maps, audio, or copied marketing layouts. Factual outbound actions point to Rockstar.

## Product, audience, and jobs

- Product type: expressive entertainment landing page / fan-made release briefing.
- Primary audience: GTA VI followers who want a fast, atmospheric view of the currently confirmed release information.
- Primary job: understand the release status and enter the concept's editorial dispatch.
- Secondary jobs: switch the visual dispatch between daylight and midnight, explore the confirmed story setup, and follow the official Rockstar source.
- Trust and risk: medium. Brand, copyright, release-date, and platform details must remain clearly attributed and never imply official affiliation.
- Device context: mobile and desktop; touch, keyboard, zoom/reflow, short viewports, reduced motion, and forced-colors support.

## Design thesis

Build a sun-bleached Gulf-coast dispatch ledger that crosses into humid cobalt night through a blunt asymmetric headline, original screen-print cartography, and tactile controls—preserving a plain, unmistakably unofficial path to Rockstar's verified release information instead of imitating official GTA key art or a generic cinematic game template.

## Locked visual system

- Density profile: `marketing-landing`; paced editorial strips, one major story beat at a time, no card grid.
- Type pair: **Rockwell Extra Bold / Rockwell** for wide editorial display, **Avenir Next / Segoe UI / Trebuchet MS** for reading, and **Menlo / Consolas** for dispatch metadata. No Inter, Roboto, Arial, Pricedown-like lettering, or official GTA wordmark treatment.
- Type scale: display `clamp(4.4rem, 12vw, 11.5rem)` at `0.78` line-height; H2 `clamp(3rem, 7vw, 7rem)` at `0.86`; lead `clamp(1.15rem, 2vw, 1.55rem)`; body `1rem–1.125rem`; metadata `0.72rem` with tracked uppercase labels.
- Spacing scale: 8px base; steps 8 / 16 / 24 / 40 / 64 / 96 / 144; section rhythm `clamp(5rem, 10vw, 9rem)`.
- Color roles: asphalt ink `#111310`; newsprint background `#f2e8d1`; warm-white surface `#fffdf6`; sun accent `#ffc145`; coral alert `#f45b55`; lagoon detail `#168c86`; cobalt night `#263b63`; mangrove `#1d402f`. One warm sun/coral accent family controls emphasis; lagoon and cobalt define environmental planes.
- Material: flat ink and weathered newsprint with offset screen-print shadows; halftone texture is decorative and never sits behind reading text.
- Signature signals: a continuous horizon/road stripe; narrow dispatch metadata rails; warm editorial photography with ink-stamped interface framing.
- First viewport: edge-to-edge split plane with request-local brand signal, one blunt headline, one support sentence, one CTA group, a factual release rail, and one dominant original coastal photograph. No stats, promo chips, badges, card clusters, or social proof.
- Imagery: original AI-generated editorial photography of a fictional Gulf-coast causeway by day and a rain-darkened coastal boulevard at night. No official assets, copied frames, brand marks, or recognizable characters.
- Why this is not generic: the page behaves like a physical Gulf-coast dispatch ledger—the same horizon rule, offset-ink typography, and day-to-night editorial map system organize every section, rather than applying neon glass and feature cards to a game logo.

## Motion grammar

At most three roles:

1. **Focal:** a one-time 520ms broadcast-tune-in mask reveals the hero art and headline; reduced motion renders both immediately.
2. **State:** the daylight/midnight dispatch switch crossfades colors and repositions the route line for orientation; reduced motion swaps instantly without movement.
3. **Feedback:** buttons compress by 2px with their offset shadow and the copy-link status appears immediately; reduced motion keeps the visual pressed/state change without transition.

Intentionally static: body copy, story sections, release facts, and all ordinary reading content. There is no universal scroll reveal, parallax, scroll hijacking, custom cursor, or looping text marquee.

## Text-only content outline

1. Skip link and compact masthead: `LEONIDA / HEAT LEDGER`, dispatch anchors, theme switch, and external official source.
2. First viewport: `VICE CITY RUNS HOT.`; one sentence naming Jason, Lucia, Vice City, Leonida, and the verified November 19, 2026 release; actions `Open the dispatch` and `Visit Rockstar`; factual release rail.
3. Situation report: `Two names. One state.` with a concise paraphrase of the confirmed story setup and an original route graphic.
4. Environment chapter: `Daylight lies. Midnight keeps receipts.` with a real daylight/midnight control that changes the photographic dispatch, caption, and live status.
5. Release strip: `The date is on the wire.` with date, platforms, attribution, and one external official action.
6. Footer: clear unofficial-concept disclosure, source link, local build statement, and back-to-top action.

## Interaction and state ownership

- Native anchor links own navigation; the URL hash preserves section position.
- A native button group owns the `daylight` / `midnight` view. `aria-pressed`, visible labels, caption copy, root `data-dispatch`, and the live status derive from the same JavaScript state.
- Mobile navigation uses a real button with `aria-expanded`; Escape closes it and focus returns to the opener.
- The source-copy control writes the official URL to the clipboard when available; failure exposes the selectable URL and a recovery message without claiming success.
- LocalStorage remembers only the visual dispatch preference. No user data is sent or implied.
- External links state their destination and open in the same tab unless the user explicitly chooses otherwise.

## Required states

- Navigation: desktop, mobile closed, mobile open, focus-visible, current hash, Escape close.
- Dispatch: daylight selected, midnight selected, returning preference, reduced motion, storage unavailable fallback.
- Copy source: default, copying, success, failure/recovery.
- External source: default, hover, focus-visible, active.
- Runtime: JavaScript unavailable (core content and official link remain visible), image unavailable (solid framed fallback and captions remain), offline (local page still works; external link remains an honest boundary).

## Accessibility and responsive acceptance

- Semantic landmarks, one page `h1`, ordered headings, skip link, native buttons/links, programmatic names, live status, and visible high-contrast focus.
- Minimum 44px clustered targets; no color-only state; captions and pressed labels express day/night state.
- Body copy always rests on solid high-contrast material. Decorative art is `aria-hidden`; the meaningful visual state is described in text.
- Layout recomposes at content-driven boundaries. From 320 CSS pixels upward: no page-level horizontal scroll, no clipped CTA, no obscured footer, and no text smaller than 16px for body copy.
- At 200% zoom: reading and interaction order survive; the release rail stacks rather than shrinking.
- Forced colors retains borders, focus, native controls, and selected-state text. Reduced motion removes the mask, route trace, crossfade, and smooth scrolling.

## Performance and verification plan

- No third-party runtime, remote font, analytics, official media, or motion library. One stylesheet, one deferred script, and two optimized original JPEG photographs with explicit dimensions.
- Run JavaScript syntax, Python compilation, production build, repository accessibility audit, direct route/asset/header checks, and applicable repository release gates.
- Verify keyboard path, focus visibility, mobile menu Escape/return focus, dispatch state, clipboard recovery, localStorage reload, offline shell behavior, console state, reduced motion, 320px reflow, intermediate width, short viewport, and page-level overflow.
- Capture and inspect desktop and mobile primary views plus the midnight state. Name and fix the three highest-impact weaknesses, then recapture matching viewports; run a second identity/first-viewport pass if the brand test still fails.

## Known limitations

- The interface is an original fan concept and not a Rockstar product, pre-order flow, gameplay demo, or complete game-information source.
- Release information can change; the visible date and platform list are attributed to the official Rockstar page and should be rechecked before publication.
- Real screen-reader output, physical-device behavior, and non-Chromium browsers require separate verification before a public launch.

## Rendered refinement and image provenance

- First photographic capture: desktop 1440×1000 and mobile 375×812, plus the mobile midnight state. The three highest-impact weaknesses were a heavy halftone that muted photographic realism, a mobile header that removed the product name, and mobile hero copy/actions that pushed most of the dominant image below the first screen.
- Fixes: removed the hero halftone and reduced global texture, restored the compact `Heat Ledger` mobile wordmark, tightened the mobile headline/spacing, placed the two CTAs side by side, and brought the photo visibly into the first viewport. Matching desktop/mobile views were recaptured after the fixes; the brand test passed without a second identity pass.
- Generated assets: built-in image generation produced two fictional, unbranded Gulf-coast editorial photographs. Project-bound optimized copies are `assets/hero-coast.jpg` and `assets/midnight-coast.jpg`; the untouched generation outputs remain under the local Codex generated-image directory.
- Day prompt intent: realistic golden-hour causeway, mangrove water, fictional coastal skyline, anonymous coral coupe, wide editorial framing, no logos, characters, landmarks, weapons, key art, or game-screenshot treatment.
- Night prompt intent: realistic rain-darkened coastal boulevard, mangrove water, anonymous vintage coupe, cobalt and amber practical light, no logos, characters, landmarks, weapons, key art, or game-screenshot treatment.
- Browser evidence remains local under the task visualization directory rather than being added to reusable plugin evidence or committed to the repository.
