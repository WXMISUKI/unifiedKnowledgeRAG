## Why

Phase 7 and Phase 8 evidence now shows this provider is ready for local handoff review, but there is still no single Phase 9 artifact that translates provider-side evidence into a MyPrivateAgent local-consumption contract.

We need a lightweight, read-only Phase 9 slice that:
- documents MyPrivateAgent local consumption boundaries,
- exports machine-readable local consumption readiness,
- adds a compact local consumption smoke summary,
- and records the current local-consumption decision without changing runtime defaults.

## What Changes

- Add a Phase 9 MyPrivateAgent local-consumption contract document.
- Add a Phase 9 local-consumption readiness export service + script + tests.
- Add a Phase 9 local-consumption smoke summary service + script + tests.
- Wire Phase 9 readiness/smoke into provider handoff bundle and handoff refresh as optional evidence.
- Add a Phase 9 local-consumption decision record.
- Update roadmap and provider improvement tracker with Phase 9 artifacts.

## Non-Goals

- No runtime default promotion for Qdrant/BGE-M3/hybrid.
- No GraphRAG execution implementation.
- No source-to-agent binding mutation.
- No caller control-plane ownership changes.
