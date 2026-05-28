## ADDED Requirements

### Requirement: Chunking strategy candidates can be evaluated locally

The system SHALL export local evidence for chunking strategy candidates without changing runtime ingestion behavior.

#### Scenario: Chunking candidate evidence is exported
- **WHEN** chunking strategy evaluation is run with source ids and an output directory
- **THEN** the system writes JSON and Markdown evidence with one result per candidate strategy

#### Scenario: Implemented strategy reports source metrics
- **WHEN** an implemented chunking strategy is evaluated
- **THEN** the evidence includes source ids, chunk counts, citation stability, chunking strategy id, and implementation status

#### Scenario: Planned strategy remains non-runnable
- **WHEN** a planned but unimplemented chunking strategy is evaluated
- **THEN** the evidence marks it as planned and does not claim retrieval metrics

#### Scenario: Evaluation does not change ingestion defaults
- **WHEN** chunking strategy evidence is exported
- **THEN** runtime Qdrant ingestion continues using the configured baseline strategy
