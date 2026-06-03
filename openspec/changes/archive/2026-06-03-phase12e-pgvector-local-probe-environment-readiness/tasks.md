## 1. Specification

- [x] 1.1 Keep the Phase 12e pgvector local probe environment aligned with `provider-roadmap` as a provider-first, evaluation-only checkpoint.
- [x] 1.2 Keep the Phase 12e pgvector local environment evidence contract aligned with `retrieval-benchmark-harness` and the shared candidate decision vocabulary.

## 2. Design and Documentation

- [x] 2.1 Add the Phase 12e design note that keeps the local pgvector environment optional, local, and outside runtime promotion.
- [x] 2.2 Add the pgvector local environment runbook, config reference, and exported readiness artifact under `docs/operations/`.
- [x] 2.3 Add the pgvector local environment review artifact to provider handoff bundle and refresh evidence.

## 3. Implementation

- [x] 3.1 Add `requirements-pgvector.txt` as an optional dependency set.
- [x] 3.2 Add `docker-compose.pgvector.example.yml` and `docker/pgvector/init.sql` for the isolated local probe environment.
- [x] 3.3 Implement `app/services/phase12e_pgvector_local_probe_environment_readiness.py`.
- [x] 3.4 Add `scripts/export_phase12e_pgvector_local_probe_environment_readiness.py`.
- [x] 3.5 Wire the new artifact into `app/services/provider_handoff_bundle.py` and `app/services/provider_handoff_refresh.py` as optional evidence.

## 4. Validation

- [x] 4.1 Add focused tests for the new environment readiness report and export helper.
- [x] 4.2 Run targeted pytest coverage for the new slice.
- [x] 4.3 Run `openspec validate phase12e-pgvector-local-probe-environment-readiness --strict` and `openspec validate --all --strict`.

## 5. Closure

- [x] 5.1 Refresh the provider improvement tracker with the new Phase 12e slice.
- [x] 5.2 Archive the change after the review pass is complete.
