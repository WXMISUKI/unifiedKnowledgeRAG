## ADDED Requirements

### Requirement: Phase 3 hybrid promotion evidence SHALL have a final decision record

The system documentation SHALL provide a Phase 3 hybrid runtime promotion decision record that maps current readiness and smoke evidence to a single verdict.

#### Scenario: Hybrid decision record references current evidence bundle

- **WHEN** the hybrid decision record is authored
- **THEN** it references current hybrid runtime promotion readiness, hybrid decision smoke, and linked Phase 3/Phase 6 prerequisite artifacts

#### Scenario: Hybrid decision record does not imply automatic promotion

- **WHEN** evidence includes local candidate wins but open gates remain
- **THEN** the record explicitly keeps runtime defaults and lists required next evidence for future promotion consideration
