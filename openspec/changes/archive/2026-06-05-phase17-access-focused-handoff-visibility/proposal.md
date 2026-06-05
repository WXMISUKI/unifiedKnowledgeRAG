## Why

Phase 14, Phase 15, and Phase 16 currently treat the full provider handoff bundle and refresh reports as gatekeepers. That is too broad for the current goal. The bundle and refresh outputs still need to preserve review-level evidence for unrelated phases, but MyPrivateAgent's repo-side trial readiness should only depend on the access-focused subset of evidence that actually governs the local access path.

This change keeps the project lightweight by avoiding another evidence pack. It only splits the existing handoff visibility into a general view and an access-focused view so the caller-facing readiness chain can move forward without being blocked by unrelated review artifacts.

## What Changes

- Add an access-focused visibility summary to the provider handoff bundle.
- Add the same access-focused visibility summary to the provider handoff refresh report.
- Make Phase 14, Phase 15, and Phase 16 consume the access-focused visibility view when classifying handoff visibility blockers.
- Keep the full bundle and refresh statuses unchanged for unrelated evidence so the broader review surface remains visible.
- Update roadmap and progress tracking so this slice is described as access-focused handoff visibility rather than more handoff evidence accumulation.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `provider-roadmap`: add the Phase 17 access-focused handoff visibility requirements that separate MyPrivateAgent trial readiness from unrelated handoff review noise while preserving provider-only boundaries and runtime defaults.

## Impact

- `app/services/provider_handoff_bundle.py`
- `app/services/provider_handoff_refresh.py`
- `app/services/phase14_myprivateagent_provider_integration_acceptance_checkpoint.py`
- `app/services/phase15_myprivateagent_repo_side_trial_dispatch_package.py`
- `app/services/phase16_myprivateagent_minimal_access_loop.py`
- `docs/roadmap/lightweight_provider_roadmap.md`
- `docs/progress/provider-improvement-tracker.md`
- focused tests for access-focused handoff visibility and downstream blocker classification
