## Why

The current Qdrant + BGE-M3 smoke evidence shows strong positive retrieval and citation alignment, but one expected-empty case still returns low-confidence evidence at the current threshold. Before changing production defaults or adding empty-intent detection, we need repeatable evidence that compares several score thresholds against the same Chinese seed cases.

## What Changes

- Add a local Qdrant smoke threshold sweep export that runs the same source ingestion and benchmark cases for multiple `RAG_SCORE_THRESHOLD` values.
- Export machine-readable JSON and human-readable Markdown summaries with per-threshold metrics, metadata, and case-level misses.
- Add CLI support to the existing Qdrant+BGE smoke script for threshold sweeps.
- Document how to use threshold sweep evidence to decide whether threshold tuning is enough or whether reranker/empty-intent work is needed.

## Capabilities

### New Capabilities

### Modified Capabilities
- `retrieval-benchmark-harness`: add threshold sweep evidence for Qdrant+BGE smoke evaluation.

## Impact

- Affected code: `app.services.retrieval_benchmark`, `scripts/export_qdrant_bge_smoke_evidence.py`.
- Affected docs: `README.md`, benchmark evidence files under `docs/benchmark/chinese-seed/retrieval-candidates`.
- Affected tests: retrieval benchmark service tests.
- No external API changes, no default threshold change, and no new runtime dependency.
