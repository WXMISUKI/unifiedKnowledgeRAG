## Context

This provider is now discoverable through `GET /api/provider/manifest`, and its invokable capabilities are discoverable through `GET /api/capabilities`. For a componentized MyPrivateAgent integration, the next useful boundary is a single preflight result that answers:

- is this the expected provider;
- is the provider contract version known;
- are required capabilities present;
- do invokable capabilities expose schema references;
- is the provider currently bindable;
- if not bindable, which checks explain why.

The preflight endpoint should stay read-only and deterministic. It may inspect readiness, but it must not mutate index state or run retrieval.

## Goals / Non-Goals

**Goals:**

- Expose `GET /api/provider/preflight`.
- Return machine-readable checks with `passed`, `status`, and details.
- Compute a top-level `bindable` flag for control-plane registration decisions.
- Reuse shared manifest, health, and capability builders.
- Keep the endpoint provider-neutral and implementation-internal-safe.

**Non-Goals:**

- Do not implement MyPrivateAgent-side binding, polling, or registry writes.
- Do not add authentication, authorization, approval policy, or tenant logic.
- Do not call RAG retrieval, answer generation, ingestion jobs, embedding models, vector databases, or graph queries.
- Do not replace smoke reports; preflight is runtime readiness, smoke remains executable local evidence.

## Decisions

- Use a read-only `GET /api/provider/preflight` endpoint.
  - Rationale: control planes can poll or check it cheaply before binding.
  - Alternative considered: `POST /api/provider/preflight` with caller requirements. Rejected for this slice because a fixed default contract is enough and avoids premature policy/input design.

- Extract `build_health_response` and `build_capabilities_response`.
  - Rationale: preflight should not duplicate router-specific logic.
  - Alternative considered: call router functions from the service. Rejected because services should not depend on HTTP router functions.

- Treat `knowledge.graph.query` as present but planned.
  - Rationale: GraphRAG execution is intentionally planned, but the contract boundary is still supported and bindable as a planned capability.

- Keep `bindable=false` when service health is degraded or required capability/schema checks fail.
  - Rationale: MyPrivateAgent should fail closed for provider registration when the runtime cannot satisfy the minimum knowledge contract.

## Risks / Trade-offs

- [Risk] Preflight can become another full smoke test. -> Keep it to metadata, readiness, capability, and schema-reference checks only.
- [Risk] Health checks may do backend readiness work. -> Reuse the same health readiness semantics that callers already rely on; do not run retrieval or ingestion.
- [Risk] Planned GraphRAG could be misread as fully implemented. -> Include planned status in details and keep execution status separate from capability presence.
