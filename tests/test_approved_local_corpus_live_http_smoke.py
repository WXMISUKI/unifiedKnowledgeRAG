import json

import httpx

from app.services.approved_local_corpus_acceptance_smoke import AcceptanceCase
from app.services.approved_local_corpus_live_http_smoke import (
    export_approved_local_corpus_live_http_smoke,
    run_approved_local_corpus_live_http_smoke,
)


SOURCE_ID = "company_profile_2025_trial"
GOOD_CITATION = f"{SOURCE_ID}#chunk-1"


def test_live_http_smoke_go_for_registered_company_source():
    client = _client_for_mode("go")

    report = run_approved_local_corpus_live_http_smoke(client=client)

    assert report.decision == "go"
    assert report.reason_code == "approved_local_corpus_live_http_accepted"
    assert report.transport_mode == "live_http"
    assert report.summary["case_count"] == 5
    assert report.summary["invalid_citation_count"] == 0
    assert all(case.status == "ready" for case in report.cases)


def test_live_http_smoke_blocks_when_provider_unreachable():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused", request=request)

    client = httpx.Client(
        base_url="http://127.0.0.1:8020",
        transport=httpx.MockTransport(handler),
    )

    report = run_approved_local_corpus_live_http_smoke(client=client)

    assert report.decision == "blocked"
    assert report.reason_code == "local_provider_unreachable"
    assert report.cases[0].id == "catalog_visibility"
    assert report.cases[0].reason_code == "catalog_http_error"


def test_live_http_smoke_blocks_invalid_answer_citation():
    client = _client_for_mode("invalid_citation")

    report = run_approved_local_corpus_live_http_smoke(
        client=client,
        cases=[
            AcceptanceCase(
                id="invalid_citation",
                query="公司主营业务是什么？",
                expected_mode="answerable",
                description="Answer returns a citation outside retrieved evidence.",
            )
        ],
    )

    assert report.decision == "blocked"
    assert report.reason_code == "answer_citation_outside_retrieval_allowlist"
    assert report.cases[0].status == "blocked"
    assert report.cases[0].invalid_citations == [f"{SOURCE_ID}#bad"]


def test_live_http_smoke_reviews_when_answerable_case_has_no_evidence():
    client = _client_for_mode("no_evidence")

    report = run_approved_local_corpus_live_http_smoke(
        client=client,
        cases=[
            AcceptanceCase(
                id="weak_case",
                query="完全不存在的专有术语 ABCXYZ",
                expected_mode="answerable",
                description="Expected answerable case with no matching evidence.",
            )
        ],
    )

    assert report.decision == "review"
    assert report.reason_code == "live_http_acceptance_needs_review"
    assert report.cases[0].status == "review"
    assert report.cases[0].reason_code == "expected_answerable_evidence_missing"


def test_live_http_smoke_does_not_write_provider_api_key(tmp_path):
    requests: list[httpx.Request] = []
    secret = "secret-live-http-key"

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return _response_for(request, mode="go")

    client = httpx.Client(
        base_url="http://127.0.0.1:8020",
        transport=httpx.MockTransport(handler),
    )

    report = export_approved_local_corpus_live_http_smoke(
        client=client,
        output_dir=tmp_path / "live-http",
        provider_api_key=secret,
    )

    assert report.decision == "go"
    assert report.api_key_supplied is True
    assert any(request.headers.get("authorization") == f"Bearer {secret}" for request in requests)
    assert secret not in json.dumps(
        report.summary,
        ensure_ascii=False,
        sort_keys=True,
    )
    assert secret not in report.json_path.read_text(encoding="utf-8")
    assert secret not in report.markdown_path.read_text(encoding="utf-8")


def _client_for_mode(mode: str) -> httpx.Client:
    return httpx.Client(
        base_url="http://127.0.0.1:8020",
        transport=httpx.MockTransport(lambda request: _response_for(request, mode=mode)),
    )


def _response_for(request: httpx.Request, *, mode: str) -> httpx.Response:
    if request.url.path == "/api/rag/sources":
        return httpx.Response(
            200,
            json={
                "knowledge_bases": [
                    {
                        "id": SOURCE_ID,
                        "status": "ready",
                    }
                ],
                "graphs": [],
            },
        )
    if request.url.path == f"/api/rag/sources/{SOURCE_ID}/documents":
        return httpx.Response(
            200,
            json={
                "ok": True,
                "result": {
                    "documents": [
                        {
                            "document_id": SOURCE_ID,
                            "title": "公司简介 2025 trial",
                        }
                    ]
                },
            },
        )
    if request.url.path == "/api/rag/retrieve":
        query = _request_query(request)
        if mode == "no_evidence" or query == "售后退款凭证规则":
            return httpx.Response(
                200,
                json={"ok": True, "result": {"documents": []}},
            )
        return httpx.Response(
            200,
            json={
                "ok": True,
                "result": {
                    "documents": [
                        {
                            "source_id": SOURCE_ID,
                            "citation": GOOD_CITATION,
                        }
                    ]
                },
            },
        )
    if request.url.path == "/api/rag/answer":
        query = _request_query(request)
        if mode == "no_evidence" or query == "售后退款凭证规则":
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {
                        "answer_status": "insufficient_evidence",
                        "citations": [],
                    },
                },
            )
        citation = f"{SOURCE_ID}#bad" if mode == "invalid_citation" else GOOD_CITATION
        return httpx.Response(
            200,
            json={
                "ok": True,
                "result": {
                    "answer_status": "answered",
                    "citations": [citation],
                },
            },
        )
    return httpx.Response(404, json={"error": "not found"})


def _request_query(request: httpx.Request) -> str:
    payload = json.loads(request.content.decode("utf-8"))
    return str(payload.get("query"))
