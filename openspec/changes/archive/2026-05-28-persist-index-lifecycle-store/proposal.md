## Why

The explicit index lifecycle slice made indexing observable, but job records are still process-local and source state is scattered across ad hoc marker files. The provider needs a small durable local store so lifecycle status survives restarts and can become the foundation for future queue-backed indexing.

## What Changes

- Persist ingestion job records to a local JSONL job store under `RAG_INDEX_DIR`.
- Persist source index status in a normalized manifest file instead of treating individual marker files as the only lifecycle truth.
- Load persisted jobs and source status after process restart.
- Keep the API surface unchanged for `POST /api/ingestion/jobs` and `GET /api/indexes/{source_id}/status`.
- Keep the implementation local-file based; production databases, queues, locks across multiple processes, and remote object stores are future changes.

## Capabilities

### New Capabilities

### Modified Capabilities

- `index-lifecycle`: Job and source index status records become durable across provider process restarts.
- `knowledge-provider`: Health/catalog lifecycle metadata must be derived from durable local index state.

## Impact

- Updates `app/services/index_lifecycle.py` to use a small file-backed store abstraction.
- Adds local manifest/job files under `RAG_INDEX_DIR` at runtime.
- Updates tests to verify restart-style reload behavior without requiring a database.
- Updates README with the durable local store layout and limitations.
