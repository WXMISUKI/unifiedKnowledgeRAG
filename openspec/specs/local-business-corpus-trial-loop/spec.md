# local-business-corpus-trial-loop Specification

## Purpose
TBD - created by archiving change add-local-business-corpus-trial-loop. Update Purpose after archive.
## Requirements
### Requirement: Provider exports a local business corpus trial loop
The system SHALL export a local-only trial report for a caller-supplied markdown business corpus without registering it as a default provider source.

#### Scenario: Business markdown corpus is usable
- **WHEN** the export command receives an existing markdown path and the trial query produces answerable evidence
- **THEN** the report has `decision=go`
- **AND** it writes a trial source overlay, JSON report, Markdown report, generated chunks, and cited answer metadata

#### Scenario: Business markdown file is missing
- **WHEN** the configured markdown path does not exist
- **THEN** the report has `decision=blocked`
- **AND** it recommends checking the markdown path or rerunning the PDF-derived markdown step

#### Scenario: Business markdown has no chunkable content
- **WHEN** the configured markdown file exists but has no chunkable text
- **THEN** the report has `decision=blocked`
- **AND** it records that the local corpus content must be repaired before trial use

#### Scenario: Business markdown evidence is weak
- **WHEN** the markdown can be chunked but the trial query produces no answerable evidence
- **THEN** the report has `decision=review`
- **AND** it recommends reviewing the query, source content, or page range used to derive the markdown

#### Scenario: Trial answer citations are outside allowlist
- **WHEN** the trial answer cites values outside the generated evidence citation allowlist
- **THEN** the report has `decision=blocked`
- **AND** it records a citation contract failure

### Requirement: Local business corpus trial remains pre-registration only
The local business corpus trial SHALL validate business markdown before formal source registration without mutating runtime provider defaults.

#### Scenario: Trial loop runs
- **WHEN** the local business corpus trial command runs
- **THEN** it does not modify the default source catalog, run formal ingestion jobs, persist index lifecycle state, create source bindings, promote retrieval backends, parse raw PDFs, start OCR services, execute GraphRAG, or run MyPrivateAgent orchestration

#### Scenario: Source overlay is written
- **WHEN** the trial writes a source overlay
- **THEN** the overlay is recorded as local trial metadata and not as an approved production source fixture

