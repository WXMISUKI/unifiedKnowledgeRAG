## Why

The provider can already run ingestion jobs, but enterprise documents need a safer pre-ingestion boundary before operators trigger indexing. We need to tell callers whether source files are present, supported, parseable at a lightweight level, chunkable, and citation-ready without adding heavy OCR or production parser dependencies.

## What Changes

- Add a read-only ingestion preflight endpoint for a configured source: `GET /api/ingestion/sources/{source_id}/preflight`.
- Return document-level diagnostics for file presence, format support, parser status, lightweight chunk preview, citation anchor readiness, and recommended action.
- Keep markdown as the only supported parser in this slice; PDF, Word, Excel, HTML, images, and unknown formats are reported as unsupported rather than parsed.
- Preserve existing ingestion job behavior and retrieval defaults.
- Document that this is a Phase 2 enterprise document ingestion boundary, not a production parser/OCR implementation.

## Capabilities

### New Capabilities

### Modified Capabilities

- `document-rag`: Document RAG sources expose a read-only ingestion preflight boundary before indexing.
- `index-lifecycle`: Ingestion lifecycle gains an explicit pre-ingestion diagnostic surface that does not create jobs or rebuild indexes.
- `provider-roadmap`: Phase 2 enterprise document ingestion baseline includes pre-ingestion diagnostics without heavy parser dependencies.

## Impact

- Affected API: new `GET /api/ingestion/sources/{source_id}/preflight`.
- Affected code: contract models, ingestion router, new ingestion preflight service.
- Affected docs: README and lightweight provider roadmap.
- No new dependencies, OCR engines, document parser packages, vector store defaults, or GraphRAG execution changes.
