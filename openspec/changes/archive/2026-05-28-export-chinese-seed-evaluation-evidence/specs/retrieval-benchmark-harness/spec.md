## ADDED Requirements

### Requirement: Chinese seed evidence can be exported as a local bundle

The system SHALL provide a local service-level helper that exports the current Chinese benchmark seed evidence for architecture review.

#### Scenario: Seed evidence bundle is exported

- **WHEN** the Chinese seed evidence export helper is run with an output directory
- **THEN** it writes retrieval candidate evidence and embedding candidate evidence under stable subdirectories

#### Scenario: Retrieval seed baseline is exported

- **WHEN** the seed evidence bundle exports retrieval evidence
- **THEN** it includes a fixture baseline candidate evaluated against the current Chinese benchmark cases

#### Scenario: Embedding candidate seed evidence is exported

- **WHEN** the seed evidence bundle exports embedding evidence
- **THEN** it includes local metadata reports for the default embedding candidate catalog without invoking hosted or local embedding services

#### Scenario: Seed bundle remains local

- **WHEN** the seed evidence bundle is exported
- **THEN** it writes local JSON and Markdown files without exposing a public HTTP API
