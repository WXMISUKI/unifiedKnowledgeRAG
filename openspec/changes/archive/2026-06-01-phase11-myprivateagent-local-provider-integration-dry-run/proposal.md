## Why

Phase 10 already provides provider-side local consumer verification evidence, but we still lack a single Phase 11 dry-run slice that simulates MyPrivateAgent local integration flow end-to-end from the provider evidence surface.

We need a read-only integration dry-run bundle that keeps runtime defaults unchanged while making caller-side consumption assumptions explicit and testable.

## What Changes

- Add a Phase 11 local provider integration contract document.
- Add a Phase 11 local integration profile export (read-only).
- Add a Phase 11 provider discovery smoke export.
- Add a Phase 11 RAG retrieve consumption smoke export.
- Add a Phase 11 source-binding preview smoke export.
- Add a Phase 11 local integration decision record.
- Wire Phase 11 artifacts into provider handoff bundle and handoff refresh as optional evidence.
- Update roadmap and progress tracker with Phase 11 artifacts.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `provider-roadmap`: add Phase 11 local provider integration dry-run as read-only evidence before MyPrivateAgent repo-side runtime integration.
- `knowledge-provider`: allow handoff bundle/refresh to summarize optional Phase 11 dry-run profile/discovery/retrieve/source-binding preview evidence.

## Impact

- Adds local evidence docs and smoke exports for Phase 11 under `docs/integration/myprivateagent-local-provider-integration/` and `docs/smoke/myprivateagent-local-provider-integration/`.
- Adds focused provider-side services/scripts/tests for local integration dry-run evidence.
- Extends existing handoff evidence aggregation and refresh chain with optional Phase 11 rows.
- Does not change provider runtime defaults, GraphRAG execution status, source-to-agent binding policy ownership, or caller control-plane ownership.
