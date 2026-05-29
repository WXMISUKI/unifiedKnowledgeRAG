# retrieval-benchmark-harness Delta

## ADDED Requirements

### Requirement: Noisy identifier gate candidates can be evaluated locally

The system SHALL provide a local export path for evaluating noisy or alias-aware identifier gating candidates without changing runtime retrieval behavior.

#### Scenario: Noisy identifier gate evidence is exported

- **WHEN** the noisy identifier gate helper is run with supported and expected-empty noisy identifier cases
- **THEN** it runs hybrid retrieval, applies the alias-aware gating candidate, and writes JSON and Markdown evidence files

#### Scenario: Canonical identifiers are retained

- **WHEN** an alias-aware gate normalizes query identifiers
- **THEN** the evidence records the resulting query identifiers, raw hybrid citations, and gated citations per case

#### Scenario: Noisy gate remains evaluation-only

- **WHEN** noisy identifier gate evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, production alias dictionaries, and production indexing dependencies remain unchanged

### Requirement: Noisy identifier fixtures are maintained separately

The system SHALL maintain noisy and alias-heavy identifier benchmark fixtures without replacing the baseline Chinese seed or clean identifier fixtures.

#### Scenario: Noisy positive fixture is loaded separately

- **WHEN** noisy identifier positive cases are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying clean identifier fixtures

#### Scenario: Noisy empty fixture is loaded separately

- **WHEN** noisy identifier expected-empty cases are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying clean empty-stress fixtures

#### Scenario: Noisy fixtures cover OCR and shorthand

- **WHEN** noisy identifier fixtures are loaded
- **THEN** they include cases with OCR-like digit confusion and local shorthand aliases

## MODIFIED Requirements

### Requirement: Hybrid gating candidates can be evaluated locally

The system SHALL provide a local export path for evaluating hybrid retrieval gating candidates against both exact-term recall cases and hybrid expected-empty stress cases without changing runtime retrieval behavior.

#### Scenario: Hybrid gating remains evaluation-only

- **WHEN** hybrid or noisy identifier gating evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, production sparse-vector dependencies, production alias dictionaries, and answer generation behavior remain unchanged
