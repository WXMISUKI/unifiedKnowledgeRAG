## Context

The provider currently supports local markdown sources as the lightweight ingestion baseline. Raw PDF, Word, Excel, OCR, and layout parsing are explicitly outside provider ingestion and are reported as unsupported formats.

The immediate user need is narrower than production PDF ingestion: test the first five pages of a real company profile PDF and decide whether it can become usable RAG material after conversion to markdown.

## Goals / Non-Goals

**Goals:**

- Convert a caller-supplied PDF page range into a local markdown artifact for trial use.
- Default the trial to the first five pages.
- Evaluate the derived markdown with deterministic local chunking and citation allowlist checks.
- Export a compact JSON and Markdown report with `go`, `review`, or `blocked`.
- Keep the PDF file and derived business content local-only unless the user explicitly promotes them.

**Non-Goals:**

- Do not make raw PDF a supported provider ingestion format.
- Do not add a provider HTTP upload endpoint.
- Do not vendor PaddleOCR or require OCR services for this provider.
- Do not change source catalog defaults or runtime retrieval defaults.
- Do not run Qdrant, pgvector, BGE-M3, GraphRAG, or MyPrivateAgent orchestration.
- Do not commit the user's original PDF into the repository.

## Decisions

- Add a local export script rather than a new API.
  - Rationale: this is a developer trial over a local file path, not a stable caller contract.

- Use optional Python PDF text extraction when available.
  - Rationale: text-based PDFs can be tested without starting OCR services or adding heavy dependencies.
  - Alternative considered: require PaddleOCR first. Rejected for the first slice because it makes the smallest trial depend on service startup, model availability, and OCR protocol stability.

- Treat OCR/Layout as an external fallback path, not a dependency.
  - Rationale: MyPrivateAgent already keeps OCR/Layout/VLM as external providers. This provider should consume derived text, not own OCR infrastructure.

- Evaluate the markdown artifact locally instead of registering it as a default source.
  - Rationale: the PDF may contain private business content. A local trial should not change default source catalog or repository fixtures.

- Use deterministic chunk citations.
  - Rationale: the trial needs citation allowlist behavior before formal source package and citation anchors are approved.

## Risks / Trade-offs

- Text extraction may be poor for scanned PDFs -> report `blocked` or `review` and recommend OCR/Layout service.
- Derived markdown may include private company content -> keep output under local run artifacts and do not promote it to fixture data automatically.
- Trial retrieval is lighter than the provider's formal source registration path -> acceptable for the first slice; formal registration can follow after the PDF-derived markdown proves useful.
