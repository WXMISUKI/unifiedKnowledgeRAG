## Design Overview

Phase 12b is a read-only candidate backend evaluation readiness slice. It does not promote any backend default, and it does not add platform control-plane behavior. Its purpose is to consolidate the evidence already spread across Phase 3, Phase 6, Phase 11, and Phase 12a into one review artifact that answers a simple question: which candidate backend families are ready for evaluation review, which gates remain open, and which engines remain reference-only.

### 1) Evidence Consolidation Layer

Build one local readiness report from existing evidence only:
- Phase 12a local RAG integration hardening profile.
- Phase 11 local provider integration profile and retrieval-consumption smoke.
- Phase 3 retrieval-quality, FP/FN, latency, and hybrid decision evidence.
- Phase 6 BGE-M3, Qdrant, deployment, and private-network evidence.

The report should group evidence by candidate family so reviewers do not have to manually cross-join artifacts.

### 2) Candidate Family Layer

Summarize the current candidate families in a way that stays compatible with the roadmap verdict `continue_provider_first_with_candidate_backends`:
- review-ready backend candidates use the existing evidence chain only;
- open gates are surfaced explicitly;
- `Haystack`, `RAGFlow`, `LightRAG`, and `pgvector` remain reference-only until a separate evidence-backed spike is added.

The report should preserve the boundary that candidate evaluation is not promotion.

### 3) Readiness/Decision Layer

Use a simple, reversible decision vocabulary:
- `keep_current_default` when the required evidence chain is missing or blocked;
- `continue_spike` when the candidate evaluation path is useful but gates remain open;
- `eligible_for_promotion_review` only when the local evidence chain is sufficiently complete for a separate promotion review;
- `reference_only` for engines that are useful as market references but are not yet evaluated as provider backends.

### 4) Smoke And Handoff Layer

Add a compact local smoke that validates the readiness artifact can be exported and parsed, and wire the new artifact into provider handoff refresh as optional review evidence.

## Non-Goals

- No runtime backend promotion.
- No new retrieval engine integration.
- No GraphRAG execution changes.
- No parser expansion or ingestion pipeline redesign.
- No caller control-plane or policy ownership changes.

## Implementation Boundaries

This slice is read-only evidence and smoke.
- It reads existing artifacts and exports JSON/Markdown only.
- It does not require new model downloads, index rebuilds, or backend migration.
- It preserves the current provider contract, caller ownership boundaries, and GraphRAG planned boundary.
