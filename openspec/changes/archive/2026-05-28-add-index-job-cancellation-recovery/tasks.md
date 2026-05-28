## 1. Specification

- [x] 1.1 Validate `add-index-job-cancellation-recovery` with OpenSpec strict mode
- [x] 1.2 Keep cancellation/recovery explicit and local-only in docs

## 2. Contract Models

- [x] 2.1 Add cancellation request/response models
- [x] 2.2 Add stale-running recovery request/response models
- [x] 2.3 Add structured errors for cancel-ineligible jobs

## 3. Store And Service

- [x] 3.1 Add store helper to append terminal canceled job state
- [x] 3.2 Add stale running job detection by age
- [x] 3.3 Add service function for job cancellation
- [x] 3.4 Add service function for stale-running recovery
- [x] 3.5 Keep source status aligned when latest source job is canceled or stale-failed

## 4. API Wiring

- [x] 4.1 Add `POST /api/ingestion/jobs/{job_id}/cancel`
- [x] 4.2 Add `POST /api/ingestion/jobs/recovery/stale-running`
- [x] 4.3 Preserve create/list/detail/retry/pagination/retention behavior

## 5. Verification

- [x] 5.1 Add tests for canceling running jobs
- [x] 5.2 Add tests for rejecting cancellation of terminal jobs
- [x] 5.3 Add tests for stale-running recovery
- [x] 5.4 Add tests that stale-recovered jobs can be retried
- [x] 5.5 Run `conda run -n GRAPHRAG python -m pytest -q`
- [x] 5.6 Run `openspec validate add-index-job-cancellation-recovery --strict`

## 6. Documentation

- [x] 6.1 Document cancellation endpoint in README
- [x] 6.2 Document stale-running recovery endpoint and limitations
