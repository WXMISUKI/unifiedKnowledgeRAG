## Context

`provider-handoff-bundle-v1` already consolidates provider identity, integration probe evidence, contract smoke evidence, deployment readiness, and reindex readiness. It is exported as JSON and Markdown under `docs/integration/provider-handoff/`, and the refresh command can regenerate prerequisite artifacts.

The next useful step is not more report generation. MyPrivateAgent and similar callers need a stable provider API they can query while binding a component. The endpoint should expose the same current handoff bundle state while preserving the project's lightweight boundary.

## Goals / Non-Goals

**Goals:**

- Expose current handoff bundle status at `GET /api/provider/handoff`.
- Make the response schema visible through FastAPI/OpenAPI.
- Advertise the endpoint through the provider integration manifest.
- Preserve side-effect-free behavior and current local export commands.

**Non-Goals:**

- Do not regenerate prerequisite evidence from the endpoint.
- Do not add provider registration, heartbeat governance, audit policy, or source-to-agent binding decisions.
- Do not trigger retrieval, answer composition, ingestion jobs, index rebuilds, embedding calls, Qdrant calls, or GraphRAG execution.
- Do not change runtime defaults or promote any retrieval backend.

## Decisions

1. Reuse `build_provider_handoff_bundle_report(...)` for the endpoint.
   - Rationale: it already provides deterministic current-state summarization over existing evidence artifacts.
   - Alternative considered: return the generated JSON file directly. That would make the API depend on stale exported paths and bypass the existing service-level missing-artifact handling.

2. Add Pydantic response models rather than returning an untyped dict.
   - Rationale: callers can inspect `/openapi.json` and bind to a stable response shape.
   - Alternative considered: annotate the route as `dict[str, Any]`; this is faster to add but weaker for component integration.

3. Keep refresh as CLI-only for now.
   - Rationale: refresh is an operator workflow that writes local evidence files. The HTTP endpoint should remain a read-only discovery surface.
   - Alternative considered: add `POST /api/provider/handoff/refresh`; that would expand operational authority into the provider API and is too heavy for this slice.

## Risks / Trade-offs

- [Risk] Callers may assume the endpoint refreshes evidence automatically. -> Mitigation: document that it reads current evidence and exposes recommended actions for missing or review artifacts.
- [Risk] The response contains filesystem-relative evidence paths. -> Mitigation: these are already provider-owned review artifact references, not secrets; keep them relative and avoid reading secret configuration.
- [Risk] Adding an operations endpoint could blur control-plane boundaries. -> Mitigation: route is read-only and manifest/roadmap text explicitly states registration and governance remain caller-owned.
