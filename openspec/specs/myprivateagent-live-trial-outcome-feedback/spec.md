# myprivateagent-live-trial-outcome-feedback Specification

## Purpose
TBD - created by archiving change phase25-myprivateagent-live-trial-outcome-feedback. Update Purpose after archive.
## Requirements
### Requirement: Provider exports MyPrivateAgent live trial outcome feedback
The system SHALL export a read-only Phase 25 feedback report from an explicit MyPrivateAgent live trial outcome JSON file.

#### Scenario: Caller trial outcome is go
- **WHEN** the input outcome has `live_trial_status=go` and provider retrieve status is `ready`
- **THEN** the Phase 25 report has `status=ready`, `provider_action=no_provider_action_required`, and records compact provider retrieve evidence facts

#### Scenario: Caller trial outcome needs review
- **WHEN** the input outcome has `live_trial_status=review` or indicates insufficient evidence without provider retrieve failure
- **THEN** the Phase 25 report has `status=review`, `provider_action=provider_review_required`, and records the review reason

#### Scenario: Caller trial outcome is blocked by provider retrieval
- **WHEN** the input outcome has `live_trial_status=blocked` and provider retrieve evidence indicates a blocked, failed, or error state
- **THEN** the Phase 25 report has `status=blocked`, `provider_action=provider_blocked`, and recommends opening a focused provider fix

#### Scenario: Input outcome is missing or invalid
- **WHEN** the configured trial outcome path is missing, unreadable, or does not contain a valid JSON object
- **THEN** the Phase 25 report has `status=blocked`, `provider_action=provider_blocked`, and identifies `invalid_trial_outcome_input`

### Requirement: Trial outcome feedback remains provider-side and read-only
The Phase 25 feedback report SHALL preserve provider/caller ownership boundaries and SHALL NOT mutate runtime behavior.

#### Scenario: Feedback report is exported
- **WHEN** the Phase 25 export command runs
- **THEN** it writes machine-readable JSON and Markdown feedback files without running MyPrivateAgent, calling provider HTTP endpoints, creating source bindings, rebuilding indexes, changing retrieval defaults, or executing GraphRAG

#### Scenario: Provider follow-up ownership remains explicit
- **WHEN** a reviewer reads the Phase 25 report
- **THEN** it states whether the provider has no action, needs review, or is blocked, while keeping final answer policy, source-to-agent binding, audit policy, and trial execution owned by MyPrivateAgent

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

