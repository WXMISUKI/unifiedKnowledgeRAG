## Context

The provider already exposes a source document manifest and an ingestion preflight endpoint. Those endpoints can report document files, fingerprints, format support, chunk previews, citation anchors, and index readiness, but they do not yet give callers a compact source-level package contract or a stable chunk-level manifest. For enterprise onboarding, operators need to review what a source claims to be and what chunks will be indexed before running ingestion.

This change stays inside the lightweight provider boundary. It improves read-only diagnostics for document RAG sources and keeps MyPrivateAgent responsible for source-to-agent binding, approval, policy, audit, and final answer behavior.

## Goals / Non-Goals

**Goals:**

- Add provider-owned source package metadata for each RAG source.
- Add deterministic chunk manifest diagnostics for supported markdown sources.
- Reuse existing source document and ingestion preflight flows instead of adding a new heavy API surface.
- Keep diagnostics read-only and safe to call before ingestion.

**Non-Goals:**

- Add OCR, PDF, Word, Excel, HTML, or table parsing.
- Change runtime retrieval defaults, Qdrant ingestion behavior, embedding selection, reranking, or GraphRAG execution.
- Create ingestion jobs, rebuild indexes, or mutate lifecycle state from diagnostic calls.
- Move source binding policy or approval workflow into this provider.

## Decisions

- Add source package metadata as a small provider-owned model associated with each source.
  - Rationale: Source package facts such as domain, language, sensitivity, supported formats, citation granularity, and default chunking strategy are useful before any specific document is parsed.
  - Alternative considered: Put all fields into every document manifest entry. Rejected because source-level facts would be duplicated and harder for callers to review.

- Add chunk manifest entries to existing diagnostics, not as a new mutation workflow.
  - Rationale: `GET /api/rag/sources/{source_id}/documents` and `GET /api/ingestion/sources/{source_id}/preflight` are already the read-only review surfaces for source readiness.
  - Alternative considered: Add a new `/api/chunks` endpoint. Rejected for this slice because it expands the public API before the manifest shape is proven.

- Generate chunk manifest only for currently supported markdown parsing.
  - Rationale: This preserves the lightweight boundary and avoids introducing parser dependencies before real corpus evidence justifies them.
  - Alternative considered: Add placeholder chunk manifests for unsupported formats. Rejected because fabricated chunk metadata would be misleading.

- Use stable fields that line up with existing evidence provenance.
  - Rationale: `source_path`, `document_id`, `chunk_id`, `citation`, `chunking_strategy`, and preview fields connect source package review, ingestion preflight, retrieval evidence, and answer grounding.

## Risks / Trade-offs

- Chunk manifests may expose text snippets from source documents. Mitigation: keep previews capped and document that diagnostics are for trusted operators/control planes.
- Source package metadata is initially static. Mitigation: treat it as provider-owned configuration and keep future catalog-backed loading as a separate change.
- Markdown-only chunk manifests do not cover all enterprise files. Mitigation: unsupported formats remain explicit `blocked` diagnostics until parser work is approved.
