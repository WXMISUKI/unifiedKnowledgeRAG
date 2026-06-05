## Context

Phase 15 already gives MyPrivateAgent a dispatch package, but the caller still needs a simpler, lower-friction way to see the minimum access path from discovery to trial readiness. The project should stay evidence-driven, but the evidence should be consumable without stitching several reports together.

The project boundary stays the same: `unifiedKnowledgeRAG` remains a lightweight evidence provider. It may expose access-loop, readiness, and handoff metadata, but it must not become a trial executor, a binding controller, or a policy plane.

## Goals / Non-Goals

**Goals:**
- Produce a single Phase 16 access loop report that consolidates the current Phase 10, Phase 11, Phase 13, Phase 14, and Phase 15 evidence chain.
- Keep the access loop read-only, local, and provider-owned.
- Surface a clear access verdict, blocker category, and caller checklist so the next action is obvious.
- Expose the access loop through handoff bundle and refresh evidence as optional review input.

**Non-Goals:**
- Do not execute a MyPrivateAgent repo-side trial.
- Do not create source-to-agent binding or change caller control-plane ownership.
- Do not promote a retrieval backend, GraphRAG behavior, or runtime defaults.
- Do not add a new runtime service surface beyond read-only export and evidence refresh.

## Decisions

1. Use a dedicated Phase 16 export service and script.
   - Why: Phase 15 already serves the dispatch question. Phase 16 should focus on access-loop packaging, not dispatch re-evaluation.
   - Alternatives considered: reusing the Phase 15 export with a different filename would blur the distinction between dispatch and access loop.

2. Treat the access loop as evidence aggregation, not orchestration.
   - Why: the package should tell MyPrivateAgent how to proceed, not run the trial or own the workflow.
   - Alternatives considered: a trial runner was rejected because it would pull this repo into caller control-plane territory.

3. Keep the verdict model conservative with explicit blocker categories.
   - Why: downstream callers need to know whether a delay comes from provider evidence, handoff visibility, or the local environment.
   - Alternatives considered: a single boolean ready/not-ready flag was rejected because it hides the next action.

4. Reuse the existing handoff bundle and refresh surfaces.
   - Why: the evidence chain is already canonical, so the access loop should appear there as optional evidence instead of creating a parallel pipeline.
   - Alternatives considered: a separate access-loop-only pipeline would be harder to discover and would fragment the evidence chain.

## Risks / Trade-offs

- [Stale evidence] The access loop can summarize older local outputs if prerequisite evidence is not refreshed. Mitigation: keep the export deterministic and cheap to rerun.
- [Scope drift] The access loop can drift toward trial orchestration. Mitigation: keep the artifact read-only and limit it to verdict, blockers, and checklist output.
- [Duplication] Phase 14, Phase 15, and Phase 16 all summarize the same evidence chain from different angles. Mitigation: keep Phase 14 as acceptance, Phase 15 as dispatch, and Phase 16 as the minimum access loop.
- [Coupling] Adding the package to handoff refresh increases the refresh surface slightly. Mitigation: keep the new step optional and non-blocking, consistent with existing evidence refresh behavior.

## Migration Plan

1. Add the Phase 16 delta spec to `provider-roadmap`.
2. Implement a dedicated export service and CLI wrapper for the access loop report.
3. Wire the new package into handoff bundle and refresh outputs as optional evidence.
4. Update roadmap and progress tracking so the next step is described as minimal access loop work.
5. Validate with focused tests and `openspec validate --all --strict`.
6. Archive the change after validation passes.
