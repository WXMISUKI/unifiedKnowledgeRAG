# approved-local-corpus-source-registration Specification

## Purpose
TBD - created by archiving change add-approved-local-corpus-source-registration. Update Purpose after archive.
## Requirements
### Requirement: Approved local corpus source can be registered
The system SHALL register a local markdown corpus as a provider-visible source only after an explicit approved handoff input.

#### Scenario: Ready handoff is registered
- **WHEN** the registration command receives a local corpus handoff with `status=ready_for_caller_review`
- **THEN** it writes an approved local source registry entry
- **AND** it materializes the markdown under the provider source directory
- **AND** it reports `registration_status=registered`

#### Scenario: Non-ready handoff is blocked
- **WHEN** the registration command receives a handoff with `status=review` or `status=blocked`
- **THEN** it reports `registration_status=blocked`
- **AND** it does not write or update the approved local source registry

#### Scenario: Handoff markdown is missing
- **WHEN** the registration command receives a ready handoff whose markdown artifact path does not exist
- **THEN** it reports `registration_status=blocked`
- **AND** it records a missing markdown reason

### Requirement: Approved local corpus registration stays local and reversible
The approved local corpus registration SHALL remain a local provider source registration and SHALL NOT perform caller-owned binding or heavy ingestion work.

#### Scenario: Registration runs
- **WHEN** an approved local source is registered
- **THEN** the provider does not create source-to-agent bindings, create formal ingestion jobs, promote retrieval backends, start OCR services, run MyPrivateAgent orchestration, call vector databases, or execute GraphRAG

#### Scenario: Registry is removed
- **WHEN** the approved local source registry entry is removed
- **THEN** the source is no longer treated as a configured provider source

