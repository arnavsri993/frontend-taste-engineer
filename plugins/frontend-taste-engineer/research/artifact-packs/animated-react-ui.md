# Animated React UI

Use motion sources for continuity, causality, feedback, and orientation—not as a default layer of spectacle. Source families include Motion/Framer Motion, GSAP, React Spring, Auto Animate, Anime.js, Lottie, Rive, Three.js/react-three-fiber/drei, and component catalogs such as Magic UI, Aceternity UI, React Bits, Animate UI, and Motion Primitives.

## Selection

- Prefer CSS or the project’s existing motion system for simple state transitions.
- Prefer Motion or React Spring when React lifecycle, interruption, layout continuity, or gesture behavior justifies a dependency.
- Prefer GSAP for complex sequenced timelines only when licensing, bundle cost, cleanup, and reduced-motion behavior are understood.
- Use Lottie or Rive only with licensed assets, a static/reduced alternative, explicit loading/failure handling, and measured delivery cost.
- Use canvas/WebGL only when the visual is central to the product thesis and an accessible, performant fallback exists.

## Contextual intensity

| Intensity | Appropriate scope |
|---:|---|
| 1 | Immediate state feedback, focus/selection continuity, and no ornamental entrance motion. |
| 2 | Small contextual transitions with conservative distance and frequency. |
| 3 | One or two narrative moments plus restrained component feedback. |
| 4 | Expressive experiences where motion is a primary communication channel, with strict performance and comfort checks. |
| 5 | Experimental art/portfolio work only; functionality, readability, interruption, and reduced-motion equivalence still win. |

Quality adjectives do not select an intensity. Domain, risk, frequency, density, devices, content, and user tolerance do.

## Required checks

- Define a reduced-motion outcome that preserves state and meaning; do not merely slow everything down.
- Test keyboard, pointer, touch, repeated activation, interruption, reversal, route changes, background tabs, and component teardown.
- Use transform/opacity when suitable, but choose semantic correctness over blanket performance rules.
- Measure added JavaScript, animation assets, main-thread work, paint cost, memory, and low-power-device behavior proportionately.
- Ensure animation does not delay work, steal focus, trap scrolling, hide content, or communicate status by motion alone.

## Anti-slop warnings

Reject random entrance sequences, ubiquitous spring scaling, scroll hijacking, glow trails, decorative particles, parallax on reading surfaces, animated gradient noise, and repeated hover choreography unless each has a product-specific job. A source demo proves only that an effect can be built; it does not prove it belongs in the product.
