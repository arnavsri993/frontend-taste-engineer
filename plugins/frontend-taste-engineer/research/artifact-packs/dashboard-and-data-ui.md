# Dashboard and data UI

Source families include Tremor and Tremor Blocks, TanStack Table, Recharts, Chart.js, Nivo, visx, MUI X Data Grid, Mantine React Table, Material React Table, ReUI, Tabler, AdminLTE, Creative Tim/Flatlogic/Metronic/Devias templates, and application-oriented Mantine examples.

## Choose by responsibility

- TanStack Table supplies headless table state and composition; the application still owns semantics, responsive behavior, virtualization, focus, selection, editing, and empty/error states.
- Recharts and Chart.js suit conventional charts; Nivo offers a broad chart catalog; visx provides lower-level composition. Select from required chart types, framework, accessibility plan, bundle/runtime cost, SSR behavior, and customization—not gallery appeal.
- Tremor and template sources accelerate dashboard composition only after real data, information hierarchy, permissions, and state requirements exist.
- Data-grid products can be appropriate for dense editing, grouping, virtualization, and enterprise features, but license tiers and accessibility support must match the exact feature set.

## Layout and density

Start with the decisions users make, then place summary, trend, exception, and detail views in that order. Keep filters and scope visible, units consistent, timestamps and freshness explicit, and dense alignment stable. Do not tile arbitrary metrics into a fake dashboard or force every panel into equal cards.

## Required states

Design loading (including partial/streaming), empty, filtered-empty, error, stale, offline, permission-denied, redacted, unsupported-range, export-in-progress, destructive confirmation, and recovery. Preserve the last safe state when refresh fails and distinguish “no data” from “no access.”

## Tables and charts

- Tables: semantic headers, captions or accessible names, sort state, keyboard reachability, focus visibility, column visibility, responsive alternatives, virtualization behavior, and non-color status cues.
- Charts: text summary or data table, meaningful labels, units, uncertainty, focus/hover equivalence, contrast, pattern/shape alternatives, resize/zoom behavior, and no motion-only meaning.
- Filters: announce applied scope, support clear-all/recovery, preserve URL/history when useful, and avoid hidden destructive changes.
- Performance: measure row/chart count, bundle cost, render time, interaction latency, memory, resize work, and server/client boundaries with realistic data.
