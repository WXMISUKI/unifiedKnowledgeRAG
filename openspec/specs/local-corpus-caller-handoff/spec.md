# local-corpus-caller-handoff Specification

## Purpose
Provide a lightweight, local-only caller review package for a successful local business corpus trial before any formal source registration or binding is approved.

## Requirements
### Requirement: Provider exports a local corpus caller handoff
The system SHALL export a local-only caller handoff package from a local business corpus trial report.

#### Scenario: Trial is go
- **WHEN** the input local business corpus trial report has `decision=go`
- **THEN** the caller handoff has `status=ready_for_caller_review`
- **AND** it includes the source id, title, markdown artifact, overlay artifact, chunks artifact, trial report path, recommended query, citation policy, and next action

#### Scenario: Trial needs review
- **WHEN** the input local business corpus trial report has `decision=review`
- **THEN** the caller handoff has `status=review`
- **AND** it recommends reviewing the trial query, markdown quality, or evidence before caller integration

#### Scenario: Trial is blocked
- **WHEN** the input local business corpus trial report has `decision=blocked`
- **THEN** the caller handoff has `status=blocked`
- **AND** it recommends fixing the blocked trial before caller review

#### Scenario: Trial report is missing
- **WHEN** the configured trial report path does not exist
- **THEN** the caller handoff has `status=blocked`
- **AND** it records that the local business corpus trial must be exported first

### Requirement: Caller handoff remains non-registration evidence
The local corpus caller handoff SHALL NOT register the source or mutate provider runtime behavior.

#### Scenario: Caller handoff is exported
- **WHEN** the caller handoff command runs
- **THEN** it does not modify the default source catalog, expose a provider HTTP source, create source bindings, run ingestion jobs, persist index lifecycle state, promote retrieval backends, run MyPrivateAgent, execute GraphRAG, or start OCR services

#### Scenario: Caller reads handoff
- **WHEN** a caller reads the handoff package
- **THEN** the handoff explicitly reports `registration_status=not_registered` and `caller_next_action=review_trial_artifacts_before_formal_binding`
