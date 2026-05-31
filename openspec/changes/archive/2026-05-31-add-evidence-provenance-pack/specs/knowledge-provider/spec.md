## ADDED Requirements

### Requirement: Evidence pack includes provenance metadata

The system SHALL include provider-owned provenance metadata in RAG evidence pack entries when the retrieval backend knows it.

#### Scenario: Retrieved evidence includes provenance

- **WHEN** a caller requests `POST /api/rag/retrieve` and documents are returned
- **THEN** each `metadata.evidence_pack.evidence` entry includes provenance fields for source path, chunk id, chunking strategy, and citation anchor when available

#### Scenario: Answer evidence includes provenance

- **WHEN** a caller requests `POST /api/rag/answer` and evidence is returned
- **THEN** the answer metadata evidence pack includes the same provenance metadata as retrieval for the returned evidence

#### Scenario: Public document envelope remains stable

- **WHEN** provenance metadata is added to evidence packs
- **THEN** the top-level returned `documents` entries retain their existing source id, document id, title, snippet, score, and citation contract

#### Scenario: Empty evidence pack remains explicit

- **WHEN** retrieval returns no documents
- **THEN** the evidence pack remains `insufficient_evidence` with an empty evidence list and no fabricated provenance
