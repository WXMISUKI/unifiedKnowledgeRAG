# retrieval-benchmark-harness Delta

## ADDED Requirements

### Requirement: Hybrid gating candidates can be evaluated locally

The system SHALL provide a local export path for evaluating hybrid retrieval gating candidates against both exact-term recall cases and hybrid expected-empty stress cases without changing runtime retrieval behavior.

#### Scenario: Hybrid gating evidence is exported

- **WHEN** the hybrid gating helper is run with exact-term cases, empty-stress cases, source ids, and an output directory
- **THEN** it indexes dense and sparse vectors, runs hybrid retrieval, applies the gating candidate, and writes JSON and Markdown evidence files

#### Scenario: Raw and gated citations are retained

- **WHEN** a hybrid gating candidate filters retrieved evidence
- **THEN** the evidence records both raw hybrid returned citations and gated returned citations per case

#### Scenario: Identifier gate protects unsupported exact tokens

- **WHEN** a query contains identifier-like tokens and the retrieved evidence does not contain every query identifier
- **THEN** the exact identifier containment gate removes that evidence before benchmark metrics are calculated

#### Scenario: Hybrid gating remains evaluation-only

- **WHEN** hybrid gating evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, production sparse-vector dependencies, and answer generation behavior remain unchanged

## MODIFIED Requirements

### Requirement: Qdrant hybrid empty-stress evidence can be exported locally

The system SHALL provide a named local export path for evaluating expected-empty stress cases against the evaluation-only Qdrant dense+sparse hybrid candidate.

#### Scenario: Hybrid empty-stress evidence records false positives

- **WHEN** hybrid retrieval returns evidence for an expected-empty case
- **THEN** the evidence records `empty_query_handling=false`, preserves the returned citations, and can be used as input for later hybrid gating candidate evaluation
