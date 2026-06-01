## ADDED Requirements

### Requirement: Phase 3 candidate evaluation protocol defines stable promotion-review gates

The system SHALL maintain a local Phase 3 candidate evaluation protocol that defines stable evidence gate expectations for retrieval candidate promotion review.

#### Scenario: Protocol covers current Phase 3 candidate gate families

- **WHEN** the protocol is reviewed
- **THEN** it includes Qdrant, BGE-M3, hybrid retrieval, hybrid gating, aggregation, relation-aware grading, and deployed-smoke follow-up gate families

#### Scenario: Protocol states required evidence classes

- **WHEN** a gate is defined in the protocol
- **THEN** it lists required evidence classes, including customer-like benchmark coverage, FP/FN review, and latency or deployment diagnostics where relevant

#### Scenario: Protocol remains evaluation-only

- **WHEN** the protocol is added or refreshed
- **THEN** runtime retrieval defaults, public HTTP APIs, and candidate promotion decisions remain unchanged
