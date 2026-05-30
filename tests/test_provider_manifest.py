from fastapi.testclient import TestClient

from app.main import create_app
from app.services.provider_manifest import build_provider_integration_manifest


client = TestClient(create_app())


def test_provider_manifest_exposes_identity_role_and_versions():
    response = client.get("/api/provider/manifest")

    assert response.status_code == 200
    body = response.json()
    assert body["provider_id"] == "unifiedKnowledgeProvider"
    assert body["provider_name"] == "unifiedKnowledgeRAG"
    assert body["provider_version"] == "0.1.0"
    assert body["manifest_version"] == "provider-integration-manifest-v1"
    assert body["contract_version"] == "knowledge-provider-contract-v1"
    assert body["component_role"] == "knowledge_data_plane"
    assert body["compatible_control_planes"] == ["MyPrivateAgent"]


def test_provider_manifest_references_integration_endpoints_and_evidence():
    response = client.get("/api/provider/manifest")

    assert response.status_code == 200
    body = response.json()
    assert body["endpoints"] == {
        "health": "/health",
        "manifest": "/api/provider/manifest",
        "capabilities": "/api/capabilities",
        "openapi": "/openapi.json",
        "catalog": "/api/catalog",
        "rag_sources": "/api/rag/sources",
        "rag_retrieve": "/api/rag/retrieve",
        "rag_answer": "/api/rag/answer",
        "graph_schemas": "/api/graph/schemas",
        "graph_query": "/api/graph/query",
        "ingestion_jobs": "/api/ingestion/jobs",
        "index_status_template": "/api/indexes/{source_id}/status",
    }
    assert body["evidence"] == {
        "provider_contract_smoke_json": (
            "docs/smoke/provider-contract/provider-contract-smoke.json"
        ),
        "provider_contract_smoke_markdown": (
            "docs/smoke/provider-contract/provider-contract-smoke.md"
        ),
        "production_indexing_decision": (
            "docs/architecture/production_indexing_architecture.md"
        ),
    }


def test_provider_manifest_lists_capability_ids_without_internal_bindings():
    response = client.get("/api/provider/manifest")

    assert response.status_code == 200
    body = response.json()
    assert body["capability_ids"] == [
        "knowledge.rag.retrieve",
        "knowledge.rag.answer",
        "knowledge.graph.query",
    ]
    boundary_text = body["boundaries"]["implementation_internals"]
    assert "provider internals" in boundary_text
    assert "not MyPrivateAgent binding contracts" in boundary_text


def test_provider_manifest_service_is_side_effect_free(monkeypatch):
    def fail_if_health_like_work_runs(*_args, **_kwargs):
        raise AssertionError("manifest should not create retrievers or run readiness probes")

    monkeypatch.setattr(
        "app.services.retrieval_backends.create_document_retriever",
        fail_if_health_like_work_runs,
    )

    manifest = build_provider_integration_manifest()

    assert manifest.provider_id == "unifiedKnowledgeProvider"
    assert manifest.endpoints["manifest"] == "/api/provider/manifest"
