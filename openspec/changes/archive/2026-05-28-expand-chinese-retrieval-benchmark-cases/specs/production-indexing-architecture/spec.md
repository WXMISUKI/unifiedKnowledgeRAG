## ADDED Requirements

### Requirement: Embedding decisions use Chinese-heavy seed evidence

The system SHALL require Chinese-heavy benchmark seed evidence before selecting a production embedding provider.

#### Scenario: Embedding candidate is compared

- **WHEN** an embedding candidate is proposed for Chinese-heavy workloads
- **THEN** the proposal references benchmark cases that include enterprise support categories beyond simple exact-match policy lookup

#### Scenario: Seed evidence is not final acceptance

- **WHEN** the local Chinese benchmark seed passes
- **THEN** the result is treated as early comparison evidence and not final production acceptance coverage
