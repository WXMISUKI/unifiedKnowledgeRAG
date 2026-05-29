# retrieval-benchmark-harness Delta

## ADDED Requirements

### Requirement: Identifier alias governance can be evaluated locally

The system SHALL provide local evidence for identifier alias governance without creating a production alias service.

#### Scenario: Alias governance evidence is exported

- **WHEN** the alias governance export helper is run with a local catalog
- **THEN** it writes JSON and Markdown evidence with alias ids, canonical identifiers, owners, versions, statuses, risk levels, and decision notes

#### Scenario: Alias catalog is auditable

- **WHEN** aliases are used for noisy identifier candidate evaluation
- **THEN** each alias pattern is represented in the local catalog with owner and status metadata

#### Scenario: Alias governance remains evaluation-only

- **WHEN** alias governance evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, and production alias dictionaries remain unchanged

### Requirement: Split-chunk identifier cases are maintained separately

The system SHALL maintain split-chunk identifier benchmark cases that expose false-negative risk when related identifiers are not co-located in the same evidence chunk.

#### Scenario: Split-chunk source is indexed separately

- **WHEN** split-chunk benchmark evidence is exported
- **THEN** the system indexes a dedicated fixture source rather than modifying the baseline refund or logistics sources

#### Scenario: Split-chunk miss is recorded honestly

- **WHEN** strict identifier gating removes all retrieved chunks because no single chunk contains every query identifier
- **THEN** the evidence records the miss instead of rewriting expected citations

#### Scenario: Split-chunk benchmark remains evaluation-only

- **WHEN** split-chunk evidence is exported
- **THEN** runtime chunking defaults, public HTTP APIs, and production retrieval behavior remain unchanged

## MODIFIED Requirements

### Requirement: Noisy identifier gate candidates can be evaluated locally

The system SHALL provide a local export path for evaluating noisy or alias-aware identifier gating candidates without changing runtime retrieval behavior.

#### Scenario: Noisy gate remains evaluation-only

- **WHEN** noisy identifier gate evidence or alias governance evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, production alias dictionaries, and production indexing dependencies remain unchanged
