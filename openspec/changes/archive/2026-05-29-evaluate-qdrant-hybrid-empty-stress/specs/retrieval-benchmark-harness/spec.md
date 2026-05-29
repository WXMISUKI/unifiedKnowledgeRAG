## ADDED Requirements

### Requirement: Hybrid empty-stress cases are maintained separately

The system SHALL maintain dedicated hybrid empty-stress benchmark cases that expose sparse-token false-positive risk without replacing the baseline Chinese retrieval seed or exact-term fixture.

#### Scenario: Hybrid empty-stress fixture is loaded separately

- **WHEN** hybrid empty-stress cases are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying the baseline retrieval benchmark fixture or exact-term fixture

#### Scenario: Hybrid empty-stress cases use unsupported token overlap

- **WHEN** hybrid empty-stress cases are loaded
- **THEN** each case expects empty retrieval while sharing lexical structure with known policy codes, form names, workflow acronyms, or order-like ids

### Requirement: Qdrant hybrid empty-stress evidence can be exported locally

The system SHALL provide a named local export path for evaluating expected-empty stress cases against the evaluation-only Qdrant dense+sparse hybrid candidate.

#### Scenario: Hybrid empty-stress evidence is exported

- **WHEN** the hybrid empty-stress helper is run with source ids and an output directory
- **THEN** it indexes dense and sparse vectors, evaluates the hybrid empty-stress fixture, and writes JSON and Markdown evidence files with stable empty-stress filenames

#### Scenario: Hybrid empty-stress evidence records false positives

- **WHEN** hybrid retrieval returns evidence for an expected-empty case
- **THEN** the evidence records `empty_query_handling=false` and preserves the returned citations

#### Scenario: Hybrid empty-stress evidence remains evaluation-only

- **WHEN** hybrid empty-stress evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, and production indexing dependencies remain unchanged

## MODIFIED Requirements

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

#### Scenario: Hybrid exact-term success requires empty-stress follow-up

- **WHEN** hybrid exact-term evidence improves identifier recall
- **THEN** the benchmark harness can export a separate expected-empty stress report before runtime hybrid promotion is considered
