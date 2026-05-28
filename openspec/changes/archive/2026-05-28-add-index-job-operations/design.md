## Context

`persist-index-lifecycle-store` introduced a durable local `jobs.jsonl` and `sources.json`, but the HTTP surface still only supports creating a job and checking source status. That is not enough for operating even a local provider because failed jobs cannot be inspected or retried without opening files manually.

This change adds a small operational API layer while preserving the local, synchronous implementation style.

## Goals / Non-Goals

**Goals:**

- List persisted ingestion jobs.
- Retrieve a single job by id.
- Retry failed jobs by creating a new ingestion job for the same source.
- Return structured errors for missing jobs and retry-ineligible jobs.
- Keep the local durable store replaceable by future database/queue infrastructure.

**Non-Goals:**

- No cancellation, retention compaction, pagination cursor, async worker, or distributed lock.
- No retry of completed or running jobs.
- No auth/tenant policy in this slice.

## Decisions

1. Reuse `IndexLifecycleJob` as the job item shape.

   The current job record already contains the fields callers need. List/detail envelopes should wrap this model rather than inventing a second DTO.

2. Implement retry by delegating to `create_ingestion_job(source_id)`.

   A retry should be a new job record, not a mutation of the old failed job. This preserves append-only history in `jobs.jsonl`.

3. Allow simple filters only.

   `source_id` and `status` are enough for current operations. Cursor pagination and retention are better handled once job volume or UI needs are clearer.

4. Keep errors in provider envelope style.

   Missing job returns `JOB_NOT_FOUND`; retrying non-failed jobs returns `JOB_RETRY_NOT_ALLOWED`.

## Risks / Trade-offs

- Listing all jobs can become expensive as JSONL grows -> acceptable for local provider slice; future retention/pagination can address it.
- Retry is synchronous -> consistent with existing ingestion behavior and easy to test.
- No auth means endpoints are local-trust only -> document that governance policy is future work.

## Migration Plan

1. Add response models for job list/detail/retry.
2. Add store lookup/filter helpers.
3. Add service functions for list/get/retry.
4. Add router endpoints.
5. Add tests and README docs.
6. Validate with pytest and OpenSpec strict mode.
