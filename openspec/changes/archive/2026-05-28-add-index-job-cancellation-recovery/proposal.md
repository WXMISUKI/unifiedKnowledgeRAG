## Why

Ingestion jobs are now persisted and queryable, but a provider restart or interrupted local process can leave jobs stuck in `running`. Operators need explicit cancellation and stale-running recovery so the lifecycle store can return to a retryable, auditable state.

## What Changes

- Add an API to cancel a running ingestion job.
- Add an API to recover stale running jobs older than a caller-supplied threshold.
- Mark stale running jobs as failed with a structured provider error so they can be retried.
- Keep cancellation/recovery local and explicit; no background scheduler is introduced in this slice.
- Preserve existing create/list/detail/retry/pagination/retention behavior.

## Capabilities

### New Capabilities

### Modified Capabilities

- `index-lifecycle`: Running ingestion jobs can be canceled or recovered from stale-running state through provider APIs.

## Impact

- Extends contract models with cancellation and stale recovery request/response envelopes.
- Extends the file-backed lifecycle store with latest running job updates.
- Extends `app/services/index_lifecycle.py` with cancel and recover operations.
- Adds router endpoints under `/api/ingestion/jobs`.
- Adds tests for cancellation, non-running cancellation rejection, stale recovery, and retry after stale recovery.
- Updates README and OpenSpec specs.
