# Contributing

## Propose a source

Open a focused change that adds or updates the source registry, inventory, license review, provenance map, and coverage matrix. Include the canonical URL, original author or organization, source type, classification, license, accessed date, revision, consulted sections, maintenance evidence, restrictions, and topics. Popularity alone is not acceptance evidence.

## Propose a rule

Add the rule as a candidate with:

- Stable ID and metadata.
- Specific action and rationale.
- Applicable contexts and exceptions.
- Implementation and verification guidance.
- Source IDs and license status.
- Related, conflicting, or superseded rules.
- Evidence from retrieval and frontend evals across more than one showcase.

Do not edit stable records from an automated maintenance job. Create a candidate branch and pull request.

## Development

Use Python 3.9 or newer for the zero-dependency core. Keep optional browser/accessibility integrations isolated and documented. Avoid network access in tests unless the test is explicitly marked as a source freshness check.

Run the validation commands in `AGENTS.md`. Package both the plugin and standalone Skill and inspect their file lists before release.

## Review criteria

Reviewers check provenance, license compatibility, specificity, mandatory-rule recall, retrieval relevance, performance, accessibility implications, trend dependence, duplication, contradictions, and context cost. Experimental aesthetic guidance cannot silently become stable.
