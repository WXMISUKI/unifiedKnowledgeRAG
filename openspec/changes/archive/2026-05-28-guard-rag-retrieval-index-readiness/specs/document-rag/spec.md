## MODIFIED Requirements

### Requirement: RAG retrieve returns compact evidence context

The system SHALL return compact answer context and document evidence for matching document RAG queries while preserving the existing response contract across retrieval backends and enforcing explicit source index lifecycle readiness before backend retrieval work begins.

#### Scenario: Retrieval finds matching documents

- **WHEN** a caller requests `POST /api/rag/retrieve` with a valid query and ready knowledge base id whose index status is ready
- **THEN** the response has `ok=true`, `result.answer_context`, and `result.documents` with stable `citation` values

#### Scenario: LlamaIndex retrieval preserves provider citations

- **WHEN** the LlamaIndex backend returns matching indexed nodes
- **THEN** each response document is assembled from provider-owned metadata and includes `source_id`, `document_id`, `title`, `snippet`, `score`, and stable `citation`

#### Scenario: Indexed source is not ready

- **WHEN** a caller requests `POST /api/rag/retrieve` for a known source whose index status is not ready
- **THEN** the response has `ok=false` and an `error.code` that identifies the index readiness failure

#### Scenario: Not-ready source does not execute backend retrieval

- **WHEN** a caller requests `POST /api/rag/retrieve` for a known source whose index status is not ready
- **THEN** the provider returns `INDEX_NOT_READY` before calling the selected backend retrieval implementation

### Requirement: RAG retrieve rejects unknown sources

The system SHALL reject retrieval requests for unknown or unavailable knowledge base ids with structured provider errors before backend retrieval work begins.

#### Scenario: Unknown source is requested

- **WHEN** a caller requests `POST /api/rag/retrieve` with an unknown knowledge base id
- **THEN** the response has `ok=false` and an `error.code` that identifies the unknown source

#### Scenario: Unknown source does not execute backend retrieval

- **WHEN** a caller requests `POST /api/rag/retrieve` with an unknown knowledge base id
- **THEN** the provider returns `UNKNOWN_KNOWLEDGE_BASE` before calling the selected backend retrieval implementation
