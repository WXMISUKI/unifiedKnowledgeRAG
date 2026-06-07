## Context

The project already has a stable downstream chain:

`normalized parser artifact -> materialized markdown/source overlay -> approved source ingestion -> local QA trial`

That chain intentionally does not parse raw PDFs or call PaddleOCR. The missing local usability slice is the upstream bridge that can call an already-running PaddleOCR service and produce the normalized parser artifact that the downstream chain expects.

## Goals / Non-Goals

**Goals:**
- Provide a local, explicit, operator-run PDF bridge for the first pages of a real business PDF.
- Convert PaddleOCR-compatible output into the existing normalized parser artifact fields.
- Reuse the parser artifact local ingestion loop instead of creating a parallel ingestion path.
- Produce a compact `go / review / blocked` report with paths and recommended next actions.

**Non-Goals:**
- Do not install or start PaddleOCR from this project.
- Do not call MyPrivateAgent as a tool/skill middleman.
- Do not change `/api/chat` behavior.
- Do not promote Qdrant, BGE, hybrid retrieval, or GraphRAG.
- Do not implement background ingestion jobs, upload UI, permissions, or source binding policy.
- Do not claim production-grade PDF parsing quality from one local trial.

## Decisions

1. Use a new upstream bridge instead of changing the existing normalized artifact boundary.

   The existing boundary is valuable because it proves that RAG ingestion only needs a normalized artifact. Changing it to call OCR would blur that contract. A separate bridge keeps provider invocation explicit and easy to disable.

2. Call PaddleOCR directly from `unifiedKnowledgeRAG` for this local trial.

   The alternative was `unifiedKnowledgeRAG -> MyPrivateAgent -> PaddleOCR`, but that would create circular control-plane/data-plane coupling. Direct provider access keeps this project independently runnable while still allowing MyPrivateAgent to orchestrate uploads later.

3. Normalize to text blocks with page-level citation anchors.

   Downstream materialization already requires at least one citation anchor. The bridge will preserve page provenance where available and generate deterministic fallback anchors such as `<source_id>#page-1`.

4. Keep the provider client injectable.

   Tests can use a fake transport so unit tests do not require PaddleOCR to be running. The real local provider is reserved for the trial exporter.

## Risks / Trade-offs

- PaddleOCR response shape may vary by pipeline or version -> normalize defensively from common fields (`text`, `pages`, `blocks`, `rec_texts`, `markdown`) and surface unsupported shapes as `blocked`.
- OCR quality for scanned or complex PDF layouts may be imperfect -> report `review` when output exists but citation/text coverage is weak, and keep this as a trial bridge rather than parser quality certification.
- Page range may not be enforced by the OCR provider itself -> the bridge records the requested max pages and filters normalized page blocks when page metadata is available.
- Large PDFs can be slow on CPU -> default to a bounded `--max-pages 5` local trial and do not add background workers in this slice.
