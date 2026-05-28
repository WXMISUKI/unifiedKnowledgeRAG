## MODIFIED Requirements

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

### Requirement: LlamaIndex backend manages local index readiness

The system SHALL report local LlamaIndex readiness from explicit source index lifecycle state rather than performing hidden indexing during retrieval.

#### Scenario: LlamaIndex index is ready

- **WHEN** configured source documents and source index lifecycle status are ready
- **THEN** the backend readiness status is `ready`

#### Scenario: LlamaIndex index is unavailable

- **WHEN** configured source documents or source index lifecycle status cannot be loaded or built
- **THEN** the backend readiness status is `degraded` with a machine-readable reason
