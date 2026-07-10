# Mega component catalog

This pack routes component-source families; it does not copy components or grant reuse rights. Start from the product thesis and required behavior, then apply the source-selection gate before inspecting or integrating a candidate.

## Source-fit matrix

| Need | Start with | Use when | Avoid when |
|---|---|---|---|
| Native-looking application controls | Registered design-system docs, shadcn/ui, Radix, React Aria, Ariakit, Headless UI, Ark UI | Behavior, keyboard, state, and composition requirements are known | A native HTML control already covers the interaction |
| Marketing sections | Tailwind/shadcn block families, Origin UI, HyperUI, Preline, Flowbite | A section pattern accelerates layout without dictating the brand | The source is premium/unclear-license or the result becomes a generic template |
| Expressive hero/feature moments | Aceternity UI, Magic UI, React Bits, Animate UI, Motion Primitives | One restrained interaction supports the narrative | Repeated motion, WebGL, or decoration obscures content or harms performance |
| Dense dashboard/application UI | Tremor, TanStack Table, Mantine UI, ReUI, chart libraries | Data semantics, states, permissions, and responsive strategy are defined | A decorative dashboard mockup would replace real data behavior |
| Command palettes and overlays | cmdk plus a maintained dialog/popover/focus primitive | Search, keyboard model, focus restoration, and empty/error states are specified | The palette is merely a fashionable shortcut with no discoverable alternative |

## High-value categories

- Hero: use a source for composition or implementation mechanics, then rewrite hierarchy, content, media, and responsive behavior for the product.
- Pricing: preserve honest plan data, comparison semantics, localization, billing cadence, and purchase-state handling; never invent prices or savings.
- Features: organize around user outcomes and evidence, not a reflexive three-card grid.
- FAQ: prefer semantic disclosure when sufficient; verify headings, keyboard operation, deep links, print behavior, and expanded-state persistence.
- Testimonials: include only supplied, verifiable proof with publication permission. A catalog layout never authorizes fabricated people or quotes.
- Dashboards: design loading, empty, error, stale, permission, offline, and dense-data behavior before visual polish.
- Command palettes: provide accessible names, search feedback, keyboard navigation, escape, focus restoration, and a non-palette route to core actions.
- Navigation: preserve location, hierarchy, mobile transformation, focus order, skip links, and truthful destinations.
- Bento grids: use only when block size expresses priority or content relationships; do not use it as default decoration.
- Forms/auth/settings: use maintained primitives, explicit labels, validation/recovery, password-manager support, saving states, destructive confirmation, and permission boundaries.
- Tables/charts: keep underlying data available, explain units and uncertainty, support keyboard/zoom/reflow, and provide meaningful empty/error states.

## Copy, adapt, or reference

- `code-copy`: allowed only when the exact code and dependencies have clear terms, required notices are preserved, entitlement is confirmed, and product integration is verified.
- `adapted-implementation`: rewrite for the project while honoring license/attribution and validating semantics, states, responsiveness, performance, and maintainability.
- `inspiration-only`: extract a generalized pattern or question; copy no code, asset, exact text, screenshot, token set, or brand expression.
- `unresolved` or `inaccessible`: link for review only. Do not integrate.

Never treat popularity, a copy button, an AI installer, or a package command as permission or quality evidence.
