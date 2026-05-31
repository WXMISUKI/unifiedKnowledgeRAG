## Why

Source binding summary exposes readiness and coverage facts, but external control planes still need source package context to judge whether a source is appropriate for a specific agent use case. Adding a compact package context keeps binding review lightweight while reusing existing provider-owned metadata.

## What Changes

- Add source package context fields to each source binding summary row: domain, language, sensitivity, citation granularity, and supported formats.
- Populate these fields from the existing source document manifest `source_package`.
- Include package context in exported source binding JSON and Markdown evidence.
- Keep package context informational and read-only; it does not change bindability by itself.
- Do not add parser support, ingestion jobs, vector-store behavior, answer composition, policy, approval, audit, or GraphRAG execution.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Extend source binding summary with source package context fields.
- `provider-roadmap`: Record package context in source binding review as Phase 2/6 lightweight evidence.

## Impact

- Adds non-breaking optional/additive fields to `SourceBindingSummaryRow`.
- Updates provider source binding service, export Markdown, tests, README, roadmap, and OpenSpec specs.
- No new dependencies, no runtime default changes, and no mutation of source/index state.
