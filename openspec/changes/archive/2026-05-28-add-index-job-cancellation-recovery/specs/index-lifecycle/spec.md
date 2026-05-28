## ADDED Requirements

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
