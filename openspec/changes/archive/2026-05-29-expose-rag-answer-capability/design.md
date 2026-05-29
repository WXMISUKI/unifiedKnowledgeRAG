## Context

The system now has two distinct document RAG runtime surfaces:

- `/api/rag/retrieve` for raw cited evidence and diagnostics.
- `/api/rag/answer` for cited answer orchestration with evidence gating and composer selection.

Only the retrieval surface is currently discoverable through `/api/capabilities`, which makes the answer surface less usable for MyPrivateAgent or any external orchestrator that relies on capability discovery.

## Goals / Non-Goals

**Goals:**
- Expose `knowledge.rag.answer` as a stable provider capability id.
- Preserve existing `knowledge.rag.retrieve` and `knowledge.graph.query` ids.
- Keep the capability provider-neutral; it reports the contract surface, not a production LLM approval.

**Non-Goals:**
- Add per-capability endpoint URLs, schemas, or auth policy metadata.
- Add readiness details beyond the existing simple status field.
- Change answer endpoint behavior.

## Decisions

1. Add `knowledge.rag.answer` with `status=ready`.

   Rationale: the endpoint exists, is tested, and has fail-closed behavior for unsupported composers. It is ready as a provider contract even though hosted/local LLM adapters remain deferred.

2. Keep capability response shape unchanged.

   Rationale: this is a small compatibility-safe registry update. Rich capability descriptors can be added later when MyPrivateAgent needs endpoint/schema metadata.

## Risks / Trade-offs

- Callers may assume `knowledge.rag.answer` means a production LLM is active -> The description and README explicitly state the current composer boundary and deterministic default.
- Capability metadata remains sparse -> This is acceptable until an upper-layer integration requires endpoint/schema/action metadata.
