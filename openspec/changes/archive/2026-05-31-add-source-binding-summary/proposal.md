## Why

The provider exposes source catalog, source document diagnostics, ingestion preflight, and index readiness, but external control planes still need to stitch several endpoints together before deciding which knowledge sources are safe to bind. A lightweight source binding summary gives MyPrivateAgent one read-only entry point for binding review without moving source-to-agent binding decisions into this provider.

## What Changes

- Add a read-only provider source binding summary endpoint.
- Summarize each configured knowledge base with source status, retrieval backend readiness, index readiness, document drift status, ingestion preflight status, bindability, and recommended action.
- Advertise the endpoint in the provider manifest.
- Keep the provider boundary intact: the endpoint does not bind sources, create ingestion jobs, rebuild indexes, execute retrieval, call embedding/vector stores, or execute GraphRAG.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Add source binding summary discovery for external control-plane binding review.
- `provider-roadmap`: Treat source binding summary as Phase 2 and Phase 6 bridge work that supports binding review without owning binding policy.

## Impact

- Adds a provider source binding service and HTTP endpoint under `/api/provider/source-bindings`.
- Adds response models and focused tests for ready, drifted, and not-ready sources.
- Updates README, roadmap, manifest behavior, and OpenSpec specs.
- No breaking API changes and no new dependencies.
