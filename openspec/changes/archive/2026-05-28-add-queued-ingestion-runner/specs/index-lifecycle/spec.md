## ADDED Requirements

### Requirement: Ingestion jobs can be queued for explicit local execution

The system SHALL allow callers to create persisted ingestion jobs without immediately building the index.

#### Scenario: Queued ingestion job is created

- **WHEN** a caller requests `POST /api/ingestion/jobs` with `run_mode=queued`
- **THEN** the provider persists a job with `status=queued` and does not build the source index

#### Scenario: Synchronous ingestion remains the default

- **WHEN** a caller requests `POST /api/ingestion/jobs` without `run_mode`
- **THEN** the provider preserves the existing synchronous indexing behavior

### Requirement: Queued ingestion jobs can be processed explicitly

The system SHALL expose an explicit local operation that processes the next queued ingestion job.

#### Scenario: Next queued job completes

- **WHEN** a caller requests `POST /api/ingestion/jobs/queue/run-next` and a queued job can be indexed
- **THEN** the provider appends `running` and `completed` records for that job

#### Scenario: Next queued job fails

- **WHEN** a caller requests `POST /api/ingestion/jobs/queue/run-next` and indexing fails
- **THEN** the provider appends `running` and `failed` records with a structured provider error

#### Scenario: No queued job is available

- **WHEN** a caller requests `POST /api/ingestion/jobs/queue/run-next` and no queued job exists
- **THEN** the response uses a structured provider error code that states the queue is empty
