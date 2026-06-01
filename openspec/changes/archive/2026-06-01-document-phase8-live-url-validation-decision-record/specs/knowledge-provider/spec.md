## ADDED Requirements

### Requirement: Knowledge-provider docs keep a traceable Phase 8 live-url decision checkpoint

The system SHALL keep a Phase 8 decision record that explains live-url validation posture and next-step gates for reviewers.

#### Scenario: Reviewers can read one stable Phase 8 verdict

- **WHEN** reviewers inspect Phase 8 artifacts
- **THEN** they can reference one decision record for verdict, evidence basis, and required follow-up gates

#### Scenario: Decision record does not imply runtime switch

- **WHEN** decision record indicates review posture
- **THEN** runtime defaults remain unchanged unless a separate promotion change is approved
