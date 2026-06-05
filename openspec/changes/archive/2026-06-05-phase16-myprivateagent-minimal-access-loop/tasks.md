## 1. Specification and Documentation

 - [x] 1.1 Add the Phase 16 access loop requirements to `openspec/changes/phase16-myprivateagent-minimal-access-loop/specs/provider-roadmap/spec.md`.
 - [x] 1.2 Update `docs/roadmap/lightweight_provider_roadmap.md` and `docs/progress/provider-improvement-tracker.md` so Phase 16 is described as the minimal access loop, not another handoff-only artifact.

## 2. Export Implementation

 - [x] 2.1 Implement `app/services/phase16_myprivateagent_minimal_access_loop.py`.
 - [x] 2.2 Add `scripts/export_phase16_myprivateagent_minimal_access_loop.py`.
 - [x] 2.3 Emit JSON and Markdown access-loop artifacts under `docs/integration/myprivateagent-minimal-access-loop/`.

## 3. Handoff Integration

 - [x] 3.1 Wire optional Phase 16 evidence into `app/services/provider_handoff_bundle.py`.
 - [x] 3.2 Wire optional Phase 16 evidence into `app/services/provider_handoff_refresh.py` without making it a blocking dependency.

## 4. Validation and Closure

- [x] 4.1 Add focused tests for the access loop package and handoff visibility.
- [x] 4.2 Run targeted pytest coverage and `openspec validate --all --strict`.
 - [x] 4.3 Archive the change after validation passes.
