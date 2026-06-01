## ADDED Requirements

### Requirement: Phase 2 unsupported-format negative-control smoke remains read-only

The project SHALL treat Phase 2 unsupported-format negative-control smoke as lightweight evidence visibility work when it validates parser-expansion boundary controls from local readiness evidence.

#### Scenario: Smoke checks unsupported-format boundaries

- **WHEN** the smoke report runs with Phase 2 readiness input
- **THEN** it validates markdown positive control and unsupported/non-markdown negative controls without enabling parser expansion

#### Scenario: Smoke preserves runtime boundary

- **WHEN** smoke checks fail
- **THEN** the result remains review/blocked evidence and does not change runtime defaults
