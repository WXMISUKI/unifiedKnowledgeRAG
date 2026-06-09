## ADDED Requirements

### Requirement: Phase 25 feedback defines the minimal caller input contract
The system SHALL document the minimal caller-side live trial outcome input contract required by the Phase 25 feedback report.

#### Scenario: Required fields are explicit
- **WHEN** a caller wants to export a live trial outcome for provider consumption
- **THEN** the project documents the minimum required fields and the expected nested provider retrieve fields

#### Scenario: Example payload is available
- **WHEN** a caller or reviewer needs to understand the contract quickly
- **THEN** the project provides a reusable example JSON payload for the Phase 25 input shape

### Requirement: Phase 25 feedback handles missing critical fields conservatively
The system SHALL fail closed when the trial outcome file exists but omits critical fields needed for provider follow-up classification.

#### Scenario: Missing trial status is treated conservatively
- **WHEN** the input file is readable but omits `live_trial_status`
- **THEN** the Phase 25 report does not classify the provider as `no_provider_action_required`
- **AND** it records the missing field as warning or blocker evidence

#### Scenario: Missing provider retrieve status is treated conservatively
- **WHEN** the input file is readable but omits `provider_retrieve.status`
- **THEN** the Phase 25 report remains `review` or `blocked`
- **AND** it records that the caller input was incomplete for provider follow-up classification
