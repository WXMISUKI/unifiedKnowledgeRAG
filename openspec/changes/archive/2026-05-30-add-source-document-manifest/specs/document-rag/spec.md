## ADDED Requirements

### Requirement: RAG source document manifest is available
The system SHALL expose a read-only document manifest for each configured document RAG source so callers can inspect source documents, citation anchors, chunking metadata, and index readiness without running retrieval.

#### Scenario: Source document manifest is returned
- **WHEN** a caller requests `GET /api/rag/sources/{source_id}/documents` for a configured RAG source
- **THEN** the response has `ok=true`, the requested source id, current index readiness metadata, and document manifests with document id, title, source path, format, version, chunking strategy, and citation anchors

#### Scenario: Unknown source returns structured error
- **WHEN** a caller requests `GET /api/rag/sources/{source_id}/documents` for an unknown source
- **THEN** the response has `ok=false` and an `error.code` that identifies the unknown source

#### Scenario: Manifest does not execute retrieval work
- **WHEN** a caller requests a source document manifest
- **THEN** the provider does not run document retrieval, answer composition, embedding, vector search, ingestion, or graph execution
