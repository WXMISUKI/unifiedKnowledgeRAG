import json
from dataclasses import replace
from pathlib import Path

from app.config import Settings

from app.services.retrieval_benchmark import (
    benchmark_report_to_dict,
    candidate_evaluation_to_dict,
    default_embedding_candidates,
    default_chunking_strategy_candidates,
    default_evidence_grading_candidates,
    default_query_rewrite_candidates,
    evidence_grading_candidate_evaluation_to_dict,
    embedding_candidate_result_to_dict,
    EmbeddingCandidate,
    export_chunking_strategy_evaluation,
    export_chinese_seed_evidence_bundle,
    export_evidence_grading_candidate_evaluation,
    export_query_rewrite_candidate_evaluation,
    export_qdrant_bge_chunking_comparison_evidence,
    export_qdrant_bge_smoke_evidence,
    export_qdrant_bge_threshold_sweep_evidence,
    export_qdrant_threshold_recommendation,
    evaluate_evidence_grading_candidates,
    evaluate_query_rewrite_candidates,
    evaluate_retrieval_candidates,
    evaluate_embedding_candidates,
    export_benchmark_report_json,
    export_benchmark_report_markdown,
    load_benchmark_cases,
    render_chunking_strategy_evaluation_markdown,
    render_evidence_grading_candidate_evaluation_markdown,
    render_embedding_candidate_markdown,
    render_benchmark_report_markdown,
    render_query_rewrite_candidate_evaluation_markdown,
    render_qdrant_chunking_comparison_markdown,
    render_qdrant_threshold_recommendation_markdown,
    render_qdrant_threshold_sweep_evidence_markdown,
    fixture_chinese_seed_retrieval_candidate,
    query_rewrite_candidate_evaluation_to_dict,
    RetrievalCandidate,
    run_retrieval_benchmark,
    ThresholdRecommendationGates,
    chunking_strategy_evaluation_to_dict,
    qdrant_chunking_comparison_to_dict,
    qdrant_threshold_recommendation_to_dict,
    qdrant_threshold_sweep_evidence_to_dict,
)


FIXTURE_PATH = Path("tests/fixtures/retrieval_benchmark_cases.json")


def test_loads_retrieval_benchmark_cases():
    cases = load_benchmark_cases(FIXTURE_PATH)

    assert [case.id for case in cases] == [
        "refund-delayed-shipping",
        "logistics-delay",
        "empty-moon-warehouse",
        "refund-delivery-paraphrase",
        "refund-evidence-records",
        "logistics-carrier-paraphrase",
        "multi-source-after-sales",
        "refund-customized-exception",
        "refund-high-value-review",
        "refund-address-change-before-shipping",
        "logistics-same-city-timeout",
        "logistics-lost-package-cross-team",
        "logistics-address-intercept",
        "refund-appeal-second-review",
        "logistics-batch-exception-escalation",
        "empty-membership-points",
        "empty-invoice-tax-policy",
        "empty-membership-tier-recovery",
        "empty-coupon-approval",
        "empty-password-reset-email",
        "empty-finance-reconciliation",
    ]
    assert cases[0].expected_citation == "refund_policy_2026#section-3"
    assert cases[-1].expect_empty is True
    assert cases[-1].category == "empty"


def test_fixture_backend_benchmark_reports_success_metrics():
    cases = load_benchmark_cases(FIXTURE_PATH)
    report = run_retrieval_benchmark(cases, Settings(rag_retrieval_backend="fixture"))

    assert report.summary.backend == "fixture"
    assert report.summary.total_cases == 21
    assert report.summary.hit_rate == 1.0
    assert report.summary.citation_match_rate == 1.0
    assert report.summary.empty_handling_rate == 1.0
    assert all(result.latency_ms >= 0 for result in report.cases)


def test_empty_retrieval_case_reports_empty_handling():
    cases = load_benchmark_cases(FIXTURE_PATH)
    report = run_retrieval_benchmark(cases, Settings(rag_retrieval_backend="fixture"))

    empty_case = next(
        result for result in report.cases if result.id == "empty-moon-warehouse"
    )
    assert empty_case.hit_at_k is True
    assert empty_case.citation_match is True
    assert empty_case.empty_query_handling is True
    assert empty_case.returned_citations == []


def test_benchmark_cases_cover_required_categories():
    cases = load_benchmark_cases(FIXTURE_PATH)

    assert {case.category for case in cases} >= {
        "policy",
        "faq",
        "evidence",
        "paraphrase",
        "multi-source",
        "exception-policy",
        "operational-escalation",
        "sla",
        "cross-source",
        "multi-intent",
        "long-section",
        "empty",
    }
    assert {case.difficulty for case in cases} >= {"easy", "medium", "hard"}


