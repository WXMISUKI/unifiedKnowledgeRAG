## ADDED Requirements

### Requirement: Provider can publish a read-only private-network promotion decision record

The system SHALL allow provider-owned publication of private-network promotion decision records as read-only governance evidence.

#### Scenario: Decision record is discoverable

- **WHEN** reviewers inspect local operations evidence
- **THEN** the private-network decision record clearly states current verdict, review state, and open gates

#### Scenario: Decision record does not imply runtime change

- **WHEN** the decision record is updated
- **THEN** it does not automatically switch retrieval or embedding runtime defaults
