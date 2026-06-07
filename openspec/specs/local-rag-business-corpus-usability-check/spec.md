# local-rag-business-corpus-usability-check Specification

## Purpose

Define a lightweight local usability check that summarizes whether a real local business corpus is usable through the existing RAG provider path.

## Requirements

### Requirement: Local RAG business corpus usability check can be exported
The system SHALL export a compact local RAG business corpus usability report that summarizes existing local corpus trial and approved corpus smoke results.

#### Scenario: Local usability passes
- **WHEN** the local business corpus trial passes and the approved local corpus acceptance smoke passes
- **THEN** the report decision is `go`
- **AND** it records source id, check decisions, reason codes, citation validity summary, and recommended next action

#### Scenario: Local usability needs review
- **WHEN** no required check is blocked but at least one required check returns `review`
- **THEN** the report decision is `review`
- **AND** it recommends reviewing corpus content, page range, query set, or retrieval behavior

#### Scenario: Local usability is blocked
- **WHEN** any required check is blocked
- **THEN** the report decision is `blocked`
- **AND** it records the blocking check and machine-readable reason code

### Requirement: Local RAG business corpus usability check may include live HTTP
The local usability check SHALL optionally include live HTTP validation against an already running local provider.

#### Scenario: Live HTTP is requested
- **WHEN** the CLI is run with live HTTP enabled
- **THEN** the report includes the live HTTP smoke result
- **AND** provider unreachable, HTTP contract failure, missing source, manifest failure, or invalid citation blocks the usability result

#### Scenario: Live HTTP is not requested
- **WHEN** the CLI is run without live HTTP
- **THEN** the report excludes live HTTP from required checks
- **AND** it records that live HTTP was not requested

### Requirement: Usability check remains lightweight
The local RAG business corpus usability check SHALL remain a read-only local validation entrypoint.

#### Scenario: Usability check runs
- **WHEN** the usability check runs
- **THEN** it does not start servers, register sources, create source-to-agent bindings, create ingestion jobs, start OCR services, promote retrieval backends, run MyPrivateAgent orchestration, call vector databases, execute GraphRAG, or change default RAG API behavior
