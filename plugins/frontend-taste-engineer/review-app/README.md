# Leonida Heat Ledger

Leonida Heat Ledger is a dependency-free, unofficial GTA VI release briefing concept. It uses original AI-generated Gulf-coast editorial photography, verified release information linked to Rockstar Games, a keyboard-operable daylight/midnight view, clipboard recovery, local preference persistence, and responsive/reduced-motion fallbacks.

It is not affiliated with Rockstar Games or Take-Two Interactive. No official logos, screenshots, trailer frames, character likenesses, maps, audio, or key art are included.

## Run locally

```bash
cd plugins/frontend-taste-engineer/review-app
npm run dev
```

Open `http://127.0.0.1:8765/`.

## Build and preview

```bash
npm run build
npm run preview
```

The deployable output is written to `review-app/dist/`. The Python builder includes the page shell, stylesheet, script, favicon, original JPEG assets, static-host redirect, security headers, and a `404.html` fallback. There are no frontend dependencies, remote fonts, trackers, or external runtime image requests.

## Product boundaries

- Rockstar's official page is the source for the visible November 19, 2026 date, PlayStation 5 and Xbox Series X|S platforms, and the Jason/Lucia premise.
- The daylight/midnight preference is the only value saved locally. No data leaves the browser.
- The copy control uses the Clipboard API when available and exposes a selectable address when it is not.
- The page remains readable and navigable without JavaScript; the visual switch and copy helper are hidden progressive enhancements.

See `DESIGN.md` for the classification, system lock, content outline, motion grammar, accessibility target, and verification plan.
