## Context

The answer endpoint now depends on two broad readiness surfaces:

- retrieval readiness: source validation, backend readiness, and index lifecycle readiness.
- answer composer readiness: deterministic composer available now, hosted/local composers intentionally not implemented yet.

Health currently reports only RAG retrieval and graph readiness. Capabilities currently report `knowledge.rag.answer` as ready even if `RAG_ANSWER_COMPOSER=hosted` or `local`, where invocation will fail closed.

## Goals / Non-Goals

**Goals:**
- Surface answer composer readiness in `/health`.
- Reflect answer composer availability in the `knowledge.rag.answer` capability status.
- Include machine-readable backend/provider metadata where the existing status model allows it.
- Keep the answer endpoint fail-closed behavior unchanged.

**Non-Goals:**
- Implement hosted or local LLM composers.
- Add per-source answer readiness.
- Add a new health endpoint or change retrieval readiness semantics.

## Decisions

1. Add an `answer` component to `HealthResponse`.

   Rationale: answer orchestration has separate runtime dependencies from retrieval. A distinct component keeps degraded composer configuration visible without overloading `rag.backend_status`.

2. Use composer readiness only for `knowledge.rag.answer` capability status.

   Rationale: `knowledge.rag.retrieve` should remain ready when retrieval is ready, even if answer composition is unavailable.

3. Treat deterministic composer as ready and hosted/local/unsupported composers as degraded.

   Rationale: this matches current runtime behavior and keeps future model integration explicit.

## Risks / Trade-offs

- Adding a top-level health field changes response content -> It is additive and Pydantic response models make the contract explicit.
- Capability status remains coarse -> This is enough for immediate orchestration; richer error/reason metadata can be added later if callers need it.
