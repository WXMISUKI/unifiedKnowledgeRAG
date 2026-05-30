## ADDED Requirements

### Requirement: Multi-chunk aggregation promotion requires split-chunk evidence

The system SHALL require explicit benchmark evidence before promoting split-chunk aggregation, parent context, or similar multi-chunk retrieval behavior into runtime defaults.

#### Scenario: Runtime aggregation is proposed

- **WHEN** a future change proposes runtime multi-chunk aggregation, parent context retrieval, or section-level context expansion
- **THEN** the change references split-chunk aggregation evidence and explains recall improvement, false-positive risk, citation granularity, latency impact, and operational complexity

#### Scenario: Local aggregation evidence is insufficient for production approval

- **WHEN** local split-chunk aggregation evidence passes on seed fixtures
- **THEN** the evidence remains a review input and does not automatically approve runtime hybrid retrieval, runtime aggregation, reranker use, or production parent-document storage
