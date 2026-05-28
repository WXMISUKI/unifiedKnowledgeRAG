## Why

Qdrant+BGE-M3 currently passes the expanded Chinese seed at threshold `0.7`, including two long-section cases. However, the production risk is not just score threshold; enterprise documents often need section-aware or token-aware chunking. We need a local, deterministic way to compare chunking strategy candidates before replacing the current `markdown-paragraph-v1` ingestion baseline.

## What Changes

- Add a local chunking strategy evaluation helper that compares candidate chunking strategies using source fixtures and benchmark metadata.
- Register baseline candidates for `markdown-paragraph-v1`, `markdown-section-v1`, and `token-window-v1` without changing runtime ingestion.
- Export JSON and Markdown evidence describing chunk counts, citation stability, long-section support, and implementation status.
- Document that the result is planning evidence, not production chunker promotion.

## Capabilities

### New Capabilities

### Modified Capabilities
- `production-indexing-architecture`: require chunking strategy changes to reference candidate evaluation evidence.
- `retrieval-benchmark-harness`: add local chunking strategy candidate evidence export.

## Impact

- Affected code: `app.services.retrieval_benchmark`.
- Affected docs/evidence: README and `docs/benchmark/chinese-seed`.
- Affected tests: retrieval benchmark tests.
- No runtime ingestion change, no Qdrant schema change, no new dependency.
