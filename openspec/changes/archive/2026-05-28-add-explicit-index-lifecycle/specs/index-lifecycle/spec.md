## ADDED Requirements

### Requirement: Ingestion jobs can be created for document RAG sources

The system SHALL expose an ingestion job endpoint that starts a source-scoped document index lifecycle operation.

#### Scenario: Local ingestion job is accepted

- **WHEN** a caller requests `POST /api/ingestion/jobs` with a known document RAG `source_id`
- **THEN** the response includes a stable `job_id`, `source_id`, `status`, `requested_at`, and `completed_at` when the local build finishes

#### Scenario: Unknown source ingestion is rejected

- **WHEN** a caller requests `POST /api/ingestion/jobs` with an unknown `source_id`
- **THEN** the response uses a structured provider error code that identifies the unknown source

### Requirement: Source index status is inspectable

The system SHALL expose a source-scoped index status endpoint for document RAG sources.

#### Scenario: Indexed source status is returned

- **WHEN** a caller requests `GET /api/indexes/{source_id}/status` for an indexed source
- **THEN** the response includes `source_id`, `status=ready`, `backend`, `indexed_at`, and the latest `job_id`

#### Scenario: Source without index is reported explicitly

- **WHEN** a caller requests `GET /api/indexes/{source_id}/status` before an index has been built
- **THEN** the response includes `source_id`, `status=not_indexed`, `backend`, and a machine-readable reason

### Requirement: Index lifecycle failures are machine-readable

The system SHALL preserve failed ingestion details as structured lifecycle status.

#### Scenario: Ingestion job fails

- **WHEN** a local index build fails for a known source
- **THEN** the job status is `failed` and the index status includes a machine-readable failure reason
