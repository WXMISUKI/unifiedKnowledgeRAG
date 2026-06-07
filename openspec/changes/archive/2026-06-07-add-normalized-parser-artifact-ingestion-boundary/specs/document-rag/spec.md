## ADDED Requirements

### Requirement: Document RAG can accept normalized parser-derived markdown artifacts
The document RAG ingestion path SHALL allow externally parsed document output to enter the existing markdown-based local source flow through normalized parser artifacts.

#### Scenario: Parser artifact becomes markdown source artifact
- **WHEN** an external parser output has been validated as a normalized parser artifact with `decision=go`
- **THEN** the provider can materialize markdown and source overlay files that are compatible with local business corpus trial, source onboarding, and approved-source ingestion loop inputs

#### Scenario: Raw PDF remains unsupported by provider ingestion
- **WHEN** a caller or operator provides a raw PDF path directly to provider ingestion
- **THEN** provider ingestion still reports the file as unsupported
- **AND** it recommends producing a normalized parser artifact before retrying

#### Scenario: Parser artifact conversion preserves existing RAG contracts
- **WHEN** parser-derived markdown artifacts are generated
- **THEN** existing `GET /api/rag/sources`, `GET /api/ingestion/sources/{source_id}/preflight`, `POST /api/rag/retrieve`, and `POST /api/rag/answer` request and response contracts remain unchanged
