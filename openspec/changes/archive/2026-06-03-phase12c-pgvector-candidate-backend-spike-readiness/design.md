## Context

Phase 12b already produced a review-only candidate backend readiness layer, and the roadmap now wants the first backend-specific spike to be narrow and reversible. `pgvector` is the best fit for that first spike because it tests PostgreSQL-native vector search without pulling the project toward a heavyweight platform surface.

The current repository does not carry a PostgreSQL driver dependency, and the existing evidence flow is deliberately lightweight. That makes this phase a good place to keep the spike configuration-driven, evidence-backed, and read-only instead of starting a live backend migration.

## Goals / Non-Goals

**Goals:**
- Create a pgvector-specific candidate readiness slice that is clearly distinct from the broader Phase 12b candidate summary.
- Keep the readiness report read-only and local.
- Make the candidate posture visible in handoff and refresh evidence without changing runtime defaults.
- Preserve the provider-first boundary and keep caller ownership, GraphRAG execution, and parser expansion out of scope.

**Non-Goals:**
- No default backend promotion.
- No new PostgreSQL driver dependency in this change.
- No live ingestion, indexing, or vector database writes.
- No caller control-plane changes, identity policy changes, or answer policy changes.
- No GraphRAG execution enablement.

## Decisions

1. **Use pgvector as the first backend-specific spike**
   - Rationale: it is operationally familiar, fits the roadmap's medium-term engine-comparison goal, and is less disruptive than platform-style candidates.
   - Alternatives considered:
     - `Haystack`: useful, but more pipeline-oriented and not as direct for operational reuse.
     - `RAGFlow`: strong reference, but too platform-shaped for the first backend spike.
     - `LightRAG`: more graph-adjacent than we want for the first backend slice.

2. **Keep the spike configuration-driven and read-only**
   - Rationale: the repo currently has no PostgreSQL driver dependency, and adding one now would expand the maintenance surface before the candidate is justified by evidence.
   - Alternatives considered:
     - Add a live PostgreSQL probe immediately. Rejected because it would increase dependency and environment complexity before the evaluation contract exists.
     - Treat pgvector as reference-only forever. Rejected because we do want a first real candidate spike, just not a runtime promotion.

3. **Reuse the existing provider handoff/refresh evidence flow**
   - Rationale: the project already treats handoff as the review entry point, so the new artifact should appear there as optional evidence instead of inventing a new reporting lane.
   - Alternatives considered:
     - Standalone report outside handoff. Rejected because it would fragment review ergonomics.

4. **Keep the same reversible decision vocabulary**
   - Rationale: `keep_current_default`, `continue_spike`, `eligible_for_promotion_review`, and `reference_only` already match the candidate-evaluation language used by Phase 12b.
   - Alternatives considered:
     - Introduce a pgvector-specific status taxonomy. Rejected because it would make review harder to compare across candidates.

## Risks / Trade-offs

- [Risk] The spike stays too evidence-light if we never add a real pgvector-backed local probe.
  [Mitigation] Keep the export structured so a future change can add a probe without reshaping the contract.
- [Risk] The pgvector slice can look redundant next to Phase 12b.
  [Mitigation] Make the report candidate-specific, with pgvector-focused evidence and explicit open gates.
- [Risk] Reviewers may assume this implies a backend migration.
  [Mitigation] Keep the decision state `continue_spike`/`reference_only` unless a separate promotion change is approved.

## Migration Plan

1. Add the pgvector candidate readiness spec and design.
2. Implement the read-only export and smoke.
3. Wire the artifact into handoff and refresh as optional evidence.
4. Validate with focused tests and strict OpenSpec checks.
5. Archive the change after the review pass.

Rollback is simple: remove the optional artifact wiring and leave the provider defaults unchanged. Because this phase does not alter runtime behavior, rollback does not require data migration.

## Open Questions

- Should the next phase add a real PostgreSQL probe once a local environment standard is agreed?
- Do we want pgvector to remain evaluation-only until its own candidate-evidence chain reaches `eligible_for_promotion_review`, or should it stay as a recurring review artifact only?
