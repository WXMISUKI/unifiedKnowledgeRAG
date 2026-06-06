import json

import httpx

from app.services.local_usable_run_loop import (
    export_local_usable_run_loop_report,
    render_local_usable_run_loop_markdown,
    run_local_usable_run_loop,
)


def test_local_usable_run_loop_returns_go_and_uses_auth_headers():
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=_payload_for(request.url.path))

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url="http://provider.test",
    )

    report = run_local_usable_run_loop(
        "http://provider.test/",
        provider_api_key="secret-token",
        client=client,
    )
    payload = report.__dict__

    assert report.decision == "go"
    assert report.reason_code == "local_provider_usable"
    assert report.base_url == "http://provider.test"
    assert report.summary["retrieve_document_count"] == 1
    assert report.summary["retrieve_evidence_pack_status"] == "answerable"
    assert report.summary["answer_status"] == "answered"
    assert [request.method for request in requests] == [
        "GET",
        "GET",
        "GET",
        "GET",
        "GET",
        "POST",
        "POST",
    ]
    assert [request.url.path for request in requests] == [
        "/live",
        "/ready",
        "/health",
        "/api/provider/manifest",
        "/api/provider/preflight",
        "/api/rag/retrieve",
        "/api/rag/answer",
    ]
    assert "authorization" not in requests[0].headers
    assert "authorization" not in requests[1].headers
    assert "authorization" not in requests[2].headers
    for request in requests[3:]:
        assert request.headers["authorization"] == "Bearer secret-token"
        assert request.headers["x-provider-api-key"] == "secret-token"
    assert "secret-token" not in json.dumps(payload, default=str)


def test_local_usable_run_loop_blocks_when_provider_is_unreachable():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused", request=request)

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url="http://provider.test",
    )

    report = run_local_usable_run_loop("http://provider.test", client=client)
    checks = {check.name: check for check in report.checks}

    assert report.decision == "blocked"
    assert report.reason_code == "local_provider_unreachable"
    assert checks["live_probe"].status == "blocked"
    assert "ConnectError" in checks["live_probe"].error
    assert "start_local_provider_with_uvicorn_app_main_app_reload_port_8020" in (
        report.recommended_actions
    )


def test_local_usable_run_loop_returns_review_for_insufficient_retrieval_evidence():
    def handler(request: httpx.Request) -> httpx.Response:
        payload = _payload_for(request.url.path)
        if request.url.path == "/api/rag/retrieve":
            payload["result"]["documents"] = []
            payload["result"]["metadata"]["evidence_pack"] = {
                "status": "insufficient_evidence",
                "allowed_citations": [],
            }
        if request.url.path == "/api/rag/answer":
            payload["result"]["answer_status"] = "insufficient_evidence"
            payload["result"]["citations"] = []
        return httpx.Response(200, json=payload)

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url="http://provider.test",
    )

    report = run_local_usable_run_loop("http://provider.test", client=client)
    checks = {check.name: check for check in report.checks}

    assert report.decision == "review"
    assert report.reason_code == "retrieval_evidence_needs_review"
    assert checks["rag_retrieve"].status == "review"
    assert checks["rag_answer"].status == "review"
    assert report.summary["retrieve_document_count"] == 0
    assert report.summary["answer_status"] == "insufficient_evidence"


def test_local_usable_run_loop_blocks_when_answer_citation_is_not_allowed():
    def handler(request: httpx.Request) -> httpx.Response:
        payload = _payload_for(request.url.path)
        if request.url.path == "/api/rag/answer":
            payload["result"]["citations"] = ["outside#citation"]
        return httpx.Response(200, json=payload)

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url="http://provider.test",
    )

    report = run_local_usable_run_loop("http://provider.test", client=client)
    checks = {check.name: check for check in report.checks}

    assert report.decision == "blocked"
    assert report.reason_code == "rag_answer_blocked"
    assert checks["rag_answer"].status == "blocked"
    assert checks["rag_answer"].details["invalid_citations"] == ["outside#citation"]
    assert checks["rag_answer"].error == "Answer citations are outside retrieve allowlist."


def test_local_usable_run_loop_export_writes_json_and_markdown_without_secret(
    tmp_path,
):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=_payload_for(request.url.path))

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url="http://provider.test",
    )

    report = export_local_usable_run_loop_report(
        output_dir=tmp_path / "local-run",
        base_url="http://provider.test",
        provider_api_key="secret-token",
        client=client,
    )

    assert report.decision == "go"
    assert report.json_path is not None
    assert report.markdown_path is not None
    json_text = report.json_path.read_text(encoding="utf-8")
    markdown = report.markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_text)
    assert payload["id"] == "local-usable-run-loop-v1"
    assert payload["json_path"] == str(report.json_path)
    assert payload["markdown_path"] == str(report.markdown_path)
    assert "# Local Usable Run Loop" in markdown
    assert "- Decision: `go`" in markdown
    assert "rag_retrieve" in json_text
    assert "rag_answer" in markdown
    assert "secret-token" not in json_text
    assert "secret-token" not in markdown


def test_local_usable_run_loop_markdown_marks_blocked_check():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/rag/answer":
            return httpx.Response(500, json={"error": "boom"})
        return httpx.Response(200, json=_payload_for(request.url.path))

    client = httpx.Client(
        transport=httpx.MockTransport(handler),
        base_url="http://provider.test",
    )
    report = run_local_usable_run_loop("http://provider.test", client=client)

    markdown = render_local_usable_run_loop_markdown(report)

    assert "- Decision: `blocked`" in markdown
    assert "| `rag_answer` | `POST /api/rag/answer` | `blocked` | `500` |" in markdown


def _payload_for(path: str) -> dict:
    if path == "/live":
        return {
            "status": "ok",
            "service": "unifiedKnowledgeProvider",
        }
    if path == "/ready":
        return {
            "status": "ok",
        }
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
    if path == "/api/rag/retrieve":
        return {
            "ok": True,
            "result": {
                "documents": [
                    {
                        "id": "refund-policy-doc",
                        "content": "三天未发货可申请退款。",
                        "citation": "refund_policy_2026#section-3",
                    }
                ],
                "metadata": {
                    "evidence_pack": {
                        "status": "answerable",
                        "allowed_citations": ["refund_policy_2026#section-3"],
                        "evidence_count": 1,
                    }
                },
            },
        }
    if path == "/api/rag/answer":
        return {
            "ok": True,
            "result": {
                "answer_status": "answered",
                "answer": "可以申请退款，需以订单和政策证据为准。",
                "citations": ["refund_policy_2026#section-3"],
                "documents": [],
                "metadata": {},
            },
        }
    raise AssertionError(path)
