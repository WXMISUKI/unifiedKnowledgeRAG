## ADDED Requirements

### Requirement: Reindex readiness plan can be exported locally
The system SHALL provide a local read-only reindex readiness plan that summarizes configured source index state before operators trigger reindex work.

#### Scenario: Reindex plan includes per-source status
- **WHEN** the reindex readiness export runs
- **THEN** the report includes each configured source id, source file presence, current index status, latest ingestion job metadata, and recommended action

#### Scenario: Reindex plan includes job history summary
- **WHEN** the reindex readiness export runs
- **THEN** the report includes total latest logical job count and per-status job counts from the local lifecycle store

#### Scenario: Reindex plan remains read-only
- **WHEN** the reindex readiness export runs
- **THEN** it does not start ingestion jobs, rebuild indexes, compact job history, download models, call embedding services, call vector databases, or execute graph queries

#### Scenario: Reindex plan writes review artifacts
- **WHEN** a caller runs the reindex readiness export command
- **THEN** the system writes machine-readable JSON and human-readable Markdown evidence files
