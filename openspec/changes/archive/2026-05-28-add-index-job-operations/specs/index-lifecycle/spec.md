## ADDED Requirements

### Requirement: Ingestion jobs are queryable

The system SHALL expose persisted ingestion job history through provider APIs.

#### Scenario: Jobs are listed

- **WHEN** a caller requests `GET /api/ingestion/jobs`
- **THEN** the response includes persisted ingestion jobs ordered by request time

#### Scenario: Jobs are filtered by source and status

- **WHEN** a caller requests `GET /api/ingestion/jobs` with `source_id` or `status` query parameters
- **THEN** the response includes only jobs matching the supplied filters

#### Scenario: Job detail is returned

- **WHEN** a caller requests `GET /api/ingestion/jobs/{job_id}` for a persisted job
- **THEN** the response includes the matching job record

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
