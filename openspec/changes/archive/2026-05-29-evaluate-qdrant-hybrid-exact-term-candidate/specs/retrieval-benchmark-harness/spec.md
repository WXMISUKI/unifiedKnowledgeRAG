## ADDED Requirements

### Requirement: Qdrant hybrid exact-term smoke evidence can be exported locally

The system SHALL provide a named local export path for evaluating exact-term identifier cases against an evaluation-only Qdrant dense+sparse hybrid candidate.

#### Scenario: Hybrid exact-term smoke evidence is exported

- **WHEN** the hybrid exact-term smoke helper is run with source ids and an output directory
- **THEN** it indexes dense and sparse vectors, evaluates the exact-term identifier fixture, and writes JSON and Markdown evidence files with stable hybrid filenames

#### Scenario: Hybrid evidence includes vector strategy metadata

- **WHEN** hybrid exact-term evidence is exported
- **THEN** the output includes dense vector name, sparse vector name, fusion strategy, sparse vectorizer id, indexed sources, returned citations, and benchmark metrics

#### Scenario: Hybrid evidence remains evaluation-only

- **WHEN** hybrid exact-term evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, and production indexing dependencies remain unchanged

#### Scenario: Hybrid evidence records misses honestly

- **WHEN** dense+sparse retrieval returns citations that differ from exact-term fixture expectations
- **THEN** the evidence records the miss instead of rewriting expected citations

## MODIFIED Requirements

### Requirement: Qdrant exact-term smoke evidence can be exported locally

The system SHALL provide a named local export path for running the exact-term identifier fixture through Qdrant+BGE smoke retrieval without changing runtime defaults.

#### Scenario: Exact-term Qdrant smoke evidence is exported

- **WHEN** the exact-term Qdrant smoke helper is run with source ids and an output directory
- **THEN** it indexes the sources, evaluates the exact-term identifier fixture, and writes JSON and Markdown evidence files with stable exact-term filenames

#### Scenario: Exact-term Qdrant smoke keeps expected citations

- **WHEN** dense-only retrieval returns citations that differ from the exact-term fixture expectations
- **THEN** the evidence records the miss instead of rewriting expected citations

#### Scenario: Dense-only exact-term misses can seed hybrid comparison

- **WHEN** exact-term Qdrant smoke evidence shows dense-only misses
- **THEN** the benchmark harness can export a separate hybrid candidate report without changing dense-only runtime behavior

#### Scenario: Exact-term Qdrant smoke remains evaluation-only

- **WHEN** exact-term Qdrant smoke evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, and hybrid retrieval decisions remain unchanged
