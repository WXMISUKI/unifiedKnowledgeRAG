## Why

The ingestion job API now exposes persisted job history, but `GET /api/ingestion/jobs` returns an unbounded list and the append-only JSONL file can grow indefinitely. The next slice should make job history safe for governance UI consumption and give local operators a controlled compaction path.

## What Changes

- Add `limit` and `offset` pagination to `GET /api/ingestion/jobs`.
- Return `total`, `limit`, `offset`, and `has_more` metadata with job list responses.
- Treat job listing as the latest state per `job_id`, so append-only intermediate records do not appear as duplicate jobs.
- Add a local retention/compaction API that keeps the newest N logical jobs and rewrites `jobs.jsonl`.
- Preserve source/status filters and existing detail/retry behavior.
- Keep pagination offset-based and retention local-only; cursor pagination, scheduled retention, archival export, and auth policy remain future changes.

## Capabilities

### New Capabilities

### Modified Capabilities

- `index-lifecycle`: Job history listing becomes paginated, deduplicated by latest job state, and locally compactable.

## Impact

- Extends job list response metadata in `app/models/contracts.py`.
- Adds retention request/response models.
- Extends `IndexLifecycleStore` with latest-job projection, pagination, and compaction.
- Extends `app/routers/ingestion.py` with retention compaction.
- Adds focused tests for pagination, filter totals, deduplication, and compaction.
- Updates README and OpenSpec specs.
