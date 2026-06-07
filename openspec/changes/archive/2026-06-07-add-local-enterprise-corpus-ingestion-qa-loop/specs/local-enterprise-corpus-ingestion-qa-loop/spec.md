## ADDED Requirements

### Requirement: Local enterprise file can enter the approved-source ingestion QA loop
The provider SHALL expose a lightweight local enterprise corpus ingestion and QA loop that starts from a local file path and reuses the approved-source ingestion pipeline.

#### Scenario: Markdown file is ingested and tested
- **WHEN** a local `.md` or `.markdown` file exists
- **AND** the existing approved-source ingestion loop returns `go`
- **THEN** the local enterprise corpus loop decision is `go`
- **AND** the output includes the source id, title, original file path, materialized markdown path, query, downstream steps, artifacts, and recommended next action

#### Scenario: Text file is normalized before ingestion
- **WHEN** a local `.txt` file exists
- **THEN** the loop materializes a markdown staging file
- **AND** it passes that markdown file to the approved-source ingestion loop
- **AND** the output records `input_format=txt` and the staging markdown path

#### Scenario: Downstream ingestion needs review
- **WHEN** the approved-source ingestion loop returns `review`
- **THEN** the local enterprise corpus loop decision is `review`
- **AND** the output preserves the downstream reason code and artifacts

#### Scenario: Downstream ingestion is blocked
- **WHEN** the approved-source ingestion loop returns `blocked`
- **THEN** the local enterprise corpus loop decision is `blocked`
- **AND** the output preserves the downstream reason code and artifacts

### Requirement: Unsupported or missing local files fail clearly
The provider SHALL return bounded blocked states for missing files and unsupported direct-ingestion formats.

#### Scenario: File is missing
- **WHEN** the requested local file path does not exist
- **THEN** the loop decision is `blocked`
- **AND** the reason code is `input_file_missing`

#### Scenario: Raw PDF is supplied
- **WHEN** the requested local file path has a `.pdf` suffix
- **THEN** the loop decision is `blocked`
- **AND** the reason code is `raw_pdf_requires_parser_artifact`
- **AND** recommended actions point to parser/OCR-derived markdown or normalized parser artifact ingestion

#### Scenario: Unsupported format is supplied
- **WHEN** the requested local file path has an unsupported suffix
- **THEN** the loop decision is `blocked`
- **AND** the reason code is `unsupported_input_format`

### Requirement: Local enterprise corpus loop preserves lightweight boundaries
The local enterprise corpus loop SHALL remain a provider-local explicit trial and not promote caller behavior.

#### Scenario: Loop is run
- **WHEN** the loop exporter runs
- **THEN** it does not call MyPrivateAgent, create source-to-agent binding, start OCR/parser services, change default retrieval backend, mutate chat runtime, or execute GraphRAG
