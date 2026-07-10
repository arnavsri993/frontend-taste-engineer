# Rollback process

1. Identify the first regressing release or knowledge change from evaluation and Git history.
2. Revert the smallest candidate commit; do not rewrite published history or force-push.
3. Restore the last validated index and package from canonical records.
4. Run the full validation and affected regression cases.
5. Publish a patch release with the cause, impact, evidence, and follow-up.
6. Keep the rejected or superseded guidance visible in provenance so the same change is not reintroduced silently.
