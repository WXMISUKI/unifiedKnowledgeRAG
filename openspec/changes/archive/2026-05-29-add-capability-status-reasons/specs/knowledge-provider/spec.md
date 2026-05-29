## MODIFIED Requirements

### Requirement: Provider capabilities expose stable knowledge capability ids
The system SHALL expose stable capability identifiers and optional status reason and invocation metadata, including request and response schema references when available, for document RAG retrieval, document RAG cited answer orchestration, and graph query boundaries while keeping production infrastructure choices behind explicit architecture decision records.

#### Scenario: Capabilities are discoverable
- **WHEN** a caller requests `GET /api/capabilities`
- **THEN** the response includes `knowledge.rag.retrieve`, `knowledge.rag.answer`, and `knowledge.graph.query` capability ids with machine-readable status and HTTP invocation metadata

#### Scenario: Retrieval capability is invokable
- **WHEN** a caller inspects the `knowledge.rag.retrieve` capability
- **THEN** its invocation metadata identifies `POST /api/rag/retrieve` and references the retrieval request and response schemas

#### Scenario: Answer capability is invokable
- **WHEN** a caller inspects the `knowledge.rag.answer` capability
- **THEN** its invocation metadata identifies `POST /api/rag/answer` and references the answer request and response schemas

#### Scenario: Answer composer is not ready
- **WHEN** the configured answer composer is unavailable
- **THEN** the `knowledge.rag.answer` capability status is `degraded` and includes a reason

#### Scenario: Graph query is planned
- **WHEN** a caller inspects the `knowledge.graph.query` capability
- **THEN** its status is `planned` and includes a reason

#### Scenario: Production infrastructure is not yet selected
- **WHEN** embedding model, vector database, queue worker, reranker, graph storage, or production answer composer choices are still open
- **THEN** provider capabilities remain provider-neutral and do not expose implementation-specific dependency details as API contracts
