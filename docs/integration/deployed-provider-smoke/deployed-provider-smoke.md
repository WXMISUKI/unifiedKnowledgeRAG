# Deployed Provider Smoke Report

- Report: `deployed-provider-smoke-v1`
- Status: `review`
- Generated At: `2026-06-13T13:10:47.772274+00:00`
- Base URL: `http://127.0.0.1:8020`
- Provider: `unifiedKnowledgeProvider`
- Contract: `knowledge-provider-contract-v1`
- Handoff Status: `review`

## Checks

| Check | Endpoint | Status | HTTP | Details |
|---|---|---|---|---|
| `health_readiness` | `GET /health` | `ready` | `200` | `{"answer_status": "ready", "graph_status": "planned", "provider_status": "ok", "rag_status": "ready", "service": "unifiedKnowledgeProvider"}` |
| `provider_manifest` | `GET /api/provider/manifest` | `ready` | `200` | `{"component_role": "knowledge_data_plane", "contract_version": "knowledge-provider-contract-v1", "manifest_version": "provider-integration-manifest-v1", "provider_id": "unifiedKnowledgeProvider", "provider_name": "unifiedKnowledgeRAG", "provider_version": "0.1.0"}` |
| `provider_preflight` | `GET /api/provider/preflight` | `ready` | `200` | `{"bindable": true, "check_count": 6, "contract_version": "knowledge-provider-contract-v1"}` |
| `provider_source_bindings` | `GET /api/provider/source-bindings` | `ready` | `200` | `{"bindable_source_count": 6, "id": "provider-source-binding-summary-v1", "recommended_action_counts": {"bind_source_from_control_plane": 6}, "source_count": 6, "source_status_counts": {"ready": 6}, "status": "ready"}` |
| `provider_handoff` | `GET /api/provider/handoff` | `review` | `200` | `{"artifact_count": 53, "id": "provider-handoff-bundle-v1", "status": "review"}` |

## Operation Notes

- This probe validates an already-running provider over HTTP.
- It only calls health, manifest, preflight, source binding, and handoff discovery endpoints.
- External deployment owners still manage TLS, reverse proxy policy, managed secrets, registration, heartbeat governance, audit policy, and source-to-agent binding.
- No provider API credentials were supplied; this is only expected for local or intentionally open deployments.
