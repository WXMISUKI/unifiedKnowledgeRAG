## Context

Current ingestion can create jobs and build local indexes for known sources, but it does not expose a focused pre-ingestion diagnostic surface. Operators can discover source manifests and reindex readiness, yet they still lack a source-scoped answer to: "If I try to ingest this enterprise document source now, what will fail and why?"

This change adds a lightweight boundary that helps future enterprise document ingestion scale without overbuilding. It should be useful for markdown fixtures today and ready to extend to PDF, Word, Excel, HTML, OCR, table parsing, and richer chunking later through separate gated changes.

## Goals / Non-Goals

**Goals:**

- Provide a source-scoped ingestion preflight endpoint.
- Report document file status, format support, parser status, chunk preview/count, citation anchor readiness, index status, and recommended action.
- Fail closed for unknown sources, missing files, unsupported formats, empty markdown content, and missing citation anchors.
- Keep the endpoint read-only and side-effect free.

**Non-Goals:**

- Do not parse PDF, Word, Excel, HTML, scanned images, or attachments.
- Do not add OCR, table extraction, tokenizer, document layout, or parser dependencies.
- Do not start ingestion jobs, write lifecycle records, rebuild indexes, call embedding models, call Qdrant, or execute GraphRAG.
- Do not change default runtime retrieval behavior.

## Decisions

1. Add a dedicated preflight service instead of extending ingestion job creation.
   - Rationale: job creation is a lifecycle mutation; preflight is a read-only diagnostic contract.
   - Alternative considered: add validation inside `POST /api/ingestion/jobs`; useful later, but it would not give external control planes a safe preview surface.

2. Reuse source document manifests as the first document registry.
   - Rationale: manifests already carry source path, format, version, chunking strategy, citation anchors, fingerprints, and source ownership context.
   - Alternative considered: add a new document registry file. That would create duplicate source-of-truth before we have real corpus pressure.

3. Support markdown diagnostics only in this slice.
   - Rationale: markdown is the current runnable path and enough to prove the contract.
   - Alternative considered: add unstructured/document parser dependencies now. That is too heavy before representative enterprise files and deployment constraints are confirmed.

4. Include chunk preview but cap it.
   - Rationale: operators need evidence that content can be chunked, but the response should stay compact and safe for control-plane use.

## Risks / Trade-offs

- [Risk] A preflight endpoint may be mistaken for production parser readiness. -> Mitigation: report explicit parser status and unsupported formats; document non-goals.
- [Risk] Markdown-only support may feel narrow. -> Mitigation: this is the right contract slice; richer formats become separate parser adapter changes.
- [Risk] Chunk preview can expose document text. -> Mitigation: cap preview count and length; this is still a provider API for trusted internal control-plane use.
