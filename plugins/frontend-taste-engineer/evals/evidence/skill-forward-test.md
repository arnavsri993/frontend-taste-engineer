# Skill forward-test — local evidence review UI

Date: 2026-07-10

Prompt shape: use the standalone `frontend-taste-engineer` Skill to audit the local `review-app/` artifact, return the three highest-impact issues, do not edit, and do not imply a browser run.

## Observed behavior

- Correctly classified the task as a `visual-audit` of an internal developer/evidence-review page.
- Formed a product job and design thesis before findings.
- Detected MCP/browser unavailability and used only the narrow offline references and static audit.
- Explicitly stated that the scanner covered three source files but did not prove browser, keyboard, assistive-technology, visual, network, or performance behavior.
- Returned severity, exact file evidence, product/user impact, correction, relevant stable rule, and verification for each finding.

## Findings and disposition

1. **Critical:** the record browser accepted canonical metadata but not a flat record index. Fixed by loading `ingestion/knowledge-index.json` while retaining `knowledge/index.json` for counts and policy.
2. **High:** the evaluation panel requested nonexistent summary artifacts. Fixed by reading the real retrieval and frontend result files, separating retrieval metrics from honest frontend `not-run` evidence.
3. **High:** narrow layouts removed the load status from visual and accessibility trees, and filter-count changes had no persistent live status. Fixed by retaining compact mobile status, adding a polite atomic result status, and coalescing rapid input updates.

## Remaining verification

The browser-control workflow could not start because localhost binding required an escalation that was rejected when the workspace approval budget was exhausted. Runtime assertions, viewport sweeps, console inspection, and screen-reader spot checks remain manual gates. No frontend-output rubric score is assigned from this forward-test.
