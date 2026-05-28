## Why

Ingestion lifecycle operations are now observable, retryable, cancelable, and recoverable, but indexing still executes synchronously by default. The next low-risk slice should introduce a queued execution state without choosing production queue infrastructure, embedding models, or vector databases yet.

## What Changes

- Add optional `run_mode="queued"` to ingestion job creation.
- Queued jobs are persisted with status `queued` and do not build the index immediately.
- Add an explicit local runner endpoint to process the next queued job.
- Runner transitions a job through `running` into `completed` or `failed`.
- Preserve existing synchronous `POST /api/ingestion/jobs` behavior as the default.
- Keep this local and in-process; external queues, background services, worker pools, embedding model choices, and vector database choices are future decisions to discuss separately.

## Capabilities

### New Capabilities

### Modified Capabilities

- `index-lifecycle`: Ingestion jobs support queued local execution and explicit processing of the next queued job.

## Impact

- Extends ingestion job request contracts with `run_mode`.
- Adds a queue runner response model.
- Extends lifecycle services with enqueue and run-next behavior.
- Adds route `POST /api/ingestion/jobs/queue/run-next`.
- Adds tests for queued creation, run-next success, run-next empty queue, run-next failure, and preservation of synchronous defaults.
- Updates README and OpenSpec specs.
