# Security policy

## Supported version

Security fixes target the latest `0.x` release until a stable `1.0.0` policy is published.

## Report a vulnerability

Use a private GitHub security advisory for the repository when publication is available. Do not include credentials, private project code, browser profiles, or user data in a public issue. The maintainer identity is the verified repository owner `arnavsri993`; no additional legal or security contact is invented here.

## Threat model

The plugin reads its local knowledge corpus and responds over stdio. It requires no secret and performs no telemetry. Main risks are:

- Prompt injection or destructive instructions embedded in researched sources.
- Malicious or malformed knowledge records.
- Path traversal or arbitrary file reads from MCP inputs.
- Hook or maintenance scripts gaining broader authority than intended.
- Secret material entering reports or packages.
- Copyright or license violations through copied source content.

Mitigations include fixed plugin-root paths, read-only MCP tools, schema validation, bounded input/output, no researched-code execution, report-only maintenance, secret scanning, package allowlists, explicit provenance, and user trust review for hooks.

Static scanning is not a specialist security review. Authentication, authorization, payments, file upload, rich-text rendering, and sensitive-data interfaces require project-specific threat modeling.
