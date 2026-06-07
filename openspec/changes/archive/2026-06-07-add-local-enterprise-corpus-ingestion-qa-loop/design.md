## Context

The repository already provides several useful pieces:

- `local_business_corpus_trial` can chunk and answer over markdown input.
- `local_document_source_onboarding` can turn a successful local trial into registration and acceptance artifacts.
- `local_approved_source_ingestion_loop` can create a formal ingestion job, check index status, and run acceptance.
- `/api/rag/retrieve` and `/api/rag/answer` already expose the runtime query path.

The missing practical slice is a single local entrypoint that starts from a business file path and tells the user whether the material is ready for local RAG QA.

## Goals / Non-Goals

**Goals:**

- Accept a local enterprise material file path and produce a single JSON/Markdown report.
- Normalize safe text inputs into markdown staging artifacts.
- Reuse the existing approved-source ingestion loop instead of duplicating registration/indexing logic.
- Preserve clear failure states for missing files, unsupported formats, downstream review, and downstream blockers.
- Make raw PDF handling honest: blocked until a parser/OCR-derived markdown or parser artifact exists.

**Non-Goals:**

- Do not parse raw PDFs in this change.
- Do not start OCR, VLM, parser, MyPrivateAgent, Qdrant, or GraphRAG services.
- Do not mutate source-to-agent bindings or caller control-plane policy.
- Do not add background workers or a UI.
- Do not replace existing ingestion lifecycle APIs.

## Decisions

1. Add a wrapper service over the existing approved-source ingestion loop.
   - Rationale: the existing loop already owns onboarding, preflight, ingestion job, index readiness, and acceptance.
   - Alternative considered: extend every existing phase script. Rejected because it keeps the user-facing path fragmented.

2. Support `.txt` by materializing a markdown staging file.
   - Rationale: many enterprise notes and extracted documents start as plain text; this is safe and dependency-free.
   - Alternative considered: force users to manually rename `.txt` to `.md`. Rejected because it weakens day-to-day usability for no real safety gain.

3. Block raw `.pdf` with explicit recovery actions.
   - Rationale: pretending raw PDF parsing is solved would be worse than a clear blocked state. PDF parsing quality depends on text extraction, layout, OCR, and scanned-image handling.
   - Alternative considered: add optional PDF extraction. Rejected for this slice because it risks pulling parser/OCR complexity back into the lightweight provider loop.

4. Keep output as local artifacts and CLI first.
   - Rationale: the immediate goal is local usability and repeatable verification, not a management UI.

## Risks / Trade-offs

- Raw PDFs still require a prior parser/OCR step -> mitigated by explicit `blocked` output and recovery actions.
- Text normalization may lose rich document structure -> acceptable for the minimal loop; parser artifacts remain the richer path.
- The report may mutate approved source registry and materialized source files through existing registration logic -> this is intentional for approved-source ingestion, but the report records that caller bindings and runtime defaults remain unchanged.
