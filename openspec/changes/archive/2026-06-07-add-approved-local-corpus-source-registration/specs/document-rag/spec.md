## MODIFIED Requirements

### Requirement: RAG sources are listed separately from graph sources

The system SHALL expose document RAG source metadata through a dedicated endpoint, including each built-in and approved local source's configured retrieval backend and backend readiness status.

#### Scenario: RAG source list is available

- **WHEN** a caller requests `GET /api/rag/sources`
- **THEN** the response includes configured knowledge base ids, readiness status, version, freshness metadata, retrieval backend, and backend readiness status

#### Scenario: Approved local source list is available

- **WHEN** a local corpus has been registered through the approved local source registry
- **THEN** `GET /api/rag/sources` includes the approved local source without changing graph source output

### Requirement: RAG source document manifest is available

The system SHALL expose a read-only document manifest for each configured document RAG source, including approved local markdown sources, so callers can inspect source documents, citation anchors, chunking metadata, and index readiness without running retrieval.

#### Scenario: Source document manifest is returned

- **WHEN** a caller requests `GET /api/rag/sources/{source_id}/documents` for a configured RAG source
- **THEN** the response has `ok=true`, the requested source id, current index readiness metadata, and document manifests with document id, title, source path, format, version, chunking strategy, and citation anchors

#### Scenario: Approved local source manifest is returned

- **WHEN** a caller requests `GET /api/rag/sources/{source_id}/documents` for an approved local markdown source
- **THEN** the response has `ok=true`
- **AND** the manifest includes source package metadata, fingerprint diagnostics, and deterministic chunk manifest entries

### Requirement: RAG retrieve returns compact evidence context

The system SHALL return compact answer context and document evidence for matching document RAG queries while preserving the existing response contract across retrieval backends and enforcing explicit source index lifecycle readiness before backend retrieval work begins.

#### Scenario: Retrieval finds matching documents

- **WHEN** a caller requests `POST /api/rag/retrieve` with a valid query and ready knowledge base id whose index status is ready
- **THEN** the response has `ok=true`, `result.answer_context`, and `result.documents` with stable `citation` values

#### Scenario: Approved local source retrieval returns evidence

- **WHEN** a caller requests `POST /api/rag/retrieve` for a ready approved local markdown source and a matching query
- **THEN** the response returns evidence documents with the approved source id, provider-owned source path metadata, deterministic chunk id, and stable citation
