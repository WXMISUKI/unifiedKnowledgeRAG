## Why

Deployed provider smoke validates provider health, manifest, preflight, and handoff over HTTP, but it does not verify that the formal source binding review endpoint is reachable in a deployed component. Since `knowledge.provider.source_bindings` is now a promoted capability, live deployment evidence should include this read-only binding review surface.

## What Changes

- Add `GET /api/provider/source-bindings` to the deployed provider smoke probe.
- Validate that source binding summary returns a recognized status and source rows.
- Summarize source count and bindable source count in deployed smoke evidence.
- Keep the probe read-only and bounded to discovery/binding-review endpoints.
- Do not execute retrieval, answer composition, ingestion, index rebuilds, embedding/vector stores, model downloads, GraphRAG, registration, heartbeat, audit, or binding creation.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Extend deployed provider smoke evidence with source binding endpoint validation.
- `provider-roadmap`: Record source binding deployed smoke as Phase 6 integration/operations evidence.

## Impact

- Updates deployed smoke service, report output, focused tests, README, roadmap, and OpenSpec specs.
- No new dependencies and no runtime default changes.