def test_benchmark_report_includes_category_summaries():
    cases = load_benchmark_cases(FIXTURE_PATH)
    report = run_retrieval_benchmark(cases, Settings(rag_retrieval_backend="fixture"))

    summaries = report.summary.category_summaries
    assert summaries["policy"]["total_cases"] == 1
    assert summaries["paraphrase"]["total_cases"] == 2
    assert summaries["operational-escalation"]["total_cases"] == 2
    assert summaries["long-section"]["total_cases"] == 2
    assert summaries["empty"]["total_cases"] == 7
    assert summaries["empty"]["empty_handling_rate"] == 1.0


def test_exports_benchmark_report_json(tmp_path):
    cases = load_benchmark_cases(FIXTURE_PATH)
    report = run_retrieval_benchmark(cases, Settings(rag_retrieval_backend="fixture"))
    output_path = tmp_path / "reports" / "benchmark.json"

    exported_path = export_benchmark_report_json(report, output_path)
    payload = json.loads(exported_path.read_text(encoding="utf-8"))

    assert exported_path == output_path
    assert payload == benchmark_report_to_dict(report)
    assert payload["summary"]["backend"] == "fixture"
    assert payload["summary"]["category_summaries"]["empty"]["total_cases"] == 7
    assert payload["cases"][0]["returned_citations"]


def test_exports_benchmark_report_markdown(tmp_path):
    cases = load_benchmark_cases(FIXTURE_PATH)
    report = run_retrieval_benchmark(cases, Settings(rag_retrieval_backend="fixture"))
    output_path = tmp_path / "reports" / "benchmark.md"

    markdown = render_benchmark_report_markdown(report)
    exported_path = export_benchmark_report_markdown(report, output_path)
    exported_markdown = exported_path.read_text(encoding="utf-8")

    assert "# Retrieval Benchmark Report" in markdown
    assert "| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |" in markdown
    assert "| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |" in markdown
    assert "refund-delayed-shipping" in markdown
    assert exported_markdown == markdown


def test_rejects_invalid_retrieval_candidate_ids():
    cases = load_benchmark_cases(FIXTURE_PATH)

    invalid_candidate = RetrievalCandidate(
        id="fixture/default",
        backend="fixture",
        description="Invalid path-like id",
    )

    try:
        evaluate_retrieval_candidates(cases, [invalid_candidate])
    except ValueError as error:
        assert "Invalid retrieval candidate id" in str(error)
    else:
        raise AssertionError("Expected invalid candidate id to be rejected")


def test_rejects_duplicate_retrieval_candidate_ids():
    cases = load_benchmark_cases(FIXTURE_PATH)
    candidates = [
        RetrievalCandidate(
            id="fixture-baseline",
            backend="fixture",
            description="Fixture baseline",
        ),
        RetrievalCandidate(
            id="fixture-baseline",
            backend="fixture",
            description="Duplicate fixture baseline",
        ),
    ]

    try:
        evaluate_retrieval_candidates(cases, candidates)
    except ValueError as error:
        assert "Duplicate retrieval candidate id" in str(error)
    else:
        raise AssertionError("Expected duplicate candidate id to be rejected")


def test_evaluates_multiple_retrieval_candidates():
    cases = load_benchmark_cases(FIXTURE_PATH)
    candidates = [
        RetrievalCandidate(
            id="fixture-baseline",
            backend="fixture",
            description="Fixture baseline",
            metadata={"embedding": "none", "vector_store": "none"},
        ),
        RetrievalCandidate(
            id="fixture-control",
            backend="fixture",
            description="Fixture control",
            metadata={"notes": "same backend for comparison workflow"},
        ),
    ]

    evaluations = evaluate_retrieval_candidates(cases, candidates)

    assert [evaluation.candidate.id for evaluation in evaluations] == [
        "fixture-baseline",
        "fixture-control",
    ]
    assert all(evaluation.report.summary.hit_rate == 1.0 for evaluation in evaluations)
    assert evaluations[0].candidate.metadata == {
        "embedding": "none",
        "vector_store": "none",
    }


def test_exports_retrieval_candidate_evaluation_reports(tmp_path):
    cases = load_benchmark_cases(FIXTURE_PATH)
    candidate = RetrievalCandidate(
        id="fixture-baseline",
        backend="fixture",
        description="Fixture baseline",
        metadata={"embedding": "none"},
    )

    evaluations = evaluate_retrieval_candidates(
        cases,
        [candidate],
        output_dir=tmp_path / "candidate-reports",
    )

    evaluation = evaluations[0]
    assert evaluation.json_path == tmp_path / "candidate-reports" / "fixture-baseline.json"
    assert evaluation.markdown_path == tmp_path / "candidate-reports" / "fixture-baseline.md"

    payload = json.loads(evaluation.json_path.read_text(encoding="utf-8"))
    markdown = evaluation.markdown_path.read_text(encoding="utf-8")

    assert payload == candidate_evaluation_to_dict(candidate, evaluation.report)
    assert payload["candidate"]["metadata"]["embedding"] == "none"
    assert "# Retrieval Candidate Evaluation" in markdown
    assert "| fixture-baseline | fixture | Fixture baseline |" in markdown
    assert "# Retrieval Benchmark Report" in markdown


