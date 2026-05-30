## Why

The roadmap now points the provider toward Phase 4 evidence packaging: callers need a stable, machine-readable evidence bundle they can trust before composing final answers. Current retrieve and answer responses expose documents, traces, and answer diagnostics, but the caller still has to infer which citations are allowed and whether the evidence is usable.

## What Changes

- Add a lightweight `evidence_pack-v1` metadata object for successful RAG retrieve responses.
- Reuse the same evidence pack metadata in RAG answer responses so callers can correlate retrieval evidence with answer gating.
- Include citation policy, allowed citations, score summary, evidence status, and diagnostic reason without changing runtime retrieval defaults.
- Document that this advances roadmap Phase 4 and does not promote hybrid retrieval, reranking, answer LLMs, or GraphRAG.

## Capabilities

### New Capabilities

### Modified Capabilities
- `document-rag`: Retrieval and answer envelopes expose provider-owned evidence pack metadata for caller-side answer composition and hallucination control.
- `provider-roadmap`: Future roadmap-aligned evidence packaging work can be identified as Phase 4 without moving caller-owned final answer policy into this provider.

## Impact

- Affected code: RAG router, answer orchestrator metadata, a new evidence pack service, provider contract smoke checks, focused tests.
- Affected API surface: successful `/api/rag/retrieve` and `/api/rag/answer` responses add backward-compatible metadata only.
- Dependencies: no new runtime or infrastructure dependency.
