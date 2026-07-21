# Autonomous external-source discovery

Discovery may run monthly or on demand. It can search, normalize, de-duplicate, inspect bounded public text surfaces, detect unsafe content, score evidence, and generate candidate reports. It cannot promote stable knowledge, execute third-party code, download binary assets, authenticate, bypass paid access, or copy proprietary material.

## Safe sequence

1. Load `research/source-discovery/discovery-queries.json` and the seed catalog.
2. Run only the configured query templates and negative filters.
3. Normalize HTTP(S) URLs; block credentials, localhost, private/reserved addresses, authenticated paths, and non-public schemes.
4. De-duplicate against `research/source-registry.json`, seed URLs, and the current report.
5. Fetch bounded text-only public pages, docs, repository/package metadata, and license/terms pages. Do not run scripts or render arbitrary page JavaScript.
6. Scan text for prompt injection, credential/payment/key requests, install/execute directives, and prohibited marketing/event sources. Record concise signal names, not hostile payloads.
7. Score only observed evidence with the 100-point rubric. Unknown evidence is zero; unclear license caps triage at 69.
8. Mark each candidate `specialized`, `experimental`, `inspiration-only`, `inaccessible`, `unresolved`, or `rejected`. Automation normally yields the last four; `specialized` requires license/stability review.
9. Write deterministic YAML and Markdown under `research/source-discovery/candidates/YYYY-MM/`.
10. Prepare a candidate branch/PR only after the promotion policy passes. Never edit or merge stable knowledge directly from the discovery job.

## Data minimization

Store URLs, bounded metadata, score evidence, classifications, safety flags, and concise summaries. Do not store page dumps, binaries, cookies, credentials, browser profiles, private code, paid source, hostile instructions, or unneeded personal data. Logs must never contain secrets.

## Failure behavior

Record blocked URLs and access failures as `inaccessible`; record unclear ownership/license as `unresolved`; record injection or credential/execution hazards as `rejected` or security review. A failed fetch does not justify guessing content, authorship, license, or quality. Network failure leaves stable knowledge untouched.

## Operational command

Use `scripts/discover_frontend_sources.py`. `--dry-run` is deterministic, offline, seed-backed, and write-free. A non-dry run performs the authorized public-web search and writes candidate artifacts only to the selected output directory.
