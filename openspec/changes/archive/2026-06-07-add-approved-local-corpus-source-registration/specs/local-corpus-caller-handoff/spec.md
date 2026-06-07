## ADDED Requirements

### Requirement: Ready local corpus handoff can feed explicit source registration
The system SHALL allow a `ready_for_caller_review` local corpus handoff to be used as input for a separate approved local source registration step.

#### Scenario: Ready handoff feeds registration
- **WHEN** a local corpus handoff has `status=ready_for_caller_review`
- **THEN** an approved local source registration command can use its source id, title, markdown artifact, and trial artifact pointers as registration input

#### Scenario: Review or blocked handoff does not feed registration
- **WHEN** a local corpus handoff has `status=review` or `status=blocked`
- **THEN** approved local source registration is blocked before any provider source registry is written
