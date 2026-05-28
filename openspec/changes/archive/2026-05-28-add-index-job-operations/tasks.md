## 1. Specification

- [x] 1.1 Validate `add-index-job-operations` with OpenSpec strict mode
- [x] 1.2 Keep the slice limited to list/detail/retry operations

## 2. Contract Models

- [x] 2.1 Add ingestion job list response model
- [x] 2.2 Add ingestion job detail response model
- [x] 2.3 Add retry response envelope using existing job shape
- [x] 2.4 Add structured errors for missing jobs and retry-ineligible jobs

## 3. Store And Service

- [x] 3.1 Add filtered job listing to `IndexLifecycleStore`
- [x] 3.2 Add job lookup by `job_id`
- [x] 3.3 Add service function for job listing
- [x] 3.4 Add service function for job detail
- [x] 3.5 Add service function for retrying failed jobs

## 4. API Wiring

- [x] 4.1 Add `GET /api/ingestion/jobs`
- [x] 4.2 Add `GET /api/ingestion/jobs/{job_id}`
- [x] 4.3 Add `POST /api/ingestion/jobs/{job_id}/retry`
- [x] 4.4 Preserve existing `POST /api/ingestion/jobs`

## 5. Verification

- [x] 5.1 Add tests for job listing and filters
- [x] 5.2 Add tests for job detail and missing job error
- [x] 5.3 Add tests for failed job retry
- [x] 5.4 Add tests for non-failed retry rejection
- [x] 5.5 Run `conda run -n GRAPHRAG python -m pytest -q`
- [x] 5.6 Run `openspec validate add-index-job-operations --strict`

## 6. Documentation

- [x] 6.1 Document job list/detail/retry endpoints in README
- [x] 6.2 Document retry limitations and future retention/pagination scope
