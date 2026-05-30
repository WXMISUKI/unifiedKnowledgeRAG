## ADDED Requirements

### Requirement: Runtime aggregation promotion requires relation-aware grading evidence

The system SHALL require relation-aware evidence before promoting multi-chunk aggregation, parent context retrieval, or similar grouping behavior into runtime defaults.

#### Scenario: Runtime aggregation promotion is proposed

- **WHEN** a future change proposes runtime aggregation or parent context retrieval
- **THEN** it references relation-aware grading evidence in addition to split-chunk recovery and negative-control evidence

#### Scenario: Relation grading is local only

- **WHEN** local relation-aware grading evidence exists
- **THEN** the evidence remains a review input and does not automatically approve runtime reranking, graph relation checks, LLM grading, or answer generation changes
