# Privacy and artifact handling

User-provided names, messages, and project content are request-local by default.

## Persistence boundary

A name or message may appear in the project the user explicitly asks to build. Do not copy it into reusable plugin material:

- Skill instructions or templates.
- Canonical knowledge or research records.
- Committed test fixtures or example prompts.
- Public evaluation reports, screenshots, or traces.
- Package metadata or public repository assets.

Use fictional names such as `Alex` or `Jordan`, or `RECIPIENT_NAME`, in reusable examples. Recipient extraction must remain generic; never hard-code a real name as a classifier signal.

## Recipient profile

When a prompt contains a recipient, record:

- `recipient_visibility: user-supplied`.
- `persistence: request-local`.
- `publication_risk: review-before-public-release`.

Return the name to the active project workflow when needed. Use `redact_user_content` for reports that do not require the literal value.

## Artifact review

Before committing or packaging evidence:

1. Inspect report text, filenames, logs, traces, and pending diffs.
2. Inspect archive filenames and text contents.
3. Inspect screenshots visually; the scanner does not OCR raster pixels.
4. Replace private content with a fictional fixture or redact it.
5. Keep real-project end-to-end evidence local unless publication is explicitly approved.

Configure local scanning with `FTE_PRIVATE_TERMS_FILE=.private-terms`. Keep that file untracked. Run `scripts/scan_private_terms.py --require-terms` after generating packages. The report prints file/line locations and term fingerprints, never the complete configured value.

## Verification

- `.private-terms` is ignored by Git.
- Tracked files and added diff lines contain no configured private term.
- Generated reports, logs, evidence, filenames, and ZIP contents pass the scan.
- Public screenshots use synthetic content and receive manual visual review.
- Canonical knowledge remains recipient-agnostic.
