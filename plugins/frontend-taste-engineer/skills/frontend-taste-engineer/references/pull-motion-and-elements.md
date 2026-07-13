# Pull motion elements and catalogs

Use this reference whenever the creative profile is non-static, the user asks for animation/interaction polish, or the task mode is `motion-refinement`. The goal is to retrieve a compact motion system and matching element catalogs—not to dump the whole seed library.

## Decision: when to pull motion early

Pull motion guidance in the **brief** stage when any of these are true:

- `classify_frontend_task` returns medium-high/high motion intensity, kinetic/tactile/narrative direction, or `needs_early_motion` / early-motion evidence.
- The prompt explicitly asks for animation, motion, transitions, scroll effects, micro-interactions, “alive,” “kinetic,” “cinematic,” or “playful” interaction.
- The product type is campaign, entertainment, expressive personal/portfolio, robotics/demo showcase, or another surface where motion is part of the thesis.

Otherwise keep brief retrieval calm: implement structure first, then pull motion in **refinement**.

Never raise motion intensity only because the user said “stunning” or “premium.”

## Required MCP sequence for expressive work

Run these calls in order. Keep queries narrow.

### 1. Classify

```text
classify_frontend_task
  task: <exact user prompt>
  context: { known framework/route/page type if any }
```

Read `creative_profile.visual_intensity`, `creative_profile.motion_intensity` (or equivalent), direction labels, and `recommended_retrieval.topics`. If motion is listed or intensity is medium-high/high, continue with early motion pulls.

### 2. Corpus motion rules

```text
get_motion_guidance
  query: "motion grammar continuity causality feedback reduced-motion interruption"
  context_budget: 1800
```

Also acceptable:

```text
search_frontend_guidance
  query: "purposeful motion reduced-motion state continuity feedback"
  topics: ["motion"]
```

From the packet, extract and write into `DESIGN.md`:

- At most **three** motion roles (focal/narrative, state continuity, direct feedback)
- Where each role may appear
- What is intentionally static
- Reduced-motion equivalent for every animated meaning

### 3. External motion element catalogs

Call catalogs **only after** the visual system lock in `premium-quality-bar.md`. Call `get_external_source_catalog` **twice** when motion is intentional: once for libraries, once for animated section/components. Derive queries from the thesis (e.g. `editorial kinetic robotics sparse`), not bare `animated components`.

**Libraries / technique (refinement or early brief for kinetic work):**

```text
get_external_source_catalog
  stage: "refinement"
  query: "react motion transitions gestures spring reduced-motion"
  intended_use: "adapted-implementation"
  max_results: 6
```

Expect sources such as Motion/Framer Motion, React Spring, AutoAnimate, GSAP (license-gated), Lenis, Theatre.js, View Transitions, Transitions.dev, easings.

**Animated sections / kinetic UI elements:**

```text
get_external_source_catalog
  stage: "refinement"
  query: "animated marketing landing sections kinetic effects micro-interactions"
  category: "component-catalogs"
  intended_use: "inspiration-only"
  max_results: 6
```

Expect Magic UI, Aceternity UI, React Bits, Animate UI, Motion Primitives, Farm UI, Eldora UI, Hover.dev.

**Optional template pack when the user wants a full kinetic landing scaffold to study:**

```text
get_external_source_catalog
  stage: "planning"
  query: "animated landing page template kinetic hero sections"
  intended_use: "inspiration-only"
  max_results: 4
```

### 4. Gate before using any returned source

For each selected source, read `summary`, `best_for`, `not_for`, `classification`, `usage.decision`, and `license`.

Rules:

- `inspiration-only` → observe patterns only; invent original implementation.
- `unresolved` / license review required → link and study publicly; do not copy code, tokens, assets, or exact layouts.
- Prefer CSS/`@media (prefers-reduced-motion)` or the project’s existing motion system before adding Motion/GSAP/Lottie/Rive/Three.
- Prefer one motion library, not a stack of competing ones.
- Never paste demo markup from Magic UI / Aceternity / similar catalogs into the product as-is.

### 5. Implement a motion grammar, not a demo reel

Map retrieved ideas onto the three buckets only:

| Role | Typical elements | Good uses | Bad uses |
|---|---|---|---|
| Focal / narrative | hero reveal, one scroll chapter, route transition | thesis-defining moment | animating every section on enter |
| State continuity | layout move, shared-element feel, drawer/sheet | orientation after a user action | decorative parallax on reading text |
| Direct feedback | button press, toggle, success toast, hover affordance | proves the control worked | spring-scaling every card |

If the catalog suggests particles, glow trails, infinite marquees, scroll-hijacking, or canvas spectacle, keep them only when the product thesis explicitly needs that channel and a reduced-motion fallback exists.

## Query recipes (copy and adapt)

| Need | Tool | Query |
|---|---|---|
| Motion rules | `get_motion_guidance` | `motion grammar feedback interruption reduced-motion` |
| Micro-interactions | `get_external_source_catalog` stage=`refinement` | `button hover icon morph toast feedback micro-interactions` |
| Hero / landing kinetic | catalog stage=`refinement` category=`component-catalogs` | `animated hero landing sections kinetic effects` |
| Scroll storytelling | catalog stage=`refinement` | `scroll narrative transitions view transitions lenis` |
| Complex timelines | catalog stage=`refinement` | `gsap timeline sequencing theatrejs` |
| 3D / WebGL | catalog stage=`refinement` | `threejs react-three-fiber webgl fallback` |
| Template study | catalog stage=`planning` | `animated landing template kinetic saas` |
| Icons/motion assets | catalog stage=`refinement` category=`icons-illustrations-backgrounds` or motion | `lottie rive interactive animation assets` |

Always set `intended_use` explicitly. Default to `inspiration-only` for catalogs; use `adapted-implementation` only for clear-license libraries you will integrate through public docs/APIs.

## Intensity → pull budget

| Motion intensity | What to pull | Cap |
|---|---|---|
| 1 | Feedback-only corpus rules; skip animated catalogs | 0–2 catalog sources |
| 2 | Corpus motion + tiny feedback catalog | ≤3 |
| 3 | Corpus motion + one library family + one section catalog | ≤6 total across two calls |
| 4–5 | Early motion rules + library + animated sections + optional template study | stage budgets still apply (≤6 refinement); still max 3 roles |

## Offline fallback

If MCP is unavailable:

1. Read this file plus `creative-direction.md` and `offline-core.md`.
2. Still define a motion grammar in `DESIGN.md`.
3. Prefer CSS transitions/keyframes and `prefers-reduced-motion`.
4. Do not invent licenses for Magic UI / Aceternity / GSAP / Lottie assets.
5. Report reduced catalog coverage.

## Done checks for motion pulls

- [ ] Motion roles are named in `DESIGN.md` before polish.
- [ ] At least one corpus motion retrieval ran for non-static work.
- [ ] Catalog pulls used specific queries, not “components” or empty query.
- [ ] Each adopted idea has a purpose, interruption plan, and reduced-motion path.
- [ ] No wholesale template/demo paste.
- [ ] Runtime verification covered repeated activation, interruption, and reduced motion.
