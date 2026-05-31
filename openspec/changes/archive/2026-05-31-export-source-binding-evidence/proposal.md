## Why

The provider now exposes `GET /api/provider/source-bindings`, but handoff refresh and handoff bundle evidence still do not persist or summarize source bindability. Before handing this module to MyPrivateAgent, operators should be able to regenerate one evidence set and see whether configured sources are bindable, reviewable, or blocked.

## What Changes

- Add a local export command for source binding summary evidence.
- Write machine-readable JSON and human-readable Markdown under `docs/integration/source-bindings/`.
- Include source binding evidence as required local evidence in the provider handoff bundle.
- Add source binding evidence to provider handoff refresh before the final bundle step.
- Keep all behavior read-only and preserve external control-plane ownership of source-to-agent binding decisions.

## Capabilities

### New Capabilities

### Modified Capabilities

- `knowledge-provider`: Source binding summary evidence can be exported and included in handoff evidence.
- `provider-roadmap`: Phase 2/6 source binding evidence participates in handoff refresh without becoming source binding policy.

## Impact

- Updates `provider_source_binding`, handoff bundle, and handoff refresh services.
- Adds a CLI exporter and generated default evidence artifacts.
- Adds focused tests for export, bundle integration, and refresh ordering.
- No new dependencies and no HTTP contract breakage.
