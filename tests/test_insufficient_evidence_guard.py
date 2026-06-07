from fastapi.testclient import TestClient

from app.main import create_app
from app.models.contracts import EvidenceDocument
from app.services.insufficient_evidence_guard import apply_insufficient_evidence_guard


def test_guard_clears_parser_derived_contract_amount_without_support():
    result = apply_insufficient_evidence_guard(
        query="公司有哪些合同金额？",
        requested_source_ids=["company_profile_2025_trial"],
        documents=[
            _document(
                citation="company_profile_2025_trial#chunk-3",
                snippet="公司主要经营高等级公路、大型桥梁和隧道工程及水运工程的施工监理、技术咨询。",
            )
        ],
    )

    assert result.documents == []
    assert result.metadata == {
        "version": "insufficient-evidence-guard-v1",
        "rule_id": "contract_amount",
        "decision": "insufficient_evidence",
        "candidate_count_before": 1,
        "candidate_count_after": 0,
        "scope": "parser_derived_local_corpus",
    }


def test_guard_preserves_answerable_company_profile_query():
    document = _document(
        citation="company_profile_2025_trial#chunk-3",
        snippet="公司主要经营高等级公路、大型桥梁和隧道工程及水运工程的施工监理、技术咨询。",
    )

    result = apply_insufficient_evidence_guard(
        query="公司主营业务是什么？",
        requested_source_ids=["company_profile_2025_trial"],
        documents=[document],
    )

    assert result.documents == [document]
    assert result.metadata is None


def test_company_profile_negative_controls_return_insufficient_evidence():
    client = TestClient(create_app())

    for query in ["公司有哪些合同金额？", "公司员工名单有哪些？"]:
        retrieve_response = client.post(
            "/api/rag/retrieve",
            json={
                "query": query,
                "knowledge_base_ids": ["company_profile_2025_trial"],
                "top_k": 3,
            },
        )
        answer_response = client.post(
            "/api/rag/answer",
            json={
                "query": query,
                "knowledge_base_ids": ["company_profile_2025_trial"],
                "top_k": 3,
            },
        )

        assert retrieve_response.status_code == 200
        retrieve = retrieve_response.json()
        assert retrieve["ok"] is True
        assert retrieve["result"]["documents"] == []
        retrieve_pack = retrieve["result"]["metadata"]["evidence_pack"]
        assert retrieve_pack["status"] == "insufficient_evidence"
        assert retrieve_pack["allowed_citations"] == []
        assert retrieve["result"]["metadata"]["request_filter_context"][
            "insufficient_evidence_guard"
        ]["decision"] == "insufficient_evidence"

        assert answer_response.status_code == 200
        answer = answer_response.json()
        assert answer["ok"] is True
        assert answer["result"]["answer_status"] == "insufficient_evidence"
        assert answer["result"]["citations"] == []
        assert answer["result"]["documents"] == []


def test_company_profile_answerable_cases_still_return_evidence():
    client = TestClient(create_app())
    response = client.post(
        "/api/rag/retrieve",
        json={
            "query": "公司主营业务是什么？",
            "knowledge_base_ids": ["company_profile_2025_trial"],
            "top_k": 3,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["result"]["documents"]
    assert all(
        document["source_id"] == "company_profile_2025_trial"
        for document in body["result"]["documents"]
    )
    assert "insufficient_evidence_guard" not in body["result"]["metadata"]["request_filter_context"]


def _document(*, citation: str, snippet: str) -> EvidenceDocument:
    return EvidenceDocument(
        source_id="company_profile_2025_trial",
        document_id="company_profile_2025_trial",
        title="公司简介 2025 trial",
        snippet=snippet,
        score=1.0,
        citation=citation,
        metadata={
            "source_path": "app/data/sources/company_profile_2025_trial.md",
            "chunk_id": citation.split("#", maxsplit=1)[-1],
        },
    )
