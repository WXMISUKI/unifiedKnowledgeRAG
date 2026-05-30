## Context

`unifiedKnowledgeRAG` is a lightweight knowledge data-plane provider. The roadmap says Phase 4 should improve evidence packaging for caller answers while preserving the boundary that MyPrivateAgent owns final answer policy and user-facing rendering.

The current API already returns evidence documents, retrieval traces, answer traces, prompt package metadata, and output validation metadata. What is missing is a single retrieval-owned metadata object that a caller can use as the canonical evidence bundle before deciding whether and how to answer.

## Goals / Non-Goals

**Goals:**
- Add a stable `evidence_pack-v1` metadata object to successful retrieve and answer envelopes.
- Keep evidence packaging deterministic, local, and provider-owned.
- Make insufficient evidence explicit through pack status and reason.
- Preserve all existing response fields and runtime defaults.

**Non-Goals:**
- Do not add LLM answer generation.
- Do not promote hybrid retrieval, aggregation, reranking, or GraphRAG.
- Do not move caller-owned refusal policy or final answer style into this provider.
- Do not add a new endpoint unless metadata proves insufficient later.

## Decisions

1. Put the evidence pack in `result.metadata.evidence_pack`.
   - Rationale: this is backward-compatible with current contracts and avoids duplicating top-level response models prematurely.
   - Alternative considered: a new `/api/rag/evidence-pack` endpoint. Rejected for now because retrieve already has the required data and the roadmap favors light slices.

2. Build the pack from retrieved `EvidenceDocument` values and request context.
   - Rationale: the pack should be retrieval-owned and deterministic, not composer-specific.
   - Alternative considered: deriving the pack from answer prompt package metadata. Rejected because retrieve callers also need it and insufficient evidence should not expose an endorsed prompt package.

3. Use explicit status values.
   - `answerable` when returned documents are present.
   - `insufficient_evidence` when no documents are returned.
   - Rationale: callers can make safe decisions without parsing prose.

4. Keep pack contents compact.
   - Include pack id, version, status, reason, citation policy, allowed citations, evidence count, score summary, requested sources, backend, filter context, and compact document entries.
   - Rationale: enough for caller-side answer composition and diagnostics without turning this into a general context assembly framework.

## Risks / Trade-offs

- Pack duplicates some information from `documents` and `retrieval_trace` -> Keep it compact and treat it as caller convenience metadata.
- Future rerankers or GraphRAG may need richer fields -> Version the pack as `evidence-pack-v1` and extend later with additive metadata.
- Callers may treat `answerable` as final approval -> Document that this is retrieval evidence status only; caller policy still owns final answer decisions.
