## ADDED Requirements

### Requirement: Phase 7 cross-phase consistency smoke remains read-only

The project SHALL treat Phase 7 cross-phase handoff consistency smoke as lightweight evidence consistency visibility work.

#### Scenario: Smoke validates cross-phase decision alignment

- **WHEN** the smoke report runs
- **THEN** it validates that Phase 2, Phase 3, Phase 4, Phase 5, and Phase 6 gate artifacts remain aligned with Phase 7 release-readiness posture

#### Scenario: Smoke preserves promotion boundary

- **WHEN** the smoke report is ready
- **THEN** it does not imply runtime default promotion and remains review evidence only