def test_default_embedding_candidates_cover_chinese_public_and_private_paths():
    candidates = default_embedding_candidates()
    by_id = {candidate.id: candidate for candidate in candidates}

    assert set(by_id) >= {
        "mock-hash-v1",
        "qwen-embedding-candidate",
        "bge-m3-local-candidate",
        "openai-embedding-candidate",
    }
    assert by_id["mock-hash-v1"].approval_status == "baseline"
    assert by_id["qwen-embedding-candidate"].provider_family == "hosted"
    assert by_id["qwen-embedding-candidate"].chinese_heavy_suitable is True
    assert by_id["bge-m3-local-candidate"].provider_family == "local"
    assert by_id["bge-m3-local-candidate"].private_network_supported is True


def test_default_chunking_strategy_candidates_include_baseline_and_planned():
    candidates = default_chunking_strategy_candidates()
    by_id = {candidate.id: candidate for candidate in candidates}

    assert by_id["markdown-paragraph-v1"].implementation_status == "implemented"
    assert by_id["markdown-section-v1"].implementation_status == "runnable"
    assert by_id["token-window-v1"].implementation_status == "runnable"
    assert "long paragraphs" in by_id["token-window-v1"].expected_fit


def test_default_query_rewrite_candidates_include_baseline_and_controlled():
    candidates = default_query_rewrite_candidates()
    by_id = {candidate.id: candidate for candidate in candidates}

    assert by_id["original-query-baseline"].rewrite_policy == "none"
    assert by_id["original-query-baseline"].implementation_status == "baseline"
    assert by_id["controlled-support-rewrite-v1"].rewrite_policy == (
        "controlled_support_rules"
    )
    assert by_id["controlled-support-rewrite-v1"].implementation_status == "candidate"


def test_default_evidence_grading_candidates_include_strict_and_source_policies():
    candidates = default_evidence_grading_candidates()
    by_id = {candidate.id: candidate for candidate in candidates}

    assert by_id["citation-match-grader-v1"].grading_policy == "citation_match"
    assert by_id["citation-match-grader-v1"].implementation_status == "candidate"
    assert by_id["source-match-grader-v1"].grading_policy == "source_match"
    assert by_id["source-match-grader-v1"].implementation_status == "candidate"


def test_evidence_grading_candidate_labels_expected_empty_cases():
    cases = load_benchmark_cases(FIXTURE_PATH)

    evaluation = evaluate_evidence_grading_candidates(
        cases=cases,
        settings=Settings(rag_retrieval_backend="fixture"),
    )

    citation_result = next(
        result
        for result in evaluation.results
        if result.candidate.id == "citation-match-grader-v1"
    )
    empty_case = next(
        case for case in citation_result.cases if case.case_id == "empty-moon-warehouse"
    )

    assert citation_result.total_cases == 21
    assert citation_result.answer_bearing_rate == 1.0
    assert citation_result.related_insufficient_count == 0
    assert citation_result.missing_evidence_count == 0
    assert citation_result.unexpected_evidence_count == 0
    assert citation_result.expected_empty_pass_rate == 1.0
    assert empty_case.grading_label == "no_evidence_expected"
    assert empty_case.returned_citations == []


def test_evidence_grading_distinguishes_citation_and_source_policies():
    cases = load_benchmark_cases(FIXTURE_PATH)
    mutated_cases = [
        replace(case, expected_citation="refund_policy_2026#missing-anchor")
        if case.id == "refund-delayed-shipping"
        else case
        for case in cases
    ]

    evaluation = evaluate_evidence_grading_candidates(
        cases=mutated_cases,
        settings=Settings(rag_retrieval_backend="fixture"),
    )

    by_id = {result.candidate.id: result for result in evaluation.results}
    strict_case = next(
        case
        for case in by_id["citation-match-grader-v1"].cases
        if case.case_id == "refund-delayed-shipping"
    )
    source_case = next(
        case
        for case in by_id["source-match-grader-v1"].cases
        if case.case_id == "refund-delayed-shipping"
    )

    assert strict_case.grading_label == "related_insufficient"
    assert "expected citation was missing" in strict_case.grading_reason
    assert by_id["citation-match-grader-v1"].related_insufficient_count == 1
    assert by_id["citation-match-grader-v1"].answer_bearing_rate < 1.0
    assert source_case.grading_label == "answer_bearing"
    assert by_id["source-match-grader-v1"].answer_bearing_rate == 1.0


def test_exports_evidence_grading_candidate_evaluation(tmp_path):
    output_dir = tmp_path / "evidence-grading"

    evaluation = export_evidence_grading_candidate_evaluation(output_dir=output_dir)

    assert evaluation.json_path == output_dir / "evidence-grading-candidates.json"
    assert evaluation.markdown_path == output_dir / "evidence-grading-candidates.md"

    payload = json.loads(evaluation.json_path.read_text(encoding="utf-8"))
    markdown = evaluation.markdown_path.read_text(encoding="utf-8")

    assert payload == evidence_grading_candidate_evaluation_to_dict(evaluation)
    assert payload["results"][0]["candidate"]["id"] == "citation-match-grader-v1"
    assert payload["results"][0]["cases"][0]["grading_label"] == "answer_bearing"
    assert "# Evidence Grading Candidate Evaluation" in markdown
    assert "| Candidate | Status | Total Cases | Answer-bearing Rate |" in markdown
    assert "citation-match-grader-v1" in markdown
    assert "no_evidence_expected" in markdown
    assert render_evidence_grading_candidate_evaluation_markdown(evaluation) == markdown


