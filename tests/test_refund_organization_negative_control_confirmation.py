from app.services.local_business_rag_golden_cases import (
    DEFAULT_REFUND_ORGANIZATION_CONFIRMATION_CASE_FILE,
    RealBusinessGoldenCase,
    export_refund_organization_negative_control_confirmation,
    run_refund_organization_negative_control_confirmation,
)


def test_refund_confirmation_writes_query_mismatch_verdict(tmp_path):
    report = export_refund_organization_negative_control_confirmation(
        cases=_confirmation_cases(),
        output_dir=tmp_path / "refund-confirmation",
        client=_query_mismatch_client(),
    )

    assert report.decision == "review"
    assert report.summary["likely_failure_class"] == "confirmed_query_mismatch_variant"
    assert (
        report.summary["recommended_next_gate"]
        == "open_refund_query_mismatch_followup_before_query_rewrite_candidate"
    )
    assert report.summary["expected_empty_review_count"] == 0
    assert report.summary["answerable_pass_count"] == 0
    assert report.case_file == DEFAULT_REFUND_ORGANIZATION_CONFIRMATION_CASE_FILE
    assert report.json_path.exists()
    assert report.markdown_path.exists()
    assert (
        "# Refund Organization Negative Control Confirmation"
        in report.markdown_path.read_text(encoding="utf-8")
    )


def test_refund_confirmation_distinguishes_negative_control_variant():
    report = run_refund_organization_negative_control_confirmation(
        cases=_confirmation_cases(),
        client=_negative_control_variant_client(),
    )

    assert report.decision == "review"
    assert report.summary["likely_failure_class"] == "confirmed_negative_control_variant"
    assert (
        report.summary["recommended_next_gate"]
        == "open_refund_negative_control_hardening_scope_review"
    )
    assert report.summary["expected_empty_review_count"] == 5
    assert report.summary["answerable_pass_count"] == 3
    assert report.review_pattern_summary["negative_control_returned_evidence"] == 5
    assert report.review_pattern_summary["answerable_case_passed"] == 3


def _confirmation_cases():
    return [
        RealBusinessGoldenCase(
            id="refund-organization-department-negative",
            source_id="refund_policy_docs",
            query="退款政策中有哪些公司部门？",
            expected_mode="insufficient_evidence",
            expected_citation_prefix=None,
            business_question_type="organization_negative_control",
            failure_mode="query_mismatch",
            risk_level="high",
            description="Department inventory should fail closed.",
        ),
        RealBusinessGoldenCase(
            id="refund-organization-department-involved-negative",
            source_id="refund_policy_docs",
            query="退款文档里涉及哪些部门？",
            expected_mode="insufficient_evidence",
            expected_citation_prefix=None,
            business_question_type="organization_negative_control",
            failure_mode="query_mismatch",
            risk_level="high",
            description="Department listing should fail closed.",
        ),
        RealBusinessGoldenCase(
            id="refund-organization-owner-negative",
            source_id="refund_policy_docs",
            query="退款流程归哪个部门负责？",
            expected_mode="insufficient_evidence",
            expected_citation_prefix=None,
            business_question_type="organization_negative_control",
            failure_mode="query_mismatch",
            risk_level="high",
            description="Department owner should fail closed.",
        ),
        RealBusinessGoldenCase(
            id="refund-organization-role-list-negative",
            source_id="refund_policy_docs",
            query="退款政策里有哪些岗位人员？",
            expected_mode="insufficient_evidence",
            expected_citation_prefix=None,
            business_question_type="organization_negative_control",
            failure_mode="query_mismatch",
            risk_level="high",
            description="Role list should fail closed.",
        ),
        RealBusinessGoldenCase(
            id="refund-organization-staff-list-negative",
            source_id="refund_policy_docs",
            query="退款文档里有哪些员工名单？",
            expected_mode="insufficient_evidence",
            expected_citation_prefix=None,
            business_question_type="organization_negative_control",
            failure_mode="query_mismatch",
            risk_level="high",
            description="Staff roster should fail closed.",
        ),
        RealBusinessGoldenCase(
            id="refund-role-high-value-review",
            source_id="refund_policy_docs",
            query="高价值退款由谁复核？",
            expected_mode="answerable",
            expected_citation_prefix="refund_policy_2026#",
            business_question_type="role_lookup",
            failure_mode="query_mismatch",
            risk_level="medium",
            description="High-value role lookup.",
        ),
        RealBusinessGoldenCase(
            id="refund-role-appeal-review-owner",
            source_id="refund_policy_docs",
            query="退款申诉复核由谁处理？",
            expected_mode="answerable",
            expected_citation_prefix="refund_policy_2026#",
            business_question_type="role_lookup",
            failure_mode="query_mismatch",
            risk_level="medium",
            description="Appeal role lookup.",
        ),
        RealBusinessGoldenCase(
            id="refund-role-high-value-approval-review",
            source_id="refund_policy_docs",
            query="退款超过五千元谁来审批复核？",
            expected_mode="answerable",
            expected_citation_prefix="refund_policy_2026#",
            business_question_type="role_lookup",
            failure_mode="query_mismatch",
            risk_level="medium",
            description="High-value approval role lookup.",
        ),
    ]


