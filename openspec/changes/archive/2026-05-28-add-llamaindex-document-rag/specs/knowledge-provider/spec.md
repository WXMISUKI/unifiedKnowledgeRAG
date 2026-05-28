## MODIFIED Requirements

### Requirement: Provider health reports machine-readable readiness

The system SHALL expose provider health with machine-readable service, RAG, graph, and document retrieval backend readiness fields.

#### Scenario: Provider health is ready

- **WHEN** a caller requests `GET /health`
- **THEN** the response includes `status`, `service`, `rag.status`, `rag.backend`, `rag.backend_status`, and `graph.status`

#### Scenario: Document retrieval backend is degraded

- **WHEN** the configured document retrieval backend cannot load or build its index
- **THEN** `GET /health` reports provider `status=degraded` and includes a machine-readable RAG degradation reason

### Requirement: Catalog exposes source readiness

The system SHALL expose a source catalog that lists knowledge bases and graph namespaces with stable ids, status, owners, version metadata, and backend readiness metadata.

#### Scenario: Catalog lists configured sources

- **WHEN** a caller requests `GET /api/catalog`
- **THEN** the response includes `knowledge_bases` and `graphs` arrays with stable source ids, readiness status, and document retrieval backend metadata