def test_query_rewrite_candidate_preserves_expected_empty_cases():
    cases = load_benchmark_cases(FIXTURE_PATH)
    candidate = next(
        candidate
        for candidate in default_query_rewrite_candidates()
        if candidate.id == "controlled-support-rewrite-v1"
    )

    evaluation = evaluate_query_rewrite_candidates(
        cases=cases,
        candidates=[candidate],
        settings=Settings(rag_retrieval_backend="fixture"),
    )

    result = evaluation.results[0]
    assert result.rewritten_cases == 6
    assert result.expected_empty_rewrites == 0
    assert result.report.summary.hit_rate == 1.0
    assert result.report.summary.citation_match_rate == 1.0
    assert result.report.summary.empty_handling_rate == 1.0
    assert all(
        case.original_query == case.rewritten_query
        for case in result.cases
        if case.expect_empty
    )


def test_exports_query_rewrite_candidate_evaluation(tmp_path):
    output_dir = tmp_path / "query-rewrite"

    evaluation = export_query_rewrite_candidate_evaluation(output_dir=output_dir)

    assert evaluation.json_path == output_dir / "query-rewrite-candidates.json"
    assert evaluation.markdown_path == output_dir / "query-rewrite-candidates.md"

    payload = json.loads(evaluation.json_path.read_text(encoding="utf-8"))
    markdown = evaluation.markdown_path.read_text(encoding="utf-8")

    assert payload == query_rewrite_candidate_evaluation_to_dict(evaluation)
    by_id = {result.candidate.id: result for result in evaluation.results}
    assert by_id["original-query-baseline"].rewritten_cases == 0
    assert by_id["controlled-support-rewrite-v1"].rewritten_cases == 6
    assert by_id["controlled-support-rewrite-v1"].expected_empty_rewrites == 0
    assert "# Query Rewrite Candidate Evaluation" in markdown
    assert "| Candidate | Status | Total Cases | Rewritten Cases | Rewrite Rate |" in markdown
    assert "controlled-support-rewrite-v1" in markdown
    assert "refund-delivery-paraphrase" in markdown
    assert render_query_rewrite_candidate_evaluation_markdown(evaluation) == markdown


def test_embedding_candidate_evaluation_remains_review_only():
    evaluations = evaluate_embedding_candidates()

    qwen = next(
        evaluation
        for evaluation in evaluations
        if evaluation.result.candidate.id == "qwen-embedding-candidate"
    )
    bge = next(
        evaluation
        for evaluation in evaluations
        if evaluation.result.candidate.id == "bge-m3-local-candidate"
    )

    assert qwen.result.readiness_status == "review_required"
    assert qwen.result.criteria_coverage["chinese_heavy_suitable"] is True
    assert qwen.result.criteria_coverage["private_network_supported"] is False
    assert any("does not approve or invoke" in note for note in qwen.result.decision_notes)
    assert any("Public data egress" in note for note in qwen.result.decision_notes)
    assert bge.result.criteria_coverage["private_network_supported"] is True


def test_rejects_invalid_embedding_candidate_ids():
    invalid_candidate = EmbeddingCandidate(
        id="qwen/candidate",
        provider_family="hosted",
        model_name="qwen",
        deployment_mode="public-hosted",
        language_profile="chinese-heavy",
        vector_dimension=None,
        data_residency="provider-dependent",
        operational_complexity="medium",
        reranker_compatibility="candidate-specific",
        approval_status="candidate",
        chinese_heavy_suitable=True,
        private_network_supported=False,
        notes=[],
    )

    try:
        evaluate_embedding_candidates([invalid_candidate])
    except ValueError as error:
        assert "Invalid embedding candidate id" in str(error)
    else:
        raise AssertionError("Expected invalid embedding candidate id to be rejected")


def test_rejects_duplicate_embedding_candidate_ids():
    candidate = default_embedding_candidates()[0]

    try:
        evaluate_embedding_candidates([candidate, candidate])
    except ValueError as error:
        assert "Duplicate embedding candidate id" in str(error)
    else:
        raise AssertionError("Expected duplicate embedding candidate id to be rejected")


