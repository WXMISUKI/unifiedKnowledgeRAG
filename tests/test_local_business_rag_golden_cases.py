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


def _client(*, registered=True, citation_by_query=None, chunk_quality=None):
    citation_by_query = citation_by_query or {
        "公司主营业务是什么？": ["company_profile_2025_trial#chunk-1"],
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
                sources = [{"id": "company_profile_2025_trial"}] if registered else []
                return FakeResponse({"knowledge_bases": sources})
            if path.endswith("/documents"):
                if not registered:
                    return FakeResponse({"ok": False, "result": {"documents": []}})
                if chunk_quality is not None:
                    chunks = [
                        {
                            "chunk_id": f"chunk-{index}",
                            "citation": f"company_profile_2025_trial#chunk-{index}",
                            "char_count": 5 if index <= chunk_quality.tiny_chunk_count else 80,
                            "text_preview": "<!-- citation: company_profile_2025_trial#page-1 --> 样本文本",
                        }
                        for index in range(1, chunk_quality.total_chunk_count + 1)
                    ]
                else:
                    chunks = [
                        {
                            "chunk_id": "chunk-1",
                            "citation": "company_profile_2025_trial#chunk-1",
                            "char_count": 80,
                            "text_preview": "<!-- citation: company_profile_2025_trial#page-1 --> 主营业务样本",
                        },
                        {
                            "chunk_id": "chunk-2",
                            "citation": "company_profile_2025_trial#chunk-2",
                            "char_count": 80,
                            "text_preview": "<!-- citation: company_profile_2025_trial#page-2 --> 资质样本",
                        },
                        {
                            "chunk_id": "chunk-3",
                            "citation": "company_profile_2025_trial#chunk-3",
                            "char_count": 80,
                            "text_preview": "<!-- citation: company_profile_2025_trial#page-3 --> 组织样本",
                        },
                    ]
                return FakeResponse(
                    {
                        "ok": True,
                        "result": {
                            "documents": [
                                {
                                    "citation_anchors": [
                                        "company_profile_2025_trial#chunk-1",
                                        "company_profile_2025_trial#chunk-2",
                                        "company_profile_2025_trial#chunk-3",
                                    ],
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
                    "source_id": "company_profile_2025_trial",
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
