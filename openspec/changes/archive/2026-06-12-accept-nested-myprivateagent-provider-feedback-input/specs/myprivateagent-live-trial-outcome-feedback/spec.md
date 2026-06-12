## ADDED Requirements

### Requirement: Phase 25 feedback accepts nested provider feedback payloads
The system SHALL accept a MyPrivateAgent repo-side trial outcome file that contains the Phase 25-compatible payload under `provider_feedback_input`.

#### Scenario: MyPrivateAgent trial outcome contains provider feedback input
- **WHEN** the configured trial outcome JSON has a `provider_feedback_input` object
- **THEN** Phase 25 feedback consumes that nested object as the caller feedback payload
- **AND** it applies the same classification rules used for the flat input contract

#### Scenario: Flat trial outcome remains supported
- **WHEN** the configured trial outcome JSON uses the original flat Phase 25 input contract
- **THEN** Phase 25 feedback continues to consume the top-level payload without requiring a wrapper

#### Scenario: Nested provider feedback input is incomplete
- **WHEN** `provider_feedback_input` exists but omits required Phase 25 fields
- **THEN** Phase 25 feedback remains conservative
- **AND** it does not classify the provider as `no_provider_action_required`
