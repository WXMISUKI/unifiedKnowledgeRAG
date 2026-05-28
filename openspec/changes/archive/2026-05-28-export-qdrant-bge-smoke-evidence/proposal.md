## Why

The project now has Qdrant ingestion/retrieval helpers and a downloaded local BGE-M3 model artifact, but there is no repeatable evidence workflow that proves the two can run together locally. Before discussing production promotion, we need a small, local smoke report that exercises ingestion, query, lifecycle readiness, and evidence export in one controlled path.

This is especially important because `QDRANT_URL=:memory:` is useful for local testing, but separate Qdrant clients do not share state. A smoke helper should keep a single client for the whole run so local evidence reflects the actual ingest-and-query flow.

## What Changes

- Add a service-level Qdrant + local embedding smoke evidence export helper.
- Add a CLI script that writes JSON and Markdown evidence under `docs/benchmark/chinese-seed/retrieval-candidates/`.
- Include metadata for embedding provider/model path, Qdrant collection/vector, indexed sources, generated jobs, and output paths.
- Keep the helper local-only and opt-in; do not expose a public HTTP API and do not change default backend/provider settings.
- Add focused tests using mocked embedding/client behavior so normal test runs do not load BGE-M3.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `retrieval-benchmark-harness`: Add local Qdrant smoke evidence export as a benchmark evidence workflow.
- `production-indexing-architecture`: Require Qdrant + BGE smoke evidence before treating the local stack as more than a candidate path.

## Impact

- Affects `app.services.retrieval_benchmark` with a local export helper.
- Adds a script under `scripts/`.
- Adds tests and README usage guidance.
- No new runtime dependency; uses existing Qdrant, embedding, lifecycle, and benchmark modules.
