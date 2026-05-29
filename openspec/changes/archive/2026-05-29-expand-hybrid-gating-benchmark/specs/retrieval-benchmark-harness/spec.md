# retrieval-benchmark-harness Delta

## ADDED Requirements

### Requirement: Expanded hybrid gating fixtures are maintained separately

The system SHALL maintain expanded hybrid gating benchmark fixtures that cover both supported and expected-empty identifier-heavy cases without replacing the baseline Chinese seed, exact-term fixture, or first hybrid empty-stress fixture.

#### Scenario: Expanded positive fixture is loaded separately

- **WHEN** expanded hybrid gating positive cases are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying the baseline exact-term fixture

#### Scenario: Expanded empty fixture is loaded separately

- **WHEN** expanded hybrid gating expected-empty cases are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying the first hybrid empty-stress fixture

#### Scenario: Expanded fixtures cover partial identifiers

- **WHEN** expanded hybrid gating expected-empty cases are loaded
- **THEN** at least one case uses a partial identifier that must not be accepted as evidence for a longer known identifier

#### Scenario: Expanded fixtures cover multi-identifier positives

- **WHEN** expanded hybrid gating positive cases are loaded
- **THEN** at least one case requires a single evidence chunk to contain multiple query identifiers

## MODIFIED Requirements

### Requirement: Hybrid gating candidates can be evaluated locally

The system SHALL provide a local export path for evaluating hybrid retrieval gating candidates against both exact-term recall cases and hybrid expected-empty stress cases without changing runtime retrieval behavior.

#### Scenario: Identifier gate protects unsupported exact tokens

- **WHEN** a query contains identifier-like tokens and the retrieved evidence does not contain every query identifier as an exact extracted identifier
- **THEN** the exact identifier containment gate removes that evidence before benchmark metrics are calculated
