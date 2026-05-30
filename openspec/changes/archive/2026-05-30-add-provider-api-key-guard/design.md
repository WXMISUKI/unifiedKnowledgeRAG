## Context

`unifiedKnowledgeRAG` is intended to run as an external knowledge provider for MyPrivateAgent and other callers. The project should stay lightweight and provider-neutral, but an HTTP component still needs a minimal way to avoid exposing ingestion, retrieval, handoff, and diagnostic APIs in local/public/private-network deployments.

The caller remains responsible for identity, roles, approvals, audit policy, and source-to-agent binding. This change only adds a component-level shared secret gate for provider API access.

## Goals / Non-Goals

**Goals:**

- Add a default-off access guard for `/api/*`.
- Support `Authorization: Bearer <token>` and `X-Provider-Api-Key`.
- Keep `/health` public.
- Return a machine-readable provider error on unauthorized requests.
- Redact the configured secret from readiness evidence.

**Non-Goals:**

- Do not add users, sessions, OAuth, RBAC, ACL policy, approval workflow, or audit storage.
- Do not protect `/health` in this slice.
- Do not change request/response contracts for successful provider capabilities.
- Do not require auth for local tests unless explicitly configured.

## Decisions

1. Implement as middleware.
   - Rationale: `/api/*` includes multiple routers and future endpoints; middleware gives one consistent boundary.
   - Alternative considered: per-router dependencies. That would be more repetitive and easier to forget on new routes.

2. Make the guard default-off.
   - Rationale: current local fixture tests and developer flows should keep working without secrets.
   - Alternative considered: require a key always. That would be safer for deployment but too disruptive for the current local workflow.

3. Keep `/health` public.
   - Rationale: health checks commonly need unauthenticated liveness/readiness probes. Detailed provider data remains under `/api/*`.

4. Report only boolean configuration state.
   - Rationale: readiness evidence should show whether the guard is configured without leaking the token.

## Risks / Trade-offs

- [Risk] Shared secret is not full enterprise identity. -> Mitigation: document it as a component access guard, not user auth or policy.
- [Risk] Default-off guard may be forgotten in deployment. -> Mitigation: deployment readiness reports whether it is configured and adds review notes.
- [Risk] Middleware could block docs/OpenAPI exploration. -> Mitigation: only `/api/*` is guarded; `/openapi.json` remains available in this slice.
