## Context

The provider already exposes `/health`, `/api/capabilities`, `/api/catalog`, RAG endpoints, graph boundary endpoints, lifecycle endpoints, and an executable local smoke report. For a componentized integration with MyPrivateAgent, a control plane should be able to ask one cheap read-only endpoint:

- what provider is this;
- what role does it play;
- what contract version does it implement;
- where are health, capabilities, OpenAPI, and smoke evidence;
- which capability ids are safe to bind against.

This is a discovery and compatibility surface, not a registry service.

## Goals / Non-Goals

**Goals:**

- Expose a stable manifest at `GET /api/provider/manifest`.
- Make the provider role explicit as the knowledge data plane for MyPrivateAgent.
- Include versioned provider and contract metadata suitable for preflight checks.
- Include key endpoint paths and capability ids without duplicating full schemas.
- Keep the endpoint deterministic and side-effect free.

**Non-Goals:**

- Do not implement MyPrivateAgent-side registration or remote polling.
- Do not add auth, tenant policy, runtime governance, or approval logic.
- Do not expose vector-store, embedding, queue, or graph-store internals as binding contracts.
- Do not replace `/api/capabilities`; the manifest points to it.

## Decisions

- Add a dedicated endpoint under `/api/provider/manifest`.
  - Rationale: provider identity and compatibility are broader than capability invocation metadata but still belong under the public API namespace.
  - Alternative considered: enrich `/health`. Rejected because health should remain operational readiness, not integration metadata.

- Keep manifest generation in a small service module.
  - Rationale: tests, router, and future smoke checks can share a single source of truth.
  - Alternative considered: inline router response. Rejected because manifest shape is likely to be reused by smoke/reporting.

- Use simple semantic strings for version fields.
  - Rationale: MyPrivateAgent can compare `contract_version` and `manifest_version` without parsing OpenAPI.
  - Alternative considered: expose full OpenAPI schema inline. Rejected because `/openapi.json` already exists.

- Include smoke evidence paths as local documentation/report references.
  - Rationale: local and CI preflight can find the latest checked-in smoke evidence without guessing docs layout.

## Risks / Trade-offs

- [Risk] Manifest can drift from real capabilities. -> Generate capability ids from the same capability response helper or pin focused tests against `/api/capabilities`.
- [Risk] Version strings can become stale. -> Keep initial versions explicit and update them only when public integration behavior changes.
- [Risk] Callers may treat smoke evidence paths as runtime URLs. -> Label them as local evidence paths, while endpoint paths remain HTTP paths.
