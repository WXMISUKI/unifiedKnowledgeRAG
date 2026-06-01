## ADDED Requirements

### Requirement: Phase 3 aggregation and relation-aware negative-control smoke can be exported locally

The system SHALL export a local Phase 3 aggregation/relation negative-control smoke report that combines multi-chunk aggregation evidence with relation-aware grading evidence.

#### Scenario: Smoke export is local

- **WHEN** the Phase 3 aggregation/relation negative-control smoke export is run
- **THEN** the system writes JSON and Markdown evidence files under `docs/smoke/aggregation-relation-negative-control/`

#### Scenario: Smoke covers positive and negative controls

- **WHEN** the smoke report is generated
- **THEN** it validates the positive split-chunk control, the same-document negative control, and the relation-aware grading label for the unsupported relationship case

#### Scenario: Smoke remains evaluation-only

- **WHEN** the aggregation/relation negative-control smoke is exported
- **THEN** runtime retrieval defaults and graph execution behavior remain unchanged
