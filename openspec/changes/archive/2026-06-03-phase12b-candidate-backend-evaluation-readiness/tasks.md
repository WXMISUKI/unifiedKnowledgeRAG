## 1. Specification

- [x] 1.1 Add Phase 12b candidate backend evaluation readiness gates to `provider-roadmap`.
- [x] 1.2 Add a shared candidate backend evidence/export contract to `retrieval-benchmark-harness`.

## 2. Design and Documentation

- [x] 2.1 Add the Phase 12b design note that keeps candidate backend review read-only and provider-first.
- [x] 2.2 Add the candidate backend evaluation readiness exporter and smoke documentation under `docs/operations/` and `docs/smoke/`.
- [x] 2.3 Add the candidate backend review artifact to provider handoff bundle and refresh evidence.

## 3. Implementation

- [x] 3.1 Implement `app/services/phase12b_candidate_backend_evaluation_readiness.py`.
- [x] 3.2 Add `scripts/export_phase12b_candidate_backend_evaluation_readiness.py`.
- [x] 3.3 Wire the new artifact into `app/services/provider_handoff_bundle.py` and `app/services/provider_handoff_refresh.py` as optional evidence.

## 4. Validation

- [x] 4.1 Add focused tests for the new readiness report and export helper.
- [x] 4.2 Run targeted pytest coverage for the new slice.
- [x] 4.3 Run `openspec validate phase12b-candidate-backend-evaluation-readiness --strict` and `openspec validate --all --strict`.

## 5. Closure

- [x] 5.1 Refresh the provider improvement tracker with the new Phase 12b slice.
- [x] 5.2 Archive the change after the review pass is complete.
