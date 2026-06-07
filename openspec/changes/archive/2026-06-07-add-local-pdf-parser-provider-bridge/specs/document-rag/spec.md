# document-rag Specification Delta

## ADDED Requirements

### Requirement: Document RAG can consume local PDF parser provider bridge artifacts
The document RAG ingestion path SHALL allow a local PDF parser provider bridge to produce normalized parser artifacts that enter the existing parser-artifact local ingestion loop.

#### Scenario: PDF bridge artifact enters existing ingestion path
- **WHEN** a local PDF parser provider bridge creates a normalized parser artifact with `decision=go`
- **THEN** document RAG reuses the existing parser artifact materialization and local approved-source ingestion loop
- **AND** raw PDF direct ingestion remains unsupported
- **AND** retrieval defaults, source binding policy, and GraphRAG execution remain unchanged
