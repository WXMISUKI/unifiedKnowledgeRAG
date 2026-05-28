## Why

The current retrieval endpoint can call the selected backend before it checks explicit source index readiness. That is risky for production backends such as Qdrant because an unindexed source can still trigger an external vector query or model call before the API returns `INDEX_NOT_READY`.

Now that local BGE-M3 artifacts, Qdrant ingestion, and persisted lifecycle state exist, retrieval should treat lifecycle readiness as a hard precondition rather than a post-query check.

## What Changes

- Validate requested source ids before executing backend retrieval.
- Check source index lifecycle readiness before executing backend retrieval.
- Make Qdrant source readiness read the persisted lifecycle status instead of marking all known sources not ready.
- Add regression tests proving not-ready sources do not call Qdrant retrieval.
- Update documentation to show the expected ingestion-before-retrieval flow.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `document-rag`: Retrieval must enforce source/index readiness before backend retrieval work starts.
- `index-lifecycle`: Persisted source status is the canonical readiness gate for Qdrant retrieval.

## Impact

- Affects `POST /api/rag/retrieve` behavior ordering while preserving its response contract.
- Affects Qdrant backend `not_ready_sources` implementation.
- Adds focused API/backend regression tests.
- No new runtime dependencies.
