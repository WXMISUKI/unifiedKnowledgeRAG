## 1. Specification

- [x] 1.1 Add the Phase 13 provider-roadmap decision checkpoint requirement to `provider-roadmap`.
- [x] 1.2 Add the handoff visibility requirement that keeps the Phase 13 checkpoint optional and review-only.

## 2. Design and Documentation

- [x] 2.1 Add the Phase 13 design note that makes the next recommended focus explicit and keeps runtime defaults unchanged.
- [x] 2.2 Add the checkpoint export artifact under `docs/operations/provider-roadmap-decision-checkpoint/`.
- [x] 2.3 Update roadmap and progress docs so the next phase is described as a global decision, not a pgvector-only drift.

## 3. Implementation

- [x] 3.1 Implement `app/services/phase13_provider_roadmap_decision_checkpoint.py`.
- [x] 3.2 Add `scripts/export_phase13_provider_roadmap_decision_checkpoint.py`.
- [x] 3.3 Wire the new checkpoint into `app/services/provider_handoff_bundle.py` and `app/services/provider_handoff_refresh.py` as optional evidence.

## 4. Validation

- [x] 4.1 Add focused tests for the new checkpoint report, export helper, and handoff visibility.
- [x] 4.2 Run targeted pytest coverage for the new slice.
- [x] 4.3 Run `openspec validate phase13-provider-roadmap-decision-checkpoint --strict` and `openspec validate --all --strict`.

## 5. Closure

- [x] 5.1 Refresh the provider improvement tracker with the Phase 13 checkpoint.
- [x] 5.2 Archive the change after the review pass is complete.
