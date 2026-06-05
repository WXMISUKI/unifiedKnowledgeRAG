## 1. Specification and Documentation

 - [x] 1.1 Add Phase 17 access-focused handoff visibility requirements to `openspec/changes/phase17-access-focused-handoff-visibility/specs/provider-roadmap/spec.md`.
 - [x] 1.2 Update `docs/roadmap/lightweight_provider_roadmap.md` and `docs/progress/provider-improvement-tracker.md` so the next slice is described as access-focused handoff visibility.

## 2. Access-Focused Visibility Implementation

 - [x] 2.1 Extend `app/services/provider_handoff_bundle.py` with an access-focused visibility summary that ignores unrelated review-only phases.
 - [x] 2.2 Extend `app/services/provider_handoff_refresh.py` with the same access-focused visibility summary.
 - [x] 2.3 Update Phase 14, Phase 15, and Phase 16 blocker classification to consume the access-focused visibility summary.

## 3. Validation and Closure

 - [x] 3.1 Add focused tests for access-focused visibility and downstream blocker classification.
 - [x] 3.2 Run targeted pytest coverage and `openspec validate --all --strict`.
 - [x] 3.3 Archive the change after validation passes.
