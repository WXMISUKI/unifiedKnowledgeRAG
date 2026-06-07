# parser-artifact-local-ingestion-loop Specification

## Purpose
TBD - created by archiving change add-parser-artifact-local-ingestion-loop. Update Purpose after archive.
## Requirements
### Requirement: Parser artifact local ingestion loop can be exported
The system SHALL export a local parser-artifact ingestion loop report that verifies a normalized external parser artifact can become provider-managed RAG material through the existing local markdown ingestion path.

#### Scenario: Parser artifact ingestion loop passes
- **WHEN** the parser artifact boundary returns `decision=go`
- **AND** it provides a materialized markdown path, source id, and title
- **AND** the approved-source ingestion loop returns `decision=go`
- **THEN** the parser artifact local ingestion loop report has `decision=go`
- **AND** it records artifact id, source id, parser id, materialized markdown path, source overlay path, ingestion step statuses, artifact paths, and recommended next action

#### Scenario: Parser artifact ingestion loop needs review
- **WHEN** the parser artifact boundary returns `decision=review`
- **THEN** the parser artifact local ingestion loop report has `decision=review`
- **AND** it does not run onboarding or ingestion
- **AND** it records the artifact review reason and recommended artifact fixes

#### Scenario: Parser artifact ingestion loop is blocked
- **WHEN** the parser artifact boundary returns `decision=blocked`
- **OR** the approved-source ingestion loop returns `decision=blocked`
- **THEN** the parser artifact local ingestion loop report has `decision=blocked`
- **AND** it records the blocking step and machine-readable reason code

### Requirement: Parser artifact local ingestion loop remains lightweight
The parser artifact local ingestion loop SHALL orchestrate existing local provider steps without taking ownership of parsing engines or runtime promotion decisions.

#### Scenario: Loop runs
- **WHEN** the parser artifact local ingestion loop command runs
- **THEN** it does not parse raw PDFs
- **AND** it does not start OCR services
- **AND** it does not call PaddleOCR or other parser engines
- **AND** it does not call MyPrivateAgent
- **AND** it does not create source-to-agent bindings
- **AND** it does not mutate `/api/chat`
- **AND** it does not promote retrieval backend defaults
- **AND** it does not call vector databases outside the existing explicit ingestion loop
- **AND** it does not execute GraphRAG

### Requirement: Parser artifact local ingestion loop exposes refreshable artifacts
The system SHALL provide a CLI exporter for refreshing the parser artifact local ingestion loop report.

#### Scenario: CLI writes artifacts
- **WHEN** the user runs the parser artifact local ingestion loop export command
- **THEN** JSON and Markdown reports are written under `docs/local-run/parser-artifact-local-ingestion-loop/`
- **AND** the command exits non-zero only when the report decision is `blocked`

