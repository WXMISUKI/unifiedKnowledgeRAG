## ADDED Requirements

### Requirement: Qdrant and BGE-M3 smoke evidence gates promotion

The system SHALL require local Qdrant + BGE-M3 smoke evidence before treating the stack as more than a candidate retrieval path.

#### Scenario: Local stack is evaluated

- **WHEN** the project evaluates Qdrant with local BGE-M3 for Chinese-heavy retrieval
- **THEN** the evaluation references exported smoke evidence that includes ingestion, retrieval, metadata, and benchmark metrics

#### Scenario: Smoke evidence is not production approval

- **WHEN** Qdrant + BGE-M3 smoke evidence exists
- **THEN** the project treats it as early integration evidence and not final production acceptance
