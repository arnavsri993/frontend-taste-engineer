# Accessible primitives

Prefer native HTML for simple behavior. For complex composite widgets, prefer a maintained primitive when its keyboard/focus behavior, API, license, dependency cost, styling model, SSR/runtime fit, and maintenance burden are safer than custom ownership.

## Selection guide

| Source | Strong fit | Main caution |
|---|---|---|
| React Aria / React Spectrum | React behavior, internationalization, modality, collections, and complex widgets | React-specific; styling and composed-flow accessibility remain the product’s responsibility |
| Radix Primitives | React overlays, focus management, menus, dialogs, popovers, and composable headless behavior | Preview/unstable APIs, portal/SSR integration, and styling/state completeness |
| Ariakit | Accessible React composites with explicit stores and flexible composition | Confirm current API/version and avoid unnecessary abstraction for native controls |
| Headless UI | Tailwind/React/Vue-aligned headless components | Smaller catalog; verify semantics after customization and framework/version fit |
| Ark UI / Zag | State-machine primitives across supported frameworks | Generated/state-machine complexity, package size, and framework parity |
| Floating UI | Positioning for tooltips, popovers, menus, and floating surfaces | Positioning only; semantics, focus, dismissal, modality, and content remain yours |
| cmdk | Command-menu filtering and keyboard interaction in React | Compose with a correct dialog/popover, label search, expose empty states, restore focus, and provide alternative navigation |
| Vaul | Drawer behavior for React | Mobile gestures, focus, scroll locking, dismissal, and reduced motion need integration testing |
| Sonner | Toast presentation | Announcements, timing, action focus, persistence, deduplication, and critical-error alternatives remain product decisions |

## Risk matrix

| Component | Custom risk | Preferred baseline |
|---|---:|---|
| Button, link, checkbox, radio, simple disclosure | Low–medium | Native HTML, progressively styled |
| Dialog, menu, popover, tabs, tooltip | Medium–high | Maintained primitive plus ARIA APG verification |
| Combobox, listbox, tree, grid, date picker | High | React Aria, Ariakit, Radix/Ark/Zag where the exact pattern is supported |
| Drag/drop, virtualized grid, rich text editor | Very high | Specialist library plus keyboard alternatives, performance, and assistive-technology testing |

## Verification

Verify accessible name/role/value, keyboard model, visible focus, focus entry/containment/restoration, escape/dismissal, pointer/touch parity, zoom/reflow, long content, RTL/localization, loading/empty/error/disabled/read-only states, reduced motion, portals, nested overlays, SSR/hydration, and browser/assistive-technology behavior proportionate to risk. Importing an “accessible” primitive never proves the composed application is accessible.
