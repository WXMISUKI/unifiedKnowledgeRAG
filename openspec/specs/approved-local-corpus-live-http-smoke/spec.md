# approved-local-corpus-live-http-smoke Specification

## Purpose

Validate that a registered approved local corpus source is usable through an already running local provider HTTP endpoint before moving real trial work into the caller repository.

## Requirements

### Requirement: Approved local corpus live HTTP smoke can be exported
The system SHALL export a live HTTP smoke report for a registered approved local corpus source through an already running provider base URL.

#### Scenario: Live HTTP corpus passes
- **WHEN** the configured base URL is reachable, the approved source is visible in the provider catalog, the source manifest is available, and answerable business questions return evidence with valid citations
- **THEN** the report has `decision=go`
- **AND** it records the base URL, source id, case-level retrieve counts, answer statuses, citations, invalid citation counts, and HTTP transport mode

#### Scenario: Live HTTP corpus needs review
- **WHEN** the provider is reachable but one or more expected-answerable questions return weak or missing evidence, or the negative-control query returns unexpected evidence
- **THEN** the report has `decision=review`
- **AND** it recommends reviewing the corpus content, page range, query set, or retrieval behavior before MyPrivateAgent-side trial usage

#### Scenario: Live HTTP corpus is blocked
- **WHEN** the provider base URL is unreachable, the source is not visible, the manifest fails, retrieve/answer HTTP calls fail, response contracts are not `ok`, or an answer cites outside the retrieved evidence allowlist
- **THEN** the report has `decision=blocked`
- **AND** it records the blocking reason without mutating provider state

### Requirement: Live HTTP smoke supports caller-shaped access
The live HTTP smoke SHALL behave like an external caller rather than an in-process test.

#### Scenario: Provider API key is supplied
- **WHEN** the smoke command receives a provider API key
- **THEN** it sends the key through supported provider API headers
- **AND** it never writes the secret value into JSON or Markdown output

#### Scenario: Provider API key is omitted
- **WHEN** no provider API key is supplied
- **THEN** the smoke calls the public local provider endpoints without credentials
- **AND** protected endpoint failures are reported as blocked HTTP contract failures

### Requirement: Live HTTP smoke remains lightweight
The approved local corpus live HTTP smoke SHALL validate existing local provider behavior without mutating runtime state.

#### Scenario: Live HTTP smoke runs
- **WHEN** the smoke command runs
- **THEN** it does not start the server, register sources, create source-to-agent bindings, create formal ingestion jobs, start OCR services, promote retrieval backends, run MyPrivateAgent orchestration, call vector databases, or execute GraphRAG
