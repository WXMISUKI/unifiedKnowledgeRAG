## Why

The local provider can now prove that the service and fixture RAG loop are usable, but the next practical question is whether a real PDF document can become usable local RAG material without turning this provider into a heavy OCR platform.

The user has a real company profile PDF whose main content is in the first five pages. We need a small trial that converts only those pages into a local markdown artifact and reports whether the derived text is usable for retrieval and cited answers.

## What Changes

- Add a local PDF-derived markdown corpus trial export.
- Read a caller-supplied PDF path and limit extraction to a small page range, defaulting to the first five pages.
- Convert extracted text into a markdown artifact under `docs/local-run/pdf-derived-corpus/`.
- Evaluate the derived markdown with local chunking, lightweight lexical retrieval, evidence pack semantics, and citation-constrained answer checks.
- Export JSON and Markdown trial reports with `go`, `review`, or `blocked`.
- Keep the current provider parser boundary unchanged: raw PDF remains unsupported by provider ingestion in this slice.
- Treat PaddleOCR or PP-Structure as optional external extraction providers; this repository does not vendor or depend on them.

## Capabilities

### New Capabilities

- `pdf-derived-markdown-corpus-trial`: Local-only trial for turning a small page range from a real PDF into a markdown artifact and judging whether the derived text is usable as RAG evidence.

### Modified Capabilities

- `document-rag`: Clarify that raw PDF ingestion remains unsupported in the provider, while PDF-derived markdown may be evaluated through a separate local trial.

## Impact

- Affected code: new local trial service, export script, and focused tests.
- Affected docs: quickstart/README local trial notes, progress tracker, generated local trial report.
- Affected APIs: none.
- Dependencies: prefer existing/local Python PDF text extraction if available; external PaddleOCR/PP-Structure services are optional and remain out of process.
- Systems: no runtime default changes, no direct PDF ingestion endpoint, no model downloads, no bundled PaddleOCR dependency, no Qdrant/pgvector promotion, no GraphRAG execution, no MyPrivateAgent orchestration changes.
