from fastapi.testclient import TestClient

from app.main import create_app
from app.services.provider_integration_client import probe_provider_binding


def test_provider_integration_probe_passes_default_provider():
    report = probe_provider_binding(TestClient(create_app()))
    payload = report.to_dict()

    assert payload["bindable"] is True
    assert payload["provider_id"] == "unifiedKnowledgeProvider"
    assert payload["provider_name"] == "unifiedKnowledgeRAG"
    assert payload["contract_version"] == "knowledge-provider-contract-v1"
    assert payload["manifest_version"] == "provider-integration-manifest-v1"
    assert payload["requested_contract_version"] == "knowledge-provider-contract-v1"
    assert payload["requested_capability_ids"] == [
        "knowledge.rag.retrieve",
        "knowledge.rag.answer",
        "knowledge.graph.query",
    ]
    assert payload["errors"] == []
    bindings = {binding["id"]: binding for binding in payload["capability_bindings"]}
    assert bindings["knowledge.rag.retrieve"]["status"] == "ready"
    assert bindings["knowledge.rag.retrieve"]["invocation"]["path"] == (
        "/api/rag/retrieve"
    )
    assert bindings["knowledge.rag.retrieve"]["has_example_request"] is True
    assert bindings["knowledge.rag.answer"]["has_example_request"] is True
    assert bindings["knowledge.graph.query"]["status"] == "planned"
    assert bindings["knowledge.graph.query"]["has_example_request"] is True
    assert {check["name"] for check in payload["checks"]} == {
        "manifest_identity",
        "contract_version",
        "health_readiness",
        "required_capabilities",
        "schema_references",
        "graph_boundary",
    }


def test_provider_integration_probe_fails_closed_on_incompatible_requirements():
    report = probe_provider_binding(
        TestClient(create_app()),
        required_contract_version="knowledge-provider-contract-v2",
        required_capability_ids=[
            "knowledge.rag.retrieve",
            "knowledge.graph.traverse",
        ],
    )
    payload = report.to_dict()

    assert payload["bindable"] is False
    assert payload["requested_contract_version"] == "knowledge-provider-contract-v2"
    assert payload["requested_capability_ids"] == [
        "knowledge.rag.retrieve",
        "knowledge.graph.traverse",
    ]
    checks = {check["name"]: check for check in payload["checks"]}
    assert checks["contract_version"]["passed"] is False
    assert checks["required_capabilities"]["passed"] is False
    assert checks["required_capabilities"]["details"]["missing_capability_ids"] == [
        "knowledge.graph.traverse"
    ]
    assert payload["errors"] == [
        {
            "code": "MISSING_CAPABILITY",
            "message": "Required capabilities are missing from discovery.",
            "details": {"capability_ids": ["knowledge.graph.traverse"]},
        }
    ]


def test_provider_integration_probe_is_read_only(monkeypatch):
    def fail_retrieve(*args, **kwargs):
        raise AssertionError("integration probe must not execute retrieval")

    monkeypatch.setattr("app.routers.rag.retrieve_documents", fail_retrieve)
    monkeypatch.setattr("app.routers.rag.answer_documents", fail_retrieve)
    monkeypatch.setattr("app.routers.graph.query_graph", fail_retrieve)
    monkeypatch.setattr("app.routers.ingestion.create_job", fail_retrieve)
    client = TestClient(create_app())

    report = probe_provider_binding(client)

    assert report.bindable is True


def test_provider_integration_probe_reports_missing_examples():
    class Response:
        def __init__(self, payload):
            self.status_code = 200
            self._payload = payload

        def json(self):
            return self._payload

    class Client:
        def get(self, path, *, params=None):
            if path == "/api/provider/manifest":
                return Response(
                    {
                        "provider_id": "unifiedKnowledgeProvider",
                        "provider_name": "unifiedKnowledgeRAG",
                        "contract_version": "knowledge-provider-contract-v1",
                        "manifest_version": "provider-integration-manifest-v1",
                    }
                )
            if path == "/api/provider/preflight":
                return Response({"bindable": True, "checks": []})
            if path == "/api/capabilities":
                return Response(
                    {
                        "capabilities": [
                            {
                                "id": "knowledge.rag.retrieve",
                                "status": "ready",
                                "reason": None,
                                "invocation": {
                                    "method": "POST",
                                    "path": "/api/rag/retrieve",
                                    "request_schema_ref": (
                                        "#/components/schemas/RagRetrieveRequest"
                                    ),
                                    "response_schema_ref": (
                                        "#/components/schemas/RagRetrieveResponse"
                                    ),
                                },
                            }
                        ]
                    }
                )
            raise AssertionError(path)

    report = probe_provider_binding(
        Client(),
        required_capability_ids=["knowledge.rag.retrieve"],
    )

    assert report.bindable is False
    assert report.errors == [
        {
            "code": "MISSING_INVOCATION_EXAMPLE",
            "message": "Required capability invocation examples are missing.",
            "details": {"capability_ids": ["knowledge.rag.retrieve"]},
        }
    ]
