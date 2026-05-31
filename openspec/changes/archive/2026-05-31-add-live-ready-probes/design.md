## Context

`/health` currently returns rich readiness details for RAG, answer composition, and GraphRAG boundary state. That is useful for operators, but high-availability deployments usually need a separate liveness probe that only answers whether the process can serve HTTP, and a readiness probe that answers whether the instance should receive traffic.

## Goals / Non-Goals

**Goals:**

- Provide a side-effect-free liveness probe at `/live`.
- Provide a readiness probe at `/ready` with the same readiness contract as `/health`.
- Keep `/health` compatible for existing callers.
- Make the probes discoverable from the provider manifest and deployment profile.

**Non-Goals:**

- Add metrics, tracing, alerting, Prometheus, or OpenTelemetry.
- Add Kubernetes manifests or platform-specific controller logic.
- Change retrieval, answer, ingestion, index lifecycle, Qdrant, embedding, or GraphRAG behavior.
- Hide readiness behind component API key protection; these probes remain public operational checks like `/health`.

## Decisions

- Keep `/health` as the compatibility readiness endpoint and add `/ready` as an alias over the same readiness builder.
  - Rationale: Existing tests, scripts, and control planes can continue using `/health`, while deployment configs can move to clearer readiness semantics.
  - Alternative considered: Change `/health` to liveness-only; rejected because it would break current readiness expectations.

- Implement `/live` with a small response model and no backend construction.
  - Rationale: Liveness should not depend on retriever, index, embedding, Qdrant, answer composer, or GraphRAG readiness.
  - Alternative considered: Reuse the full health response; rejected because that recreates the current readiness coupling.

- Use `/ready` in Docker Compose healthcheck.
  - Rationale: Docker health status should reflect whether the component can serve provider traffic, not merely whether the process is alive.
  - Alternative considered: Leave Compose on `/health`; rejected because the new endpoint exists to clarify readiness usage.

## Risks / Trade-offs

- Some operators may still use `/health` out of habit. Mitigation: Keep `/health` compatible and document `/ready` as the preferred traffic-readiness probe.
- `/live` can be green while `/ready` is degraded. Mitigation: This is intentional; documentation explains that `/live` is only process liveness, not bindability or retrieval readiness.
