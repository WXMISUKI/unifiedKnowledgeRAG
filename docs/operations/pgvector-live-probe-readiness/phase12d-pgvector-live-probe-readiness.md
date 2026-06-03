# Phase 12d PGVector Live Probe Readiness

- Report: `phase12d-pgvector-live-probe-readiness-v1`
- Status: `blocked`
- Evaluation State: `pgvector_probe_configuration_blocked`
- Decision: `keep_current_default`
- Strategy Verdict: `continue_provider_first_with_candidate_backends`
- Generated At: `2026-06-03T02:41:59.359091+00:00`

## Summary

| Metric | Value |
|---|---|
| strategy_verdict | `continue_provider_first_with_candidate_backends` |
| candidate_backend_id | `pgvector` |
| candidate_backend_kind | `postgresql_native_vector_search_live_probe` |
| probe_mode | `optional_psycopg_live_probe` |
| pgvector_database_url_present | `False` |
| pgvector_driver_available | `False` |
| pgvector_connection_attempted | `False` |
| pgvector_connection_status | `blocked` |
| pgvector_extension_installed | `False` |
| pgvector_schema_exists | `False` |
| pgvector_table_exists | `False` |
| pgvector_index_exists | `False` |
| pgvector_server_version | `unknown` |
| pgvector_schema | `public` |
| pgvector_table | `knowledge_chunks` |
| pgvector_index_name | `knowledge_chunks_embedding_idx` |
| pgvector_vector_size | `1024` |
| probe_timeout_seconds | `5` |
| open_gate_ids | `["pgvector_configuration", "pgvector_driver", "pgvector_connection", "pgvector_extension", "pgvector_schema", "pgvector_table", "pgvector_index", "phase12c_pgvector_candidate_backend_readiness", "phase12b_candidate_backend_evaluation_readiness"]` |
| review_ready_family_ids | `[]` |
| ready_family_ids | `["candidate_evidence_bridge_gate"]` |
| blocked_family_ids | `["pgvector_probe_gate", "pgvector_runtime_gate"]` |

## Candidate Families

| Family | Status | Decision | Evidence Paths | Notes |
|---|---|---|---|---|
| `PGVector Probe Gate` | `blocked` | `keep_current_default` | ["environment:PGVECTOR_DATABASE_URL,PGVECTOR_SCHEMA,PGVECTOR_TABLE,PGVECTOR_INDEX_NAME,PGVECTOR_VECTOR_SIZE,PGVECTOR_PROBE_TIMEOUT_SECONDS", "environment:PGVECTOR_DATABASE_URL,PGVECTOR_SCHEMA,PGVECTOR_TABLE,PGVECTOR_INDEX_NAME,PGVECTOR_VECTOR_SIZE,PGVECTOR_PROBE_TIMEOUT_SECONDS", "environment:PGVECTOR_DATABASE_URL,PGVECTOR_SCHEMA,PGVECTOR_TABLE,PGVECTOR_INDEX_NAME,PGVECTOR_VECTOR_SIZE,PGVECTOR_PROBE_TIMEOUT_SECONDS"] | ["This family keeps the live pgvector probe explicit while avoiding runtime promotion."] |
| `PGVector Runtime Gate` | `blocked` | `keep_current_default` | ["environment:PGVECTOR_DATABASE_URL,PGVECTOR_SCHEMA,PGVECTOR_TABLE,PGVECTOR_INDEX_NAME,PGVECTOR_VECTOR_SIZE,PGVECTOR_PROBE_TIMEOUT_SECONDS", "environment:PGVECTOR_DATABASE_URL,PGVECTOR_SCHEMA,PGVECTOR_TABLE,PGVECTOR_INDEX_NAME,PGVECTOR_VECTOR_SIZE,PGVECTOR_PROBE_TIMEOUT_SECONDS", "environment:PGVECTOR_DATABASE_URL,PGVECTOR_SCHEMA,PGVECTOR_TABLE,PGVECTOR_INDEX_NAME,PGVECTOR_VECTOR_SIZE,PGVECTOR_PROBE_TIMEOUT_SECONDS", "environment:PGVECTOR_DATABASE_URL,PGVECTOR_SCHEMA,PGVECTOR_TABLE,PGVECTOR_INDEX_NAME,PGVECTOR_VECTOR_SIZE,PGVECTOR_PROBE_TIMEOUT_SECONDS"] | ["This family checks the minimum runtime posture needed for a realistic pgvector candidate review."] |
| `Candidate Evidence Bridge Gate` | `ready` | `continue_spike` | ["docs/operations/pgvector-candidate-backend-readiness/phase12c-pgvector-candidate-backend-readiness.json", "docs/operations/candidate-backend-evaluation-readiness/phase12b-candidate-backend-evaluation-readiness.json"] | ["This family keeps the earlier candidate evidence visible next to the live probe."] |

## Signals

| Signal | Required | Status | Summary | Recommended Action |
|---|---|---|---|---|
| `pgvector_configuration` | `True` | `blocked` | status=blocked; connection_mode=not_configured_local_dev; database_url_present=False; schema=public; table=knowledge_chunks; index_name=knowledge_chunks_embedding_idx; vector_size=1024; probe_timeout_seconds=5; next_step=configure_pgvector_database_url | `review_evidence_notes` |
| `pgvector_driver` | `True` | `blocked` | status=blocked; driver_available=False; driver_module=psycopg; next_step=configure_pgvector_database_url | `review_evidence_notes` |
| `pgvector_connection` | `True` | `blocked` | status=blocked; connection_attempted=False; connection_mode=not_configured_local_dev | `review_evidence_notes` |
| `pgvector_extension` | `True` | `blocked` | status=blocked; vector_extension_installed=False; next_step=restore_connection | `review_evidence_notes` |
| `pgvector_schema` | `True` | `blocked` | status=blocked; schema_exists=False; next_step=restore_connection | `review_evidence_notes` |
| `pgvector_table` | `True` | `blocked` | status=blocked; table_exists=False; next_step=restore_connection | `review_evidence_notes` |
| `pgvector_index` | `True` | `blocked` | status=blocked; index_exists=False; next_step=restore_connection | `review_evidence_notes` |
| `phase12c_pgvector_candidate_backend_readiness` | `False` | `blocked` | status=blocked; evaluation_state=pgvector_candidate_configuration_blocked; decision=keep_current_default | `regenerate_phase12c_pgvector_candidate_backend_readiness` |
| `phase12b_candidate_backend_evaluation_readiness` | `False` | `review` | status=review; strategy_verdict=continue_provider_first_with_candidate_backends | `regenerate_phase12b_candidate_backend_evaluation_readiness` |

## Notes

- Phase 12d is read-only and keeps runtime defaults unchanged.
- The live probe is optional and intentionally does not write to PostgreSQL or rebuild indexes.
- pgvector remains candidate-only until a separate promotion change closes the required gates.
