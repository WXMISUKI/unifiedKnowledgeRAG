## Why

The provider currently exposes `/health` as a combined operational check. Lightweight high-availability deployments benefit from separating process liveness from traffic readiness so containers and external control planes can avoid restarting a live process just because a backend is temporarily degraded.

## What Changes

- Add `GET /live` as a public liveness probe that confirms the FastAPI process can respond without constructing retrieval backends or checking indexes.
- Add `GET /ready` as a public readiness probe that reuses the provider readiness details currently exposed by `/health`.
- Advertise `live` and `ready` endpoints from the provider manifest.
- Update the lightweight Docker Compose healthcheck to use `/ready`.
- Document the probe split and keep `/health` as a compatibility endpoint.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Add lightweight liveness and readiness probe requirements to the provider operational contract.
- `provider-roadmap`: Mark liveness/readiness split as Phase 6 high-availability deployment work that preserves the provider boundary.

## Impact

- Affected API contracts: `GET /live`, `GET /ready`, `GET /health`, `GET /api/provider/manifest`
- Affected deployment profile: `docker-compose.example.yml`
- Affected code: health router/service, provider manifest, tests, README, roadmap, OpenSpec specs
- No new dependencies, persistence changes, monitoring platform, orchestration engine, retrieval execution, ingestion execution, vector DB calls, or GraphRAG execution
