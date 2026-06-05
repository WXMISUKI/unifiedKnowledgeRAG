## Context

`unifiedKnowledgeRAG` has accumulated a useful handoff evidence chain for MyPrivateAgent, but the latest access path still has a loop: Phase 14/15/16 reports depend on handoff visibility, and access-focused handoff visibility includes some downstream Phase 14/15 evidence as tracked items. This keeps the access verdict in `review` even when the actual provider access primitives are already ready.

The project direction is to stop growing evidence-only slices and move toward a real MyPrivateAgent repo-side trial. Phase 18 therefore narrows the gate to the minimum provider-owned signals needed for that trial.

## Goals / Non-Goals

**Goals:**

- Define a small, reusable MyPrivateAgent access gate.
- Separate primitive blockers from review-only context.
- Let Phase 14/15/16 classify blockers from primitive access evidence rather than downstream reports.
- Keep the full handoff bundle and refresh status intact for broader operations review.
- Keep all changes read-only and provider-first.

**Non-Goals:**

- Execute a MyPrivateAgent repo-side trial.
- Promote any retrieval backend or embedding model.
- Change runtime defaults.
- Create source-to-agent bindings.
- Move registration, audit, heartbeat governance, policy, or final answer ownership into this provider.

## Decisions

### Decision: Use a shared access gate helper

The implementation will add a small shared helper for MyPrivateAgent access gate classification. This avoids duplicating the same ready/review/blocked logic across provider handoff, handoff refresh, and Phase 14/15/16 reports.

Alternative considered: update each report independently. That is lower upfront code movement, but it preserves drift risk and makes future blocker classification harder to reason about.

### Decision: Gate on primitive access signals only

The required primitive gate uses the provider-owned smoke/probe artifacts that directly represent whether a caller can discover, consume retrieval evidence, and inspect source-binding preview:

- `provider_contract_smoke`
- `phase10_myprivateagent_local_consumer_probe`
- `phase11_provider_discovery_smoke`
- `phase11_rag_retrieve_consumption_smoke`
- `phase11_source_binding_preview_smoke`

Phase 10 readiness, Phase 11 profile, Phase 13 checkpoint, Phase 14/15/16 reports, full handoff bundle, and refresh remain visible as review context but do not block the access gate by themselves.

### Decision: Preserve full handoff status

The provider handoff bundle may continue to be `review` when broader operations, deployment, backend candidate, or promotion evidence is still in review. Phase 18 changes only access-focused visibility and downstream access verdicts.

## Risks / Trade-offs

- Access gate may report `ready` while broader deployment posture is still `review` -> The report will expose review context separately so callers can see non-blocking risks before a real trial.
- Primitive gate can be too permissive if a missing real trial dependency is not represented by the five signals -> The next phase is repo-side trial outcome capture; real failures should become concrete bug fixes, not more generic evidence layers.
- Existing docs may still contain older review wording until regenerated -> Phase 18 will refresh affected reports and update the progress tracker.
