## Why

Phase 15 already turns the provider evidence chain into a caller-facing dispatch package. What is still missing is a smaller, more actionable entry point for the caller: a minimal access loop that tells MyPrivateAgent how to start from local discovery and decide, in one pass, whether the provider can be used for a real repo-side trial.

This change keeps the project lightweight by avoiding new platform behavior. It only makes the access path easier to inspect and rerun.

## What Changes

- Add a Phase 16 minimal access loop report that consolidates the existing local consumer, local provider integration, roadmap checkpoint, acceptance checkpoint, dispatch package, handoff bundle, and refresh evidence into one caller-facing artifact.
- Export machine-readable and human-readable access-loop outputs under `docs/integration/myprivateagent-minimal-access-loop/`.
- Surface the Phase 16 access loop as optional evidence in provider handoff bundle and refresh outputs.
- Update roadmap and progress tracking so the next step is framed as a minimal access loop rather than another handoff-only artifact.
- Keep runtime defaults, source binding, GraphRAG execution, and caller control-plane ownership unchanged.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `provider-roadmap`: add the Phase 16 minimal access loop requirements that consolidate existing provider evidence into a caller-facing access artifact while preserving provider-only boundaries and runtime defaults.

## Impact

- `app/services/phase16_myprivateagent_minimal_access_loop.py`
- `scripts/export_phase16_myprivateagent_minimal_access_loop.py`
- `docs/integration/myprivateagent-minimal-access-loop/`
- `app/services/provider_handoff_bundle.py`
- `app/services/provider_handoff_refresh.py`
- `docs/roadmap/lightweight_provider_roadmap.md`
- `docs/progress/provider-improvement-tracker.md`
- focused tests for the new access loop package and handoff visibility
