## Context

`jobs.jsonl` is append-only. A single logical job may have multiple records, such as `running` followed by `completed` or `failed`. The current list endpoint returns all records, which is useful for raw debugging but not ideal as a governance API. A user-facing job history should show the latest logical state per job id and should be bounded.

This change adds a small local retention operation to keep the file from growing forever in local provider runs.

## Goals / Non-Goals

**Goals:**

- Add bounded list responses using `limit` and `offset`.
- Include pagination metadata.
- List latest logical job state per `job_id`.
- Compact `jobs.jsonl` to retain the newest N logical jobs.
- Keep existing detail/retry contracts stable.

**Non-Goals:**

- No cursor tokens, scheduled retention, archival export, or delete-by-id API.
- No multi-process locking beyond the existing local atomic write style.
- No auth/tenant policy.
- No UI work.

## Decisions

1. List latest logical jobs, not every raw JSONL event.

   Detail and retry already use latest-by-job-id semantics. The list API should match that operational view.

2. Sort newest first for API listing and retention.

   Operators usually care about recent ingestion work first. Retention will keep the newest N logical jobs.

3. Keep `limit` capped.

   The router should constrain `limit` to a small maximum to avoid accidental huge responses.

4. Implement retention as explicit compaction.

   Retention is not automatic in this slice. A caller must invoke the compaction endpoint with `keep_latest`.

## Risks / Trade-offs

- Offset pagination can drift if jobs are created while browsing -> acceptable for local provider; cursor pagination can come later.
- Compaction discards older job records -> explicit endpoint and `keep_latest` count make the behavior clear.
- Raw intermediate records are no longer visible in list -> the API is an operational logical view; raw file remains local implementation detail until compaction.

## Migration Plan

1. Extend contract models.
2. Add latest-job projection and pagination in the store.
3. Add explicit retention compaction.
4. Wire router parameters/endpoints.
5. Add tests and docs.
6. Validate with pytest and OpenSpec strict mode.
