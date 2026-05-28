## ADDED Requirements

### Requirement: Embedding candidates can be evaluated consistently

The system SHALL provide a local service-level evaluation shape for embedding candidates without invoking real embedding providers.

#### Scenario: Embedding candidate catalog is loaded

- **WHEN** embedding candidates are requested
- **THEN** the catalog includes the mock baseline and explicit hosted/local Chinese-heavy candidate placeholders

#### Scenario: Embedding candidate ids are validated

- **WHEN** embedding candidate evaluation is requested
- **THEN** duplicate or filesystem-unsafe candidate ids are rejected before exporting evidence

#### Scenario: Embedding candidate evidence is exported

- **WHEN** embedding candidate evaluation is run with an output directory
- **THEN** each candidate writes `<candidate-id>.json` and `<candidate-id>.md` files containing candidate metadata and readiness notes

#### Scenario: Evaluation remains local

- **WHEN** embedding candidate evaluation exports evidence
- **THEN** it writes local files without exposing a new public HTTP API or calling hosted/local embedding services
