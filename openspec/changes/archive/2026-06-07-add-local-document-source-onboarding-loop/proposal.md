## Why

The provider can already validate a markdown business corpus, export caller handoff, register an approved local source, and run acceptance smoke. These steps work, but operators still have to remember and chain several commands manually. The next lightweight usability slice is a single local onboarding loop that wires those existing steps together for day-1 business documents.

## What Changes

- Add a local document source onboarding loop that orchestrates existing markdown corpus trial, caller handoff, approved source registration, and acceptance smoke steps.
- Default to the current company-profile source id and markdown artifact.
- Export one JSON and Markdown summary under `docs/local-run/document-source-onboarding/`.
- Return a single `decision`: `go`, `review`, or `blocked`.
- Preserve boundaries: no raw PDF parser promotion, no OCR startup, no formal ingestion jobs, no source-to-agent binding, no vector backend promotion, no MyPrivateAgent orchestration, and no GraphRAG execution.

## Capabilities

### New Capabilities

- `local-document-source-onboarding-loop`: A lightweight operator loop for onboarding local markdown business documents as provider-visible sources.

### Modified Capabilities

- None.

## Impact

- Affected code:
  - new orchestration service under `app/services/`
  - new export script under `scripts/`
- Affected tests:
  - focused service/script tests for go, review/blocked propagation, missing markdown, and boundaries
- Affected docs:
  - roadmap/local-run guidance for the unified onboarding command
- No runtime default changes.
