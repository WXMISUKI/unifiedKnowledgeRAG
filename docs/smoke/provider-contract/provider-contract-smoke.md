# Provider Contract Smoke Report

- Report: `provider-contract-smoke-v1`
- Status: `passed`
- Generated At: `2026-06-04T07:37:45.284692+00:00`
- Checks: `9/9` passed

| Check | Endpoint | Status | Details |
|---|---|---|---|
| `health_readiness` | `GET /health` | `passed` | `{"rag_status": "ready", "answer_status": "ready", "graph_status": "planned"}` |
| `provider_integration_manifest` | `GET /api/provider/manifest` | `passed` | `{"manifest_version": "provider-integration-manifest-v1", "contract_version": "knowledge-provider-contract-v1", "component_role": "knowledge_data_plane", "capability_count": 5}` |
| `provider_preflight` | `GET /api/provider/preflight` | `passed` | `{"contract_version": "knowledge-provider-contract-v1", "check_count": 6, "graph_status": "planned"}` |
| `capability_invocation_metadata` | `GET /api/capabilities` | `passed` | `{"example_request_count": 5, "graph_status": "planned"}` |
| `graph_schema_discovery` | `GET /api/graph/schemas` | `passed` | `{"graph_count": 1, "graph_status": "planned", "graph_store": "neo4j_planned", "entity_type_count": 4, "relation_type_count": 3}` |
| `rag_retrieve_contract` | `POST /api/rag/retrieve` | `passed` | `{"document_count": 2, "retrieval_trace_version": "retrieval-trace-v1", "evidence_pack_version": "evidence-pack-v1", "evidence_pack_status": "answerable"}` |
| `rag_answer_contract` | `POST /api/rag/answer` | `passed` | `{"answer_status": "answered", "citation_count": 2, "retrieval_trace_version": "retrieval-trace-v1", "evidence_pack_version": "evidence-pack-v1", "evidence_pack_status": "answerable", "answer_trace_version": "answer-trace-v1", "final_status": "answered"}` |
| `rag_insufficient_evidence_pack_contract` | `POST /api/rag/retrieve + POST /api/rag/answer` | `passed` | `{"retrieval_pack_status": "insufficient_evidence", "retrieval_pack_reason": "no_documents", "retrieval_allowed_citation_count": 0, "retrieval_evidence_count": 0, "answer_status": "insufficient_evidence", "answer_pack_status": "insufficient_evidence", "answer_pack_reason": "no_documents", "answer_allowed_citation_count": 0, "answer_evidence_count": 0}` |
| `graph_planned_boundary` | `POST /api/graph/query` | `passed` | `{"error_code": "GRAPH_NOT_IMPLEMENTED"}` |
