## ADDED Requirements

### Requirement: Provider can publish a read-only deployed handoff consistency smoke

The system SHALL allow provider-owned publication of deployed handoff consistency smoke evidence as read-only review evidence.

#### Scenario: Consistency smoke is discoverable

- **WHEN** reviewers inspect local operations evidence
- **THEN** the deployed handoff consistency smoke clearly states the readiness posture, bundle posture, and alignment status

#### Scenario: Consistency smoke does not imply runtime change

- **WHEN** the smoke is updated
- **THEN** it does not automatically switch retrieval, embedding, or deployment defaults
