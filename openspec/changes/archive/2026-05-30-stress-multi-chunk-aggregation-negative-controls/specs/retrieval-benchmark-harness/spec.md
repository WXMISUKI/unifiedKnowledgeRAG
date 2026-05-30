## ADDED Requirements

### Requirement: Multi-chunk aggregation negative controls are maintained separately

The system SHALL maintain expected-empty negative-control benchmark cases for multi-chunk aggregation without replacing split-chunk positive fixtures.

#### Scenario: Same-document negative controls are loaded separately

- **WHEN** multi-chunk aggregation negative controls are evaluated
- **THEN** the cases are loaded from a dedicated fixture rather than modifying split-chunk positive cases

#### Scenario: Unsupported same-document relationship is expected empty

- **WHEN** a negative-control query asks for an unsupported relationship between identifiers that can appear in the same source document
- **THEN** the benchmark case marks `expect_empty=true` and has no expected citation

### Requirement: Multi-chunk aggregation evidence reports negative-control behavior

The system SHALL include expected-empty negative controls in multi-chunk aggregation evidence so reviewers can see both split-chunk recovery and over-broad grouping risk.

#### Scenario: Aggregation report includes positive and negative cases

- **WHEN** multi-chunk aggregation evidence is exported with positive and negative-control fixtures
- **THEN** the report summary includes hit rate, citation match rate, and empty handling rate across both fixture groups

#### Scenario: Over-broad aggregation is recorded honestly

- **WHEN** multi-chunk aggregation returns evidence for an expected-empty same-document negative control
- **THEN** the report records empty handling failure instead of hiding or rewriting the returned citations

#### Scenario: Negative-control evidence remains evaluation-only

- **WHEN** negative-control evidence is exported
- **THEN** runtime retrieval defaults, public HTTP APIs, production parent-document stores, production rerankers, graph stores, and answer generation behavior remain unchanged
