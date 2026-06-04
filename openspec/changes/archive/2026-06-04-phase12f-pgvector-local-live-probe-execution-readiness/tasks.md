## 1. Specification

- [x] 1.1 Keep the Phase 12f pgvector local live-probe execution readiness aligned with `provider-roadmap` as a provider-first, execution-oriented checkpoint.
- [x] 1.2 Keep the Phase 12f pgvector local execution evidence contract aligned with `retrieval-benchmark-harness` and the shared candidate decision vocabulary.

## 2. Design and Documentation

- [x] 2.1 Add the Phase 12f design note that keeps the rerun path optional, local, and outside runtime promotion.
- [x] 2.2 Add the pgvector local live-probe execution runbook and exported readiness artifact under `docs/operations/`.
- [x] 2.3 Add the pgvector local live-probe execution review artifact to provider handoff bundle and refresh evidence.

## 3. Implementation

- [x] 3.1 Implement `app/services/phase12f_pgvector_local_live_probe_execution_readiness.py`.
- [x] 3.2 Add `scripts/export_phase12f_pgvector_local_live_probe_execution_readiness.py`.
- [x] 3.3 Wire the new artifact into `app/services/provider_handoff_bundle.py` and `app/services/provider_handoff_refresh.py` as optional evidence.

## 4. Validation

- [x] 4.1 Add focused tests for the new execution readiness report and export helper.
- [x] 4.2 Run targeted pytest coverage for the new slice.
- [x] 4.3 Run `openspec validate phase12f-pgvector-local-live-probe-execution-readiness --strict` and `openspec validate --all --strict`.

## 5. Closure

- [x] 5.1 Refresh the provider improvement tracker with the new Phase 12f slice.
- [x] 5.2 Archive the change after the review pass is complete.
