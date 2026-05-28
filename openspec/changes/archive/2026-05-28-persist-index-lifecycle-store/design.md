## Context

The provider now exposes explicit ingestion jobs and source index status. The current implementation is deliberately simple: jobs live in memory and source readiness is read from per-source marker files. That is enough for a first lifecycle contract, but it means job history is lost on restart and health/catalog metadata cannot reliably explain the current source lifecycle state.

This change keeps the provider lightweight and local while introducing a durable store boundary that future queue-backed indexing or database persistence can replace.

## Goals / Non-Goals

**Goals:**

- Persist ingestion jobs across provider process restarts.
- Persist source index status in one normalized source manifest.
- Keep the existing HTTP API contracts unchanged.
- Keep storage local-file based under `RAG_INDEX_DIR`.
- Make the store implementation small, testable, and replaceable.

**Non-Goals:**

- No SQL database, migration framework, distributed lock, external queue, or remote object store.
- No multi-process write coordination beyond simple atomic local file replacement.
- No new job listing API in this slice.
- No source document upload or incremental indexing semantics.

## Decisions

1. Use a dedicated file-backed store helper.

   `index_lifecycle.py` should not directly manage every JSON read/write detail inline. A small helper can own `jobs.jsonl`, `sources.json`, atomic writes, and defensive read fallbacks.

2. Store jobs append-only in `jobs.jsonl`.

   JSONL keeps job records inspectable and append-friendly. The service can load the latest job record for a source by scanning the small local file. A later database-backed implementation can preserve the same service methods.

3. Store source lifecycle state in `sources.json`.

   Source status is a map keyed by `source_id`, which is simpler for health/catalog lookups than scanning marker files. Existing per-source markers may remain as transitional artifacts, but the manifest becomes the primary local truth.

4. Keep fixture backend logically ready.

   `fixture` remains a deterministic contract backend and does not require persisted index state. Durable lifecycle storage mainly affects the LlamaIndex path.

5. Use atomic replace for manifest writes.

   Writing a temp file then replacing the manifest avoids partially-written JSON in normal local development. Multi-process correctness is explicitly out of scope.

## Risks / Trade-offs

- JSONL can grow without compaction -> acceptable for this slice; future job listing/retention can add compaction.
- Local file writes are not a production concurrency model -> document the limitation and preserve the service boundary for replacement.
- Existing marker files may confuse developers -> README should identify `sources.json` as the canonical local manifest after this change.

## Migration Plan

1. Add a file-backed lifecycle store helper.
2. Update job creation and source status lookup to use the store.
3. Keep response models and API routes unchanged.
4. Update health/catalog status derivation to read the durable manifest.
5. Add restart-style tests using a fresh service import/path with existing files.
6. Update README and validate with pytest plus OpenSpec strict mode.
