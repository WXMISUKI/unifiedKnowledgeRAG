## ADDED Requirements

### Requirement: Provider preflight summarizes graph boundary schemas

The system SHALL include compact graph schema discovery details in provider preflight graph boundary evidence without executing graph queries.

#### Scenario: Preflight summarizes graph namespaces

- **WHEN** a caller requests `GET /api/provider/preflight`
- **THEN** the `graph_boundary` check details include graph schema count and configured graph ids

#### Scenario: Preflight preserves planned graph execution

- **WHEN** graph schemas are summarized in provider preflight
- **THEN** the `graph_boundary` check still reports graph query execution as planned until GraphRAG execution is separately approved

#### Scenario: Graph boundary preflight remains read-only

- **WHEN** provider preflight summarizes graph schemas
- **THEN** it does not execute graph queries, connect to graph stores, create ingestion jobs, extract entities, build ontology workflows, rebuild indexes, execute retrieval, or compose answers
