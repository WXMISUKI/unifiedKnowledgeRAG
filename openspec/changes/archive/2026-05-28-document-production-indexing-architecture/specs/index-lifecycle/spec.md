## MODIFIED Requirements

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
