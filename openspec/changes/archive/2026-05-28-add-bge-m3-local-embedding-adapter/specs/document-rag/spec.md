## ADDED Requirements

### Requirement: Local BGE-M3 embeddings integrate with Qdrant evidence chunks

The system SHALL allow Qdrant evidence chunks to be embedded with the opt-in local BGE-M3 adapter.

#### Scenario: Qdrant chunks are embedded with BGE-M3

- **WHEN** `EMBEDDING_PROVIDER=bge_m3_local` is selected and Qdrant chunks are embedded
- **THEN** chunk metadata identifies the embedding provider and model used for dense vectors

#### Scenario: BGE-M3 is not the default path

- **WHEN** no embedding provider is configured
- **THEN** the system continues using the deterministic mock adapter for local contract tests
