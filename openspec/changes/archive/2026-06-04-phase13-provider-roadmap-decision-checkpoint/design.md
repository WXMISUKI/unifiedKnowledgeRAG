## Context

Phase 12b through Phase 12f already separate candidate evaluation, pgvector candidate posture, live-probe readiness, local environment packaging, and local rerun readiness. What is missing is a single review artifact that says what we should do next at the roadmap level.

The goal here is not more pgvector refinement. The goal is to make the next slice obvious, bounded, and aligned with the provider's short-term role as a lightweight external knowledge service.

## Goals / Non-Goals

**Goals:**
- Create a Phase 13 checkpoint that summarizes the current candidate-backend evidence chain.
- Make the next recommended focus explicit so the project can step away from endless local backend tuning.
- Keep the checkpoint visible in the existing handoff and refresh flow.
- Preserve provider-first ownership and keep runtime defaults unchanged.

**Non-Goals:**
- No backend promotion.
- No new pgvector live execution.
- No new benchmark family.
- No GraphRAG execution.
- No caller control-plane policy or ownership changes.

## Decisions

1. **Use a global checkpoint instead of another backend-specific spike**
   - Rationale: Phase 12f already covers the local pgvector rerun path. The next value is in deciding whether to continue that path or pause it in favor of broader provider work.
   - Alternatives considered:
     - Add a Phase 12g pgvector benchmark. Rejected because it would keep the work inside the same local optimization loop.

2. **Keep the recommendation provider-first**
   - Rationale: the roadmap still says the short-term priority is a smooth local provider integration surface.
   - Alternatives considered:
     - Move to a backend-first roadmap. Rejected because it would blur the lightweight provider boundary.

3. **Expose the checkpoint through handoff and refresh evidence**
   - Rationale: reviewers already use those artifacts to inspect current readiness and optional evidence.
   - Alternatives considered:
     - Keep the checkpoint standalone. Rejected because it would fragment the evidence chain.

4. **Keep the checkpoint read-only**
   - Rationale: it should help us pick the next slice, not change runtime behavior.
   - Alternatives considered:
     - Couple the checkpoint to execution. Rejected because this change is meant to stay lightweight.

## Risks / Trade-offs

- [Risk] The checkpoint can be mistaken for a promotion decision.
  - Mitigation: keep the output explicit that this is a roadmap decision checkpoint only.
- [Risk] The checkpoint can still feel too close to pgvector if it only summarizes pgvector evidence.
  - Mitigation: include the broader provider integration and handoff posture in the summary and recommendation.
- [Risk] The recommendation may be read as a hard stop rather than a pause.
  - Mitigation: phrase the result as a next-step focus, not a permanent backend verdict.

## Migration Plan

1. Add the Phase 13 provider-roadmap checkpoint requirement and optional handoff visibility requirement.
2. Implement the checkpoint service and export script.
3. Wire the new report into provider handoff bundle and refresh.
4. Update the roadmap and progress tracker to state the next phase clearly.
5. Validate with focused tests and strict OpenSpec checks.
6. Archive the change after the review pass is complete.
