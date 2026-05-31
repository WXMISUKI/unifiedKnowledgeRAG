## Why

Source binding summary already tells external control planes whether a source is generally bindable, but it does not expose how much citation and chunking evidence is available without opening lower-level diagnostics. Adding lightweight coverage counts helps MyPrivateAgent review whether a source has enough grounding metadata before binding, while keeping detailed document diagnostics in the existing manifest and preflight endpoints.

## What Changes

- Add citation anchor and chunk manifest coverage counts to each source binding summary row.
- Include parser support coverage so callers can see how many configured documents are parser-ready versus unsupported.
- Keep the summary read-only and derived from existing source document manifest and ingestion preflight data.
- Update source binding handoff evidence and documentation to describe the new coverage fields.
- Do not add parsers, ingestion jobs, vector-store behavior, answer composition, or GraphRAG execution.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Extend source binding summary with binding evidence coverage fields.
- `provider-roadmap`: Record the Phase 2/6 lightweight coverage summary boundary.

## Impact

- Updates `ProviderSourceBindingSummaryResponse` row shape with non-breaking additive fields.
- Updates provider source binding service, export markdown, tests, README, roadmap, and OpenSpec specs.
- No new dependencies, no runtime default changes, and no mutation of source/index state.
