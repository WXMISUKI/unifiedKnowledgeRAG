# document-rag Specification

## Purpose
TBD - created by archiving change add-knowledge-provider-v1. Update Purpose after archive.
## Requirements
### Requirement: RAG sources are listed separately from graph sources

The system SHALL expose document RAG source metadata through a dedicated endpoint, including each source's configured retrieval backend and backend readiness status.

#### Scenario: RAG source list is available

- **WHEN** a caller requests `GET /api/rag/sources`
- **THEN** the response includes configured knowledge base ids, readiness status, version, freshness metadata, retrieval backend, and backend readiness status

### Requirement: RAG retrieve returns compact evidence context

The system SHALL return compact answer context and document evidence for matching document RAG queries while preserving the existing response contract across retrieval backends and respecting explicit source index lifecycle status.

#### Scenario: Retrieval finds matching documents

- **WHEN** a caller requests `POST /api/rag/retrieve` with a valid query and ready knowledge base id whose index status is ready
- **THEN** the response has `ok=true`, `result.answer_context`, and `result.documents` with stable `citation` values

#### Scenario: LlamaIndex retrieval preserves provider citations

- **WHEN** the LlamaIndex backend returns matching indexed nodes
- **THEN** each response document is assembled from provider-owned metadata and includes `source_id`, `document_id`, `title`, `snippet`, `score`, and stable `citation`

#### Scenario: Indexed source is not ready

- **WHEN** a caller requests `POST /api/rag/retrieve` for a known source whose index status is not ready
- **THEN** the response has `ok=false` and an `error.code` that identifies the index readiness failure

### Requirement: RAG retrieval backend is configurable

The system SHALL select the document retrieval backend from configuration without changing the HTTP API contract.

#### Scenario: Fixture backend is selected

- **WHEN** `RAG_RETRIEVAL_BACKEND` is configured as `fixture`
- **THEN** document retrieval uses the deterministic local fixture backend

#### Scenario: LlamaIndex backend is selected

- **WHEN** `RAG_RETRIEVAL_BACKEND` is configured as `llamaindex`
- **THEN** document retrieval uses the LlamaIndex-backed local index service

### Requirement: LlamaIndex backend manages local index readiness

The system SHALL report local LlamaIndex readiness from explicit source index lifecycle state rather than performing hidden indexing during retrieval.

#### Scenario: LlamaIndex index is ready

- **WHEN** configured source documents and source index lifecycle status are ready
- **THEN** the backend readiness status is `ready`

#### Scenario: LlamaIndex index is unavailable

- **WHEN** configured source documents or source index lifecycle status cannot be loaded or built
- **THEN** the backend readiness status is `degraded` with a machine-readable reason

### Requirement: RAG retrieve handles empty retrieval explicitly

The system SHALL treat no matching evidence as a successful empty retrieval result.

#### Scenario: Retrieval finds no documents

- **WHEN** a caller requests `POST /api/rag/retrieve` with a valid query that has no matching evidence
- **THEN** the response has `ok=true`, an empty `result.documents` array, and an empty `result.answer_context`

#### Scenario: LlamaIndex retrieval finds no documents

- **WHEN** a LlamaIndex retrieval query has no matching evidence above the configured threshold
- **THEN** the response has `ok=true`, an empty `result.documents` array, and an empty `result.answer_context`

### Requirement: RAG retrieve rejects unknown sources

The system SHALL reject retrieval requests for unknown or unavailable knowledge base ids with structured provider errors.

#### Scenario: Unknown source is requested

- **WHEN** a caller requests `POST /api/rag/retrieve` with an unknown knowledge base id
- **THEN** the response has `ok=false` and an `error.code` that identifies the unknown source
