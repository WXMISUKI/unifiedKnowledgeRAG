import json
from pathlib import Path

from app.config import Settings

from app.services.retrieval_benchmark import (
    benchmark_report_to_dict,
    candidate_evaluation_to_dict,
    default_embedding_candidates,
    embedding_candidate_result_to_dict,
    EmbeddingCandidate,
    evaluate_retrieval_candidates,
    evaluate_embedding_candidates,
    export_benchmark_report_json,
    export_benchmark_report_markdown,
    load_benchmark_cases,
    render_embedding_candidate_markdown,
    render_benchmark_report_markdown,
    RetrievalCandidate,
    run_retrieval_benchmark,
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
        "empty-membership-points",
        "empty-invoice-tax-policy",
    ]
    assert cases[0].expected_citation == "refund_policy_2026#section-3"
    assert cases[-1].expect_empty is True
    assert cases[-1].category == "empty"


def test_fixture_backend_benchmark_reports_success_metrics():
    cases = load_benchmark_cases(FIXTURE_PATH)
    report = run_retrieval_benchmark(cases, Settings(rag_retrieval_backend="fixture"))

    assert report.summary.backend == "fixture"
    assert report.summary.total_cases == 15
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
    assert summaries["empty"]["total_cases"] == 3
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
    assert payload["summary"]["category_summaries"]["empty"]["total_cases"] == 3
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
