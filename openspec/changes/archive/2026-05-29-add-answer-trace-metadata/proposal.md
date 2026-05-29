# Change: Add answer trace metadata

## Why

The cited answer endpoint now has retrieval, evidence gating, prompt packaging, prompt rendering, output parsing, output validation, and finalization boundaries. Those stages are individually represented in metadata, but callers still need a stable machine-readable trace that explains the end-to-end answer decision without reverse-engineering provider-specific metadata keys.

Before hosted or local LLM composers are introduced, the provider should expose a compact answer trace that MyPrivateAgent and operators can use for audit, diagnostics, governance UI, and fail-closed troubleshooting.

## What

- Add `metadata.answer_trace` to `POST /api/rag/answer` results.
- Include ordered stages for retrieval, evidence gate, composer, output parser, output validator, and final decision.
- Preserve the existing public answer envelope and existing metadata fields.
- Keep trace payload compact and free of full prompt text or raw model output.

## Non-Goals

- No hosted/local LLM implementation.
- No persistence of traces outside the response envelope.
- No new tracing backend, OpenTelemetry exporter, or distributed trace id.
- No changes to retrieval ranking, chunking, vector store, or citation semantics.
