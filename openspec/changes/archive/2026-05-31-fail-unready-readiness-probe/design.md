## Context

The provider has separate `/live`, `/ready`, and `/health` endpoints. `/ready` currently uses the same response body as `/health`, which is good for diagnostics, but its HTTP status does not yet encode readiness failure. For high-availability deployments, readiness HTTP status must be actionable by simple infrastructure components such as Docker healthchecks, reverse proxies, and load balancers.

## Goals / Non-Goals

**Goals:**

- Make `/ready` return HTTP 503 when the provider is degraded.
- Preserve the full readiness body on both HTTP 200 and HTTP 503.
- Keep `/health` returning HTTP 200 for compatibility and human/operator diagnostics.

**Non-Goals:**

- Change liveness semantics.
- Change provider health body shape.
- Add Kubernetes, Prometheus, alert routing, autoscaling, or orchestration policy.
- Change retrieval, answer, ingestion, index lifecycle, embedding, vector store, or GraphRAG behavior.

## Decisions

- Derive `/ready` HTTP status from `HealthResponse.status`.
  - Rationale: The existing body already centralizes provider readiness into `ok` versus `degraded`.
  - Alternative considered: Recompute readiness in the router; rejected to avoid divergent readiness logic.

- Keep `/health` as HTTP 200 even when degraded.
  - Rationale: Existing callers and tests already treat `/health` as a diagnostic endpoint with machine-readable body status.
  - Alternative considered: Also return 503 from `/health`; rejected as a compatibility break.

## Risks / Trade-offs

- Operators using `/ready` directly may need to read the body from a 503 response for diagnostics. Mitigation: the response body remains the same readiness model.
- Some deployment setups may still point at `/health`. Mitigation: README and roadmap clarify `/ready` is the traffic-readiness probe.
