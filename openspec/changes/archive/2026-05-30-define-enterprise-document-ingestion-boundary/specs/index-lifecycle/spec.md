## ADDED Requirements

### Requirement: Index lifecycle exposes pre-ingestion diagnostics

The system SHALL provide source-scoped pre-ingestion diagnostics before lifecycle jobs are created, while keeping actual indexing as an explicit job operation.

#### Scenario: Preflight precedes job creation

- **WHEN** a caller requests source ingestion preflight
- **THEN** the provider reports whether the source is ready for an ingestion job without creating a job

#### Scenario: Preflight includes current lifecycle state

- **WHEN** source ingestion preflight runs
- **THEN** it includes the current index lifecycle status and latest index job id for the source

#### Scenario: Job execution remains explicit

- **WHEN** preflight recommends running ingestion
- **THEN** the caller must still explicitly create an ingestion job through `POST /api/ingestion/jobs`
