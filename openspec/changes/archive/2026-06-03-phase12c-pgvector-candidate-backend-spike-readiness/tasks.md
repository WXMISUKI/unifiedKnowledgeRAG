## 1. Specification

- [x] 1.1 Keep the Phase 12c pgvector candidate backend spike aligned with `provider-roadmap` as a provider-first, evaluation-only checkpoint.
- [x] 1.2 Keep the Phase 12c pgvector candidate evidence contract aligned with `retrieval-benchmark-harness` and the shared candidate decision vocabulary.

## 2. Design and Documentation

- [x] 2.1 Add the Phase 12c design note that keeps pgvector read-only, configuration-driven, and outside runtime promotion.
- [x] 2.2 Add the pgvector candidate readiness export contract and local evidence artifact documentation under `docs/operations/` and `docs/smoke/`.
- [x] 2.3 Add the pgvector candidate review artifact to provider handoff bundle and refresh evidence.

## 3. Implementation

- [x] 3.1 Implement `app/services/phase12c_pgvector_candidate_backend_readiness.py`.
- [x] 3.2 Add `scripts/export_phase12c_pgvector_candidate_backend_readiness.py`.
- [x] 3.3 Wire the new artifact into `app/services/provider_handoff_bundle.py` and `app/services/provider_handoff_refresh.py` as optional evidence.

## 4. Validation

- [x] 4.1 Add focused tests for the new readiness report and export helper.
- [x] 4.2 Run targeted pytest coverage for the new slice.
- [x] 4.3 Run `openspec validate phase12c-pgvector-candidate-backend-spike-readiness --strict` and `openspec validate --all --strict`.

## 5. Closure

- [x] 5.1 Refresh the provider improvement tracker with the new Phase 12c slice.
- [x] 5.2 Archive the change after the review pass is complete.
