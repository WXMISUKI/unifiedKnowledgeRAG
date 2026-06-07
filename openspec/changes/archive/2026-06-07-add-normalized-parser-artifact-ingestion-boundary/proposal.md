## Why

The provider can now register and ingest an approved local markdown source, but real business documents often arrive as PDF, Word, Excel, or OCR output before they become markdown. This change adds a lightweight parser-artifact boundary so externally parsed document output can enter the existing local ingestion loop without turning the provider into an OCR/PDF parsing platform.

## What Changes

- Introduce a normalized parser artifact contract for externally parsed document content.
- Add validation rules for artifact identity, provenance, text content, source metadata, citations, and parser status.
- Add a local exporter that materializes a ready normalized artifact into provider-managed markdown plus source overlay artifacts for the existing onboarding and ingestion loops.
- Keep raw PDF parsing, OCR service startup, parser engine orchestration, source binding, backend promotion, and GraphRAG execution out of scope.
- Update roadmap/progress notes so Stage 2 is closed and Stage 3 becomes the active RAG maturity slice.

## Capabilities

### New Capabilities
- `normalized-parser-artifact-ingestion-boundary`: Defines how externally parsed PDF/Word/Excel/OCR-derived artifacts are validated and materialized for provider-managed local RAG ingestion.

### Modified Capabilities
- `document-rag`: Clarifies that raw PDF remains unsupported by provider ingestion while normalized external parser artifacts can be converted into markdown-based source artifacts.

## Impact

- Affected code: new provider-side service and CLI exporter for normalized parser artifacts.
- Affected docs: RAG maturity roadmap and provider progress tracker.
- Affected tests: focused unit tests for ready/review/blocked artifact paths and explicit non-goal boundaries.
- Dependencies: no new runtime parser, OCR, vector database, or GraphRAG dependency.
