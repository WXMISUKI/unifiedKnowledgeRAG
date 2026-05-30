from fastapi.testclient import TestClient

from app.main import create_app
from app.services.provider_preflight import build_provider_preflight_response


def test_provider_preflight_passes_default_local_provider():
    client = TestClient(create_app())

    response = client.get("/api/provider/preflight")

    assert response.status_code == 200
    body = response.json()
    assert body["provider_id"] == "unifiedKnowledgeProvider"
    assert body["contract_version"] == "knowledge-provider-contract-v1"
    assert body["manifest_version"] == "provider-integration-manifest-v1"
    assert body["control_plane_hint"] == "MyPrivateAgent"
    assert body["bindable"] is True
    checks = {check["name"]: check for check in body["checks"]}
    assert checks["manifest_identity"]["passed"] is True
    assert checks["health_readiness"]["passed"] is True
    assert checks["required_capabilities"]["passed"] is True
    assert checks["schema_references"]["passed"] is True


def test_provider_preflight_reports_degraded_health(monkeypatch):
    monkeypatch.setenv("RAG_ANSWER_COMPOSER", "hosted")
    client = TestClient(create_app())

    response = client.get("/api/provider/preflight")

    assert response.status_code == 200
    body = response.json()
    checks = {check["name"]: check for check in body["checks"]}
    assert body["bindable"] is False
    assert checks["health_readiness"]["passed"] is False
    assert checks["health_readiness"]["status"] == "degraded"
    assert checks["health_readiness"]["details"]["answer_status"] == "degraded"
    assert checks["required_capabilities"]["passed"] is True
    assert checks["schema_references"]["passed"] is True


def test_provider_preflight_preserves_planned_graph_boundary():
    client = TestClient(create_app())

    response = client.get("/api/provider/preflight")

    assert response.status_code == 200
    body = response.json()
    checks = {check["name"]: check for check in body["checks"]}
    graph_check = checks["graph_boundary"]
    assert graph_check["passed"] is True
    assert graph_check["status"] == "planned"
    assert graph_check["details"] == {
        "capability_id": "knowledge.graph.query",
        "capability_status": "planned",
        "execution_status": "planned",
        "reason": "Graph query execution is not implemented in this slice.",
    }
    required = checks["required_capabilities"]["details"]["required_capability_ids"]
    assert "knowledge.graph.query" in required


def test_provider_preflight_does_not_execute_retrieval_or_graph(monkeypatch):
    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("preflight must not execute retrieval or graph queries")

    monkeypatch.setattr(
        "app.services.retrieval_backends.FixtureDocumentRetriever.retrieve",
        fail_if_called,
    )
    monkeypatch.setattr("app.routers.graph.query_graph", fail_if_called)

    preflight = build_provider_preflight_response()

    assert preflight.provider_id == "unifiedKnowledgeProvider"
    assert {check.name for check in preflight.checks} == {
        "manifest_identity",
        "health_readiness",
        "required_capabilities",
        "schema_references",
        "graph_boundary",
    }
