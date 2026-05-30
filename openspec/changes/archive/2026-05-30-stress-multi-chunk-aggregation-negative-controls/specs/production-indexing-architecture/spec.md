## ADDED Requirements

### Requirement: Aggregation promotion requires negative-control evidence

The system SHALL require same-document negative-control evidence before promoting multi-chunk aggregation, parent context, or similar grouping behavior into runtime retrieval.

#### Scenario: Aggregation promotion is proposed

- **WHEN** a future change proposes runtime multi-chunk aggregation or parent context retrieval
- **THEN** it references both split-chunk positive recovery evidence and same-document expected-empty evidence

#### Scenario: Negative controls fail

- **WHEN** local same-document negative controls show over-broad aggregation
- **THEN** runtime aggregation remains unapproved and the architecture records the need for stricter relation evidence, reranking, graph checks, or evidence grading before promotion
