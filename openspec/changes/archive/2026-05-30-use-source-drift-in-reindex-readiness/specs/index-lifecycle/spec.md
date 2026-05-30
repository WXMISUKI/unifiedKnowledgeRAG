## ADDED Requirements

### Requirement: Reindex readiness uses source fingerprint drift diagnostics
The system SHALL include source document fingerprint drift diagnostics in local reindex readiness plans so operators can identify source changes before triggering or skipping reindex work.

#### Scenario: Reindex plan includes document drift summary
- **WHEN** the reindex readiness export runs
- **THEN** each source row includes document fingerprint summaries and an aggregate source fingerprint status

#### Scenario: Changed source recommends ingestion
- **WHEN** a source document reports `drift_status=changed`
- **THEN** the reindex readiness report recommends `run_ingestion_job` for that source and marks the overall report as `review`

#### Scenario: Unchecked fingerprint requires review
- **WHEN** a source document has no expected fingerprint and reports `drift_status=unchecked`
- **THEN** the reindex readiness report recommends `review_source_fingerprint` for that source

#### Scenario: Reindex drift planning remains read-only
- **WHEN** reindex readiness consumes source fingerprint diagnostics
- **THEN** it does not create ingestion jobs, rebuild indexes, compact job history, download models, call embedding services, call vector databases, or execute graph queries
