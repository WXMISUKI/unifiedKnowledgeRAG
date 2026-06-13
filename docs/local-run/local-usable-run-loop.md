# Local Usable Run Loop

- Report: `local-usable-run-loop-v1`
- Decision: `go`
- Reason: `local_provider_usable`
- Generated At: `2026-06-13T13:13:04.474894+00:00`
- Base URL: `http://127.0.0.1:8020`
- Query: `客户三天未发货能否退款？`
- Source ID: `refund_policy_docs`

## Summary

| Metric | Value |
|---|---|
| `decision` | `go` |
| `ready_checks` | `7` |
| `review_checks` | `0` |
| `blocked_checks` | `0` |
| `retrieve_document_count` | `3` |
| `retrieve_evidence_pack_status` | `answerable` |
| `retrieve_allowed_citation_count` | `3` |
| `answer_status` | `answered` |
| `answer_citation_count` | `3` |
| `runtime_promotion_status` | `keep_runtime_defaults` |
| `backend_promotion_status` | `not_promoted_by_local_run_loop` |
| `graph_execution_status` | `not_executed` |

## Checks

| Check | Endpoint | Status | HTTP | Details |
|---|---|---|---|---|
| `live_probe` | `GET /live` | `ready` | `200` | `{"service": "unifiedKnowledgeProvider", "status": "live"}` |
| `ready_probe` | `GET /ready` | `ready` | `200` | `{"status": "ok"}` |
| `health_readiness` | `GET /health` | `ready` | `200` | `{"answer_status": "ready", "rag_status": "ready", "service": "unifiedKnowledgeProvider", "status": "ok"}` |
| `provider_manifest` | `GET /api/provider/manifest` | `ready` | `200` | `{"contract_version": "knowledge-provider-contract-v1", "manifest_version": "provider-integration-manifest-v1", "provider_id": "unifiedKnowledgeProvider"}` |
| `provider_preflight` | `GET /api/provider/preflight` | `ready` | `200` | `{"bindable": true, "check_count": 6, "contract_version": "knowledge-provider-contract-v1"}` |
| `rag_retrieve` | `POST /api/rag/retrieve` | `ready` | `200` | `{"allowed_citation_count": 3, "document_count": 3, "evidence_pack_status": "answerable", "ok": true}` |
| `rag_answer` | `POST /api/rag/answer` | `ready` | `200` | `{"answer_status": "answered", "citation_count": 3}` |

## Recommended Actions

- use_http_127_0_0_1_8020_as_local_provider_url
- connect_myprivateagent_to_local_provider_when_needed
- keep_runtime_defaults_unchanged

## Notes

- This report validates an already-running local provider service.
- It does not start uvicorn, download models, start Docker/Qdrant/pgvector, rebuild indexes, create source bindings, promote retrieval defaults, or execute GraphRAG.
- The default query and source are fixture-friendly local smoke inputs, not production corpus approval.
- No provider API key was supplied; this is expected for default local development.
