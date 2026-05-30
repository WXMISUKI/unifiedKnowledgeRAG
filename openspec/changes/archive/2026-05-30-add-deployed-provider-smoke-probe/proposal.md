## Why

The provider now has local contract smoke, handoff evidence, API key protection, and a lightweight deployment profile, but there is no one-command way to verify a running deployed component from an external URL. Before MyPrivateAgent or another control plane binds a public-network or private-network deployment, operators need read-only evidence that the deployed HTTP surface is reachable, authenticated when required, and exposing the expected handoff contract.

## What Changes

- Add a deployed provider smoke probe that calls an already-running provider over HTTP.
- Support a base URL, timeout, and optional provider API key without exposing secret values in exported evidence.
- Validate `GET /health`, `GET /api/provider/manifest`, `GET /api/provider/preflight`, and `GET /api/provider/handoff`.
- Export machine-readable JSON and human-readable Markdown evidence for deployment review.
- Fail closed on unreachable endpoints, non-200 responses, invalid JSON, incompatible manifest/preflight status, or blocked handoff evidence.
- Keep the probe read-only: no retrieval, answer composition, ingestion jobs, index rebuilds, vector database calls, model downloads, or GraphRAG execution.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Add deployed HTTP smoke evidence for an already-running provider component.
- `provider-roadmap`: Treat deployed provider smoke evidence as Phase 6 deployment and operations work without expanding provider scope.

## Impact

- Adds a service module and CLI exporter for deployed provider smoke evidence.
- Adds focused tests around success, auth header propagation, fail-closed behavior, and artifact export.
- Updates README and lightweight roadmap with the deployed smoke command.
- No breaking API changes and no new runtime dependency beyond existing `httpx`.
