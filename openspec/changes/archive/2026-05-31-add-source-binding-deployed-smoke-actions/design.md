## Context

The deployed provider smoke probe calls a running provider's health, manifest, preflight, source binding, and handoff discovery endpoints. It already fails closed when source binding evidence is blocked, but its source binding check details only include source count and bindable source count.

This change mirrors the handoff bundle's compact source binding rollup at deployed-smoke time. It stays within existing HTTP discovery evidence and does not expand the provider's runtime responsibilities.

## Goals / Non-Goals

**Goals:**

- Add source binding row status counts to deployed smoke source binding check details.
- Add source binding recommended action counts to deployed smoke source binding check details.
- Preserve existing ready/review/blocked pass-fail semantics.
- Keep credentials redacted from exported JSON and Markdown reports.

**Non-Goals:**

- Creating source-to-agent bindings.
- Regenerating local handoff artifacts.
- Changing the `/api/provider/source-bindings` response contract.
- Running retrieval, answer composition, ingestion jobs, index rebuilds, embedding models, vector stores, or GraphRAG.

## Decisions

- Compute counts from the existing `sources` array returned by `/api/provider/source-bindings`.
  - Rationale: The endpoint already owns source binding row-level evidence, so the smoke report should summarize it rather than introducing new evidence sources.
  - Alternative considered: Add a separate source binding diagnostics endpoint for deployed smoke. That would be heavier and unnecessary.

- Store rollups as dictionaries in check details.
  - Rationale: Deployed smoke JSON is machine-readable; dictionaries are easier for external control planes to consume than a formatted string.
  - Alternative considered: Match the handoff bundle's single summary string. That is friendlier for tables but less useful in JSON evidence.

- Keep the Markdown renderer unchanged except for naturally rendering the new detail fields.
  - Rationale: `_compact_check_details` already serializes check details, so adding fields to details keeps the output path simple and deterministic.

## Risks / Trade-offs

- Live providers that omit `status` or `recommended_action` on source rows will produce empty count maps. Mitigation: the smoke report still records source count and bindable count and keeps existing pass/fail behavior.
- More detail can make Markdown rows wider. Mitigation: the report already compactly serializes check details as sorted JSON.
