from app.services.local_business_rag_golden_cases import (
    ChunkQualityDiagnostics,
    LocalBusinessGoldenCase,
    run_local_business_rag_golden_cases,
    export_local_business_rag_golden_cases,
)


def test_local_business_rag_golden_cases_go_writes_report(tmp_path):
    report = export_local_business_rag_golden_cases(
        source_id="company_profile_2025_trial",
        cases=_cases(),
        output_dir=tmp_path / "golden",
        client=_client(),
    )

    assert report.decision == "go"
    assert report.reason_code == "local_business_rag_baseline_go"
    assert report.summary["case_count"] == 3
    assert report.summary["hit_rate"] == 1.0
    assert report.summary["citation_match_rate"] == 1.0
    assert report.summary["empty_handling_rate"] == 1.0
    assert report.summary["runtime_promotion_status"] == "keep_runtime_defaults"
    assert report.chunk_quality.status == "ready"
    assert report.chunk_quality.total_chunk_count == 3
    assert report.json_path.exists()
    assert report.markdown_path.exists()
    assert "- Decision: `go`" in report.markdown_path.read_text(encoding="utf-8")


def test_local_business_rag_golden_cases_reviews_on_negative_leakage():
    client = _client(
        citation_by_query={
            "公司主营业务是什么？": ["company_profile_2025_trial#chunk-1"],
            "公司有哪些合同金额？": ["company_profile_2025_trial#chunk-2"],
        }
    )

    report = run_local_business_rag_golden_cases(
        source_id="company_profile_2025_trial",
        cases=_cases(),
        client=client,
    )

    assert report.decision == "review"
    assert report.reason_code == "local_business_rag_baseline_needs_review"
    assert report.summary["empty_handling_rate"] < 1.0
    assert "negative_contract_amount" in report.summary["review_case_ids"]


def test_local_business_rag_golden_cases_reviews_on_chunk_quality():
    report = run_local_business_rag_golden_cases(
        source_id="company_profile_2025_trial",
        cases=_cases(),
        client=_client(
            chunk_quality=ChunkQualityDiagnostics(
                status="review",
                reason_code="tiny_chunk_ratio_high",
                provenance_mode="page",
                total_chunk_count=10,
                tiny_chunk_count=8,
                tiny_chunk_ratio=0.8,
                citation_anchor_count=10,
                citation_coverage_ratio=1.0,
                page_coverage_count=1,
                page_ids=["page-1"],
                noisy_chunk_samples=[],
                thresholds={},
            )
        ),
    )

    assert report.decision == "review"
    assert report.summary["chunk_quality_status"] == "review"
    assert "review_tiny_or_noisy_chunks_before_changing_chunk_defaults" in report.recommended_actions


def test_local_business_rag_golden_cases_non_page_markdown_does_not_review_on_page_coverage():
    report = run_local_business_rag_golden_cases(
        source_id="refund_policy_docs",
        cases=[
            LocalBusinessGoldenCase(
                id="refund-rule",
                query="退款规则是什么？",
                expected_mode="answerable",
                expected_source_id="refund_policy_docs",
                expected_citation_prefix="refund_policy_docs#section-",
                business_question_type="policy_lookup",
                description="Refund policy rule should be answerable.",
            )
        ],
        client=_client(
            source_id="refund_policy_docs",
            citation_by_query={"退款规则是什么？": ["refund_policy_docs#section-1"]},
            page_provenance=False,
        ),
    )

    assert report.decision == "go"
    assert report.chunk_quality.status == "ready"
    assert report.chunk_quality.provenance_mode == "non_page"
    assert report.chunk_quality.reason_code == "chunk_quality_ready"
    assert report.review_observations == []


def test_local_business_rag_golden_cases_blocks_when_source_missing():
    report = run_local_business_rag_golden_cases(
        source_id="missing_source",
        cases=_cases(),
        client=_client(registered=False),
    )

    assert report.decision == "blocked"
    assert report.reason_code == "local_business_rag_baseline_blocked"
    assert report.summary["blocked_case_ids"] == ["source_manifest"]
    assert report.chunk_quality.status == "blocked"


