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
    assert body["requested_contract_version"] == "knowledge-provider-contract-v1"
    assert body["requested_capability_ids"] == [
        "knowledge.rag.source_documents",
        "knowledge.rag.retrieve",
        "knowledge.rag.answer",
        "knowledge.provider.source_bindings",
        "knowledge.graph.query",
    ]
    assert body["control_plane_hint"] == "MyPrivateAgent"
    assert body["bindable"] is True
    checks = {check["name"]: check for check in body["checks"]}
    assert checks["manifest_identity"]["passed"] is True
    assert checks["contract_version"]["passed"] is True
    assert checks["health_readiness"]["passed"] is True
    assert checks["required_capabilities"]["passed"] is True
    assert checks["schema_references"]["passed"] is True


def test_provider_preflight_accepts_matching_required_contract_version():
    client = TestClient(create_app())

    response = client.get(
        "/api/provider/preflight",
        params={"required_contract_version": "knowledge-provider-contract-v1"},
    )

    assert response.status_code == 200
    body = response.json()
    checks = {check["name"]: check for check in body["checks"]}
    assert body["bindable"] is True
    assert body["requested_contract_version"] == "knowledge-provider-contract-v1"
    assert checks["contract_version"] == {
        "name": "contract_version",
        "passed": True,
        "status": "ready",
        "details": {
            "required_contract_version": "knowledge-provider-contract-v1",
            "provider_contract_version": "knowledge-provider-contract-v1",
        },
        "reason": None,
    }


def test_provider_preflight_fails_closed_on_contract_version_mismatch():
    client = TestClient(create_app())

    response = client.get(
        "/api/provider/preflight",
        params={"required_contract_version": "knowledge-provider-contract-v2"},
    )

    assert response.status_code == 200
    body = response.json()
    checks = {check["name"]: check for check in body["checks"]}
    assert body["bindable"] is False
    assert body["requested_contract_version"] == "knowledge-provider-contract-v2"
    assert checks["contract_version"]["passed"] is False
    assert checks["contract_version"]["status"] == "failed"
    assert checks["contract_version"]["details"] == {
        "required_contract_version": "knowledge-provider-contract-v2",
        "provider_contract_version": "knowledge-provider-contract-v1",
    }


def test_provider_preflight_accepts_matching_required_capability_ids():
    client = TestClient(create_app())

    response = client.get(
        "/api/provider/preflight",
        params=[
            ("required_capability_ids", "knowledge.rag.retrieve"),
            ("required_capability_ids", "knowledge.rag.answer"),
        ],
    )

    assert response.status_code == 200
    body = response.json()
    checks = {check["name"]: check for check in body["checks"]}
    assert body["bindable"] is True
    assert body["requested_capability_ids"] == [
        "knowledge.rag.retrieve",
        "knowledge.rag.answer",
    ]
    assert checks["required_capabilities"]["details"]["required_capability_ids"] == [
        "knowledge.rag.retrieve",
        "knowledge.rag.answer",
    ]
    assert checks["required_capabilities"]["details"]["missing_capability_ids"] == []
    assert checks["schema_references"]["details"]["checked_capability_ids"] == [
        "knowledge.rag.retrieve",
        "knowledge.rag.answer",
    ]


def test_provider_preflight_accepts_get_diagnostic_capability_without_request_schema():
    client = TestClient(create_app())

    response = client.get(
        "/api/provider/preflight",
        params=[
            ("required_capability_ids", "knowledge.rag.source_documents"),
        ],
    )

    assert response.status_code == 200
    body = response.json()
    checks = {check["name"]: check for check in body["checks"]}
    assert body["bindable"] is True
    assert checks["schema_references"]["passed"] is True
    assert checks["schema_references"]["details"]["checked_capability_ids"] == [
        "knowledge.rag.source_documents"
    ]
    assert checks["schema_references"]["details"][
        "missing_schema_ref_capability_ids"
    ] == []


def test_provider_preflight_accepts_source_binding_capability():
    client = TestClient(create_app())

    response = client.get(
        "/api/provider/preflight",
        params=[
            ("required_capability_ids", "knowledge.provider.source_bindings"),
        ],
    )

    assert response.status_code == 200
    body = response.json()
    checks = {check["name"]: check for check in body["checks"]}
    assert body["bindable"] is True
    assert body["requested_capability_ids"] == [
        "knowledge.provider.source_bindings"
    ]
    assert checks["required_capabilities"]["passed"] is True
    assert checks["schema_references"]["passed"] is True
    assert checks["schema_references"]["details"]["checked_capability_ids"] == [
        "knowledge.provider.source_bindings"
    ]


def test_provider_preflight_fails_closed_on_missing_required_capability():
    client = TestClient(create_app())

    response = client.get(
        "/api/provider/preflight",
        params=[
            ("required_capability_ids", "knowledge.rag.retrieve"),
            ("required_capability_ids", "knowledge.rag.rerank"),
        ],
    )

    assert response.status_code == 200
    body = response.json()
    checks = {check["name"]: check for check in body["checks"]}
    assert body["bindable"] is False
    assert checks["required_capabilities"]["passed"] is False
    assert checks["required_capabilities"]["details"]["missing_capability_ids"] == [
        "knowledge.rag.rerank"
    ]
    assert checks["schema_references"]["passed"] is True
    assert checks["schema_references"]["details"]["checked_capability_ids"] == [
        "knowledge.rag.retrieve"
    ]


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
        "graph_schema_count": 1,
        "graph_ids": ["ecommerce_order_graph"],
        "graph_statuses": {"ecommerce_order_graph": "planned"},
        "graph_stores": {"ecommerce_order_graph": "neo4j_planned"},
        "boundary_note": (
            "Graph schemas are discoverable, but graph query execution "
            "remains planned until a separate GraphRAG change is approved."
        ),
    }
    required = checks["required_capabilities"]["details"]["required_capability_ids"]
    assert "knowledge.rag.source_documents" in required
    assert "knowledge.provider.source_bindings" in required
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
        "contract_version",
        "health_readiness",
        "required_capabilities",
        "schema_references",
        "graph_boundary",
    }
