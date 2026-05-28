## MODIFIED Requirements

### Requirement: RAG sources are listed separately from graph sources

The system SHALL expose document RAG source metadata through a dedicated endpoint, including each source's configured retrieval backend and backend readiness status.

#### Scenario: RAG source list is available

- **WHEN** a caller requests `GET /api/rag/sources`
- **THEN** the response includes configured knowledge base ids, readiness status, version, freshness metadata, retrieval backend, and backend readiness status

### Requirement: RAG retrieve returns compact evidence context

The system SHALL return compact answer context and document evidence for matching document RAG queries while preserving the existing response contract across retrieval backends.

#### Scenario: Retrieval finds matching documents

- **WHEN** a caller requests `POST /api/rag/retrieve` with a valid query and ready knowledge base id
- **THEN** the response has `ok=true`, `result.answer_context`, and `result.documents` with stable `citation` values

#### Scenario: LlamaIndex retrieval preserves provider citations

- **WHEN** the LlamaIndex backend returns matching indexed nodes
- **THEN** each response document is assembled from provider-owned metadata and includes `source_id`, `document_id`, `title`, `snippet`, `score`, and stable `citation`

## ADDED Requirements

### Requirement: RAG retrieval backend is configurable

The system SHALL select the document retrieval backend from configuration without changing the HTTP API contract.

#### Scenario: Fixture backend is selected

- **WHEN** `RAG_RETRIEVAL_BACKEND` is configured as `fixture`
- **THEN** document retrieval uses the deterministic local fixture backend

#### Scenario: LlamaIndex backend is selected

- **WHEN** `RAG_RETRIEVAL_BACKEND` is configured as `llamaindex`
- **THEN** document retrieval uses the LlamaIndex-backed local index service

### Requirement: LlamaIndex backend manages local index readiness

The system SHALL load or build a local LlamaIndex document index from configured source documents before reporting the backend as ready.

#### Scenario: LlamaIndex index is ready

- **WHEN** configured source documents and index storage are available
- **THEN** the backend readiness status is `ready`

#### Scenario: LlamaIndex index is unavailable

- **WHEN** configured source documents or index storage cannot be loaded or built
- **THEN** the backend readiness status is `degraded` with a machine-readable reason

### Requirement: Empty retrieval remains explicit across backends

The system SHALL preserve explicit empty retrieval behavior for every configured document RAG backend.

#### Scenario: LlamaIndex retrieval finds no documents

- **WHEN** a LlamaIndex retrieval query has no matching evidence above the configured threshold
- **THEN** the response has `ok=true`, an empty `result.documents` array, and an empty `result.answer_context`
