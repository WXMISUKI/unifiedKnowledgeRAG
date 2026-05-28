## ADDED Requirements

### Requirement: Qdrant smoke evidence can be exported locally

The system SHALL provide a local helper that runs a Qdrant ingestion-and-retrieval smoke flow and exports durable evidence files.

#### Scenario: Qdrant smoke evidence is exported

- **WHEN** the Qdrant smoke helper is run with source ids, benchmark cases, and an output directory
- **THEN** it indexes the sources, queries the cases, and writes JSON and Markdown evidence files

#### Scenario: Smoke evidence includes runtime metadata

- **WHEN** the Qdrant smoke helper exports evidence
- **THEN** the output includes Qdrant collection/vector metadata, embedding provider/model metadata, indexed source ids, and generated ingestion job ids

#### Scenario: Smoke helper remains local

- **WHEN** Qdrant smoke evidence is exported
- **THEN** the system writes local files without exposing a public HTTP API

### Requirement: Qdrant smoke uses one client per run

The system SHALL use one Qdrant client instance for both source ingestion and retrieval within a single smoke run.

#### Scenario: In-memory Qdrant is used

- **WHEN** the Qdrant smoke helper is configured with an in-memory Qdrant URL
- **THEN** source ingestion and retrieval use the same client so indexed chunks are queryable during the same run

#### Scenario: Smoke run reports actual retrieval misses

- **WHEN** indexed Qdrant retrieval returns citations that differ from expected benchmark citations
- **THEN** the evidence report records the miss rather than rewriting expected outcomes
