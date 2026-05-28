# index-lifecycle Specification

## Purpose
Defines provider-owned source index lifecycle contracts for document RAG sources.

## Requirements
### Requirement: Ingestion jobs can be created for document RAG sources

The system SHALL expose an ingestion job endpoint that starts a source-scoped document index lifecycle operation and persists the resulting job record in the local lifecycle store.

#### Scenario: Local ingestion job is accepted

- **WHEN** a caller requests `POST /api/ingestion/jobs` with a known document RAG `source_id`
- **THEN** the response includes a stable `job_id`, `source_id`, `status`, `requested_at`, and `completed_at` when the local build finishes

#### Scenario: Ingestion job survives provider restart

- **WHEN** a local ingestion job has completed and the provider process restarts
- **THEN** the local lifecycle store still contains the completed job record and the source status references the latest `job_id`

#### Scenario: Unknown source ingestion is rejected

- **WHEN** a caller requests `POST /api/ingestion/jobs` with an unknown `source_id`
- **THEN** the response uses a structured provider error code that identifies the unknown source

### Requirement: Source index status is inspectable

The system SHALL expose a source-scoped index status endpoint for document RAG sources using durable local source lifecycle state.

#### Scenario: Indexed source status is returned

- **WHEN** a caller requests `GET /api/indexes/{source_id}/status` for an indexed source
- **THEN** the response includes `source_id`, `status=ready`, `backend`, `indexed_at`, and the latest `job_id`

#### Scenario: Source status survives provider restart

- **WHEN** a source index status was persisted as ready and the provider process restarts
- **THEN** `GET /api/indexes/{source_id}/status` still returns `status=ready` from the local manifest

#### Scenario: Source without index is reported explicitly

- **WHEN** a caller requests `GET /api/indexes/{source_id}/status` before an index has been built
- **THEN** the response includes `source_id`, `status=not_indexed`, `backend`, and a machine-readable reason

### Requirement: Index lifecycle failures are machine-readable

The system SHALL preserve failed ingestion details as structured lifecycle status in the durable local lifecycle store.

#### Scenario: Ingestion job fails

- **WHEN** a local index build fails for a known source
- **THEN** the job status is `failed` and the index status includes a machine-readable failure reason

### Requirement: Ingestion jobs are queryable

The system SHALL expose persisted ingestion job history through provider APIs as a paginated logical job view.

#### Scenario: Jobs are listed

- **WHEN** a caller requests `GET /api/ingestion/jobs`
- **THEN** the response includes the latest persisted state for each ingestion job ordered by newest request time

#### Scenario: Jobs are filtered by source and status

- **WHEN** a caller requests `GET /api/ingestion/jobs` with `source_id` or `status` query parameters
- **THEN** the response includes only logical jobs matching the supplied filters

#### Scenario: Jobs are paginated

- **WHEN** a caller requests `GET /api/ingestion/jobs` with `limit` and `offset`
- **THEN** the response includes `jobs`, `total`, `limit`, `offset`, and `has_more`

#### Scenario: Job detail is returned

- **WHEN** a caller requests `GET /api/ingestion/jobs/{job_id}` for a persisted job
- **THEN** the response includes the matching latest job record

#### Scenario: Missing job detail is structured

- **WHEN** a caller requests `GET /api/ingestion/jobs/{job_id}` for an unknown job id
- **THEN** the response uses a structured provider error code that identifies the missing job

### Requirement: Failed ingestion jobs can be retried

The system SHALL allow a failed ingestion job to be retried by creating a new ingestion job for the same source.

#### Scenario: Failed job retry creates a new job

- **WHEN** a caller requests `POST /api/ingestion/jobs/{job_id}/retry` for a failed job
- **THEN** the response includes a new job id for the same `source_id`

#### Scenario: Non-failed job retry is rejected

- **WHEN** a caller requests `POST /api/ingestion/jobs/{job_id}/retry` for a job that is not failed
- **THEN** the response uses a structured provider error code that states retry is not allowed

### Requirement: Ingestion job history can be compacted locally

