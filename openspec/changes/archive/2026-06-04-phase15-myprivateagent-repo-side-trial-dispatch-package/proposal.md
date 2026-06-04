## Why

Phase 14 already answers a narrower question: whether the provider is ready for a MyPrivateAgent repo-side trial. What is still missing is a single dispatch package that turns that acceptance posture into a clean, caller-facing handoff artifact without drifting into trial execution or control-plane behavior. Phase 15 creates that package so we can keep moving on the roadmap without reopening backend-specific optimization loops.

## What Changes

- Add a Phase 15 repo-side trial dispatch package that consolidates the Phase 10, Phase 11, Phase 13, and Phase 14 evidence chain into one dispatch artifact.
- Export machine-readable and human-readable dispatch outputs under `docs/integration/myprivateagent-repo-side-trial-dispatch/`.
- Surface the Phase 15 dispatch package as optional evidence in provider handoff bundle and refresh outputs.
- Update roadmap and progress tracking so the next step is framed as repo-side trial dispatch, not backend promotion or backend tuning.
- Keep runtime defaults, source binding, GraphRAG execution, and caller control-plane ownership unchanged.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `provider-roadmap`: add the Phase 15 repo-side trial dispatch package requirements that consolidate provider evidence into a caller-facing dispatch artifact while preserving provider-only boundaries and runtime defaults.

## Impact

- `app/services/phase15_myprivateagent_repo_side_trial_dispatch_package.py`
- `scripts/export_phase15_myprivateagent_repo_side_trial_dispatch_package.py`
- `docs/integration/myprivateagent-repo-side-trial-dispatch/`
- `app/services/provider_handoff_bundle.py`
- `app/services/provider_handoff_refresh.py`
- `docs/roadmap/lightweight_provider_roadmap.md`
- `docs/progress/provider-improvement-tracker.md`
- focused tests for the new dispatch package and handoff visibility
