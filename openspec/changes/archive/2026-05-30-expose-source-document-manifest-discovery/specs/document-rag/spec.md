## ADDED Requirements

### Requirement: Source document manifest diagnostics are discoverable
The document RAG source document manifest endpoint SHALL be discoverable through provider-owned capability metadata.

#### Scenario: Source document manifest capability points to endpoint
- **WHEN** a caller inspects provider capabilities
- **THEN** the source document manifest capability identifies `GET /api/rag/sources/{source_id}/documents` and the `SourceDocumentManifestResponse` schema

#### Scenario: Diagnostic discovery does not change retrieval behavior
- **WHEN** source document manifest discovery metadata is added
- **THEN** existing retrieve and answer request and response contracts remain unchanged
