# Paid-client frontend bar

Use this for every client frontend. “Good” is failure. The page must feel authored for one specific product, audience, and promise—something a stranger could not confuse with a generic AI landing page after removing the logo.

## Non-negotiable sequence

Do these in order. Compact, diversified source retrieval comes before direction lock; copying or installing any component/template still requires the license and implementation gate.

1. Inspect the project and inventory supplied facts, unknowns, and prohibited claims (no fake proof).
2. `classify_frontend_task` with the exact prompt.
3. Ask one bounded clarification batch if needed, or record reversible judgment defaults.
4. Retrieve core UX, source-derived design, copy, responsive, accessibility, integrity, and verification evidence.
5. Generate and compare two or three materially different candidate directions.
6. Select one direction and lock the **visual system** in `DESIGN.md`; lock facts, hierarchy, actions, and responsive copy in `CONTENT.md`.
7. Implement structure, states, and responsive behavior with that system. Copy/install external code only after the source-use gate.
8. Run the mandatory screenshot refine loop twice if the first pass still looks generic.
9. Production build + completion report with the anti-generic proof line.

If you skip retrieval/candidate comparison and start from Magic UI / Aceternity / ThemeWagon / a SaaS starter, restart.

## Visual system lock (required fields)

Before implementation, `DESIGN.md` must name:

| Field | Requirement |
|---|---|
| Thesis | One sentence that rejects alternatives (not “modern and clean”) |
| Density profile | `sparse-editorial` · `marketing-landing` · `product-marketing` · `dense-app` · `data-dashboard` · `portfolio-expressive` |
| Type pair | Distinct display + body (no Inter, Roboto, Arial, system-ui as the identity) |
| Type scale | Explicit steps for display / H2 / body / meta |
| Spacing scale | Base unit + section rhythm |
| Color roles | bg / surface / text / mute / accent (1 accent family, not a rainbow) |
| Material | One primary surface language (flat ink, paper, metal, glass-limited, etc.) |
| Hero composition | Full-bleed or edge-to-edge plane; brand signal; one headline; one support line; one CTA group; one dominant visual |
| Motion grammar | At most **3 roles**: focal · state · feedback (+ reduced-motion for each) |
| Avoid list | Patterns deliberately rejected for this job |

Also write one line: **Why this is not generic:** …

## First viewport law

The first screen is one composition, not a dashboard of marketing modules.

Allowed: brand/name as a hero-level signal, one headline, one short supporting sentence, one CTA group, one dominant image/visual plane.

Forbidden in the first viewport unless the product *is* a dashboard and the brief demands it: stat strips, logo clouds, feature card grids, schedules, address blocks, promo chips, floating badges, “as seen in”, testimonial quotes, secondary nav forests, multi-column promo tiles.

Brand test: if you remove the nav/logo wordmark and the page could still belong to any startup, branding is too weak—strengthen name treatment, custom type, or the hero visual until the page is recognizable.

## Hard reject list (default AI cluster)

During implementation and the anti-slop pass, reject unless the thesis has a one-sentence justification:

- Inter / Roboto / Arial / generic system stack as the display identity
- Purple-on-white or purple-to-indigo gradient themes
- Warm cream + terracotta + default serif “AI brochure” look used without product reason
- Centered hero + three equal feature cards as the whole page idea
- Glow, neon borders, glassmorphism stacks, gradient text on every heading
- Rounded-full pill forests and badge stickers on the hero
- Decorative bento grids with no content hierarchy
- Fake dashboards, fake metrics, fake testimonials, fake avatars
- Scroll-hijacking and animate-every-section-on-enter
- Stock “team smiling in office” imagery with no product truth
- Soft UI / glass / dark cinematic defaults applied to calm high-trust products

## Density profiles (pick one)

| Profile | Spacing | Type | Chrome | Motion |
|---|---|---|---|---|
| `sparse-editorial` | Large section gaps, long measure control | Expressive display, quiet body | Almost no cards | 0–2 roles |
| `marketing-landing` | Generous but paced | Strong display + clear body | Few sections, not a card dump | 1–3 roles |
| `product-marketing` | Medium | Product-named UI type | Selective product chrome | 1–2 roles |
| `dense-app` | Tight, aligned | UI sans, tabular nums if needed | Real app chrome | feedback + rare state |
| `data-dashboard` | Compact, grid-led | Numeric precision first | Toolbars/tables honest | feedback only unless asked |
| `portfolio-expressive` | Dramatic but readable | Custom display | Minimal chrome | up to 3 roles |

Do not put `dense-app` chrome on a campaign landing. Do not put `portfolio-expressive` motion on a banking flow.

## Copy bar (paid client)

- Headline names the specific audience + outcome or conflict (not “Welcome to the future”).
- Support line adds new information; it does not restate the headline.
- CTA is a concrete verb (“Book a pilot”, “See live telemetry”) not “Get started” / “Learn more” unless no better verb exists.
- Every section has one job; delete duplicate promise blocks.
- No invented metrics, customers, press, or partnerships.

Run a dedicated copy pass after first layout: read the page as text only and cut anything that does not change a decision, trust, instruction, or recovery.

## Catalog / template discipline

- Query from the thesis, e.g. `editorial serif kinetic robotics sparse portfolio`, never bare `animated components`.
- Retrieve reviewed observations before the system lock; record source IDs and allowed-use restrictions.
- Copy or install components/templates only after direction selection and the source gate. Adapt permitted ideas into the selected type/color/material.
- One motion library max. Three motion roles max.
- Templates are IA references, not final skins.

## Screenshot refine gate (mandatory)

No completion without:

1. Real running preview
2. Desktop + mobile captures of the primary view (and primary interactive state if relevant)
3. Written list of the **three highest-impact** weaknesses (composition / hierarchy / type / copy / generic pattern / motion / mobile)
4. All three fixed
5. Recapture + re-inspect

If after pass one the page still fails the brand test or still matches the reject list, run a **second** refine pass focused only on identity and first viewport.

## Completion proof (user-facing)

The completion report must include:

1. Thesis + density profile + type pair
2. **Why this is not generic:** one sentence
3. Motion roles (or “static by intent”)
4. Screenshot paths + three weaknesses fixed
5. Production build result
6. Honest limitations

If you cannot write a credible “why this is not generic” line, the work is not done.
