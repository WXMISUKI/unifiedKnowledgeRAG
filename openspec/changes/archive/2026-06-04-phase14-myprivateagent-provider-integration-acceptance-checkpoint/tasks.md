## 1. Specification and Documentation

- [x] 1.1 Add the Phase 14 acceptance checkpoint requirements to `openspec/changes/phase14-myprivateagent-provider-integration-acceptance-checkpoint/specs/provider-roadmap/spec.md`.
- [x] 1.2 Update `docs/roadmap/lightweight_provider_roadmap.md` and `docs/progress/provider-improvement-tracker.md` so Phase 14 is described as repo-side trial acceptance, not backend promotion.

## 2. Export Implementation

- [x] 2.1 Implement `app/services/phase14_myprivateagent_provider_integration_acceptance_checkpoint.py`.
- [x] 2.2 Add `scripts/export_phase14_myprivateagent_provider_integration_acceptance_checkpoint.py`.
- [x] 2.3 Emit JSON and Markdown acceptance artifacts under `docs/integration/myprivateagent-provider-integration-acceptance/`.

## 3. Handoff Integration

- [x] 3.1 Wire optional Phase 14 evidence into `app/services/provider_handoff_bundle.py`.
- [x] 3.2 Wire optional Phase 14 evidence into `app/services/provider_handoff_refresh.py` without making it a blocking dependency.

## 4. Validation and Closure

- [x] 4.1 Add focused tests for the acceptance checkpoint export and handoff visibility.
- [x] 4.2 Run targeted pytest coverage and `openspec validate --all --strict`.
- [x] 4.3 Archive the change after validation passes.
