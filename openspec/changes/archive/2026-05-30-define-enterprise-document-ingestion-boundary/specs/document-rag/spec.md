## ADDED Requirements

### Requirement: Document ingestion preflight is available

The system SHALL expose a read-only pre-ingestion diagnostic surface for configured document RAG sources so callers can inspect document readiness before creating ingestion jobs.

#### Scenario: Source ingestion preflight returns document diagnostics

- **WHEN** a caller requests `GET /api/ingestion/sources/{source_id}/preflight` for a configured source
- **THEN** the response includes source id, overall status, current index status, document diagnostics, operation notes, and a recommended action

#### Scenario: Ingestion preflight is discoverable

- **WHEN** a caller requests `GET /api/provider/manifest`
- **THEN** the manifest endpoints include `ingestion_source_preflight_template` with the path `/api/ingestion/sources/{source_id}/preflight`

#### Scenario: Markdown document is preflighted

- **WHEN** a configured markdown source file exists and has non-empty chunkable content
- **THEN** the document diagnostic reports `parser_status=ready`, `format_supported=true`, chunk count, chunk preview, citation anchor count, and `recommended_action=run_ingestion_job`

#### Scenario: Unsupported document format fails closed

- **WHEN** a configured document has a format other than markdown in this slice
- **THEN** the document diagnostic reports `format_supported=false`, `parser_status=unsupported_format`, and does not attempt to parse the file

#### Scenario: Missing source file is diagnosed

- **WHEN** a configured document source file is missing
- **THEN** the document diagnostic reports `file_status=missing`, `parser_status=missing_source_file`, and the source preflight recommends restoring the source file before ingestion

#### Scenario: Ingestion preflight is side-effect free

- **WHEN** a caller requests source ingestion preflight
- **THEN** the provider does not create ingestion jobs, write lifecycle records, rebuild indexes, call embedding models, call vector databases, execute retrieval, answer composition, or GraphRAG
