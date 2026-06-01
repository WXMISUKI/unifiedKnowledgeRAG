## Why

Phase 2 currently keeps Markdown as the lightweight parser baseline, while PDF/Word/Excel/OCR/table parsing remains intentionally deferred. We need a clear demand contract so parser expansion is triggered by real corpus evidence, not by speculative implementation pressure.

## What Changes

- Add a local Phase 2 contract document for parser expansion demand and gate criteria.
- Define required evidence classes before any non-Markdown parser slice is proposed.
- Keep this slice documentation-only; no parser dependency changes and no ingestion runtime behavior changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: records parser expansion demand governance as Phase 2 ingestion evidence work.
- `knowledge-provider`: records provider-owned parser demand boundary as read-only review context.

## Impact

- Affected docs: one new contract markdown plus tracker refresh.
- No code-path, parser-runtime, deployment, or API behavior impact.
