## Why

The LlamaIndex backend currently proves provider-owned citation metadata and backend readiness, but index construction is still an implicit local startup concern. The next slice should make indexing an explicit provider lifecycle so callers can create, inspect, and retry source indexing without coupling retrieval traffic to index build behavior.

## What Changes

- Add an ingestion job API for document sources, starting with `POST /api/ingestion/jobs`.
- Add an index status API for source-scoped readiness, starting with `GET /api/indexes/{source_id}/status`.
- Track source index lifecycle states separately from retrieval backend process readiness.
- Preserve the existing retrieval contract while making not-yet-indexed sources return structured provider errors or degraded readiness metadata.
- Keep the first implementation local and deterministic; production queues, external vector stores, rerankers, incremental indexing, and auth policy remain future changes.

## Capabilities

### New Capabilities

- `index-lifecycle`: Source-scoped document index job creation, status inspection, and lifecycle state reporting.

### Modified Capabilities

- `document-rag`: Retrieval readiness must respect explicit source index status rather than relying only on backend initialization.
- `knowledge-provider`: Health and catalog metadata must expose source index lifecycle state in addition to backend readiness.

## Impact

- Adds API routes under `app/routers/` for ingestion jobs and index status.
- Adds service/model code for local index job records, source index status, and explicit LlamaIndex build orchestration.
- Updates `app/services/llamaindex_retriever.py` so index build can be invoked by lifecycle services instead of only on demand.
- Extends provider contract tests for job creation, status responses, degraded source readiness, and retrieval compatibility.
- Updates README and OpenSpec specs to document the new lifecycle boundary.
