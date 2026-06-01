## ADDED Requirements

### Requirement: Phase 7 release decision record is documentation-only governance evidence

The project SHALL allow a Phase 7 release decision record that captures local-handoff and runtime-promotion verdicts without changing runtime defaults.

#### Scenario: Decision record captures cross-phase verdict

- **WHEN** Phase 7 release decision record is generated
- **THEN** it captures the current-cycle verdict over acceptance contract, release-readiness, and cross-phase consistency smoke evidence

#### Scenario: Decision record preserves promotion boundaries

- **WHEN** the verdict keeps runtime defaults
- **THEN** runtime promotion remains a separate future change gated by additional evidence