def test_exports_embedding_candidate_evaluation_reports(tmp_path):
    candidate = default_embedding_candidates()[2]

    evaluations = evaluate_embedding_candidates(
        [candidate],
        output_dir=tmp_path / "embedding-candidates",
    )

    evaluation = evaluations[0]
    assert evaluation.json_path == tmp_path / "embedding-candidates" / f"{candidate.id}.json"
    assert evaluation.markdown_path == tmp_path / "embedding-candidates" / f"{candidate.id}.md"

    payload = json.loads(evaluation.json_path.read_text(encoding="utf-8"))
    markdown = evaluation.markdown_path.read_text(encoding="utf-8")

    assert payload == embedding_candidate_result_to_dict(evaluation.result)
    assert payload["candidate"]["id"] == "bge-m3-local-candidate"
    assert payload["readiness_status"] == "review_required"
    assert "# Embedding Candidate Evaluation" in markdown
    assert "| bge-m3-local-candidate | local | bge-m3 |" in markdown
    assert "This evaluation does not approve or invoke the embedding provider." in markdown
    assert render_embedding_candidate_markdown(evaluation.result) == markdown


def test_fixture_chinese_seed_candidate_is_contract_baseline_only():
    candidate = fixture_chinese_seed_retrieval_candidate()

    assert candidate.id == "fixture-chinese-seed-baseline"
    assert candidate.backend == "fixture"
    assert candidate.metadata["benchmark_seed"] == "chinese-enterprise-support-v1"
    assert candidate.metadata["quality_claim"] == "contract-baseline-only"


def test_exports_chinese_seed_evidence_bundle(tmp_path):
    output_dir = tmp_path / "chinese-seed"

    bundle = export_chinese_seed_evidence_bundle(output_dir)

    assert bundle.output_dir == output_dir
    assert [item.candidate.id for item in bundle.retrieval_evaluations] == [
        "fixture-chinese-seed-baseline"
    ]
    assert bundle.retrieval_evaluations[0].report.summary.total_cases == 21
    assert bundle.retrieval_evaluations[0].report.summary.hit_rate == 1.0
    assert {item.result.candidate.id for item in bundle.embedding_evaluations} >= {
        "mock-hash-v1",
        "qwen-embedding-candidate",
        "bge-m3-local-candidate",
        "openai-embedding-candidate",
    }

    retrieval_json = (
        output_dir / "retrieval-candidates" / "fixture-chinese-seed-baseline.json"
    )
    retrieval_markdown = (
        output_dir / "retrieval-candidates" / "fixture-chinese-seed-baseline.md"
    )
    embedding_json = output_dir / "embedding-candidates" / "bge-m3-local-candidate.json"
    embedding_markdown = output_dir / "embedding-candidates" / "bge-m3-local-candidate.md"

    assert retrieval_json.exists()
    assert retrieval_markdown.exists()
    assert embedding_json.exists()
    assert embedding_markdown.exists()

    retrieval_payload = json.loads(retrieval_json.read_text(encoding="utf-8"))
    assert retrieval_payload["candidate"]["metadata"]["quality_claim"] == (
        "contract-baseline-only"
    )
    assert retrieval_payload["report"]["summary"]["total_cases"] == 21

    embedding_payload = json.loads(embedding_json.read_text(encoding="utf-8"))
    assert embedding_payload["candidate"]["id"] == "bge-m3-local-candidate"
    assert embedding_payload["readiness_status"] == "review_required"


def test_exports_chunking_strategy_evaluation(tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n"
        "客户三天未发货可以申请退款。\n\n"
        "退款处理需要保留订单编号。\n\n"
        "定制商品不支持无理由退款。\n\n"
        "五千元以上退款需要主管复核。\n\n"
        "未发货地址变更应先暂停发货。\n\n"
        "退款申诉复核场景中，应提交二线审核。",
        encoding="utf-8",
    )
    (source_dir / "logistics_faq.md").write_text(
        "# 物流常见问题\n\n"
        "物流轨迹超过二十四小时未更新时，应先联系承运商。\n\n"
        "同城配送超过两小时未送达时，客服应核实骑手位置。\n\n"
        "承运商确认包裹丢失后，客服应创建物流异常工单。\n\n"
        "订单已经出库后要改地址，应先联系承运商拦截。\n\n"
        "批量物流异常处理中，应创建批量异常工单。",
        encoding="utf-8",
    )

    evaluation = export_chunking_strategy_evaluation(
        output_dir=tmp_path / "chunking",
        settings=Settings(rag_source_dir=source_dir),
    )

    assert evaluation.json_path == tmp_path / "chunking" / "chunking-strategy-candidates.json"
    assert evaluation.markdown_path == tmp_path / "chunking" / "chunking-strategy-candidates.md"

    by_id = {result.candidate.id: result for result in evaluation.results}
    assert by_id["markdown-paragraph-v1"].total_chunks == 11
    assert by_id["markdown-paragraph-v1"].citation_stability == "stable"
    assert by_id["markdown-paragraph-v1"].long_section_support == "covered"
    assert by_id["markdown-section-v1"].total_chunks == 2
    assert by_id["markdown-section-v1"].citation_stability == "stable"
    assert by_id["markdown-section-v1"].long_section_support == "covered-by-section"
    assert by_id["token-window-v1"].total_chunks == 2
    assert by_id["token-window-v1"].citation_stability == "stable"
    assert by_id["token-window-v1"].long_section_support == "covered-by-window"

    payload = json.loads(evaluation.json_path.read_text(encoding="utf-8"))
    markdown = evaluation.markdown_path.read_text(encoding="utf-8")

    assert payload == chunking_strategy_evaluation_to_dict(evaluation)
    assert "# Chunking Strategy Candidate Evaluation" in markdown
    assert "| markdown-paragraph-v1 | implemented | 11 | stable | covered |" in markdown
    assert "| markdown-section-v1 | runnable | 2 | stable | covered-by-section |" in markdown
    assert "| token-window-v1 | runnable | 2 | stable | covered-by-window |" in markdown
    assert render_chunking_strategy_evaluation_markdown(evaluation) == markdown


