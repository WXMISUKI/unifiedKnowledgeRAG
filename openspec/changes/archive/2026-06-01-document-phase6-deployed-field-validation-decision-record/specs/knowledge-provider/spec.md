## ADDED Requirements

### Requirement: Provider can publish a read-only deployed field-validation decision record

The system SHALL allow provider-owned publication of deployed field-validation decision records as read-only governance evidence.

#### Scenario: Decision record is discoverable

- **WHEN** reviewers inspect local operations evidence
- **THEN** the deployed field-validation decision record clearly states the current verdict, review state, and open gates

#### Scenario: Decision record does not imply runtime change

- **WHEN** the decision record is updated
- **THEN** it does not automatically switch retrieval, embedding, or deployment defaults
