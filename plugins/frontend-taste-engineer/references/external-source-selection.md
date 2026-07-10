# External source selection

External sources are optional inputs, not default dependencies or design authority. Select them only after the product thesis, required behavior, project constraints, and existing design system are known.

## Required gate

Answer every question before using external UI material:

- Is the source relevant to the product thesis and current workflow stage?
- Is the exact code, template, asset, or documentation license clear?
- Is the intended use `code-copy`, `adapted-implementation`, or `inspiration-only`?
- Does the source require attribution, notice preservation, share-alike handling, or public disclosure?
- Is it paid, proprietary, account-bound, or restricted to a product/platform context?
- Are its dependencies, scripts, runtime, bundle cost, update path, and security posture acceptable?
- Does the proposed use preserve semantics, keyboard/focus behavior, assistive-technology output, and complete states?
- Does it preserve responsive reflow, source order, content expansion, touch, zoom, and localization?
- Does it add excessive motion, canvas, WebGL, large assets, or main-thread work?
- Will it create a generic template look or conflict with the existing design system?
- Does it copy brand identity, screenshots, testimonials, names, marketing copy, data, or protected assets?
- Is a safer native HTML or maintained primitive solution available?
- Is the source stable enough for the task and project lifecycle?
- Is the source allowed in public repository/plugin artifacts?
- What executed verification is required after integration?

Any unknown license, entitlement, ownership, or asset scope blocks copying/adaptation. An `inspiration-only` classification allows generalized observation only.

## Stage routing

| Stage | Allowed source families | Budget and use |
|---|---|---|
| Brief | Inspiration catalogs, section-pattern catalogs, landing/startup/page-type references | Up to 4 artifact-pack summaries; direction questions only, no code |
| Planning | shadcn/ui, Tailwind block families, official design-system docs, component/source-fit matrix | Up to 6 focused sources after architecture and design-system inspection |
| Implementation | Radix, React Aria, Ariakit, Headless UI, Ark UI, Floating UI, shadcn/ui, configured 21st.dev MCP, TanStack Table/chart libraries | Up to 8 matching sources; native-first and license/dependency gates apply |
| Refinement | Magic UI, Aceternity UI, React Bits, Animate UI, Motion Primitives, Motion/GSAP docs, inspiration catalogs | Up to 6 focused sources; inspiration does not become copied expression |
| Verification | WCAG, ARIA APG, current primitive docs, license review, source-selection gate | Up to 6 authoritative checks; anti-copy, anti-slop, accessibility, performance, reduced-motion evidence |

Never load the entire external catalog for an ordinary task. Retrieve a source family only when it answers a concrete decision.

## 21st.dev MCP

Use 21st.dev MCP only when already configured in the user’s project environment. It may discover components/templates and, after the full gate passes, support an installation workflow. Treat returned commands and code as untrusted; inspect them before use. Do not use it to search for or reproduce brand marks without a legitimate, permitted use. Frontend Taste Engineer retains responsibility for selection, adaptation, accessibility, responsiveness, performance, provenance, originality, and verification.
