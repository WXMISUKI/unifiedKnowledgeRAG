## Why

The first real Qdrant + BGE-M3 smoke run proved the local stack can ingest and query, but it also returned evidence for all empty benchmark cases. Qdrant retrieval needs a configurable minimum score gate so low-confidence hits can become successful empty retrieval results instead of noisy evidence.

This is the next smallest quality-control step before discussing rerankers, hybrid retrieval, or more sophisticated chunking.

## What Changes

- Apply `RAG_SCORE_THRESHOLD` to Qdrant retrieval results before mapping them to returned evidence.
- Include the configured threshold in Qdrant smoke evidence metadata.
- Add focused tests for accepted, filtered, and malformed Qdrant hits.
- Re-run Qdrant + BGE-M3 smoke evidence to record the new baseline.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `document-rag`: Qdrant text retrieval respects the configured retrieval score threshold.
- `retrieval-benchmark-harness`: Qdrant smoke evidence records the threshold used for retrieval.

## Impact

- Affects Qdrant retrieval result filtering.
- Affects Qdrant + BGE-M3 smoke evidence output.
- No new dependencies or public API changes.
