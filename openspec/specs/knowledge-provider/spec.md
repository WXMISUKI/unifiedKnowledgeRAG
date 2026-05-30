# knowledge-provider Specification

## Purpose
TBD - created by archiving change add-knowledge-provider-v1. Update Purpose after archive.
## Requirements
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

### Requirement: Catalog exposes source readiness

The system SHALL expose a source catalog that lists knowledge bases and graph namespaces with stable ids, status, owners, version metadata, backend readiness metadata, and durable source index lifecycle metadata.

#### Scenario: Catalog lists configured sources

- **WHEN** a caller requests `GET /api/catalog`
- **THEN** the response includes `knowledge_bases` and `graphs` arrays with stable source ids, readiness status, document retrieval backend metadata, and source index lifecycle status loaded from the local lifecycle store

### Requirement: Graph schema boundary is explicit

The system SHALL expose graph schema metadata separately from document RAG retrieval.

#### Scenario: Graph schemas are discoverable

- **WHEN** a caller requests `GET /api/graph/schemas`
- **THEN** the response includes graph ids and serializable schema metadata

### Requirement: Graph query boundary returns structured status

The system SHALL expose a graph query endpoint that returns serializable graph result envelopes or structured provider errors.

#### Scenario: Graph query is not implemented in first slice

- **WHEN** a caller requests `POST /api/graph/query` during the document-RAG-only slice
- **THEN** the response uses a structured error code that states graph query execution is not implemented

### Requirement: Provider errors expose machine-readable details
The system SHALL include optional machine-readable details on structured provider errors without changing existing error codes or messages.

#### Scenario: Unknown RAG source error includes details
- **WHEN** a caller requests document RAG retrieval or answer with unknown knowledge base ids
- **THEN** the provider error includes `details.requested_source_ids` and `details.unknown_source_ids`

#### Scenario: Not-ready RAG index error includes details
- **WHEN** a caller requests document RAG retrieval or answer for a source whose index is not ready
- **THEN** the provider error includes `details.requested_source_ids`, `details.not_ready_source_ids`, and `details.retrieval_backend`

#### Scenario: Answer composer error includes details
- **WHEN** the configured answer composer is unsupported or not implemented
- **THEN** the provider error includes the configured composer, configured model, and supported composer names

#### Scenario: Graph query not implemented error includes details
- **WHEN** a caller requests `POST /api/graph/query` before GraphRAG execution is implemented
- **THEN** the provider error includes the requested graph id, planned status, and graph capability id

#### Scenario: Existing error envelope is preserved
- **WHEN** provider error details are added
- **THEN** existing `ok=false`, `result=null`, `error.code`, and `error.message` behavior remains compatible

