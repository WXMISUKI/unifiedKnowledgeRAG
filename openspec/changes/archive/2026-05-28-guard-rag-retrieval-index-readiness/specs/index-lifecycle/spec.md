## ADDED Requirements

### Requirement: Retrieval readiness uses persisted source lifecycle state

The system SHALL use persisted source lifecycle status as the canonical source readiness gate before production retrieval backends execute source-scoped retrieval.

#### Scenario: Qdrant source is ready after ingestion

- **WHEN** Qdrant ingestion has persisted `status=ready` for a source
- **THEN** Qdrant retrieval readiness treats that source as ready

#### Scenario: Qdrant source without ready marker is blocked

- **WHEN** a Qdrant retrieval request references a known source without persisted `status=ready`
- **THEN** the provider reports that source as not ready before executing Qdrant retrieval
