## ADDED Requirements

### Requirement: Provider contract smoke validates graph schema discovery

The system SHALL validate graph schema discovery in provider contract smoke separately from planned graph query execution.

#### Scenario: Contract smoke checks graph schemas

- **WHEN** provider contract smoke runs
- **THEN** it calls `GET /api/graph/schemas` and records configured graph ids and graph metadata counts

#### Scenario: Contract smoke preserves planned graph query boundary

- **WHEN** provider contract smoke validates graph schema discovery
- **THEN** it still validates `POST /api/graph/query` as a planned not-implemented boundary rather than executable GraphRAG

#### Scenario: Graph schema contract smoke remains read-only

- **WHEN** provider contract smoke checks graph schemas
- **THEN** it does not execute graph queries, connect to graph stores, create ingestion jobs, extract entities, build ontology workflows, rebuild indexes, execute retrieval, or compose answers
