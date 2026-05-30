## Why

The provider now has a stable local handoff bundle, but external control planes still need to read generated files or run local scripts to inspect it. A lightweight read-only HTTP endpoint lets MyPrivateAgent discover the same handoff status through the provider API without adding platform control-plane behavior.

## What Changes

- Add a read-only `GET /api/provider/handoff` endpoint that returns the current `provider-handoff-bundle-v1` payload.
- Add typed API response models for the handoff bundle so `/openapi.json` can advertise the contract.
- Advertise the handoff endpoint from the provider integration manifest.
- Keep the endpoint side-effect free: it reads existing evidence artifacts and does not refresh evidence, run retrieval, start ingestion, rebuild indexes, or call external vector/embedding/graph systems.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Provider discovery includes a read-only HTTP handoff bundle endpoint for external control-plane review.
- `provider-roadmap`: Phase 6 integration evidence may be exposed through lightweight read-only HTTP discovery without moving control-plane ownership into the provider.

## Impact

- Affected API: new `GET /api/provider/handoff` route and manifest endpoint entry.
- Affected code: provider router, contract models, provider manifest tests, handoff endpoint tests.
- Affected docs/evidence: README, lightweight provider roadmap, OpenSpec specs.
- No new dependencies, background workers, storage engines, or production runtime default changes.
