## Why

`markdown-section-v1` can now generate section chunks, but it has not been measured against the same Qdrant+BGE retrieval benchmark as the current `markdown-paragraph-v1` baseline. Before considering any ingestion switch, we need side-by-side evidence that shows how each chunking strategy affects hit rate, citation match, empty handling, and long-section behavior.

## What Changes

- Add local Qdrant+BGE chunking comparison evidence export.
- Allow the smoke path to index either paragraph or section chunks while keeping runtime ingestion defaults unchanged.
- Export JSON and Markdown comparison files for `markdown-paragraph-v1` and `markdown-section-v1`.
- Document the expected trade-off: section chunks may preserve broad recall but reduce citation precision.

## Capabilities

### New Capabilities

### Modified Capabilities
- `retrieval-benchmark-harness`: add Qdrant+BGE chunking strategy comparison evidence.
- `document-rag`: allow section chunks to be used in local smoke evaluation without changing default ingestion.

## Impact

- Affected code: `app.services.retrieval_benchmark`, `app.services.qdrant_vector_store`, `scripts/export_qdrant_bge_smoke_evidence.py`.
- Affected docs/evidence: README and `docs/benchmark/chinese-seed/chunking-candidates`.
- Affected tests: retrieval benchmark tests and Qdrant vector store tests.
- No production default change, no API change, no new dependency.
