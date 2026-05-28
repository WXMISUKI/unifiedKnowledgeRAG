## ADDED Requirements

### Requirement: RAG sources are listed separately from graph sources

The system SHALL expose document RAG source metadata through a dedicated endpoint.

#### Scenario: RAG source list is available

- **WHEN** a caller requests `GET /api/rag/sources`
- **THEN** the response includes configured knowledge base ids, readiness status, version, and freshness metadata

### Requirement: RAG retrieve returns compact evidence context

The system SHALL return compact answer context and document evidence for matching document RAG queries.

#### Scenario: Retrieval finds matching documents

- **WHEN** a caller requests `POST /api/rag/retrieve` with a valid query and ready knowledge base id
- **THEN** the response has `ok=true`, `result.answer_context`, and `result.documents` with stable `citation` values

### Requirement: RAG retrieve handles empty retrieval explicitly

The system SHALL treat no matching evidence as a successful empty retrieval result.

#### Scenario: Retrieval finds no documents

- **WHEN** a caller requests `POST /api/rag/retrieve` with a valid query that has no matching evidence
- **THEN** the response has `ok=true`, an empty `result.documents` array, and an empty `result.answer_context`

### Requirement: RAG retrieve rejects unknown sources

The system SHALL reject retrieval requests for unknown or unavailable knowledge base ids with structured provider errors.

#### Scenario: Unknown source is requested

- **WHEN** a caller requests `POST /api/rag/retrieve` with an unknown knowledge base id
- **THEN** the response has `ok=false` and an `error.code` that identifies the unknown source
