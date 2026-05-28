## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: Ingestion job history can be compacted locally

The system SHALL expose an explicit local compaction operation that retains the newest logical ingestion jobs.

#### Scenario: Job history is compacted

- **WHEN** a caller requests `POST /api/ingestion/jobs/retention/compact` with `keep_latest`
- **THEN** the provider rewrites the local job store to retain only the newest `keep_latest` logical jobs

#### Scenario: Compaction reports retention metadata

- **WHEN** compaction completes
- **THEN** the response includes `before_count`, `after_count`, and `removed_count`
