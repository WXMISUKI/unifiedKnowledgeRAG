from app.services.local_business_rag_golden_cases import (
    RealBusinessGoldenCase,
    export_real_business_corpus_golden_cases,
    run_real_business_corpus_golden_cases,
)


def test_real_business_corpus_golden_cases_go_writes_aggregate_report(tmp_path):
    report = export_real_business_corpus_golden_cases(
        cases=_aggregate_cases(),
        output_dir=tmp_path / "aggregate",
        client=_client(),
    )

    assert report.decision == "go"
    assert report.reason_code == "real_business_corpus_baseline_go"
    assert report.summary["source_count"] == 2
    assert report.summary["case_count"] == 4
    assert report.summary["hit_rate"] == 1.0
    assert report.summary["citation_match_rate"] == 1.0
    assert report.summary["empty_handling_rate"] == 1.0
    assert report.failure_mode_summary["citation_or_evidence"] == 2
    assert report.risk_level_summary["high"] == 2
    assert report.json_path.exists()
    assert report.markdown_path.exists()
    assert "- Decision: `go`" in report.markdown_path.read_text(encoding="utf-8")


def test_real_business_corpus_golden_cases_reviews_on_source_case_failure():
    client = _client(
        citation_by_query={
            "公司主营业务是什么？": ["company_profile_2025_trial#chunk-1"],
            "公司有哪些合同金额？": ["company_profile_2025_trial#chunk-2"],
            "退款规则是什么？": ["refund_policy_docs#chunk-1"],
            "退款文档中的员工名单有哪些？": [],
        }
    )

    report = run_real_business_corpus_golden_cases(
        cases=_aggregate_cases(),
        client=client,
    )

    assert report.decision == "review"
    assert report.reason_code == "real_business_corpus_baseline_needs_review"
    assert "company_profile_2025_trial" in report.summary["review_sources"]
    assert report.summary["empty_handling_rate"] < 1.0


def test_real_business_corpus_golden_cases_blocks_on_missing_source():
    report = run_real_business_corpus_golden_cases(
        cases=_aggregate_cases(),
        client=_client(registered_sources={"company_profile_2025_trial"}),
    )

    assert report.decision == "blocked"
    assert report.reason_code == "real_business_corpus_baseline_blocked"
    assert "refund_policy_docs" in report.summary["blocked_sources"]


def _aggregate_cases():
    return [
        RealBusinessGoldenCase(
            id="company-business-scope",
            source_id="company_profile_2025_trial",
            query="公司主营业务是什么？",
            expected_mode="answerable",
            expected_citation_prefix="company_profile_2025_trial#chunk-",
            business_question_type="business_scope",
            failure_mode="unclassified",
            risk_level="medium",
            description="Company profile answerable case.",
        ),
        RealBusinessGoldenCase(
            id="company-negative-contract",
            source_id="company_profile_2025_trial",
            query="公司有哪些合同金额？",
            expected_mode="insufficient_evidence",
            expected_citation_prefix=None,
            business_question_type="negative_control",
            failure_mode="citation_or_evidence",
            risk_level="high",
            description="Company profile negative control.",
        ),
        RealBusinessGoldenCase(
            id="refund-rule",
            source_id="refund_policy_docs",
            query="退款规则是什么？",
            expected_mode="answerable",
            expected_citation_prefix="refund_policy_docs#chunk-",
            business_question_type="policy_lookup",
            failure_mode="unclassified",
            risk_level="medium",
            description="Refund policy answerable case.",
        ),
        RealBusinessGoldenCase(
            id="refund-negative-staff",
            source_id="refund_policy_docs",
            query="退款文档中的员工名单有哪些？",
            expected_mode="insufficient_evidence",
            expected_citation_prefix=None,
            business_question_type="negative_control",
            failure_mode="citation_or_evidence",
            risk_level="high",
            description="Refund policy negative control.",
        ),
    ]


def _client(*, registered_sources=None, citation_by_query=None):
    registered_sources = registered_sources or {
        "company_profile_2025_trial",
        "refund_policy_docs",
    }
    citation_by_query = citation_by_query or {
        "公司主营业务是什么？": ["company_profile_2025_trial#chunk-1"],
        "公司有哪些合同金额？": [],
        "退款规则是什么？": ["refund_policy_docs#chunk-1"],
        "退款文档中的员工名单有哪些？": [],
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
                return FakeResponse(
                    {"knowledge_bases": [{"id": source_id} for source_id in registered_sources]}
                )
            if path.endswith("/documents"):
                source_id = path.split("/")[-2]
                if source_id not in registered_sources:
                    return FakeResponse({"ok": False, "result": {"documents": []}})
                return FakeResponse(
                    {
                        "ok": True,
                        "result": {
                            "documents": [
                                {
                                    "citation_anchors": [
                                        f"{source_id}#chunk-1",
                                        f"{source_id}#chunk-2",
                                    ],
                                    "chunk_manifest": [
                                        {
                                            "chunk_id": "chunk-1",
                                            "citation": f"{source_id}#chunk-1",
                                            "char_count": 80,
                                            "text_preview": f"<!-- citation: {source_id}#page-1 --> 样本文本",
                                        },
                                        {
                                            "chunk_id": "chunk-2",
                                            "citation": f"{source_id}#chunk-2",
                                            "char_count": 80,
                                            "text_preview": f"<!-- citation: {source_id}#page-2 --> 样本文本",
                                        },
                                    ],
                                }
                            ]
                        },
                    }
                )
            raise AssertionError(path)

        def post(self, path, json):
            source_id = json["knowledge_base_ids"][0]
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
