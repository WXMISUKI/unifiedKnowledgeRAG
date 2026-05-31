## ADDED Requirements

### Requirement: Phase 3 retrieval promotion gap matrix summarizes current gate evidence

The system SHALL maintain a local read-only retrieval promotion gap matrix that summarizes current Qdrant, BGE-M3, hybrid, aggregation, and relation-aware grading evidence.

#### Scenario: Gap matrix includes key gate families

- **WHEN** the gap matrix is published
- **THEN** it includes rows for Qdrant, BGE-M3, hybrid retrieval, hybrid gating, multi-chunk aggregation, and relation-aware grading

#### Scenario: Gap matrix references current evidence paths

- **WHEN** the gap matrix is reviewed
- **THEN** it points to the current local benchmark and review artifacts that support each row

#### Scenario: Gap matrix remains evaluation-only

- **WHEN** the gap matrix is updated
- **THEN** it does not change runtime retrieval defaults, provider HTTP contracts, or promotion gates
