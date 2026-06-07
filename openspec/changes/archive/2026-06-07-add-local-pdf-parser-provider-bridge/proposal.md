## Why

The provider can already ingest normalized parser artifacts and markdown-derived local business corpus, but a real local PDF still needs a thin, repeatable bridge from an external OCR/parser service into that existing RAG ingestion loop. This change makes the first local PDF trial usable without embedding PaddleOCR, changing MyPrivateAgent, or promoting heavier retrieval backends.

## What Changes

- Add a local PDF parser provider bridge that calls an operator-started PaddleOCR HTTP provider for a bounded local PDF trial.
- Normalize the provider response into the existing parser artifact shape with source identity, parser metadata, original file metadata, text blocks, and citation anchors.
- Add a CLI exporter that can run `PDF -> parser artifact -> parser artifact local ingestion loop` and write JSON/Markdown trial reports.
- Keep raw PDF ingestion blocked in the existing direct markdown/source ingestion path.
- Preserve lightweight boundaries: no MyPrivateAgent tool middleman, no GraphRAG, no Qdrant/BGE promotion, no source-to-agent binding.

## Capabilities

### New Capabilities
- `local-pdf-parser-provider-bridge`: Covers local PDF-to-parser-artifact bridge execution against an external PaddleOCR-compatible provider and orchestration into the existing parser artifact local ingestion loop.

### Modified Capabilities
- `document-rag`: Records that local document RAG can accept parser artifacts produced by a local PDF parser provider bridge while keeping raw PDF direct ingestion unsupported.

## Impact

- Affected code:
  - new service module for the PDF parser provider bridge
  - new CLI exporter under `scripts/`
  - focused tests for provider response normalization, blocked provider failures, and downstream loop orchestration
- Affected docs:
  - local run artifacts under `docs/local-run/local-pdf-parser-provider-bridge/`
  - enterprise RAG maturity roadmap note for the PDF bridge stage
  - provider improvement tracker entry
- External systems:
  - optional local PaddleOCR HTTP provider at `http://127.0.0.1:8080`
- No breaking API changes.
