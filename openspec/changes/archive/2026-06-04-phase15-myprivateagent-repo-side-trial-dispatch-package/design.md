## Context

Phase 14 is already the repo-side acceptance checkpoint. The repo still needs one smaller, caller-facing artifact that turns that acceptance posture into a dispatch package that MyPrivateAgent can consume without stitching multiple reports together.

The project boundary stays the same: `unifiedKnowledgeRAG` remains a lightweight evidence provider. It may expose readiness, handoff, and dispatch metadata, but it must not become a trial executor, a binding controller, or a policy plane.

## Goals / Non-Goals

**Goals:**
- Produce a single Phase 15 dispatch package that consolidates the current Phase 10, Phase 11, Phase 13, and Phase 14 evidence chain.
- Keep the dispatch package read-only, local, and provider-owned.
- Surface a clear dispatch verdict, blocker category, and caller checklist so the next action is obvious.
- Expose the dispatch package through handoff bundle and refresh evidence as optional review input.

**Non-Goals:**
- Do not execute a MyPrivateAgent repo-side trial.
- Do not create source-to-agent binding or change caller control-plane ownership.
- Do not promote a retrieval backend, GraphRAG behavior, or runtime defaults.
- Do not add a new runtime service surface beyond read-only export and evidence refresh.

## Decisions

1. Use a dedicated Phase 15 export service and script.
   - Why: Phase 14 already serves the acceptance question. Phase 15 needs a different output contract focused on dispatch packaging, not readiness re-evaluation.
   - Alternatives considered: reusing the Phase 14 export with a different filename would blur the distinction between acceptance and dispatch.

2. Treat the dispatch package as evidence aggregation, not orchestration.
   - Why: the package should tell MyPrivateAgent what to do next, not run the trial or own the workflow.
   - Alternatives considered: a trial runner was rejected because it would pull this repo into caller control-plane territory.

3. Keep the verdict model conservative with explicit blocker categories.
   - Why: downstream callers need to know whether a delay comes from provider evidence, handoff visibility, or the local environment.
   - Alternatives considered: a single boolean ready/not-ready flag was rejected because it hides the next action.

4. Reuse the existing handoff bundle and refresh surfaces.
   - Why: the handoff chain is already the canonical local evidence path, so the dispatch package should appear there as optional evidence instead of creating a parallel pipeline.
   - Alternatives considered: a separate dispatch-only export would be harder to discover and would fragment the evidence chain.

## Risks / Trade-offs

- [Stale evidence] The dispatch package can summarize older local outputs if prerequisite evidence is not refreshed. → Mitigation: keep the export deterministic and cheap to rerun.
- [Scope drift] A dispatch package can drift toward trial orchestration. → Mitigation: keep the artifact read-only and limit it to verdict, blockers, and checklist output.
- [Duplication] Phase 14 and Phase 15 both summarize the same evidence chain from different angles. → Mitigation: Phase 14 remains the acceptance checkpoint; Phase 15 remains the caller-facing dispatch package.
- [Coupling] Adding the package to handoff refresh increases the refresh surface slightly. → Mitigation: keep the new step optional and non-blocking, consistent with existing evidence refresh behavior.

## Migration Plan

1. Add the Phase 15 delta spec to `provider-roadmap`.
2. Implement a dedicated export service and CLI wrapper for the dispatch package.
3. Wire the new package into handoff bundle and refresh outputs as optional evidence.
4. Update roadmap and progress tracking so the next step is described as repo-side trial dispatch.
5. Validate with focused tests and `openspec validate --all --strict`.
6. Archive the change after validation passes.

## Open Questions

- Should the dispatch package reuse the Phase 14 acceptance-state strings verbatim, or expose a new dispatch-specific state vocabulary?
- Should the caller checklist be a stable list of discrete actions or a compact recommendation string plus structured blocker fields?