def test_export_qdrant_bge_smoke_evidence_uses_single_client(monkeypatch, tmp_path):
    from tests.test_qdrant_vector_store import FakeQdrantClient

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n客户三天未发货可以申请退款。",
        encoding="utf-8",
    )
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(
        """
[
  {
    "id": "refund-basic",
    "category": "policy",
    "difficulty": "easy",
    "query": "客户三天未发货能否退款？",
    "knowledge_base_ids": ["refund_policy_docs"],
    "top_k": 1,
    "expected_source_id": "refund_policy_docs",
    "expected_citation": "refund_policy_2026#chunk-1",
    "expect_empty": false
  }
]
""",
        encoding="utf-8",
    )
    fake_client = FakeQdrantClient(
        collection_exists=False,
        hits=[
            {
                "score": 0.91,
                "payload": {
                    "source_id": "refund_policy_docs",
                    "document_id": "refund_policy_2026",
                    "title": "售后退款规则",
                    "text": "客户三天未发货可以申请退款。",
                    "citation": "refund_policy_2026#chunk-1",
                },
            }
        ],
    )
    clients = []

    def fake_create_client(settings):
        clients.append(fake_client)
        return fake_client

    monkeypatch.setattr(
        "app.services.retrieval_benchmark.create_qdrant_client",
        fake_create_client,
    )
    settings = Settings(
        rag_retrieval_backend="qdrant",
        rag_source_dir=source_dir,
        rag_index_dir=tmp_path / "index",
        qdrant_url=":memory:",
        rag_score_threshold=0.37,
        embedding_provider="mock",
        embedding_vector_size=3,
        qdrant_vector_size=3,
    )

    report = export_qdrant_bge_smoke_evidence(
        output_dir=tmp_path / "evidence",
        cases_path=cases_path,
        source_ids=["refund_policy_docs"],
        settings=settings,
    )

    assert clients == [fake_client]
    assert fake_client.created_collections
    assert fake_client.upserts
    assert fake_client.queries
    assert report.json_path.exists()
    assert report.markdown_path.exists()
    assert report.indexed_sources["refund_policy_docs"]["chunk_count"] == 1
    assert report.report.summary.hit_rate == 1.0
    assert report.metadata["rag_score_threshold"] == "0.37"
    assert "qdrant-bge-m3-smoke" in report.markdown_path.read_text(encoding="utf-8")


def test_export_qdrant_bge_threshold_sweep_evidence(monkeypatch, tmp_path):
    from tests.test_qdrant_vector_store import FakeQdrantClient

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n客户三天未发货可以申请退款。",
        encoding="utf-8",
    )
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(
        """
[
  {
    "id": "refund-basic",
    "category": "policy",
    "difficulty": "easy",
    "query": "客户三天未发货能否退款？",
    "knowledge_base_ids": ["refund_policy_docs"],
    "top_k": 1,
    "expected_source_id": "refund_policy_docs",
    "expected_citation": "refund_policy_2026#chunk-1",
    "expect_empty": false
  }
]
""",
        encoding="utf-8",
    )
    clients = []

    def fake_create_client(settings):
        client = FakeQdrantClient(
            collection_exists=False,
            hits=[
                {
                    "score": 0.91,
                    "payload": {
                        "source_id": "refund_policy_docs",
                        "document_id": "refund_policy_2026",
                        "title": "售后退款规则",
                        "text": "客户三天未发货可以申请退款。",
                        "citation": "refund_policy_2026#chunk-1",
                    },
                }
            ],
        )
        clients.append(client)
        return client

    monkeypatch.setattr(
        "app.services.retrieval_benchmark.create_qdrant_client",
        fake_create_client,
    )
    settings = Settings(
        rag_retrieval_backend="qdrant",
        rag_source_dir=source_dir,
        rag_index_dir=tmp_path / "index",
        qdrant_url=":memory:",
        embedding_provider="mock",
        embedding_vector_size=3,
        qdrant_vector_size=3,
    )

    report = export_qdrant_bge_threshold_sweep_evidence(
        output_dir=tmp_path / "evidence",
        thresholds=[0.5, 0.1],
        cases_path=cases_path,
        source_ids=["refund_policy_docs"],
        settings=settings,
    )

    assert len(clients) == 2
    assert report.thresholds == [0.1, 0.5]
    assert [item.metadata["rag_score_threshold"] for item in report.reports] == [
        "0.1",
        "0.5",
    ]
    assert [item.json_path for item in report.reports] == [None, None]
    assert [item.markdown_path for item in report.reports] == [None, None]
    assert all(item.report.summary.hit_rate == 1.0 for item in report.reports)
    assert report.json_path == tmp_path / "evidence" / "qdrant-bge-m3-threshold-sweep.json"
    assert report.markdown_path == tmp_path / "evidence" / "qdrant-bge-m3-threshold-sweep.md"

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload == qdrant_threshold_sweep_evidence_to_dict(report)
    assert payload["summary"][0]["threshold"] == 0.1
    assert payload["summary"][1]["threshold"] == 0.5
    assert "# Qdrant BGE-M3 Threshold Sweep Evidence" in markdown
    assert "| 0.1000 | 1 | 1.0000 | 1.0000 | 0.0000 |" in markdown
    assert render_qdrant_threshold_sweep_evidence_markdown(report) == markdown


