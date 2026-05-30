# Provider Contract Smoke Report

- Report: `provider-contract-smoke-v1`
- Status: `passed`
- Generated At: `2026-05-30T02:47:42.321284+00:00`
- Checks: `6/6` passed

| Check | Endpoint | Status | Details |
|---|---|---|---|
| `health_readiness` | `GET /health` | `passed` | `{"rag_status": "ready", "answer_status": "ready", "graph_status": "planned"}` |
| `provider_integration_manifest` | `GET /api/provider/manifest` | `passed` | `{"manifest_version": "provider-integration-manifest-v1", "contract_version": "knowledge-provider-contract-v1", "component_role": "knowledge_data_plane", "capability_count": 3}` |
| `capability_invocation_metadata` | `GET /api/capabilities` | `passed` | `{"graph_status": "planned"}` |
| `rag_retrieve_contract` | `POST /api/rag/retrieve` | `passed` | `{"document_count": 2, "retrieval_trace_version": "retrieval-trace-v1"}` |
| `rag_answer_contract` | `POST /api/rag/answer` | `passed` | `{"answer_status": "answered", "citation_count": 2, "retrieval_trace_version": "retrieval-trace-v1", "answer_trace_version": "answer-trace-v1", "final_status": "answered"}` |
| `graph_planned_boundary` | `POST /api/graph/query` | `passed` | `{"error_code": "GRAPH_NOT_IMPLEMENTED"}` |
