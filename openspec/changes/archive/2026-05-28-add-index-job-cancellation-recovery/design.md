## Context

Local ingestion jobs are currently synchronous, but the durable store is append-only and can contain `running` as the latest state for a job if the process exits between writing the running record and writing the terminal record. Without explicit recovery, these jobs remain in a confusing state and cannot be retried.

This change keeps recovery explicit and local. It avoids background workers while establishing the status transition rules needed for future asynchronous execution.

## Goals / Non-Goals

**Goals:**

- Cancel running jobs with structured lifecycle status.
- Reject cancellation of terminal jobs.
- Detect running jobs older than `max_age_seconds`.
- Mark stale running jobs as failed with machine-readable error details.
- Allow retry of stale-recovered failed jobs through the existing retry API.

**Non-Goals:**

- No async worker cancellation signal.
- No scheduled stale scanner.
- No lock manager or distributed lease.
- No UI or auth policy.

## Decisions

1. Append terminal records instead of mutating existing records.

   The store already treats `jobs.jsonl` as append-only and resolves latest state by `job_id`. Cancellation and stale recovery should append a new terminal record.

2. Use `canceled` for explicit user cancellation.

   Canceled jobs are terminal and not retryable in this slice. If retry for canceled jobs becomes useful, it should be a separate requirement.

3. Use `failed` for stale running recovery.

   Stale jobs likely represent interrupted execution. Marking them failed lets the existing retry path work without another retry state.

4. Keep source status consistent for latest source job.

   If the canceled or stale-recovered job is the latest job for its source, the source index status should reflect the terminal failure/cancellation reason.

## Risks / Trade-offs

- Clock-based stale detection depends on local timestamps -> acceptable for local provider; distributed leases can come later.
- Explicit recovery means stale jobs remain until called -> safer than silent background mutation in this slice.
- Cancel does not stop a currently executing in-process job -> local create is synchronous today; future async workers need cooperative cancellation.

## Migration Plan

1. Add request/response models.
2. Add store helpers for appending terminal job states and finding stale running jobs.
3. Add service operations.
4. Add router endpoints.
5. Add tests and README docs.
6. Validate with pytest and OpenSpec strict mode.
