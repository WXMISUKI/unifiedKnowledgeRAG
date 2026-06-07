from app.services.parser_derived_corpus_retrieval_quality_baseline import (
    ParserDerivedQualityCase,
    export_parser_derived_corpus_retrieval_quality_baseline,
    run_parser_derived_corpus_retrieval_quality_baseline,
)


def test_parser_derived_quality_baseline_go_writes_summary(tmp_path):
    report = export_parser_derived_corpus_retrieval_quality_baseline(
        source_id="company_profile_2025_trial",
        cases=_cases(),
        output_dir=tmp_path / "quality",
        client=_client(),
    )

    assert report.decision == "go"
    assert report.reason_code == "parser_derived_corpus_quality_baseline_go"
    assert report.summary["case_count"] == 3
    assert report.summary["hit_rate"] == 1.0
    assert report.summary["citation_match_rate"] == 1.0
    assert report.summary["empty_handling_rate"] == 1.0
    assert report.summary["invalid_citation_count"] == 0
    assert report.summary["runtime_promotion_status"] == "keep_runtime_defaults"
    assert report.summary["graph_execution_status"] == "not_executed"
    assert report.json_path.exists()
    assert report.markdown_path.exists()
    assert "- Decision: `go`" in report.markdown_path.read_text(encoding="utf-8")


def test_parser_derived_quality_baseline_reviews_on_citation_miss(tmp_path):
    client = _client(citation_by_query={"公司主营业务是什么？": ["wrong#chunk"]})

    report = run_parser_derived_corpus_retrieval_quality_baseline(
        source_id="company_profile_2025_trial",
        cases=_cases(),
        client=client,
    )

    assert report.decision == "review"
    assert report.reason_code == "parser_derived_corpus_quality_needs_review"
    assert report.summary["citation_match_rate"] < 1.0
    assert "business_scope" in report.summary["review_case_ids"]


def test_parser_derived_quality_baseline_reviews_on_expected_empty_leakage(tmp_path):
    client = _client(
        citation_by_query={
            "公司有哪些合同金额？": ["company_profile_2025_trial#chunk-1"],
        }
    )

    report = run_parser_derived_corpus_retrieval_quality_baseline(
        source_id="company_profile_2025_trial",
        cases=_cases(),
        client=client,
    )

    assert report.decision == "review"
    assert report.reason_code == "parser_derived_corpus_quality_needs_review"
    assert report.summary["empty_handling_rate"] == 0.0
    assert "negative_contract_amount" in report.summary["review_case_ids"]


def test_parser_derived_quality_baseline_blocks_when_source_missing(tmp_path):
    report = run_parser_derived_corpus_retrieval_quality_baseline(
        source_id="missing_source",
        cases=_cases(),
        client=_client(registered=False),
    )

    assert report.decision == "blocked"
    assert report.reason_code == "parser_derived_source_not_ready"
    assert report.summary["blocked_case_ids"] == ["catalog_visibility"]


def _cases():
    return [
        ParserDerivedQualityCase(
            id="business_scope",
            query="公司主营业务是什么？",
            expected_mode="answerable",
            expected_source_id="company_profile_2025_trial",
            expected_citation="company_profile_2025_trial#chunk-1",
            category="business_scope",
            description="Main business scope should be answerable.",
        ),
        ParserDerivedQualityCase(
            id="service_scope",
            query="公司服务对象覆盖哪些行业？",
            expected_mode="answerable",
            expected_source_id="company_profile_2025_trial",
            expected_citation="company_profile_2025_trial#chunk-2",
            category="service_scope",
            description="Service scope should be answerable.",
        ),
        ParserDerivedQualityCase(
            id="negative_contract_amount",
            query="公司有哪些合同金额？",
            expected_mode="insufficient_evidence",
            expected_source_id=None,
            expected_citation=None,
            category="negative_control",
            description="Contract amount is not in the parser-derived profile.",
        ),
    ]


def _client(*, registered=True, citation_by_query=None):
    citation_by_query = citation_by_query or {
        "公司主营业务是什么？": ["company_profile_2025_trial#chunk-1"],
        "公司服务对象覆盖哪些行业？": ["company_profile_2025_trial#chunk-2"],
        "公司有哪些合同金额？": [],
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
                return FakeResponse({"ok": registered, "result": {"documents": [{}] if registered else []}})
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
