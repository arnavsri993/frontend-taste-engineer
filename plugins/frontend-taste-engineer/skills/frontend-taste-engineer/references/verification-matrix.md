# Verification matrix

| Work | Minimum evidence |
| --- | --- |
| Tiny visual fix | Targeted screenshot, affected interaction, no new console error |
| Component | States, keyboard/focus, touch/pointer, responsive context, unit/component test |
| Page | Build/types, primary flow, desktop/mobile captures, keyboard, automated access check, content stress |
| Multi-page app | Route smoke tests, representative states, responsive set, end-to-end primary flows, bundle/performance review |
| Redesign | Before/after matched captures, preserved behavior, regression tests, hierarchy/content/access audit |
| Screenshot reconstruction | Same viewport captures, overlay/diff, responsive inference test, semantic/keyboard review |
| Motion | Runtime capture, repeated/interrupted/reversed actions, reduced motion, performance check |
| Accessibility remediation | Reproduction, automated check, keyboard path, relevant screen-reader or platform spot check |
| Performance remediation | Before/after measurement under matching conditions, bundle/network evidence, regression guard |

Always report commands run, observed results, files or URLs inspected, viewports, test data, skipped checks, and limitations. A static audit is evidence of code patterns, not proof of runtime quality.
