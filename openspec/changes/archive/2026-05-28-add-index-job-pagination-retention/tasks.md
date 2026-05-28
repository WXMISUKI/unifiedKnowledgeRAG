## 1. Specification

- [x] 1.1 Validate `add-index-job-pagination-retention` with OpenSpec strict mode
- [x] 1.2 Keep pagination and retention local-only in docs

## 2. Contract Models

- [x] 2.1 Add pagination metadata to job list response
- [x] 2.2 Add retention compaction request and response models
- [x] 2.3 Preserve existing job detail and retry response shapes

## 3. Store And Service

- [x] 3.1 Add latest logical job projection by `job_id`
- [x] 3.2 Add filter and pagination support over latest jobs
- [x] 3.3 Add local compaction that keeps newest logical jobs
- [x] 3.4 Add service wrapper for paginated listing
- [x] 3.5 Add service wrapper for retention compaction

## 4. API Wiring

- [x] 4.1 Add `limit` and `offset` query params to `GET /api/ingestion/jobs`
- [x] 4.2 Return `total`, `limit`, `offset`, and `has_more`
- [x] 4.3 Add `POST /api/ingestion/jobs/retention/compact`
- [x] 4.4 Preserve source/status filters

## 5. Verification

- [x] 5.1 Add tests for latest-state deduplicated job listing
- [x] 5.2 Add tests for limit/offset pagination metadata
- [x] 5.3 Add tests for filtered totals
- [x] 5.4 Add tests for local retention compaction
- [x] 5.5 Run `conda run -n GRAPHRAG python -m pytest -q`
- [x] 5.6 Run `openspec validate add-index-job-pagination-retention --strict`

## 6. Documentation

- [x] 6.1 Document pagination query params in README
- [x] 6.2 Document retention compaction endpoint and limitations
