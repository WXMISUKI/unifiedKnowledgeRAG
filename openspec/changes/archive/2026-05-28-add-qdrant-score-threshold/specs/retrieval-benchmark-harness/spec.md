## MODIFIED Requirements

### Requirement: Qdrant smoke evidence can be exported locally

The system SHALL provide a local helper that runs a Qdrant ingestion-and-retrieval smoke flow and exports durable evidence files, including the configured retrieval score threshold used by the run.

#### Scenario: Qdrant smoke evidence is exported

- **WHEN** the Qdrant smoke helper is run with source ids, benchmark cases, and an output directory
- **THEN** it indexes the sources, queries the cases, and writes JSON and Markdown evidence files

#### Scenario: Smoke evidence includes runtime metadata

- **WHEN** the Qdrant smoke helper exports evidence
- **THEN** the output includes Qdrant collection/vector metadata, embedding provider/model metadata, indexed source ids, generated ingestion job ids, and the configured retrieval score threshold

#### Scenario: Smoke helper remains local

- **WHEN** Qdrant smoke evidence is exported
- **THEN** the system writes local files without exposing a public HTTP API
