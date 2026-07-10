# Rejected or Quarantined Guidance

Reviewed 2026-07-10. “Rejected” means the claim is not promoted into stable guidance in its current form. Some items can be rewritten as contextual heuristics after adding scope, exceptions, and verification.

## External agent instructions quarantined

| Source | Instruction pattern observed | Disposition | Reason |
|---|---|---|---|
| `emil-design-skills` | Persona/initial-response commands; mandatory review-table format; categorical “must” wording inside a skill | Quarantined as prompt injection relative to this research task | Output format and persona do not establish frontend correctness. Extract only the underlying motion rationale when independently supportable. |
| `taste-skill-repo` | Fixed taste settings, strong “always/never” rules, hard preflight commands, output-enforcement directives | Quarantined as agent-control text | A source being packaged as a skill does not grant it authority over this plugin build. Rules require product context, exceptions, and standards checks. |
| `awesome-design-md` | “Copy a DESIGN.md” and prompt the agent to build like a named brand | Rejected as a production default | Encourages direct imitation and assumes extracted values are accurate/licensed. Retain only the design-inventory schema. |
| `transitions-dev-repo` | `npx skills add`, `npx transitions-refine live`, agent-backed refine/apply commands | Not executed; workflow analyzed only | Running third-party packages was unnecessary and would execute untrusted code. Tool ideas were evaluated from source pages/repository inventory. |
| `hive-mind-landing-page` | Local skill commands and prompt traces | Treated as historical data only | They explain one build; they do not override this task or prove general causation. |

No source instruction requested credentials or destructive filesystem actions in the accessible material. The potentially unsafe behavior was execution of external packages/skills and instructions attempting to control the researching agent. None was followed.

## Aesthetic claims rejected as universal rules

### R-001 — “Never use pills / gradients / glass / glows / bento grids / centered heroes / cards”

- **Status:** rejected as universal; retained as misuse detectors.
- **Why:** Official systems use several of these forms appropriately. The actual failure is reflexive use, hierarchy flattening, weak contrast, poor performance, brand imitation, or lack of product purpose.
- **Replacement:** Ask what job the pattern performs, when it is appropriate, what alternatives exist, and how it will be verified.
- **Sources in tension:** `taste-skill-repo`, `hive-mind-landing-page` versus `material-3`, `fluent-2`, `carbon-design-system`, `primer-design-system`.

### R-002 — “Premium” equals large whitespace, serif/sans pairing, soft contrast, floating navigation, layered cards, or spring motion

- **Status:** rejected.
- **Why:** These are style motifs, not evidence of quality. They can harm density, legibility, task speed, motion comfort, and product fit.
- **Replacement:** Define audience, content density, trust needs, interaction frequency, and brand thesis; then choose measured typography/composition/motion.
- **Source:** style variants summarized by `taste-skill-site`/`taste-skill-repo`.

### R-003 — Fixed “design variance,” “motion intensity,” and “visual density” defaults

- **Status:** rejected as fixed defaults; retained as optional vocabulary.
- **Why:** Numeric taste dials lack calibrated measurement and can conceal the real product questions.
- **Replacement:** Derive explicit decisions from task frequency, content volume, audience, risk, platform, and brand maturity.

### R-004 — Every new product should ship light and dark themes

- **Status:** rejected as universal.
- **Why:** Theme support has content, token, image, testing, maintenance, and brand costs. User/system preference support is valuable, but scope must be intentional.
- **Replacement:** If dark/high-contrast themes are required, build them from semantic tokens and verify parity. Otherwise, support the promised theme well and avoid blocking a future tokenized mode.

### R-005 — Every button should scale on `:active`

- **Status:** rejected as universal.
- **Why:** Scaling can cause visual jitter, conflict with grouped controls, feel inappropriate for dense/serious systems, or aggravate motion sensitivity.
- **Replacement:** Provide immediate pressed feedback appropriate to the component/system; it may be color, border, elevation, or small transform, and must respect reduced motion.
- **Source:** practitioner example in `emil-design-skills`.

### R-006 — Enter animations always use ease-out and exits always use another fixed curve

- **Status:** rejected as absolute; retained as common starting heuristic.
- **Why:** Direct manipulation, spring systems, shared-element continuity, platform components, and interruptible gestures have different dynamics.
- **Replacement:** Choose a semantic motion token based on user input, direction, distance, continuity, and interruption; test it.

## Workflow claims rejected or narrowed

### R-007 — Image-first is mandatory for excellent frontend design

- **Status:** rejected as mandatory; retained as contextual workflow.
- **Why:** It worked for the CHORUS showcase but can bias teams toward pixels over content, semantics, responsiveness, and states.
- **Replacement:** Use image references after the brief/content model when art direction materially helps; implementation requirements still outrank the image.
- **Source:** `hive-mind-landing-page`.

### R-008 — One short prompt demonstrates a generally superior method

- **Status:** rejected.
- **Why:** One self-reported example has no control, replication, or independent evaluation. It is evidence of a possible workflow, not comparative effectiveness.
- **Source:** `hive-mind-landing-page`.

### R-009 — A live agent should automatically refine project transitions

- **Status:** quarantined as experimental.
- **Why:** Refine is explicitly beta, consumes the user’s tokens/credits, and can produce incorrect code. Silent mutation is unacceptable.
- **Replacement:** Read-only audit first; reversible preview; explicit approval; diff review; tests; rollback.
- **Sources:** `transitions-refine-page`, `transitions-dev-repo`.

