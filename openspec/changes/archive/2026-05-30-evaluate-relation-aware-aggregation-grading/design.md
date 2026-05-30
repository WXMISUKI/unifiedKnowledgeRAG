## Context

The current multi-chunk aggregation evidence has a useful tension: it recovers a split-chunk positive case, but it also returns evidence for an expected-empty query that asks whether one identifier can override another requirement. This is not a retrieval miss; it is an evidence-interpretation problem.

This change adds a deterministic local grading candidate that can label unsupported relationship questions without changing retrieval output. It provides a reviewable bridge before heavier options like reranking, graph relation checks, or LLM evidence grading.

## Goals / Non-Goals

**Goals:**

- Evaluate multi-chunk aggregation outputs with relation-aware labels.
- Preserve raw aggregation evidence while adding grader-specific pass/fail metrics.
- Make the report exportable through the existing Qdrant+BGE smoke script.
- Keep all behavior evaluation-only.

**Non-Goals:**

- Do not filter runtime retrieval or answer outputs.
- Do not call an LLM, reranker, graph store, or external service.
- Do not claim production relation reasoning from a small local fixture.

## Decisions

1. Use deterministic relation markers for the first candidate.

   The current negative case contains explicit unsupported relation language such as `覆盖`. A deterministic candidate can label the case as `relation_unsupported` when returned evidence does not explicitly support that relation. This is intentionally narrow and auditable.

2. Grade aggregation reports rather than changing aggregation.

   The grader consumes the existing positive/negative aggregation evidence. That keeps raw retrieval diagnostics visible and avoids silently hiding over-broad evidence.

3. Export grader evidence separately.

   A separate report avoids rewriting the aggregation report and makes promotion review clearer: aggregation improves recall; relation grading is a separate gate.

## Risks / Trade-offs

- [Risk] Deterministic relation markers are too narrow for production language. → Mitigation: label this as local candidate evidence only and require broader customer-like cases before promotion.
- [Risk] A grader can look like runtime safety even though it is offline. → Mitigation: keep it out of provider HTTP paths and document that runtime defaults do not change.
- [Risk] Passing one negative case could overstate readiness. → Mitigation: report candidate limitations and keep reranker/GraphRAG/evidence grading as later gates.
