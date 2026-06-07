# local-approved-source-ingestion-loop Specification

## ADDED Requirements

### Requirement: Local approved source ingestion loop can be exported

The system SHALL export a local approved-source ingestion report that verifies a provider-visible local markdown source can be preflighted, ingested, indexed, and retrieval-smoked.

#### Scenario: Approved source ingestion loop passes
- **WHEN** the local document source onboarding step returns `decision=go`
- **AND** ingestion preflight for the source returns `status=ready`
- **AND** explicit ingestion job creation returns a completed job
- **AND** source index status returns `ready`
- **AND** approved local corpus acceptance smoke returns `decision=go`
- **THEN** the ingestion loop report has `decision=go`
- **AND** it records source id, markdown path, query, step statuses, ingestion job id, index status, artifact paths, and recommended next action

#### Scenario: Approved source ingestion loop needs review
- **WHEN** no step is blocked
- **AND** at least one non-terminal step returns `review`
- **THEN** the ingestion loop report has `decision=review`
- **AND** it records the review step and machine-readable reason code

#### Scenario: Approved source ingestion loop is blocked
- **WHEN** onboarding blocks, preflight is not ready, ingestion job creation fails, ingestion job fails, index status is not ready, or acceptance smoke blocks
- **THEN** the ingestion loop report has `decision=blocked`
- **AND** it records the blocking step and machine-readable reason code

### Requirement: Local approved source ingestion loop remains lightweight

The ingestion loop SHALL orchestrate existing local provider steps without promoting heavier runtime behavior.

#### Scenario: Loop runs
- **WHEN** the ingestion loop command runs
- **THEN** it does not parse raw PDFs as supported provider ingestion
- **AND** it does not start OCR services
- **AND** it does not call MyPrivateAgent
- **AND** it does not create source-to-agent binding
- **AND** it does not mutate `/api/chat`
- **AND** it does not promote retrieval backend defaults
- **AND** it does not execute GraphRAG

#### Scenario: Ingestion remains explicit
- **WHEN** the loop reaches ingestion
- **THEN** it creates only an explicit local ingestion job for the selected source
- **AND** production queue workers, distributed schedulers, and automatic background indexing remain out of scope

### Requirement: Local approved source ingestion loop exposes refreshable artifacts

The system SHALL provide a CLI exporter for refreshing the approved-source ingestion loop report.

#### Scenario: CLI writes artifacts
- **WHEN** the user runs the export command
- **THEN** JSON and Markdown reports are written under `docs/local-run/approved-source-ingestion-loop/`
- **AND** the command exits non-zero only when the report decision is `blocked`

