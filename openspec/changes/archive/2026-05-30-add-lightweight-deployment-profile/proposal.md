## Why

The provider now has stable contracts, access guarding, readiness evidence, and ingestion diagnostics, but it still lacks a concrete lightweight deployment profile. Operators should be able to run the provider as a component with predictable ports, health checks, environment variables, and mounted data directories without inventing deployment conventions.

## What Changes

- Add a production-oriented but lightweight `Dockerfile`.
- Add `docker-compose.example.yml` for local/public/private-network component deployment review.
- Add `.env.example` documenting safe defaults and required deployment overrides.
- Add `.dockerignore` so local indexes, models, caches, and generated artifacts are not baked into the image accidentally.
- Add documentation/tests that verify the deployment profile preserves the provider boundary.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Provider deployment includes a runnable lightweight container profile with health check and environment-driven configuration.
- `provider-roadmap`: Phase 6 deployment evidence includes a component deployment profile without moving control-plane or production infrastructure choices into the provider.

## Impact

- Affected deployment files: `Dockerfile`, `docker-compose.example.yml`, `.dockerignore`, `.env.example`.
- Affected docs: README and lightweight provider roadmap.
- No new Python dependencies, production queue workers, identity systems, vector-store defaults, OCR/parser dependencies, or GraphRAG execution.
