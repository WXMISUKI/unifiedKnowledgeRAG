# Provider Contract Smoke Report

- Report: `provider-contract-smoke-v1`
- Status: `passed`
- Generated At: `2026-05-30T06:01:12.187753+00:00`
- Checks: `7/7` passed

| Check | Endpoint | Status | Details |
|---|---|---|---|
| `health_readiness` | `GET /health` | `passed` | `{"rag_status": "ready", "answer_status": "ready", "graph_status": "planned"}` |
| `provider_integration_manifest` | `GET /api/provider/manifest` | `passed` | `{"manifest_version": "provider-integration-manifest-v1", "contract_version": "knowledge-provider-contract-v1", "component_role": "knowledge_data_plane", "capability_count": 4}` |
| `provider_preflight` | `GET /api/provider/preflight` | `passed` | `{"contract_version": "knowledge-provider-contract-v1", "check_count": 6, "graph_status": "planned"}` |
| `capability_invocation_metadata` | `GET /api/capabilities` | `passed` | `{"example_request_count": 4, "graph_status": "planned"}` |
| `rag_retrieve_contract` | `POST /api/rag/retrieve` | `passed` | `{"document_count": 2, "retrieval_trace_version": "retrieval-trace-v1", "evidence_pack_version": "evidence-pack-v1", "evidence_pack_status": "answerable"}` |
| `rag_answer_contract` | `POST /api/rag/answer` | `passed` | `{"answer_status": "answered", "citation_count": 2, "retrieval_trace_version": "retrieval-trace-v1", "evidence_pack_version": "evidence-pack-v1", "evidence_pack_status": "answerable", "answer_trace_version": "answer-trace-v1", "final_status": "answered"}` |
| `graph_planned_boundary` | `POST /api/graph/query` | `passed` | `{"error_code": "GRAPH_NOT_IMPLEMENTED"}` |
