## ADDED Requirements

### Requirement: Phase 8 live URL validation decision record remains documentation-only

The project SHALL treat the Phase 8 live URL validation decision record as governance documentation that does not change runtime defaults.

#### Scenario: Decision record captures current live-url verdict

- **WHEN** Phase 8 decision record is updated
- **THEN** it records current readiness/smoke posture, explicit verdict, and open gates

#### Scenario: Decision record preserves promotion boundary

- **WHEN** live URL validation remains review-gated
- **THEN** the decision record keeps runtime default promotion as a separate follow-up decision
