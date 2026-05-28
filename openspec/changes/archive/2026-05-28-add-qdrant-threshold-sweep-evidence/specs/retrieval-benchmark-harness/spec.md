## ADDED Requirements

### Requirement: Qdrant smoke threshold sweep evidence can be exported locally

The system SHALL provide a local helper that runs Qdrant+BGE smoke evidence across explicit score thresholds and exports comparable threshold-level evidence.

#### Scenario: Threshold sweep evidence is exported
- **WHEN** the threshold sweep helper is run with source ids, benchmark cases, thresholds, and an output directory
- **THEN** it writes JSON and Markdown evidence files that include one Qdrant smoke benchmark report per threshold

#### Scenario: Threshold sweep includes comparable metrics
- **WHEN** threshold sweep evidence is exported
- **THEN** the output includes each threshold value, hit rate, citation match rate, empty handling rate, total cases, and embedding/vector metadata

#### Scenario: Threshold sweep remains local
- **WHEN** threshold sweep evidence is exported
- **THEN** the system writes local files without exposing a public HTTP API or changing the default retrieval threshold

#### Scenario: Threshold sweep rejects invalid thresholds
- **WHEN** a threshold sweep is requested with duplicate or out-of-range thresholds
- **THEN** the request is rejected before running Qdrant ingestion or retrieval
