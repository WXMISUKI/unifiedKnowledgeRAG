## Why

`markdown-section-v1` is currently only a planned chunking candidate. To compare it meaningfully with the existing paragraph baseline, we need a runnable local candidate that can produce section-aware chunks and export evidence without changing Qdrant ingestion defaults.

## What Changes

- Implement a runnable `markdown-section-v1` chunking candidate for local markdown sources.
- Extend chunking candidate evidence to report section candidate chunk counts and citation stability.
- Keep runtime Qdrant ingestion on `markdown-paragraph-v1`.
- Update tests, evidence, and documentation to show `markdown-section-v1` is runnable but not promoted.

## Capabilities

### New Capabilities

### Modified Capabilities
- `retrieval-benchmark-harness`: chunking candidate evidence distinguishes runnable section-aware candidates from planned-only strategies.
- `document-rag`: section-aware chunking candidate preserves stable evidence metadata without becoming the default ingestion strategy.

## Impact

- Affected code: `app.services.qdrant_vector_store`, `app.services.retrieval_benchmark`.
- Affected docs/evidence: README and `docs/benchmark/chinese-seed/chunking-candidates`.
- Affected tests: Qdrant vector store and retrieval benchmark tests.
- No runtime default change, no production parser dependency, no Qdrant schema change.
