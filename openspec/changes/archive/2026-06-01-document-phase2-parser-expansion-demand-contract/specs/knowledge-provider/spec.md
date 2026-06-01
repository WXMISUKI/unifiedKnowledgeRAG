## ADDED Requirements

### Requirement: Provider can publish a read-only parser expansion demand contract

The system SHALL allow provider-owned publication of parser expansion demand contracts as read-only governance evidence.

#### Scenario: Demand contract is discoverable

- **WHEN** reviewers inspect local ingestion evidence
- **THEN** the parser expansion demand contract clearly states baseline scope, deferred formats, and required evidence classes

#### Scenario: Demand contract does not imply parser runtime change

- **WHEN** the contract is updated
- **THEN** it does not automatically enable new parsers, OCR pipelines, or table extraction runtimes
