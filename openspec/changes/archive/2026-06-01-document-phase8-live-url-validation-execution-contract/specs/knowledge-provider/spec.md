## ADDED Requirements

### Requirement: Knowledge provider live URL validation execution remains caller/deployment-reviewer consumable

The system SHALL keep a documentation-only Phase 8 live URL validation execution contract so callers and deployment reviewers can run and interpret live smoke evidence consistently.

#### Scenario: Contract defines execution inputs and status interpretation

- **WHEN** a reviewer prepares live URL validation
- **THEN** the contract defines required inputs and `ready/review/blocked` interpretation rules

#### Scenario: Contract preserves provider ownership boundary

- **WHEN** live URL validation is complete
- **THEN** caller control-plane ownership, binding policy ownership, and runtime promotion gates remain unchanged
