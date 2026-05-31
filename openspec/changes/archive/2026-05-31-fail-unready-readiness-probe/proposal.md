## Why

`/ready` now separates traffic readiness from process liveness, but it still returns HTTP 200 when the provider body says `status=degraded`. Container health checks and load balancers need a non-2xx readiness status to stop sending traffic to an unready instance.

## What Changes

- Return HTTP 200 from `GET /ready` only when the provider readiness body is `status=ok`.
- Return HTTP 503 from `GET /ready` when the readiness body is degraded, while preserving the same response body for diagnostics.
- Keep `GET /health` compatible: it continues to return HTTP 200 with the readiness body even when degraded.
- Document the HTTP status contract for readiness probes.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Tighten the readiness probe contract so degraded readiness returns HTTP 503.
- `provider-roadmap`: Record readiness HTTP status semantics as lightweight Phase 6 high-availability work.

## Impact

- Affected API contract: `GET /ready`
- Compatibility: `GET /health` remains unchanged for existing diagnostics and external callers
- Affected deployment behavior: Docker Compose healthcheck now fails when the provider readiness body is degraded
- No new dependencies, persistence changes, monitoring platform, orchestration logic, retrieval execution, ingestion execution, vector DB calls, or GraphRAG execution
