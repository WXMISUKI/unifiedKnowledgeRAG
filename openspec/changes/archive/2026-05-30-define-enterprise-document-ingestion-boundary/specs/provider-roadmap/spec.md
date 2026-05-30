## ADDED Requirements

### Requirement: Enterprise ingestion boundary advances Phase 2 without heavy parsers

The project SHALL treat pre-ingestion document diagnostics as Phase 2 enterprise document ingestion baseline work when it improves source readiness visibility without approving production parser dependencies.

#### Scenario: Ingestion boundary is phase-aligned

- **WHEN** an OpenSpec change adds source document ingestion preflight diagnostics
- **THEN** the roadmap treats it as Phase 2 document ingestion baseline work

#### Scenario: Parser dependencies remain gated

- **WHEN** ingestion preflight reports unsupported formats
- **THEN** it does not imply approval to add OCR, PDF, Word, Excel, HTML, table extraction, or layout parsing dependencies without a separate evidence-backed change
