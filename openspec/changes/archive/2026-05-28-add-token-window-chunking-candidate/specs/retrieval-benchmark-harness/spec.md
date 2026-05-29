## MODIFIED Requirements

### Requirement: Chunking strategy candidates can be evaluated locally

The system SHALL export local evidence for chunking strategy candidates without changing runtime ingestion behavior.

#### Scenario: Chunking candidate evidence is exported

- **WHEN** chunking strategy evaluation is run with source ids and an output directory
- **THEN** the system writes JSON and Markdown evidence with one result per candidate strategy

#### Scenario: Implemented strategy reports source metrics

- **WHEN** an implemented chunking strategy is evaluated
- **THEN** the evidence includes source ids, chunk counts, citation stability, chunking strategy id, and implementation status

#### Scenario: Runnable section strategy reports source metrics

- **WHEN** `markdown-section-v1` is evaluated
- **THEN** the evidence reports section chunk counts, citation stability, source ids, and runnable implementation status without changing ingestion defaults

#### Scenario: Runnable token-window strategy reports source metrics

- **WHEN** `token-window-v1` is evaluated
- **THEN** the evidence reports token-window chunk counts, citation stability, source ids, and runnable implementation status without changing ingestion defaults

#### Scenario: Evaluation does not change ingestion defaults

- **WHEN** chunking strategy evidence is exported
- **THEN** runtime Qdrant ingestion continues using the configured baseline strategy

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

#### Scenario: Token-window strategy participates in comparison

- **WHEN** chunking comparison uses `token-window-v1`
- **THEN** the comparison indexes token-window chunks and includes their strategy-level metrics

#### Scenario: Comparison remains local

- **WHEN** chunking comparison evidence is exported
- **THEN** runtime Qdrant ingestion defaults and public HTTP APIs remain unchanged
