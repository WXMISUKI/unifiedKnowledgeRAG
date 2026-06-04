## Why

Phase 13 already tells us to resume provider integration hardening, but the repo still lacks one explicit acceptance slice that answers a sharper question: is the provider ready for a MyPrivateAgent repo-side trial, or are we still blocked by provider evidence or local environment issues? Phase 14 creates that checkpoint so we can keep moving without drifting back into backend-specific optimization loops.

## What Changes

- Add a Phase 14 local acceptance checkpoint that consolidates Phase 10, Phase 11, and Phase 13 evidence into one repo-side trial readiness verdict.
- Export machine-readable and human-readable acceptance artifacts under `docs/integration/myprivateagent-provider-integration-acceptance/`.
- Surface the Phase 14 checkpoint as optional evidence in provider handoff bundle and refresh outputs.
- Update roadmap and progress tracking so the next step is framed as provider integration acceptance, not backend promotion.
- Keep runtime defaults, source binding, and caller control-plane ownership unchanged.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `provider-roadmap`: add the Phase 14 acceptance checkpoint and handoff visibility requirements that evaluate MyPrivateAgent repo-side trial readiness while preserving provider-only boundaries and runtime defaults.

## Impact

- `app/services/phase14_myprivateagent_provider_integration_acceptance_checkpoint.py`
- `scripts/export_phase14_myprivateagent_provider_integration_acceptance_checkpoint.py`
- `docs/integration/myprivateagent-provider-integration-acceptance/`
- `app/services/provider_handoff_bundle.py`
- `app/services/provider_handoff_refresh.py`
- `docs/roadmap/lightweight_provider_roadmap.md`
- `docs/progress/provider-improvement-tracker.md`
- focused tests for the new checkpoint and handoff visibility
