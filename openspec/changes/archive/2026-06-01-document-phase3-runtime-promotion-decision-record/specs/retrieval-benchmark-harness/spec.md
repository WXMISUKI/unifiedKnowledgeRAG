## ADDED Requirements

### Requirement: Phase 3 promotion evidence SHALL have a final decision record

The system documentation SHALL provide a Phase 3 decision record that maps current benchmark evidence and diagnostics to a single promotion verdict.

#### Scenario: Decision record references current evidence bundle

- **WHEN** the decision record is authored
- **THEN** it references current promotion readiness, diagnostics, and smoke artifacts used for the verdict

#### Scenario: Decision record does not imply automatic promotion

- **WHEN** evidence includes local candidate wins but open gates remain
- **THEN** the record explicitly keeps runtime defaults and lists required next evidence for future promotion consideration
