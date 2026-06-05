## Context

Phase 16 is meant to be the minimum caller-facing access loop, but it still reads the provider handoff bundle and refresh status as if every review-level artifact were equally relevant. That makes the access path look noisier than it really is. The project already has enough evidence; what it needs now is a smaller view that isolates the MyPrivateAgent access chain from unrelated review-only evidence.

## Goals / Non-Goals

**Goals:**
- Expose an access-focused handoff visibility summary alongside the full bundle and refresh outputs.
- Keep the access-focused summary derived from the Phase 10, Phase 11, Phase 13, Phase 14, Phase 15, and Phase 16 path.
- Let Phase 14, Phase 15, and Phase 16 treat the access-focused summary as the handoff visibility source of truth.
- Keep the full bundle and refresh outputs intact so unrelated review evidence stays visible.

**Non-Goals:**
- Do not delete unrelated evidence from the bundle or refresh reports.
- Do not create a new parallel evidence artifact or new trial runner.
- Do not change runtime defaults, source binding, GraphRAG execution, or caller control-plane ownership.

## Decisions

1. Add a computed access-focused visibility summary instead of a new report file.
   - Why: the access path should get sharper, not more fragmented.
   - Alternatives considered: a separate access-only handoff report would duplicate the evidence chain and create another artifact to maintain.

2. Keep the full bundle and refresh statuses unchanged.
   - Why: unrelated review-level evidence still matters for broader provider operations.
   - Alternatives considered: forcing the whole bundle to `ready` would hide real open gaps in Phase 3/6/7/8/12 evidence.

3. Make Phase 14, Phase 15, and Phase 16 consume the access-focused view for blocker classification.
   - Why: those callers are about MyPrivateAgent access readiness, not global handoff cleanliness.
   - Alternatives considered: leaving downstream consumers unchanged would preserve the same blocker noise and weaken the slice.

## Risks / Trade-offs

- [Divergence] The access-focused view could drift from the full bundle if the summary rules are duplicated. Mitigation: compute it from the same bundle and refresh payloads.
- [Interpretability] Two statuses in the same artifact can be confusing at first. Mitigation: keep the labels explicit and document the difference in the roadmap/spec.
- [Scope creep] It is easy to turn this into another review taxonomy. Mitigation: keep the summary limited to the MyPrivateAgent access chain and do not expand the evidence set.

## Migration Plan

1. Add the Phase 17 delta spec to `provider-roadmap`.
2. Extend provider handoff bundle and refresh with access-focused visibility summary fields.
3. Update Phase 14, Phase 15, and Phase 16 to classify handoff visibility from the access-focused summary.
4. Refresh the relevant evidence artifacts and run focused tests.
5. Archive the change after validation passes.
