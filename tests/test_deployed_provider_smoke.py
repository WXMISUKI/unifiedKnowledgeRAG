import json

import httpx

from app.services.deployed_provider_smoke import (
    export_deployed_provider_smoke_report,
    render_deployed_provider_smoke_markdown,
    run_deployed_provider_smoke,
)


def test_deployed_provider_smoke_passes_reviewable_handoff_and_auth_headers():
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=_payload_for(request.url.path))

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url="http://provider.test",
    )

    report = run_deployed_provider_smoke(
        "http://provider.test/",
        provider_api_key="secret-token",
        client=client,
    )
    payload = report.__dict__

    assert report.status == "review"
    assert report.base_url == "http://provider.test"
    assert report.provider["provider_id"] == "unifiedKnowledgeProvider"
    assert report.provider["contract_version"] == "knowledge-provider-contract-v1"
    assert report.handoff["status"] == "review"
    assert [request.method for request in requests] == [
        "GET",
        "GET",
        "GET",
        "GET",
        "GET",
    ]
    assert [request.url.path for request in requests] == [
        "/health",
        "/api/provider/manifest",
        "/api/provider/preflight",
        "/api/provider/source-bindings",
        "/api/provider/handoff",
    ]
    assert "authorization" not in requests[0].headers
    for request in requests[1:]:
        assert request.headers["authorization"] == "Bearer secret-token"
        assert request.headers["x-provider-api-key"] == "secret-token"
    assert "secret-token" not in json.dumps(payload, default=str)


def test_deployed_provider_smoke_is_ready_when_handoff_is_ready():
    def handler(request: httpx.Request) -> httpx.Response:
        payload = _payload_for(request.url.path)
        if request.url.path == "/api/provider/handoff":
            payload["status"] = "ready"
        return httpx.Response(200, json=payload)

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url="http://provider.test",
    )

    report = run_deployed_provider_smoke("http://provider.test", client=client)

    assert report.status == "ready"
    assert {check.status for check in report.checks} == {"ready"}
    checks = {check.name: check for check in report.checks}
    assert checks["provider_source_bindings"].details == {
        "id": "provider-source-binding-summary-v1",
        "status": "ready",
        "source_count": 2,
        "bindable_source_count": 2,
    }


def test_deployed_provider_smoke_fails_closed_on_unreachable_endpoint():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/provider/preflight":
            raise httpx.ConnectError("connection refused", request=request)
        return httpx.Response(200, json=_payload_for(request.url.path))

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url="http://provider.test",
    )

    report = run_deployed_provider_smoke("http://provider.test", client=client)
    checks = {check.name: check for check in report.checks}

    assert report.status == "blocked"
    assert checks["provider_preflight"].passed is False
    assert checks["provider_preflight"].status == "blocked"
    assert "ConnectError" in checks["provider_preflight"].error


def test_deployed_provider_smoke_fails_closed_on_incompatible_manifest():
    def handler(request: httpx.Request) -> httpx.Response:
        payload = _payload_for(request.url.path)
        if request.url.path == "/api/provider/manifest":
            payload["contract_version"] = "knowledge-provider-contract-v2"
        return httpx.Response(200, json=payload)

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url="http://provider.test",
    )

    report = run_deployed_provider_smoke("http://provider.test", client=client)
    checks = {check.name: check for check in report.checks}

    assert report.status == "blocked"
    assert checks["provider_manifest"].status == "blocked"
    assert checks["provider_manifest"].error == (
        "Manifest identity or contract is incompatible."
    )


def test_deployed_provider_smoke_fails_closed_on_blocked_source_bindings():
    def handler(request: httpx.Request) -> httpx.Response:
        payload = _payload_for(request.url.path)
        if request.url.path == "/api/provider/source-bindings":
            payload["status"] = "blocked"
            payload["sources"][0]["bindable"] = False
        return httpx.Response(200, json=payload)

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url="http://provider.test",
    )

    report = run_deployed_provider_smoke("http://provider.test", client=client)
    checks = {check.name: check for check in report.checks}

    assert report.status == "blocked"
    assert checks["provider_source_bindings"].status == "blocked"
    assert checks["provider_source_bindings"].passed is False
    assert checks["provider_source_bindings"].details["source_count"] == 2
    assert checks["provider_source_bindings"].details["bindable_source_count"] == 1
    assert checks["provider_source_bindings"].error == (
        "Provider source binding evidence is blocked or invalid."
    )


def test_deployed_provider_smoke_export_writes_json_and_markdown_without_secret(
    tmp_path,
):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=_payload_for(request.url.path))

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url="http://provider.test",
    )

    report = export_deployed_provider_smoke_report(
        output_dir=tmp_path / "smoke",
        base_url="http://provider.test",
        provider_api_key="secret-token",
        client=client,
    )

    assert report.status == "review"
    assert report.json_path is not None
    assert report.markdown_path is not None
    json_text = report.json_path.read_text(encoding="utf-8")
    markdown = report.markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_text)
    assert payload["id"] == "deployed-provider-smoke-v1"
    assert payload["json_path"] == str(report.json_path)
    assert payload["markdown_path"] == str(report.markdown_path)
    assert "# Deployed Provider Smoke Report" in markdown
    assert "- Status: `review`" in markdown
    assert "provider_source_bindings" in json_text
    assert "provider_source_bindings" in markdown
    assert "secret-token" not in json_text
    assert "secret-token" not in markdown


def test_deployed_provider_smoke_markdown_marks_blocked_check():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/provider/handoff":
            return httpx.Response(500, json={"error": "boom"})
        return httpx.Response(200, json=_payload_for(request.url.path))

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url="http://provider.test",
    )
    report = run_deployed_provider_smoke("http://provider.test", client=client)

    markdown = render_deployed_provider_smoke_markdown(report)

    assert "- Status: `blocked`" in markdown
    assert "| `provider_handoff` | `GET /api/provider/handoff` | `blocked` | `500` |" in markdown


def _payload_for(path: str) -> dict:
    if path == "/health":
        return {
            "status": "ok",
            "service": "unifiedKnowledgeProvider",
            "rag": {"status": "ready"},
            "answer": {"status": "ready"},
            "graph": {"status": "planned"},
        }
    if path == "/api/provider/manifest":
        return {
            "provider_id": "unifiedKnowledgeProvider",
            "provider_name": "unifiedKnowledgeRAG",
            "provider_version": "0.1.0",
            "contract_version": "knowledge-provider-contract-v1",
            "manifest_version": "provider-integration-manifest-v1",
            "component_role": "knowledge_data_plane",
        }
    if path == "/api/provider/preflight":
        return {
            "provider_id": "unifiedKnowledgeProvider",
            "contract_version": "knowledge-provider-contract-v1",
            "bindable": True,
            "checks": [{"name": "manifest_identity", "passed": True}],
        }
    if path == "/api/provider/source-bindings":
        return {
            "id": "provider-source-binding-summary-v1",
            "status": "ready",
            "provider": {"provider_id": "unifiedKnowledgeProvider"},
            "sources": [
                {"source_id": "refund_policy_docs", "bindable": True},
                {"source_id": "logistics_faq", "bindable": True},
            ],
        }
    if path == "/api/provider/handoff":
        return {
            "id": "provider-handoff-bundle-v1",
            "status": "review",
            "provider": {"provider_id": "unifiedKnowledgeProvider"},
            "evidence_artifacts": [{"id": "deployment_readiness", "status": "review"}],
        }
    raise AssertionError(path)
