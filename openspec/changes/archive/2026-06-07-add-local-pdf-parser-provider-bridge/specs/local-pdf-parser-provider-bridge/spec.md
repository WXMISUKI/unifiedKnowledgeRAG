# local-pdf-parser-provider-bridge Specification

## Purpose

Provide a lightweight local bridge from an operator-started PDF parser/OCR provider into the existing normalized parser artifact and local RAG ingestion loop.

## ADDED Requirements

### Requirement: Local PDF bridge can call an external parser provider
The system SHALL provide a local PDF parser provider bridge that accepts a PDF path, source identity, title, provider URL, and bounded page range for a local trial.

#### Scenario: Provider returns parseable text
- **WHEN** the bridge is run with an existing PDF path and a reachable PaddleOCR-compatible provider
- **AND** the provider response contains non-empty text content
- **THEN** the bridge report has `decision=go`
- **AND** it writes a normalized parser artifact JSON file
- **AND** the artifact includes artifact id, source id, title, original file metadata, parser metadata, text blocks, and citation anchors

#### Scenario: Provider is unreachable
- **WHEN** the bridge cannot reach the configured parser provider
- **THEN** the bridge report has `decision=blocked`
- **AND** it records `reason_code=parser_provider_unreachable`
- **AND** it does not run downstream ingestion

#### Scenario: Provider returns no usable text
- **WHEN** the provider response is reachable but no non-empty text can be normalized
- **THEN** the bridge report has `decision=blocked`
- **AND** it records `reason_code=parser_provider_returned_no_text`
- **AND** it recommends reviewing the OCR/provider output before retrying

### Requirement: Local PDF bridge feeds existing parser artifact ingestion loop
The system SHALL orchestrate successful parser artifact generation into the existing parser artifact local ingestion loop.

#### Scenario: Generated artifact ingests successfully
- **WHEN** the bridge writes a normalized parser artifact
- **AND** the parser artifact local ingestion loop returns `decision=go`
- **THEN** the bridge report has `decision=go`
- **AND** it records parser artifact path, materialized markdown path, source id, downstream decision, and local run report paths

#### Scenario: Downstream ingestion needs review
- **WHEN** the parser artifact local ingestion loop returns `decision=review`
- **THEN** the bridge report has `decision=review`
- **AND** it records the downstream reason code and artifact paths

#### Scenario: Downstream ingestion is blocked
- **WHEN** the parser artifact local ingestion loop returns `decision=blocked`
- **THEN** the bridge report has `decision=blocked`
- **AND** it records the downstream blocking reason code

### Requirement: Local PDF bridge remains lightweight
The bridge SHALL keep parsing provider execution external and avoid taking ownership of calling-project or runtime promotion concerns.

#### Scenario: Bridge runs
- **WHEN** the local PDF bridge command runs
- **THEN** it does not start PaddleOCR or OCR services
- **AND** it does not call MyPrivateAgent
- **AND** it does not create source-to-agent bindings
- **AND** it does not mutate `/api/chat`
- **AND** it does not promote retrieval backend defaults
- **AND** it does not introduce background workers
- **AND** it does not execute GraphRAG

### Requirement: Local PDF bridge exposes refreshable trial artifacts
The system SHALL provide a CLI exporter for refreshing local PDF parser provider bridge reports.

#### Scenario: CLI writes artifacts
- **WHEN** the user runs the local PDF parser provider bridge exporter
- **THEN** JSON and Markdown reports are written under `docs/local-run/local-pdf-parser-provider-bridge/`
- **AND** the command exits non-zero only when the final report decision is `blocked`