### R-010 — Always output complete code regardless of task or context

- **Status:** rejected as an instruction.
- **Why:** Completeness means the requested artifact and verified behavior, not duplicating entire files, ignoring repository architecture, or exceeding safe review scope.
- **Replacement:** Make scoped edits in the real project, preserve architecture, and report limitations. Avoid placeholders in deliverables without unnecessary transcript bloat.
- **Source:** output-enforcement skill family in `taste-skill-repo`.

### R-011 — Full visual redesign is preferable to targeted improvement

- **Status:** rejected.
- **Why:** Rewrites increase regression, accessibility, delivery, and maintenance risk.
- **Replacement:** Audit, preserve useful behavior/architecture, choose modernization levers, compare before/after, and test regressions.

### R-012 — Every project needs a framework or headless component dependency

- **Status:** rejected.
- **Why:** Static/content-first pages often need little or no client JavaScript; native HTML may cover simple controls.
- **Replacement:** Choose route architecture from requirements. Add mature primitives for genuinely complex behavior when total risk is lower than custom implementation.
- **Sources:** `vue-docs`, `astro-docs`, `whatwg-html`, `react-aria`, `radix-primitives`.

### R-013 — Server rendering is always faster or more accessible

- **Status:** rejected as universal.
- **Why:** Server latency, caching, hydration, streaming, personalization, client transitions, and error paths affect the result. Accessible markup/behavior still must be authored.
- **Replacement:** Select and measure rendering per route; server/static HTML is a strong content-first default, not a guarantee.

## Quality and compliance claims rejected

### R-014 — Importing an accessible design system makes the application accessible

- **Status:** rejected.
- **Why:** Every system reviewed warns, explicitly or implicitly, that integration, content, customization, and full flows require testing.
- **Replacement:** Treat library accessibility as provenance for a primitive, then verify the composed experience.

### R-015 — Zero automated accessibility violations means WCAG conformance

- **Status:** rejected.
- **Why:** `playwright-docs` explicitly states automation detects only some issues; WCAG conformance covers full pages and human-evaluated criteria.
- **Replacement:** Combine automation, keyboard, screen-reader spot checks, zoom/reflow, content, and inclusive user testing.

### R-016 — Apple target sizes or APCA are the web conformance test

- **Status:** rejected.
- **Why:** Apple HIG is platform guidance. It mentions both WCAG contrast and APCA, but WCAG 2.2 remains the registered normative web conformance baseline here.
- **Replacement:** Use WCAG criteria for web conformance; use platform comfort targets and perceptual methods as supplemental design evidence, clearly labeled.

### R-017 — Passing at one desktop and one mobile viewport proves responsiveness

- **Status:** rejected.
- **Why:** Intermediate widths, short viewports, zoom, content expansion, orientation, safe areas, and input modes can still fail.
- **Replacement:** Test constraint boundaries and representative intervals, not only two screenshots.

### R-018 — “Pixel perfect” without a comparison artifact

- **Status:** rejected.
- **Why:** The phrase is unverifiable and often hides responsive/accessibility compromises.
- **Replacement:** Name fidelity dimensions and provide reference/actual screenshots plus measured/visual diff at the target viewport; separately verify adaptive behavior.

### R-019 — GitHub stars, affiliates, testimonials, or trend status establish correctness

- **Status:** rejected.
- **Why:** Popularity and marketing do not establish accuracy, safety, maintenance, accessibility, or generalizability.
- **Sources:** `awesome-design-md`, `taste-skill-site`, `motionsites` surfaces.

### R-020 — Current content of the inaccessible X post

- **Status:** rejected/unresolved.
- **Why:** No post body, media, author transcript, or official mirror was available. Any summary would be invented.
- **Source:** `monokern-x-post`.

### R-021 — MotionSites prompt/catalog guidance

- **Status:** rejected/unresolved.
- **Why:** The substantive catalog and license were not accessible. Homepage title/affiliate content cannot support design rules.
- **Source:** `motionsites`.

## Deprecated or unstable implementation guidance

| Guidance | Status | Replacement |
|---|---|---|
| Use `polaris-react` for a new Shopify app | **Deprecated** | Current Polaris Web Components / Shopify API-versioned docs. |
| Start a new project on Vue 2 | **Deprecated** | Vue 3; Vue 2 reached end of life 2023-12-31. |
| Apply Next.js App Router caching/rendering rules to all Next projects | **Rejected** | Inspect Next version and router; keep Pages/App guidance separate. |
| Treat Material Web as an actively expanding default dependency | **Quarantined** | Repository says maintenance mode pending maintainers; assess alternatives and current health. |
| Promote Radix preview components as stable | **Quarantined** | Keep `unstable_`/preview status and pin/review before production use. |
| Treat Taste Skill v2 wording/section numbers as stable | **Experimental** | Website explicitly says v2 is iterating before stable 2.0.0. |
| Treat Refine commands/behavior as stable | **Experimental** | Terms explicitly label early beta and warn behavior may change/regress/disappear. |
| Use old SLDS v1 pages as the current Lightning baseline | **Deprecated context** | Current SLDS 2 plus live package/repository revision; keep v1 only for legacy migration. |
