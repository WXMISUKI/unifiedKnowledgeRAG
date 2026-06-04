## Context

Phase 13 has already been completed and archived as a global decision checkpoint. The current evidence chain reaches from Phase 10 MyPrivateAgent local consumer verification through Phase 11 local provider integration and Phase 13 roadmap posture, but there is still no single acceptance artifact that answers whether the provider is ready for a MyPrivateAgent repo-side trial.

This change keeps the project in its intended shape: a lightweight external knowledge provider that exports evidence, readiness, and handoff signals without absorbing caller control-plane duties, source binding policy, or runtime promotion responsibility.

## Goals / Non-Goals

**Goals:**
- Produce one local acceptance checkpoint that decides whether the current provider evidence is sufficient for a MyPrivateAgent repo-side trial.
- Keep the checkpoint read-only, local, and provider-first.
- Surface the checkpoint through handoff bundle and refresh outputs as optional evidence.
- Keep the verdict conservative and explicit about blocker categories.

**Non-Goals:**
- Do not start a live MyPrivateAgent integration.
- Do not introduce a new retrieval backend or promote an existing backend.
- Do not create source-to-agent binding or control-plane governance.
- Do not change runtime defaults, GraphRAG execution, or answer policy.

## Decisions

1. Use a dedicated Phase 14 export service and script rather than extending Phase 13.
   - Why: Phase 13 is a global roadmap decision checkpoint. Phase 14 is a separate acceptance slice with a different question and a different output contract.
   - Alternatives considered: reusing Phase 13 output with a different label would blur the distinction between roadmap decision and trial acceptance.

2. Treat Phase 14 as a read-only evidence aggregator.
   - Why: the checkpoint should prove readiness, not mutate provider state or assume caller-side responsibilities.
   - Alternatives considered: an active trial orchestrator was rejected because it would pull this repo toward control-plane behavior.

3. Keep the verdict model conservative and explicit.
   - Why: the repo should clearly distinguish ready states from provider evidence gaps and external environment blockers.
   - Alternatives considered: a single boolean ready/not-ready flag was rejected because it would hide the reason for the next action.

4. Continue to expose the checkpoint as optional handoff evidence.
   - Why: the handoff bundle should carry the checkpoint without making it a blocking dependency for unrelated evidence refresh flows.
   - Alternatives considered: hard-wiring the checkpoint into every refresh step would make the bundle brittle and increase coupling.

## Risks / Trade-offs

- [Stale evidence] The checkpoint may summarize older local evidence if the exports are not refreshed regularly. → Mitigation: keep the export script deterministic and cheap to rerun.
- [Scope drift] A trial-acceptance checkpoint can drift toward MyPrivateAgent-side orchestration. → Mitigation: keep the output read-only and avoid binding or promotion behavior.
- [Duplicate messaging] Phase 13 and Phase 14 both speak about next steps, which can confuse readers. → Mitigation: Phase 13 remains the global roadmap decision; Phase 14 is specifically the repo-side trial acceptance checkpoint.

## Migration Plan

1. Add the Phase 14 delta spec and supporting design/tasks artifacts.
2. Implement the acceptance export service and its CLI wrapper.
3. Wire the checkpoint into handoff bundle and refresh outputs as optional evidence.
4. Refresh roadmap and progress documentation to reflect the new acceptance slice.
5. Validate with focused tests and `openspec validate --all --strict`.
6. Archive the change after validation passes.

## Open Questions

- Should the repo-side trial verdict be surfaced as a single enum or as an enum plus blocker tags?
- Should the acceptance export reuse any Phase 13 field names verbatim to simplify downstream parsing, or should it carry a distinct schema version from the start?
