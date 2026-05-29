## MODIFIED Requirements

### Requirement: Provider health reports machine-readable readiness
The system SHALL expose provider health with machine-readable service, RAG, answer composer, graph, document retrieval backend, and source index lifecycle readiness fields.

#### Scenario: Provider health is ready
- **WHEN** a caller requests `GET /health`
- **THEN** the response includes `status`, `service`, `rag.status`, `rag.backend`, `rag.backend_status`, `rag.index_status`, `answer.status`, `answer.backend`, `answer.backend_status`, and `graph.status`

#### Scenario: Document retrieval backend is degraded
- **WHEN** the configured document retrieval backend cannot load its index lifecycle status
- **THEN** `GET /health` reports provider `status=degraded` and includes a machine-readable RAG degradation reason

#### Scenario: Answer composer is degraded
- **WHEN** the configured answer composer is unavailable
- **THEN** `GET /health` reports provider `status=degraded` and includes a machine-readable answer degradation reason

### Requirement: Provider capabilities expose stable knowledge capability ids
The system SHALL expose stable capability identifiers and optional invocation metadata for document RAG retrieval, document RAG cited answer orchestration, and graph query boundaries while keeping production infrastructure choices behind explicit architecture decision records.

#### Scenario: Capabilities are discoverable
- **WHEN** a caller requests `GET /api/capabilities`
- **THEN** the response includes `knowledge.rag.retrieve`, `knowledge.rag.answer`, and `knowledge.graph.query` capability ids with machine-readable status and HTTP invocation metadata

#### Scenario: Retrieval capability is invokable
- **WHEN** a caller inspects the `knowledge.rag.retrieve` capability
- **THEN** its invocation metadata identifies `POST /api/rag/retrieve`

#### Scenario: Answer capability is invokable
- **WHEN** a caller inspects the `knowledge.rag.answer` capability
- **THEN** its invocation metadata identifies `POST /api/rag/answer`

#### Scenario: Answer composer is not ready
- **WHEN** the configured answer composer is unavailable
- **THEN** the `knowledge.rag.answer` capability status is `degraded`

#### Scenario: Production infrastructure is not yet selected
- **WHEN** embedding model, vector database, queue worker, reranker, graph storage, or production answer composer choices are still open
- **THEN** provider capabilities remain provider-neutral and do not expose implementation-specific dependency details as API contracts
