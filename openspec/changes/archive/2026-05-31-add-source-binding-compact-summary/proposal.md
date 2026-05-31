## Why

External control planes need a fast way to decide whether source binding evidence is ready without filtering every source row themselves. The current endpoint already has the raw row data, so a compact top-level summary can improve integration ergonomics while keeping binding policy outside this provider.

## What Changes

- Add top-level source binding summary counts to `GET /api/provider/source-bindings`.
- Include total source count, bindable source count, source status counts, and recommended action counts.
- Include the same compact counts in the source binding JSON/Markdown export.
- Keep the endpoint read-only and do not add binding execution, policy, approval, audit, ingestion, retrieval, or GraphRAG behavior.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: source binding summary responses include compact aggregate counts for caller integration.
- `provider-roadmap`: records the change as lightweight Phase 2/Phase 6 binding evidence, not binding policy or execution.

## Impact

- Affected API: `GET /api/provider/source-bindings`
- Affected code: provider source binding service and response contract models
- Affected evidence: source binding JSON/Markdown export
- No new runtime dependencies
