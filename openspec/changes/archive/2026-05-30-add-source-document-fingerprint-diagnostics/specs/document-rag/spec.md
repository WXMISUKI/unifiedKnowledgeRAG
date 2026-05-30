## ADDED Requirements

### Requirement: Source document manifest includes fingerprint diagnostics
The system SHALL include read-only content fingerprint diagnostics in source document manifests for configured local source documents.

#### Scenario: Manifest reports in-sync source file
- **WHEN** a caller requests `GET /api/rag/sources/{source_id}/documents` for a configured source whose document file exists and matches the provider-owned expected digest
- **THEN** each document manifest includes `source_file_status=present`, `content_sha256`, `expected_content_sha256`, `content_byte_size`, and `drift_status=in_sync`

#### Scenario: Manifest reports changed source file
- **WHEN** a configured source document file exists but its current sha256 differs from the expected digest
- **THEN** the document manifest reports `drift_status=changed` without modifying the file or index lifecycle state

#### Scenario: Manifest reports missing source file
- **WHEN** a configured source document file is missing
- **THEN** the document manifest reports `source_file_status=missing` and `drift_status=missing`

#### Scenario: Fingerprint diagnostics remain read-only
- **WHEN** source document fingerprint diagnostics are generated
- **THEN** the provider does not run retrieval, answer composition, ingestion jobs, index rebuilds, embedding models, vector databases, directory crawling, or graph queries