def _query_mismatch_client():
    return _fake_client(
        {
            "退款政策中有哪些公司部门？": [],
            "退款文档里涉及哪些部门？": [],
            "退款流程归哪个部门负责？": [],
            "退款政策里有哪些岗位人员？": [],
            "退款文档里有哪些员工名单？": [],
            "高价值退款由谁复核？": [],
            "退款申诉复核由谁处理？": [],
            "退款超过五千元谁来审批复核？": [],
        }
    )


def _negative_control_variant_client():
    return _fake_client(
        {
            "退款政策中有哪些公司部门？": ["refund_policy_2026#exact-refund-code"],
            "退款文档里涉及哪些部门？": ["refund_policy_2026#exact-refund-code"],
            "退款流程归哪个部门负责？": ["refund_policy_2026#high-value-review"],
            "退款政策里有哪些岗位人员？": ["refund_policy_2026#appeal-review"],
            "退款文档里有哪些员工名单？": ["refund_policy_2026#section-5"],
            "高价值退款由谁复核？": ["refund_policy_2026#high-value-review"],
            "退款申诉复核由谁处理？": ["refund_policy_2026#appeal-review"],
            "退款超过五千元谁来审批复核？": ["refund_policy_2026#high-value-review"],
        }
    )


def _fake_client(citation_by_query):
    class FakeResponse:
        def __init__(self, payload, status_code=200):
            self._payload = payload
            self.status_code = status_code

        def json(self):
            return self._payload

    class FakeClient:
        def get(self, path):
            if path == "/api/rag/sources":
                return FakeResponse({"knowledge_bases": [{"id": "refund_policy_docs"}]})
            if path.endswith("/documents"):
                return FakeResponse(
                    {
                        "ok": True,
                        "result": {
                            "documents": [
                                {
                                    "citation_anchors": [
                                        "refund_policy_2026#high-value-review",
                                        "refund_policy_2026#appeal-review",
                                        "refund_policy_2026#exact-refund-code",
                                    ],
                                    "chunk_manifest": [
                                        {
                                            "chunk_id": "chunk-1",
                                            "citation": "refund_policy_2026#high-value-review",
                                            "char_count": 80,
                                            "text_preview": "高价值订单退款超过五千元时，需要售后主管复核并在工单中记录复核意见。",
                                        },
                                        {
                                            "chunk_id": "chunk-2",
                                            "citation": "refund_policy_2026#appeal-review",
                                            "char_count": 80,
                                            "text_preview": "退款申诉复核场景中，应先核对证据完整性，再提交二线审核。",
                                        },
                                        {
                                            "chunk_id": "chunk-3",
                                            "citation": "refund_policy_2026#exact-refund-code",
                                            "char_count": 80,
                                            "text_preview": "政策编号 RFD-2026-003 适用于三天未发货退款复核。",
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
                            "answer_status": (
                                "answered" if citations else "insufficient_evidence"
                            ),
                            "citations": citations,
                            "documents": documents,
                        },
                    }
                )
            raise AssertionError(path)

    return FakeClient()
