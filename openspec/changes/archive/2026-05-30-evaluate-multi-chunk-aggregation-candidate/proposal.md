## Why

The latest split-chunk identifier evidence shows that raw hybrid retrieval can return the related policy and form chunks, but the strict identifier gate filters them all because no single chunk contains every query identifier. We need a lightweight, evaluation-only candidate to measure whether multi-chunk evidence aggregation can reduce this false-negative risk before considering runtime hybrid promotion.

## What Changes

- Add a local multi-chunk aggregation candidate that evaluates identifier-bearing evidence at a source/document group level rather than requiring every identifier to appear in one chunk.
- Export JSON and Markdown evidence for the split-chunk benchmark, including raw citations, aggregated citations, query identifiers, and summary metrics.
- Add CLI support to generate this evidence through the existing Qdrant+BGE smoke export script.
- Keep the candidate evaluation-only: no public HTTP API changes, no runtime retrieval default changes, no new production vector database behavior, no answer generation changes.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `retrieval-benchmark-harness`: Adds evaluation-only split-chunk multi-chunk aggregation evidence for hybrid retrieval candidates.
- `production-indexing-architecture`: Records that split-chunk aggregation needs explicit evidence before any runtime hybrid or gating promotion.

## Impact

- Affected code: `app/services/retrieval_benchmark.py`, `scripts/export_qdrant_bge_smoke_evidence.py`, retrieval benchmark tests, generated benchmark evidence, README and architecture/research docs.
- APIs: No public HTTP API contract changes.
- Dependencies: No new runtime dependencies.
- Systems: Only local benchmark/export tooling changes; default provider retrieval remains unchanged.
