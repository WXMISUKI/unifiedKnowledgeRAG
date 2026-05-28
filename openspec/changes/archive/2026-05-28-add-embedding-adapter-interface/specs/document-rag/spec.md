## ADDED Requirements

### Requirement: Embedding adapters expose a provider-neutral contract

The system SHALL convert text into dense vectors through a provider-neutral embedding adapter interface.

#### Scenario: Mock embedding is selected

- **WHEN** the embedding provider is configured as `mock`
- **THEN** the adapter returns deterministic vectors with the configured vector size

#### Scenario: Hosted embedding is not implemented

- **WHEN** the embedding provider is configured as `hosted` before a hosted model decision is approved
- **THEN** the adapter reports degraded readiness and fails closed when called

#### Scenario: Local embedding is not implemented

- **WHEN** the embedding provider is configured as `local` before a local model decision is approved
- **THEN** the adapter reports degraded readiness and fails closed when called

### Requirement: Qdrant chunks can receive vectors from embedding adapters

The system SHALL allow evidence chunks to be embedded before Qdrant upsert without changing their evidence payload metadata.

#### Scenario: Evidence chunk is embedded

- **WHEN** an evidence chunk text is embedded
- **THEN** the resulting Qdrant chunk keeps source, document, chunk, citation, text, and metadata fields while replacing the vector

#### Scenario: Text query orchestration remains separate

- **WHEN** embedding adapter helpers are added
- **THEN** the system does not automatically switch HTTP retrieval to Qdrant text-query mode