The system SHALL expose an explicit local compaction operation that retains the newest logical ingestion jobs.

#### Scenario: Job history is compacted

- **WHEN** a caller requests `POST /api/ingestion/jobs/retention/compact` with `keep_latest`
- **THEN** the provider rewrites the local job store to retain only the newest `keep_latest` logical jobs

#### Scenario: Compaction reports retention metadata

- **WHEN** compaction completes
- **THEN** the response includes `before_count`, `after_count`, and `removed_count`

### Requirement: Running ingestion jobs can be canceled

The system SHALL expose an explicit cancellation operation for running ingestion jobs.

#### Scenario: Running job is canceled

- **WHEN** a caller requests `POST /api/ingestion/jobs/{job_id}/cancel` for a running job
- **THEN** the provider appends a terminal `canceled` job record with a machine-readable reason

#### Scenario: Terminal job cancellation is rejected

- **WHEN** a caller requests cancellation for a job that is not running
- **THEN** the response uses a structured provider error code that states cancellation is not allowed

### Requirement: Stale running ingestion jobs can be recovered

The system SHALL expose explicit stale-running recovery for ingestion jobs that exceed a caller-supplied age threshold.

#### Scenario: Stale running jobs are marked failed

- **WHEN** a caller requests `POST /api/ingestion/jobs/recovery/stale-running` with `max_age_seconds`
- **THEN** running jobs older than the threshold are appended as `failed` with a machine-readable stale-running error

#### Scenario: Stale recovery reports affected jobs

- **WHEN** stale-running recovery completes
- **THEN** the response includes the recovered job ids and `recovered_count`

#### Scenario: Fresh running jobs are not recovered

- **WHEN** a running job is newer than `max_age_seconds`
- **THEN** stale-running recovery leaves the job in `running` state

### Requirement: Ingestion jobs can be queued for explicit local execution

The system SHALL allow callers to create persisted ingestion jobs without immediately building the index.

#### Scenario: Queued ingestion job is created

- **WHEN** a caller requests `POST /api/ingestion/jobs` with `run_mode=queued`
- **THEN** the provider persists a job with `status=queued` and does not build the source index

#### Scenario: Synchronous ingestion remains the default

- **WHEN** a caller requests `POST /api/ingestion/jobs` without `run_mode`
- **THEN** the provider preserves the existing synchronous indexing behavior

### Requirement: Queued ingestion jobs can be processed explicitly

The system SHALL expose an explicit local operation that processes the next queued ingestion job, while production queue worker implementation remains gated by the production indexing architecture decision record.

#### Scenario: Next queued job completes

- **WHEN** a caller requests `POST /api/ingestion/jobs/queue/run-next` and a queued job can be indexed
- **THEN** the provider appends `running` and `completed` records for that job

#### Scenario: Next queued job fails

- **WHEN** a caller requests `POST /api/ingestion/jobs/queue/run-next` and indexing fails
- **THEN** the provider appends `running` and `failed` records with a structured provider error

#### Scenario: No queued job is available

- **WHEN** a caller requests `POST /api/ingestion/jobs/queue/run-next` and no queued job exists
- **THEN** the response uses a structured provider error code that states the queue is empty

#### Scenario: Production queue worker is proposed

- **WHEN** a change proposes a background worker, external queue, lease service, or distributed scheduler
- **THEN** the change references the production indexing architecture decision record and states the approved queue/worker boundary

### Requirement: Retrieval readiness uses persisted source lifecycle state

The system SHALL use persisted source lifecycle status as the canonical source readiness gate before production retrieval backends execute source-scoped retrieval.

#### Scenario: Qdrant source is ready after ingestion

- **WHEN** Qdrant ingestion has persisted `status=ready` for a source
- **THEN** Qdrant retrieval readiness treats that source as ready

#### Scenario: Qdrant source without ready marker is blocked

- **WHEN** a Qdrant retrieval request references a known source without persisted `status=ready`
- **THEN** the provider reports that source as not ready before executing Qdrant retrieval
