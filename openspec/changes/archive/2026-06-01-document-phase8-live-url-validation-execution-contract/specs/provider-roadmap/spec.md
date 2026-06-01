## ADDED Requirements

### Requirement: Phase 8 live URL validation execution contract remains read-only and promotion-safe

The project SHALL allow a Phase 8 live URL validation execution contract that defines operational execution boundaries without changing runtime defaults.

#### Scenario: Contract constrains live validation endpoint scope

- **WHEN** live URL validation is executed
- **THEN** the contract limits checks to read-only provider discovery and handoff endpoints

#### Scenario: Contract separates validation from promotion

- **WHEN** live URL validation evidence is ready
- **THEN** runtime default promotion remains separately gated and is not implied by this contract alone
