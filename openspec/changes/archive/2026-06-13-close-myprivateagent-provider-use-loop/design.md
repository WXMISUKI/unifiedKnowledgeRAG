## Context

`unifiedKnowledgeRAG` is positioned as a lightweight knowledge data-plane provider for MyPrivateAgent. The provider already exposes health, manifest, preflight, source binding evidence, RAG retrieve/answer contracts, and handoff evidence. The current local service at `http://127.0.0.1:8020` can return a `go` local usable run-loop, while deployed smoke remains `review` because the handoff bundle intentionally includes deployment and optional evidence posture.

The important distinction for this stage is that `review` on deployment/handoff evidence is not the same as provider unusable. MyPrivateAgent can use the local provider when the local run loop is `go`, preflight is bindable, source binding evidence is ready, and the caller keeps runtime promotion boundaries unchanged.

## Goals / Non-Goals

**Goals:**
- Define a concise closure contract for MyPrivateAgent local provider use.
- Refresh evidence for an already-running provider service.
- Document the exact caller-facing enablement and verification sequence.
- Clean stale active OpenSpec state so the repository does not look mid-change when it is actually in closure posture.
- Keep provider responsibilities limited to evidence, readiness, and retrieval contracts.

**Non-Goals:**
- No retrieval backend promotion from fixture/mock defaults.
- No Qdrant, pgvector, BGE-M3, hybrid, rerank, or query rewrite default change.
- No GraphRAG execution.
- No source-to-agent binding creation.
- No MyPrivateAgent orchestration, audit, approval, or final answer policy inside this provider.
- No parser expansion or raw PDF ingestion promotion.

## Decisions

1. Treat this as a closure/evidence change, not a feature expansion.
   - Rationale: The provider workstream rebaseline already closed access readiness and moved future work to trigger-driven lanes.
   - Alternative considered: Continue access-readiness phases. Rejected because it contradicts the closure posture and risks local infinite optimization.

2. Use existing exporters and runbooks instead of adding new API endpoints.
   - Rationale: Existing scripts already verify local run-loop, deployed smoke, handoff, and source binding evidence.
   - Alternative considered: Add a new `/api/provider/myprivateagent-readiness` endpoint. Rejected because it would duplicate existing evidence and expand the public API without a runtime need.

3. Document MyPrivateAgent enablement as caller-owned configuration.
   - Rationale: Provider can state the base URL and capability ids, but MyPrivateAgent owns provider registration, heartbeat governance, and chat behavior.
   - Alternative considered: Let provider write MyPrivateAgent configuration. Rejected because it crosses repository and control-plane boundaries.

4. Keep handoff `review` explainable instead of forcing it to `ready`.
   - Rationale: `review` can be correct when deployment readiness or optional production evidence remains unresolved. Local MyPrivateAgent use only needs a narrower evidence set.
   - Alternative considered: Modify handoff decision semantics to report `ready`. Rejected because it would weaken deployment review signals.

## Risks / Trade-offs

- [Risk] A `review` deployed smoke can be misread as provider failure. -> Mitigation: The runbook and closure spec distinguish local provider usability from production deployment promotion.
- [Risk] Cleaning a stale empty OpenSpec change could hide an intended future investigation. -> Mitigation: Record the decision in the closure docs and only remove the empty change if it has no proposal, tasks, or spec content.
- [Risk] Evidence artifacts can become stale after service restarts. -> Mitigation: The runbook names the refresh commands and treats generated timestamps as part of the evidence.
- [Risk] MyPrivateAgent integration could still fail from caller-side config. -> Mitigation: The closure points MyPrivateAgent to explicit env vars and caller-side smoke rather than claiming provider-side evidence is sufficient for caller runtime behavior.
