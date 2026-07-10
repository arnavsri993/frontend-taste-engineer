# Frontend audit rubric

## Severity

- `critical`: blocks the primary task, exposes sensitive data, creates severe deception, or makes an essential flow unusable for a protected access need.
- `high`: major task failure, inaccessible core interaction, lost data, broken responsive structure, or material trust/performance regression.
- `medium`: meaningful friction, state gap, hierarchy/content problem, inconsistent component behavior, or localized accessibility issue.
- `low`: polish, maintainability, or preference-level improvement with limited user impact.

## Required finding fields

Record title, severity, defect/risk/preference, evidence, affected files and state/viewport, user/product impact, specific correction, sources or rules, and verification.

## Review order

1. Functional integrity and data safety.
2. Keyboard, focus, semantics, names, errors, contrast, reflow, and motion access.
3. Primary flow, information architecture, content truth, and recovery.
4. Responsive structure, overflow, viewport/zoom, and device input.
5. Hierarchy, typography, composition, density, imagery, color, and motion.
6. Performance, browser behavior, maintainability, and regression risk.

Avoid style-only findings unless they undermine hierarchy, product fit, consistency, comprehension, or trust.
