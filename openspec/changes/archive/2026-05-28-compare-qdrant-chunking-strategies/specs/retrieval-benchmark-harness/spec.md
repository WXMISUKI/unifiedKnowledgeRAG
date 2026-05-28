## ADDED Requirements

### Requirement: Qdrant chunking strategies can be compared with smoke evidence

The system SHALL export local Qdrant+BGE smoke comparison evidence for selected chunking strategies without changing runtime ingestion defaults.

#### Scenario: Chunking comparison evidence is exported
- **WHEN** chunking comparison is run with source ids, benchmark cases, chunking strategy ids, and an output directory
- **THEN** the system writes JSON and Markdown evidence with one Qdrant smoke report per strategy

#### Scenario: Comparison preserves benchmark expectations
- **WHEN** a chunking strategy returns citations that differ from expected benchmark citations
- **THEN** the comparison records lower citation match instead of rewriting expected citations

#### Scenario: Comparison includes strategy-level metrics
- **WHEN** chunking comparison evidence is exported
- **THEN** the output includes each strategy id, chunk count, hit rate, citation match rate, empty handling rate, and long-section category metrics

#### Scenario: Comparison remains local
- **WHEN** chunking comparison evidence is exported
- **THEN** runtime Qdrant ingestion defaults and public HTTP APIs remain unchanged