def test_export_qdrant_bge_chunking_comparison_evidence(monkeypatch, tmp_path):
    from tests.test_qdrant_vector_store import FakeQdrantClient

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n"
        "客户三天未发货可以申请退款。\n\n"
        "退款处理需要保留订单编号。",
        encoding="utf-8",
    )
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(
        """
[
  {
    "id": "refund-basic",
    "category": "policy",
    "difficulty": "easy",
    "query": "客户三天未发货能否退款？",
    "knowledge_base_ids": ["refund_policy_docs"],
    "top_k": 1,
    "expected_source_id": "refund_policy_docs",
    "expected_citation": "refund_policy_2026#section-3",
    "expect_empty": false
  }
]
""",
        encoding="utf-8",
    )
    clients = []

    def fake_create_client(settings):
        client = FakeQdrantClient(
            collection_exists=False,
            hits=[
                {
                    "score": 0.91,
                    "payload": {
                        "source_id": "refund_policy_docs",
                        "document_id": "refund_policy_2026",
                        "title": "售后退款规则",
                        "text": "客户三天未发货可以申请退款。",
                        "citation": "refund_policy_2026#section-3",
                    },
                }
            ],
        )
        clients.append(client)
        return client

    monkeypatch.setattr(
        "app.services.retrieval_benchmark.create_qdrant_client",
        fake_create_client,
    )
    settings = Settings(
        rag_retrieval_backend="qdrant",
        rag_source_dir=source_dir,
        rag_index_dir=tmp_path / "index",
        qdrant_url=":memory:",
        embedding_provider="mock",
        embedding_vector_size=3,
        qdrant_vector_size=3,
    )

    report = export_qdrant_bge_chunking_comparison_evidence(
        output_dir=tmp_path / "evidence",
        cases_path=cases_path,
        source_ids=["refund_policy_docs"],
        settings=settings,
    )

    assert len(clients) == 3
    assert report.strategies == [
        "markdown-paragraph-v1",
        "markdown-section-v1",
        "token-window-v1",
    ]
    assert report.json_path == tmp_path / "evidence" / "qdrant-bge-m3-chunking-comparison.json"
    assert report.markdown_path == tmp_path / "evidence" / "qdrant-bge-m3-chunking-comparison.md"
    assert [
        item.indexed_sources["refund_policy_docs"]["chunk_count"]
        for item in report.reports
    ] == [2, 1, 1]
    assert [
        item.metadata["chunking_strategy"]
        for item in report.reports
    ] == ["markdown-paragraph-v1", "markdown-section-v1", "token-window-v1"]

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload == qdrant_chunking_comparison_to_dict(report)
    assert payload["summary"][0]["chunk_count"] == 2
    assert payload["summary"][1]["chunk_count"] == 1
    assert payload["summary"][2]["chunk_count"] == 1
    assert "# Qdrant BGE-M3 Chunking Comparison Evidence" in markdown
    assert "| markdown-paragraph-v1 | 2 | 1.0000 | 1.0000 | 0.0000 |" in markdown
    assert "| markdown-section-v1 | 1 | 1.0000 | 1.0000 | 0.0000 |" in markdown
    assert "| token-window-v1 | 1 | 1.0000 | 1.0000 | 0.0000 |" in markdown
    assert render_qdrant_chunking_comparison_markdown(report) == markdown


def test_qdrant_bge_chunking_comparison_rejects_invalid_strategies(tmp_path):
    settings = Settings(
        rag_retrieval_backend="qdrant",
        rag_source_dir=tmp_path / "sources",
        rag_index_dir=tmp_path / "index",
        embedding_provider="mock",
        embedding_vector_size=3,
        qdrant_vector_size=3,
    )

    for strategies, expected_message in [
        ([], "At least one chunking strategy"),
        (["markdown-paragraph-v1", "markdown-paragraph-v1"], "Duplicate chunking"),
        (["unknown-v1"], "Unsupported chunking"),
    ]:
        try:
            export_qdrant_bge_chunking_comparison_evidence(
                output_dir=tmp_path / "evidence",
                strategies=strategies,
                settings=settings,
            )
        except ValueError as error:
            assert expected_message in str(error)
        else:
            raise AssertionError("Expected invalid chunking comparison to be rejected")


