## Why

Phase 17 separated MyPrivateAgent access-focused visibility from broader handoff review noise, but the access path still lets downstream Phase 14/15/16 reports and handoff refresh posture participate as blockers. That creates a review loop where evidence reports can keep requiring themselves instead of telling the caller whether the minimal provider access primitives are usable.

This change simplifies the MyPrivateAgent trial gate so `unifiedKnowledgeRAG` can stop extending the evidence chain and move toward a real repo-side trial.

## What Changes

- Define a minimal MyPrivateAgent access gate based on provider-owned primitive evidence:
  - provider contract smoke
  - Phase 10 local consumer probe
  - Phase 11 provider discovery smoke
  - Phase 11 retrieve-consumption smoke
  - Phase 11 source-binding preview smoke
- Treat Phase 10 readiness, Phase 11 profile, Phase 13 checkpoint, Phase 14 acceptance, Phase 15 dispatch, Phase 16 access loop, full handoff bundle, and handoff refresh as review context rather than primitive blockers.
- Update access-focused handoff visibility and downstream Phase 14/15/16 blocker classification to use the simplified gate.
- Keep the full handoff bundle status unchanged for broader operations review.
- Preserve runtime defaults, source-to-agent binding ownership, and caller-side trial execution boundaries.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `provider-roadmap`: Add Phase 18 requirements for a simplified, non-circular MyPrivateAgent access gate.

## Impact

- Affected services:
  - `app/services/provider_handoff_bundle.py`
  - `app/services/provider_handoff_refresh.py`
  - `app/services/phase14_myprivateagent_provider_integration_acceptance_checkpoint.py`
  - `app/services/phase15_myprivateagent_repo_side_trial_dispatch_package.py`
  - `app/services/phase16_myprivateagent_minimal_access_loop.py`
- Affected tests:
  - provider handoff bundle and refresh tests
  - Phase 14/15/16 access classification tests
- Affected docs:
  - roadmap and progress tracker
  - generated Phase 14/15/16 and provider handoff evidence artifacts
