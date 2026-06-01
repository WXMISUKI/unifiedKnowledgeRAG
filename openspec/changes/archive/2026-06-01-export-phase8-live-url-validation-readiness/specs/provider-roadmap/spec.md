## ADDED Requirements

### Requirement: Phase 8 live URL validation readiness export remains evidence-only

The project SHALL treat Phase 8 live URL validation readiness export as local deployment-review evidence without changing runtime defaults.

#### Scenario: Export summarizes live URL validation posture

- **WHEN** the Phase 8 readiness export is generated
- **THEN** it summarizes contract, Phase 6/7 posture, deployed smoke status, live URL presence, and open gates

#### Scenario: Export preserves runtime-promotion boundary

- **WHEN** live URL validation evidence is generated
- **THEN** it does not imply runtime default promotion approval
