# local-usable-run-loop Specification

## Purpose
TBD - created by archiving change add-local-usable-run-loop. Update Purpose after archive.
## Requirements
### Requirement: Provider exports a local usable run-loop report
The system SHALL export a local-only run-loop report for an already-running provider service.

#### Scenario: Local provider is usable
- **WHEN** `/live`, `/ready`, `/health`, `/api/provider/manifest`, `/api/provider/preflight`, `/api/rag/retrieve`, and `/api/rag/answer` return usable local responses
- **THEN** the report has `decision=go`
- **AND** it records answerable retrieval evidence, allowed citations, and an answered response

#### Scenario: Local provider is unreachable
- **WHEN** any required HTTP check cannot connect to the configured local base URL
- **THEN** the report has `decision=blocked`
- **AND** it recommends starting the local `uvicorn` service

#### Scenario: Retrieval returns insufficient evidence
- **WHEN** provider discovery is usable but RAG retrieve returns no answerable evidence
- **THEN** the report has `decision=review`
- **AND** it records that the fixture query, source id, or local corpus should be reviewed

#### Scenario: Answer citations are outside retrieval allowlist
- **WHEN** the answer response cites values outside the retrieve evidence allowlist
- **THEN** the report has `decision=blocked`
- **AND** it records a citation contract failure

### Requirement: Local run-loop remains lightweight
The local usable run-loop SHALL validate local usability without mutating provider runtime behavior.

#### Scenario: Run-loop report is exported
- **WHEN** the export command runs
- **THEN** it writes JSON and Markdown artifacts without starting the service, downloading models, starting Docker/Qdrant/pgvector, rebuilding indexes, creating source bindings, promoting retrieval defaults, or executing GraphRAG

### Requirement: Local usability can include approved corpus acceptance context
The local usability workflow SHALL allow a registered local corpus acceptance smoke to provide corpus-specific readiness context without replacing the generic provider run-loop.

#### Scenario: Approved corpus acceptance is available
- **WHEN** the approved local corpus acceptance smoke has been exported
- **THEN** local usability review can use its `go`, `review`, or `blocked` decision as corpus-specific evidence

#### Scenario: Generic run-loop remains separate
- **WHEN** the approved corpus acceptance smoke is added
- **THEN** the generic local usable run-loop continues to validate provider discovery, preflight, retrieve, and answer over its configured source and query

