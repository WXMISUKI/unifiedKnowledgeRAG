## ADDED Requirements

### Requirement: Qdrant text query uses embedding adapter orchestration

The system SHALL execute opt-in Qdrant text retrieval by embedding query text before vector search.

#### Scenario: Query text is embedded

- **WHEN** Qdrant text retrieval is requested
- **THEN** the query text is embedded through the configured embedding adapter before Qdrant vector query

#### Scenario: Qdrant hits become evidence documents

- **WHEN** Qdrant vector query returns valid evidence payload hits
- **THEN** the retrieval result contains `EvidenceDocument` items using the existing evidence mapping

#### Scenario: Qdrant remains opt-in

- **WHEN** Qdrant text query orchestration is available
- **THEN** the default retrieval backend remains unchanged

### Requirement: Qdrant readiness includes embedding readiness

The system SHALL report Qdrant backend readiness from both Qdrant collection readiness and embedding adapter readiness.

#### Scenario: Embedding adapter is degraded

- **WHEN** the configured embedding adapter is not ready
- **THEN** Qdrant backend readiness is degraded with an embedding reason

#### Scenario: Qdrant collection is degraded

- **WHEN** Qdrant collection readiness is degraded
- **THEN** Qdrant backend readiness is degraded with a Qdrant reason
