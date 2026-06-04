## 1. Specification and Documentation

- [x] 1.1 Add the Phase 15 dispatch package requirements to `openspec/changes/phase15-myprivateagent-repo-side-trial-dispatch-package/specs/provider-roadmap/spec.md`.
- [x] 1.2 Update `docs/roadmap/lightweight_provider_roadmap.md` and `docs/progress/provider-improvement-tracker.md` so Phase 15 is described as repo-side trial dispatch, not backend promotion.

## 2. Export Implementation

- [x] 2.1 Implement `app/services/phase15_myprivateagent_repo_side_trial_dispatch_package.py`.
- [x] 2.2 Add `scripts/export_phase15_myprivateagent_repo_side_trial_dispatch_package.py`.
- [x] 2.3 Emit JSON and Markdown dispatch artifacts under `docs/integration/myprivateagent-repo-side-trial-dispatch/`.

## 3. Handoff Integration

- [x] 3.1 Wire optional Phase 15 evidence into `app/services/provider_handoff_bundle.py`.
- [x] 3.2 Wire optional Phase 15 evidence into `app/services/provider_handoff_refresh.py` without making it a blocking dependency.

## 4. Validation and Closure

- [x] 4.1 Add focused tests for the dispatch package and handoff visibility.
- [x] 4.2 Run targeted pytest coverage and `openspec validate --all --strict`.
- [x] 4.3 Archive the change after validation passes.