def _cases():
    return [
        LocalBusinessGoldenCase(
            id="business_scope",
            query="公司主营业务是什么？",
            expected_mode="answerable",
            expected_source_id="company_profile_2025_trial",
            expected_citation_prefix="company_profile_2025_trial#chunk-",
            business_question_type="business_scope",
            description="Main business scope should be answerable.",
        ),
        LocalBusinessGoldenCase(
            id="negative_contract_amount",
            query="公司有哪些合同金额？",
            expected_mode="insufficient_evidence",
            expected_source_id=None,
            expected_citation_prefix=None,
            business_question_type="negative_control",
            description="Contract amount is not supported.",
        ),
        LocalBusinessGoldenCase(
            id="negative_staff_roster",
            query="公司员工名单有哪些？",
            expected_mode="insufficient_evidence",
            expected_source_id=None,
            expected_citation_prefix=None,
            business_question_type="negative_control",
            description="Staff roster is not supported.",
        ),
    ]


def _client(
    *,
    registered=True,
    source_id="company_profile_2025_trial",
    citation_by_query=None,
    chunk_quality=None,
    page_provenance=True,
):
    citation_by_query = citation_by_query or {
        "公司主营业务是什么？": [f"{source_id}#chunk-1"],
        "公司有哪些合同金额？": [],
        "公司员工名单有哪些？": [],
    }

    class FakeResponse:
        def __init__(self, payload, status_code=200):
            self._payload = payload
            self.status_code = status_code

        def json(self):
            return self._payload

    class FakeClient:
        def get(self, path):
            if path == "/api/rag/sources":
                sources = [{"id": source_id}] if registered else []
                return FakeResponse({"knowledge_bases": sources})
            if path.endswith("/documents"):
                if not registered:
                    return FakeResponse({"ok": False, "result": {"documents": []}})
                if chunk_quality is not None:
                    chunks = [
                        {
                            "chunk_id": f"chunk-{index}",
                            "citation": f"{source_id}#chunk-{index}",
                            "char_count": 5 if index <= chunk_quality.tiny_chunk_count else 80,
                            "text_preview": f"<!-- citation: {source_id}#page-1 --> 样本文本",
                        }
                        for index in range(1, chunk_quality.total_chunk_count + 1)
                    ]
                else:
                    previews = (
                        [
                            f"<!-- citation: {source_id}#page-1 --> 主营业务样本",
                            f"<!-- citation: {source_id}#page-2 --> 资质样本",
                            f"<!-- citation: {source_id}#page-3 --> 组织样本",
                        ]
                        if page_provenance
                        else [
                            "退款规则样本",
                            "退款凭证样本",
                            "退款复核样本",
                        ]
                    )
                    citations = (
                        [f"{source_id}#chunk-1", f"{source_id}#chunk-2", f"{source_id}#chunk-3"]
                        if page_provenance
                        else [f"{source_id}#section-1", f"{source_id}#section-2", f"{source_id}#exact-1"]
                    )
                    chunks = [
                        {
                            "chunk_id": "chunk-1",
                            "citation": citations[0],
                            "char_count": 80,
                            "text_preview": previews[0],
                        },
                        {
                            "chunk_id": "chunk-2",
                            "citation": citations[1],
                            "char_count": 80,
                            "text_preview": previews[1],
                        },
                        {
                            "chunk_id": "chunk-3",
                            "citation": citations[2],
                            "char_count": 80,
                            "text_preview": previews[2],
                        },
                    ]
                return FakeResponse(
                    {
                        "ok": True,
                        "result": {
                            "documents": [
                                {
                                    "citation_anchors": [chunk["citation"] for chunk in chunks],
                                    "chunk_manifest": chunks,
                                }
                            ]
                        },
                    }
                )
            raise AssertionError(path)

        def post(self, path, json):
            query = json["query"]
            citations = citation_by_query.get(query, [])
            documents = [
                {
                    "source_id": source_id,
                    "citation": citation,
                    "score": 1.0,
                }
                for citation in citations
            ]
            if path == "/api/rag/retrieve":
                return FakeResponse({"ok": True, "result": {"documents": documents}})
            if path == "/api/rag/answer":
                return FakeResponse(
                    {
                        "ok": True,
                        "result": {
                            "answer_status": "answered" if citations else "insufficient_evidence",
                            "citations": citations,
                            "documents": documents,
                        },
                    }
                )
            raise AssertionError(path)

    return FakeClient()
