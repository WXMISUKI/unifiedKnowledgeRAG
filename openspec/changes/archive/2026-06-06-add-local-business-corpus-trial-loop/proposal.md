## Why

The provider can run locally, and a real company profile PDF has already produced usable PDF-derived markdown evidence. The next practical step is to verify whether that markdown can be treated as a local business corpus trial source and complete a provider-style preflight, chunking, retrieval, and cited-answer loop.

This should remain a lightweight local trial rather than registering private business content as a default provider fixture.

## What Changes

- Add a local business corpus trial loop over a caller-supplied markdown file.
- Create a local trial source overlay artifact that describes source id, title, owner, domain, language, sensitivity, and source path.
- Validate markdown file presence, format, chunkability, and citation generation.
- Run lightweight retrieval and cited-answer checks over the trial markdown.
- Export JSON and Markdown reports with `go`, `review`, or `blocked`.
- Use the existing PDF-derived markdown artifact as the first real local trial input.
- Keep raw PDF ingestion, Qdrant/BGE/pgvector promotion, GraphRAG, source binding, and MyPrivateAgent orchestration out of scope.

## Capabilities

### New Capabilities

- `local-business-corpus-trial-loop`: Local-only trial loop for validating a business markdown corpus before formal source registration.

### Modified Capabilities

- `document-rag`: Clarify that local trial source overlays can evaluate markdown corpus readiness without adding the source to the default provider catalog.

## Impact

- Affected code: new local trial service, export script, focused tests.
- Affected docs: quickstart, README, roadmap, progress tracker, generated local trial artifacts.
- Affected APIs: none.
- Dependencies: none.
- Systems: no default source catalog changes, no raw PDF ingestion, no OCR dependency, no backend promotion, no GraphRAG execution, no MyPrivateAgent integration changes.
