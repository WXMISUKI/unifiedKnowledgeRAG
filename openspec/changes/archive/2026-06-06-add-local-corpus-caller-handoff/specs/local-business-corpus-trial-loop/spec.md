## ADDED Requirements

### Requirement: Go business corpus trial can feed caller handoff
The system SHALL allow a successful local business corpus trial report to be used as input for a separate caller-facing handoff export.

#### Scenario: Business corpus trial is go
- **WHEN** a local business corpus trial report has `decision=go`
- **THEN** a caller handoff export can reference its markdown, overlay, chunks, evidence, and citation policy
- **AND** this does not change the trial source registration status

#### Scenario: Business corpus trial is not go
- **WHEN** a local business corpus trial report has `decision=review` or `decision=blocked`
- **THEN** a caller handoff export can preserve that status without promoting the source
