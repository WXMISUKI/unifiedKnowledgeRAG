## ADDED Requirements

### Requirement: Phase 9 MyPrivateAgent local-consumption evidence remains review-only

The project SHALL treat Phase 9 MyPrivateAgent local-consumption readiness and smoke exports as local review evidence without changing runtime defaults.

#### Scenario: Phase 9 readiness summarizes local-consumption posture

- **WHEN** the Phase 9 readiness export is generated
- **THEN** it summarizes local provider URL posture, Phase 7/8 readiness linkage, and caller-boundary ownership notes

#### Scenario: Phase 9 smoke checks local-consumption consistency

- **WHEN** the Phase 9 smoke export is generated
- **THEN** it validates key local-consumption evidence alignment without calling mutating endpoints

#### Scenario: Phase 9 preserves runtime-promotion boundary

- **WHEN** Phase 9 evidence is generated
- **THEN** it does not imply runtime default promotion approval
