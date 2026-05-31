## ADDED Requirements

### Requirement: RAG sources expose source package metadata
The system SHALL expose provider-owned source package metadata for document RAG sources so callers can review source identity, business ownership, document expectations, and citation policy before ingestion or binding.

#### Scenario: Source document manifest includes package metadata
- **WHEN** a caller requests `GET /api/rag/sources/{source_id}/documents` for a known RAG source
- **THEN** the result includes a `source_package` with source id, owner, version, domain, language, sensitivity, supported formats, default chunking strategy, citation granularity, and allowed parser statuses

#### Scenario: Ingestion preflight includes package metadata
- **WHEN** a caller requests `GET /api/ingestion/sources/{source_id}/preflight` for a known RAG source
- **THEN** the result includes the same source package metadata without creating ingestion jobs or rebuilding indexes

### Requirement: RAG source diagnostics expose chunk manifests
The system SHALL expose deterministic chunk manifest diagnostics for supported local markdown source documents.

#### Scenario: Source document manifest includes chunk manifest entries
- **WHEN** a caller requests `GET /api/rag/sources/{source_id}/documents` for a markdown source file that exists
- **THEN** each manifest document includes chunk manifest entries with chunk id, citation, chunking strategy, source path, character count, and capped preview text

#### Scenario: Ingestion preflight includes chunk manifest entries
- **WHEN** a caller requests `GET /api/ingestion/sources/{source_id}/preflight` for a markdown source file that can be parsed
- **THEN** each preflight document includes chunk manifest entries aligned with the chunk preview and citation anchors

#### Scenario: Unsupported documents do not fabricate chunk manifests
- **WHEN** a source document has an unsupported format or missing file
- **THEN** the diagnostic response reports the blocking parser or file status and returns an empty chunk manifest for that document

#### Scenario: Chunk manifest diagnostics remain read-only
- **WHEN** chunk manifest diagnostics are requested
- **THEN** the provider does not create ingestion jobs, write lifecycle records, call embedding models, call vector databases, execute retrieval, or execute GraphRAG
