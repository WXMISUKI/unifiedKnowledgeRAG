## Why

The provider now persists ingestion jobs, but operators can only infer state from source status. The next slice should expose job history and retry so failed or stale local indexing work can be inspected and re-run through provider-owned contracts.

## What Changes

- Add a job listing API for persisted ingestion jobs with optional `source_id` and `status` filters.
- Add a job detail API for a single persisted ingestion job.
- Add a retry API that creates a new ingestion job from an existing failed job.
- Keep retry local and synchronous for this slice.
- Preserve existing ingestion job creation and source status contracts.
- Leave retention, pagination tokens, cancellation, async queue workers, and auth policy for later changes.

## Capabilities

### New Capabilities

### Modified Capabilities

- `index-lifecycle`: Persisted ingestion jobs become queryable and failed jobs can be retried through stable provider APIs.

## Impact

- Extends `app/models/contracts.py` with job list/detail/retry response models.
- Extends `app/services/index_lifecycle.py` and `index_lifecycle_store.py` with filtered job lookup and retry orchestration.
- Extends `app/routers/ingestion.py` with `GET /api/ingestion/jobs`, `GET /api/ingestion/jobs/{job_id}`, and `POST /api/ingestion/jobs/{job_id}/retry`.
- Adds focused tests for listing, filtering, detail lookup, retry eligibility, and structured errors.
- Updates README and OpenSpec specs.
