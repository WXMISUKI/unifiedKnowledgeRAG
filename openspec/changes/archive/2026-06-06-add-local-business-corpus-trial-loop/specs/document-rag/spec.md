## ADDED Requirements

### Requirement: Local trial source overlays remain outside default document RAG catalog
The system SHALL allow local trial source overlays to evaluate markdown corpus readiness without adding those sources to the default provider source catalog.

#### Scenario: Trial source overlay is evaluated
- **WHEN** a local business corpus trial reads a trial source overlay
- **THEN** the overlay can provide source id, title, owner, domain, language, sensitivity, and markdown path for local report generation
- **AND** the default `GET /api/rag/sources` catalog remains unchanged

#### Scenario: Trial source overlay is not formal registration
- **WHEN** a trial source overlay exists under local run artifacts
- **THEN** the provider does not treat that overlay as a source-to-agent binding, production fixture, formal ingestion job, or runtime retrieval default