def test_qdrant_bge_threshold_sweep_rejects_invalid_thresholds(tmp_path):
    settings = Settings(
        rag_retrieval_backend="qdrant",
        rag_source_dir=tmp_path / "sources",
        rag_index_dir=tmp_path / "index",
        embedding_provider="mock",
        embedding_vector_size=3,
        qdrant_vector_size=3,
    )

    for thresholds, expected_message in [
        ([], "At least one threshold"),
        ([0.2, 0.2], "Duplicate threshold"),
        ([-0.1], "between 0.0 and 1.0"),
        ([1.1], "between 0.0 and 1.0"),
    ]:
        try:
            export_qdrant_bge_threshold_sweep_evidence(
                output_dir=tmp_path / "evidence",
                thresholds=thresholds,
                settings=settings,
            )
        except ValueError as error:
            assert expected_message in str(error)
        else:
            raise AssertionError("Expected invalid threshold sweep to be rejected")


def test_qdrant_threshold_recommendation_selects_lowest_passing_threshold(tmp_path):
    sweep_path = tmp_path / "qdrant-bge-m3-threshold-sweep.json"
    sweep_path.write_text(
        json.dumps(
            {
                "summary": [
                    {
                        "threshold": 0.3,
                        "total_cases": 19,
                        "hit_rate": 0.6316,
                        "citation_match_rate": 0.6316,
                        "empty_handling_rate": 0.0,
                    },
                    {
                        "threshold": 0.7,
                        "total_cases": 19,
                        "hit_rate": 1.0,
                        "citation_match_rate": 1.0,
                        "empty_handling_rate": 1.0,
                    },
                    {
                        "threshold": 0.8,
                        "total_cases": 19,
                        "hit_rate": 1.0,
                        "citation_match_rate": 1.0,
                        "empty_handling_rate": 1.0,
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    recommendation = export_qdrant_threshold_recommendation(
        sweep_path=sweep_path,
        output_dir=tmp_path,
    )

    assert recommendation.selected_threshold == 0.7
    assert recommendation.selected_metrics == {
        "total_cases": 19,
        "hit_rate": 1.0,
        "citation_match_rate": 1.0,
        "empty_handling_rate": 1.0,
    }
    assert recommendation.approval_status == "local_seed_recommendation"
    assert recommendation.json_path == tmp_path / "qdrant-bge-m3-threshold-recommendation.json"
    assert recommendation.markdown_path == tmp_path / "qdrant-bge-m3-threshold-recommendation.md"

    payload = json.loads(recommendation.json_path.read_text(encoding="utf-8"))
    markdown = recommendation.markdown_path.read_text(encoding="utf-8")

    assert payload == qdrant_threshold_recommendation_to_dict(recommendation)
    assert "# Qdrant BGE-M3 Threshold Recommendation" in markdown
    assert "| 0.7000 | local_seed_recommendation |" in markdown
    assert "does not change the runtime RAG_SCORE_THRESHOLD default" in markdown
    assert render_qdrant_threshold_recommendation_markdown(recommendation) == markdown


def test_qdrant_threshold_recommendation_can_use_relaxed_gates(tmp_path):
    sweep_path = tmp_path / "qdrant-bge-m3-threshold-sweep.json"
    sweep_path.write_text(
        json.dumps(
            {
                "summary": [
                    {
                        "threshold": 0.5,
                        "total_cases": 19,
                        "hit_rate": 0.7368,
                        "citation_match_rate": 0.7368,
                        "empty_handling_rate": 0.2857,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    recommendation = export_qdrant_threshold_recommendation(
        sweep_path=sweep_path,
        output_dir=tmp_path,
        gates=ThresholdRecommendationGates(
            min_hit_rate=0.7,
            min_citation_match_rate=0.7,
            min_empty_handling_rate=0.2,
        ),
    )

    assert recommendation.selected_threshold == 0.5


def test_qdrant_threshold_recommendation_rejects_when_no_threshold_passes(tmp_path):
    sweep_path = tmp_path / "qdrant-bge-m3-threshold-sweep.json"
    sweep_path.write_text(
        json.dumps(
            {
                "summary": [
                    {
                        "threshold": 0.5,
                        "total_cases": 19,
                        "hit_rate": 0.7368,
                        "citation_match_rate": 0.7368,
                        "empty_handling_rate": 0.2857,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    try:
        export_qdrant_threshold_recommendation(
            sweep_path=sweep_path,
            output_dir=tmp_path,
        )
    except ValueError as error:
        assert "No threshold satisfies" in str(error)
    else:
        raise AssertionError("Expected recommendation to fail when gates are unmet")
