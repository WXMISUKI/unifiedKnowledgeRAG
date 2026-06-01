## ADDED Requirements

### Requirement: Knowledge provider handoff acceptance remains caller/deployment-reviewer consumable

The system SHALL keep a documentation-only Phase 7 handoff acceptance contract so callers and deployment reviewers can consume provider evidence consistently.

#### Scenario: Acceptance contract defines required handoff evidence

- **WHEN** a caller or deployment reviewer uses provider handoff evidence
- **THEN** the contract enumerates required evidence artifacts and acceptance preconditions for local handoff

#### Scenario: Acceptance contract defines optional review evidence

- **WHEN** optional Phase 2-6 readiness/smoke artifacts are present or missing
- **THEN** the contract explains review semantics without implying runtime default promotion
