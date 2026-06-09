from app.services.local_business_rag_golden_cases import (
    DEFAULT_FAILED_QUESTION_PACK_CASE_FILE,
    RealBusinessGoldenCase,
    export_real_failed_question_pack_golden_cases,
    run_real_business_corpus_golden_cases,
)


def test_real_failed_question_pack_writes_review_report(tmp_path):
    report = export_real_failed_question_pack_golden_cases(
        cases=_failed_pack_cases(),
        output_dir=tmp_path / "failed-pack",
        client=_client(),
    )

    assert report.decision == "review"
    assert report.reason_code == "real_business_corpus_baseline_needs_review"
    assert report.summary["source_count"] == 3
    assert report.summary["case_count"] == 6
    assert report.summary["empty_handling_rate"] < 1.0
    assert report.question_origin_summary["accepted_real_failure_candidate"] == 2
    assert report.case_file == DEFAULT_FAILED_QUESTION_PACK_CASE_FILE
    assert report.json_path.exists()
    assert report.markdown_path.exists()
    assert "# Real Failed Question Pack Baseline" in report.markdown_path.read_text(
        encoding="utf-8"
    )


def test_real_failed_question_pack_classifies_query_mismatch_review():
    report = run_real_business_corpus_golden_cases(
        cases=_failed_pack_cases(),
        client=_client(),
    )

    assert report.decision == "review"
    assert report.failure_mode_summary["query_mismatch"] == 2
    assert "refund_policy_docs" in report.summary["review_sources"]
    refund_source = next(
        source for source in report.source_reports if source.source_id == "refund_policy_docs"
    )
    assert "refund-company-department-negative" in refund_source.summary["review_case_ids"]


def _failed_pack_cases():
    return [
        RealBusinessGoldenCase(
            id="company-profile-alias-qualification",
            source_id="company_profile_2025_trial",
            query="江苏交工咨询有哪些资质？",
            expected_mode="answerable",
            expected_citation_prefix="company_profile_2025_trial#chunk-",
            business_question_type="alias_lookup",
            failure_mode="query_mismatch",
            risk_level="medium",
            description="Alias qualification case.",
            question_origin="real_boundary_question",
            observed_failure="alias_wording_may_reduce_recall",
            notes="Harder alias phrasing.",
        ),
        RealBusinessGoldenCase(
            id="company-profile-after-sales-policy-negative",
            source_id="company_profile_2025_trial",
            query="公司有哪些售后政策？",
            expected_mode="insufficient_evidence",
            expected_citation_prefix=None,
            business_question_type="cross_domain_negative_control",
            failure_mode="citation_or_evidence",
            risk_level="high",
            description="Cross-domain company negative control.",
            question_origin="real_cross_domain_trap",
            observed_failure="cross_domain_policy_question_should_fail_closed",
            notes="Should remain fail-closed.",
        ),
        RealBusinessGoldenCase(
            id="refund-high-value-review-role",
            source_id="refund_policy_docs",
            query="高价值订单退款超过五千元时需要谁复核？",
            expected_mode="answerable",
            expected_citation_prefix="refund_policy_docs#chunk-",
            business_question_type="role_lookup",
            failure_mode="unclassified",
            risk_level="medium",
            description="Refund high-value role lookup.",
            question_origin="accepted_real_failure_candidate",
            observed_failure="none_currently",
            notes="Harder refund question.",
        ),
        RealBusinessGoldenCase(
            id="refund-company-department-negative",
            source_id="refund_policy_docs",
            query="退款政策中有哪些公司部门？",
            expected_mode="insufficient_evidence",
            expected_citation_prefix=None,
            business_question_type="organization_negative_control",
            failure_mode="query_mismatch",
            risk_level="high",
            description="Refund unsupported organization question.",
            question_origin="accepted_real_failure_candidate",
            observed_failure="returns_irrelevant_exact_term_evidence",
            notes="Known review candidate.",
        ),
        RealBusinessGoldenCase(
            id="logistics-address-after-outbound",
            source_id="logistics_faq",
            query="订单已出库后还能修改收货地址吗？",
            expected_mode="answerable",
            expected_citation_prefix="logistics_faq#chunk-",
            business_question_type="address_change_lookup",
            failure_mode="unclassified",
            risk_level="medium",
            description="Logistics address lookup.",
            question_origin="real_boundary_question",
            observed_failure="none_currently",
            notes="Workflow boundary case.",
        ),
        RealBusinessGoldenCase(
            id="logistics-after-sales-staff-negative",
            source_id="logistics_faq",
            query="物流FAQ里有哪些售后部门人员？",
            expected_mode="insufficient_evidence",
            expected_citation_prefix=None,
            business_question_type="negative_control",
            failure_mode="citation_or_evidence",
            risk_level="high",
            description="Logistics personnel negative control.",
            question_origin="real_cross_domain_trap",
            observed_failure="staff_roster_question_should_fail_closed",
            notes="Should stay fail-closed.",
        ),
    ]


def _client():
    class FakeResponse:
        def __init__(self, payload, status_code=200):
            self._payload = payload
            self.status_code = status_code

        def json(self):
            return self._payload

    citation_by_query = {
        "江苏交工咨询有哪些资质？": ["company_profile_2025_trial#chunk-1"],
        "公司有哪些售后政策？": [],
        "高价值订单退款超过五千元时需要谁复核？": ["refund_policy_docs#chunk-1"],
        "退款政策中有哪些公司部门？": ["refund_policy_docs#chunk-2"],
        "订单已出库后还能修改收货地址吗？": ["logistics_faq#chunk-1"],
        "物流FAQ里有哪些售后部门人员？": [],
    }

    class FakeClient:
        def get(self, path):
            if path == "/api/rag/sources":
                return FakeResponse(
                    {
                        "knowledge_bases": [
                            {"id": "company_profile_2025_trial"},
                            {"id": "refund_policy_docs"},
                            {"id": "logistics_faq"},
                        ]
                    }
                )
            if path.endswith("/documents"):
                source_id = path.split("/")[-2]
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
                {"source_id": source_id, "citation": citation, "score": 1.0}
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
