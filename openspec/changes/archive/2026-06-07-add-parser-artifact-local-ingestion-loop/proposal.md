## Why

The provider can validate and materialize normalized external parser artifacts, and it can separately run a local approved-source ingestion loop for markdown sources. This change closes the remaining practical gap: a single local loop should prove that a parser artifact can become provider-managed RAG material through the existing onboarding, preflight, ingestion, index, and acceptance steps.

## What Changes

- Add a parser artifact local ingestion loop that orchestrates artifact validation/materialization and the existing approved-source ingestion loop.
- Produce a single `go` / `review` / `blocked` report with step statuses, artifact paths, materialized markdown/source overlay paths, ingestion job evidence, index status, and acceptance smoke status.
- Add a CLI exporter for the loop using the current local company-profile parser artifact fixture by default.
- Update roadmap/progress notes to reflect Stage 3b as the parser-artifact-to-ingestion closure slice.
- Preserve existing boundaries: no raw PDF parsing, no OCR service startup, no parser engine orchestration, no MyPrivateAgent call, no source binding, no backend promotion, no GraphRAG execution.

## Capabilities

### New Capabilities
- `parser-artifact-local-ingestion-loop`: Defines the end-to-end local loop for externally parsed artifacts to enter provider-managed RAG ingestion through existing markdown-based flows.

### Modified Capabilities
- `normalized-parser-artifact-ingestion-boundary`: Clarifies that ready normalized parser artifacts can be chained into a provider-owned local ingestion loop without adding parser engine ownership.

## Impact

- Affected code: new orchestration service and CLI exporter.
- Affected tests: focused loop tests for go, review, blocked, and mid-loop failure semantics.
- Affected docs: enterprise RAG maturity roadmap and provider progress tracker.
- Dependencies: no new parser, OCR, vector database, LLM, or GraphRAG dependency.
