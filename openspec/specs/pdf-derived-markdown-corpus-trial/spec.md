# pdf-derived-markdown-corpus-trial Specification

## Purpose
TBD - created by archiving change add-pdf-derived-markdown-corpus-trial. Update Purpose after archive.
## Requirements
### Requirement: Provider exports a PDF-derived markdown corpus trial
The system SHALL export a local-only trial report that converts a caller-supplied PDF page range into a markdown artifact and evaluates whether the derived text is usable for local RAG evidence.

#### Scenario: First five PDF pages produce usable markdown
- **WHEN** the export command receives an existing PDF path and the configured page range can be extracted into non-empty markdown
- **THEN** the trial writes the derived markdown artifact and report files
- **AND** the report has `decision=go` when retrieval evidence is answerable and answer citations are inside the allowed citation list

#### Scenario: PDF text extraction is unavailable
- **WHEN** the configured PDF extractor is unavailable or cannot read the PDF page range
- **THEN** the report has `decision=blocked`
- **AND** it recommends using an external OCR/Layout provider or installing an explicit local extractor for the trial

#### Scenario: Derived markdown has weak evidence
- **WHEN** the PDF page range is converted but the query does not produce answerable evidence
- **THEN** the report has `decision=review`
- **AND** it records that the query, page range, or extracted text quality should be reviewed

#### Scenario: Answer citations are outside derived evidence allowlist
- **WHEN** the generated answer cites values outside the trial evidence allowlist
- **THEN** the report has `decision=blocked`
- **AND** it records a citation contract failure

### Requirement: PDF trial preserves provider lightweight boundaries
The PDF-derived markdown corpus trial SHALL NOT make raw PDF ingestion a default provider capability.

#### Scenario: PDF trial runs
- **WHEN** the PDF-derived trial command runs
- **THEN** it does not start provider HTTP services, add raw PDF to source catalog defaults, create source bindings, promote retrieval backends, download models, start Qdrant/pgvector, execute GraphRAG, or run MyPrivateAgent orchestration

#### Scenario: Derived markdown is written
- **WHEN** the trial writes a derived markdown artifact
- **THEN** the artifact is recorded as local trial output and not as an approved production corpus fixture

