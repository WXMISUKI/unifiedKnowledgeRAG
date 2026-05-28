## 1. Specification

- [x] 1.1 Validate `add-explicit-index-lifecycle` with OpenSpec strict mode
- [x] 1.2 Keep index lifecycle scope local-only and provider-neutral in README/docs

## 2. Contract Models

- [x] 2.1 Add ingestion job request/response and index status response models
- [x] 2.2 Add source index lifecycle fields to health/catalog contract models
- [x] 2.3 Add structured provider error codes for unknown source and index-not-ready cases

## 3. Lifecycle Services

- [x] 3.1 Add a local index lifecycle service with in-memory job records
- [x] 3.2 Add source validation and per-source lifecycle status lookup
- [x] 3.3 Add synchronous local build orchestration for known LlamaIndex sources
- [x] 3.4 Preserve failed job reasons and expose them through source index status

## 4. API Wiring

- [x] 4.1 Add `POST /api/ingestion/jobs`
- [x] 4.2 Add `GET /api/indexes/{source_id}/status`
- [x] 4.3 Register new routers in `create_app()`
- [x] 4.4 Update `/health`, `/api/catalog`, and `/api/rag/sources` metadata with index lifecycle status

## 5. Retrieval Integration

- [x] 5.1 Refactor LlamaIndex index build/load helpers so lifecycle service can invoke indexing explicitly
- [x] 5.2 Prevent retrieval from silently building indexes for sources whose lifecycle status is not ready
- [x] 5.3 Preserve fixture backend behavior and existing `/api/rag/retrieve` response shape

## 6. Verification

- [x] 6.1 Add tests for ingestion job creation and unknown source rejection
- [x] 6.2 Add tests for source index status before and after local indexing
- [x] 6.3 Add tests for retrieval index-not-ready structured errors
- [x] 6.4 Add tests for health/catalog lifecycle metadata
- [x] 6.5 Run `conda run -n GRAPHRAG python -m pytest -q`
- [x] 6.6 Run `openspec validate add-explicit-index-lifecycle --strict`

## 7. Documentation

- [x] 7.1 Document index lifecycle endpoints in README
- [x] 7.2 Document rollback path to fixture backend and local-only job persistence limitations
