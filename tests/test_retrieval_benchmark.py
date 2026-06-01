import json
from dataclasses import replace
from pathlib import Path

from app.config import Settings
from app.models.contracts import EvidenceDocument

from app.services.retrieval_benchmark import (
    apply_alias_aware_identifier_gate,
    apply_exact_identifier_containment_gate,
    apply_source_document_identifier_aggregation,
    benchmark_report_to_dict,
    candidate_evaluation_to_dict,
    default_embedding_candidates,
    default_chunking_strategy_candidates,
    default_evidence_grading_candidates,
    default_query_rewrite_candidates,
    evidence_grading_candidate_evaluation_to_dict,
    embedding_candidate_result_to_dict,
    EmbeddingCandidate,
    export_identifier_alias_governance_evidence,
    export_chunking_strategy_evaluation,
    export_chinese_seed_evidence_bundle,
    export_evidence_grading_candidate_evaluation,
    export_query_rewrite_candidate_evaluation,
    export_qdrant_bge_chunking_comparison_evidence,
    export_qdrant_bge_exact_term_smoke_evidence,
    export_qdrant_bge_hybrid_empty_stress_evidence,
    export_qdrant_bge_hybrid_alias_gating_candidate_evidence,
    export_qdrant_bge_hybrid_exact_term_smoke_evidence,
    export_qdrant_bge_hybrid_gating_candidate_evidence,
    export_qdrant_bge_hybrid_multi_chunk_aggregation_evidence,
    export_qdrant_bge_hybrid_relation_aggregation_grading_evidence,
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
    extract_alias_aware_identifiers,
    identifier_alias_governance_to_dict,
    load_identifier_alias_catalog,
    query_rewrite_candidate_evaluation_to_dict,
    relation_aware_aggregation_grading_candidates,
    RetrievalCandidate,
    run_retrieval_benchmark,
    ThresholdRecommendationGates,
    chunking_strategy_evaluation_to_dict,
    qdrant_chunking_comparison_to_dict,
    qdrant_hybrid_gating_evidence_to_dict,
    qdrant_threshold_recommendation_to_dict,
    qdrant_threshold_sweep_evidence_to_dict,
)


FIXTURE_PATH = Path("tests/fixtures/retrieval_benchmark_cases.json")
EVIDENCE_GRADING_STRESS_PATH = Path(
    "tests/fixtures/evidence_grading_stress_cases.json"
)
EXACT_TERM_IDENTIFIER_PATH = Path(
    "tests/fixtures/exact_term_identifier_cases.json"
)
HYBRID_EMPTY_STRESS_PATH = Path("tests/fixtures/hybrid_empty_stress_cases.json")
HYBRID_GATING_POSITIVE_PATH = Path(
    "tests/fixtures/hybrid_gating_positive_cases.json"
)
HYBRID_GATING_EMPTY_EXPANDED_PATH = Path(
    "tests/fixtures/hybrid_gating_empty_expanded_cases.json"
)
NOISY_IDENTIFIER_POSITIVE_PATH = Path(
    "tests/fixtures/noisy_identifier_positive_cases.json"
)
NOISY_IDENTIFIER_EMPTY_PATH = Path("tests/fixtures/noisy_identifier_empty_cases.json")
SPLIT_CHUNK_IDENTIFIER_PATH = Path("tests/fixtures/split_chunk_identifier_cases.json")
MULTI_CHUNK_AGGREGATION_NEGATIVE_PATH = Path(
    "tests/fixtures/multi_chunk_aggregation_negative_cases.json"
)
NO_BENCHMARK_CASES_PATH = Path("tests/fixtures/no_benchmark_cases.json")


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
        "refund-high-value-review-customer-like",
        "empty-datacenter-temperature-alert",
        "empty-social-security-reconciliation",
        "refund-high-value-review-audit-trace-customer-like",
        "refund-high-value-review-customer-like-audit-trace-2",
        "logistics-exact-id-customer-like",
        "empty-refund-high-value-auto-compensation",
        "empty-refund-high-value-auto-compensation-customer-like-2",
        "refund-high-value-review-customer-like-v2",
        "logistics-exact-id-customer-like-v2",
        "empty-refund-high-value-cross-train-v2",
    ]
    assert cases[0].expected_citation == "refund_policy_2026#section-3"
    assert cases[-1].expect_empty is True
    assert cases[-1].category == "empty"


def test_fixture_backend_benchmark_reports_success_metrics():
    cases = load_benchmark_cases(FIXTURE_PATH)
    report = run_retrieval_benchmark(cases, Settings(rag_retrieval_backend="fixture"))

    assert report.summary.backend == "fixture"
    assert report.summary.total_cases == 32
    assert report.summary.hit_rate == 0.9062
    assert report.summary.citation_match_rate == 0.9062
    assert report.summary.empty_handling_rate == 0.75
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
    assert summaries["policy-nuance"]["total_cases"] == 4
    assert summaries["paraphrase"]["total_cases"] == 2
    assert summaries["operational-escalation"]["total_cases"] == 2
    assert summaries["long-section"]["total_cases"] == 2
    assert summaries["identifier-noise"]["total_cases"] == 2
    assert summaries["empty"]["total_cases"] == 12
    assert summaries["empty"]["empty_handling_rate"] == 0.75


def test_exports_benchmark_report_json(tmp_path):
    cases = load_benchmark_cases(FIXTURE_PATH)
    report = run_retrieval_benchmark(cases, Settings(rag_retrieval_backend="fixture"))
    output_path = tmp_path / "reports" / "benchmark.json"

    exported_path = export_benchmark_report_json(report, output_path)
    payload = json.loads(exported_path.read_text(encoding="utf-8"))

    assert exported_path == output_path
    assert payload == benchmark_report_to_dict(report)
    assert payload["summary"]["backend"] == "fixture"
    assert payload["summary"]["category_summaries"]["empty"]["total_cases"] == 12
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
    assert all(evaluation.report.summary.hit_rate == 0.9062 for evaluation in evaluations)
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


def test_relation_aware_aggregation_grading_candidate_is_local_only():
    candidates = relation_aware_aggregation_grading_candidates()

    assert [candidate.id for candidate in candidates] == [
        "relation-aware-aggregation-grader-v1"
    ]
    assert candidates[0].grading_policy == "relation_aware_identifier"
    assert "Does not call an LLM" in candidates[0].risk_notes[1]


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

    assert citation_result.total_cases == 32
    assert citation_result.answer_bearing_rate == 0.9062
    assert citation_result.related_insufficient_count == 0
    assert citation_result.missing_evidence_count == 0
    assert citation_result.unexpected_evidence_count == 3
    assert citation_result.expected_empty_pass_rate == 0.75
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
    assert by_id["source-match-grader-v1"].answer_bearing_rate == 0.9062


def test_loads_evidence_grading_stress_cases_separately():
    baseline_cases = load_benchmark_cases(FIXTURE_PATH)
    stress_cases = load_benchmark_cases(EVIDENCE_GRADING_STRESS_PATH)

    assert len(baseline_cases) == 32
    assert [case.id for case in stress_cases] == [
        "stress-refund-source-but-wrong-citation",
        "stress-missing-evidence-unmatched-vocabulary",
        "stress-unexpected-evidence-membership-refund-overlap",
    ]
    assert {case.category for case in stress_cases} == {
        "insufficient-evidence",
        "missing-evidence",
        "unexpected-evidence",
    }


def test_loads_exact_term_identifier_cases_separately():
    baseline_cases = load_benchmark_cases(FIXTURE_PATH)
    exact_cases = load_benchmark_cases(EXACT_TERM_IDENTIFIER_PATH)

    assert len(baseline_cases) == 32
    assert [case.id for case in exact_cases] == [
        "exact-refund-policy-code",
        "exact-refund-form-name",
        "exact-logistics-workflow-acronym",
        "exact-logistics-order-id",
    ]
    assert {case.category for case in exact_cases} == {
        "policy-code",
        "form-name",
        "workflow-acronym",
        "order-like-id",
    }


def test_loads_hybrid_empty_stress_cases_separately():
    baseline_cases = load_benchmark_cases(FIXTURE_PATH)
    exact_cases = load_benchmark_cases(EXACT_TERM_IDENTIFIER_PATH)
    stress_cases = load_benchmark_cases(HYBRID_EMPTY_STRESS_PATH)

    assert len(baseline_cases) == 32
    assert len(exact_cases) == 4
    assert [case.id for case in stress_cases] == [
        "hybrid-empty-fake-refund-form",
        "hybrid-empty-fake-refund-policy-code",
        "hybrid-empty-fake-logistics-workflow",
        "hybrid-empty-fake-order-id",
    ]
    assert all(case.expect_empty for case in stress_cases)
    assert {case.category for case in stress_cases} == {
        "hybrid-empty-form-name",
        "hybrid-empty-policy-code",
        "hybrid-empty-workflow-acronym",
        "hybrid-empty-order-like-id",
    }


def test_loads_expanded_hybrid_gating_cases_separately():
    positive_cases = load_benchmark_cases(HYBRID_GATING_POSITIVE_PATH)
    empty_cases = load_benchmark_cases(HYBRID_GATING_EMPTY_EXPANDED_PATH)

    assert [case.id for case in positive_cases] == [
        "hybrid-gating-positive-refund-multi-id",
        "hybrid-gating-positive-logistics-multi-id",
        "hybrid-gating-positive-refund-contextual-id",
    ]
    assert all(not case.expect_empty for case in positive_cases)
    assert {case.category for case in positive_cases} == {
        "hybrid-gating-multi-id",
        "hybrid-gating-contextual-id",
    }
    assert [case.id for case in empty_cases] == [
        "hybrid-gating-empty-partial-refund-form",
        "hybrid-gating-empty-partial-refund-policy",
        "hybrid-gating-empty-partial-logistics-workflow",
        "hybrid-gating-empty-same-prefix-order",
    ]
    assert all(case.expect_empty for case in empty_cases)
    assert {case.category for case in empty_cases} == {
        "hybrid-gating-partial-id",
        "hybrid-gating-same-prefix-id",
    }


def test_loads_noisy_identifier_cases_separately():
    positive_cases = load_benchmark_cases(NOISY_IDENTIFIER_POSITIVE_PATH)
    empty_cases = load_benchmark_cases(NOISY_IDENTIFIER_EMPTY_PATH)

    assert [case.id for case in positive_cases] == [
        "noisy-positive-refund-policy-ocr",
        "noisy-positive-refund-form-chinese-alias",
        "noisy-positive-logistics-workflow-chinese-alias",
        "noisy-positive-logistics-order-ocr-spacing",
    ]
    assert all(not case.expect_empty for case in positive_cases)
    assert {case.category for case in positive_cases} == {
        "noisy-identifier-ocr",
        "noisy-identifier-alias",
    }
    assert [case.id for case in empty_cases] == [
        "noisy-empty-refund-form-chinese-alias",
        "noisy-empty-refund-policy-ocr",
        "noisy-empty-logistics-workflow-chinese-alias",
        "noisy-empty-logistics-order-ocr-spacing",
    ]
    assert all(case.expect_empty for case in empty_cases)
    assert {case.category for case in empty_cases} == {
        "noisy-identifier-empty-alias",
        "noisy-identifier-empty-ocr",
    }


def test_loads_split_chunk_identifier_cases_separately():
    cases = load_benchmark_cases(SPLIT_CHUNK_IDENTIFIER_PATH)

    assert [case.id for case in cases] == ["split-chunk-refund-policy-and-form"]
    assert cases[0].knowledge_base_ids == ["split_refund_policy_docs"]
    assert cases[0].expected_citation == "split_refund_policy_2026#form-code"
    assert cases[0].expect_empty is False


def test_loads_multi_chunk_aggregation_negative_cases_separately():
    positive_cases = load_benchmark_cases(SPLIT_CHUNK_IDENTIFIER_PATH)
    negative_cases = load_benchmark_cases(MULTI_CHUNK_AGGREGATION_NEGATIVE_PATH)

    assert len(positive_cases) == 1
    assert [case.id for case in negative_cases] == [
        "multi-chunk-empty-unsupported-form-policy-link"
    ]
    assert negative_cases[0].knowledge_base_ids == ["split_refund_policy_docs"]
    assert negative_cases[0].expected_source_id is None
    assert negative_cases[0].expected_citation is None
    assert negative_cases[0].expect_empty is True


def test_exact_term_identifier_cases_pass_fixture_backend():
    exact_cases = load_benchmark_cases(EXACT_TERM_IDENTIFIER_PATH)

    report = run_retrieval_benchmark(
        exact_cases,
        Settings(rag_retrieval_backend="fixture"),
    )

    assert report.summary.total_cases == 4
    assert report.summary.hit_rate == 1.0
    assert report.summary.citation_match_rate == 1.0
    assert report.summary.empty_handling_rate == 0.0
    assert report.cases[0].returned_citations[0] == "refund_policy_2026#exact-refund-code"
    assert report.cases[-1].returned_citations[0] == "logistics_faq_2026#exact-logistics-id"


def test_evidence_grading_stress_cases_expose_failure_labels():
    stress_cases = load_benchmark_cases(EVIDENCE_GRADING_STRESS_PATH)

    evaluation = evaluate_evidence_grading_candidates(
        cases=stress_cases,
        settings=Settings(rag_retrieval_backend="fixture"),
    )

    by_id = {result.candidate.id: result for result in evaluation.results}
    strict = by_id["citation-match-grader-v1"]
    loose = by_id["source-match-grader-v1"]
    strict_labels = {case.case_id: case.grading_label for case in strict.cases}
    loose_labels = {case.case_id: case.grading_label for case in loose.cases}

    assert strict_labels == {
        "stress-refund-source-but-wrong-citation": "related_insufficient",
        "stress-missing-evidence-unmatched-vocabulary": "missing_evidence",
        "stress-unexpected-evidence-membership-refund-overlap": "unexpected_evidence",
    }
    assert loose_labels["stress-refund-source-but-wrong-citation"] == "answer_bearing"
    assert loose_labels["stress-missing-evidence-unmatched-vocabulary"] == "missing_evidence"
    assert loose_labels["stress-unexpected-evidence-membership-refund-overlap"] == "unexpected_evidence"
    assert strict.related_insufficient_count == 1
    assert strict.missing_evidence_count == 1
    assert strict.unexpected_evidence_count == 1
    assert strict.answer_bearing_rate == 0.0
    assert loose.answer_bearing_rate == 0.3333


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
    assert result.report.summary.hit_rate == 0.9062
    assert result.report.summary.citation_match_rate == 0.9062
    assert result.report.summary.empty_handling_rate == 0.75
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
    assert bundle.retrieval_evaluations[0].report.summary.total_cases == 32
    assert bundle.retrieval_evaluations[0].report.summary.hit_rate == 0.9062
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
    assert retrieval_payload["report"]["summary"]["total_cases"] == 32

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
        "政策编号 RFD-2026-003 适用于三天未发货退款复核。\n\n"
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
        "工作流缩写 LST-BATCH-OPS 是批量物流异常升级代号。\n\n"
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
    assert by_id["markdown-paragraph-v1"].total_chunks == 13
    assert by_id["markdown-paragraph-v1"].citation_stability == "stable"
    assert by_id["markdown-paragraph-v1"].long_section_support == "covered"
    assert by_id["markdown-section-v1"].total_chunks == 2
    assert by_id["markdown-section-v1"].citation_stability == "stable"
    assert by_id["markdown-section-v1"].long_section_support == "covered-by-section"
    assert by_id["token-window-v1"].total_chunks == 3
    assert by_id["token-window-v1"].citation_stability == "stable"
    assert by_id["token-window-v1"].long_section_support == "covered-by-window"

    payload = json.loads(evaluation.json_path.read_text(encoding="utf-8"))
    markdown = evaluation.markdown_path.read_text(encoding="utf-8")

    assert payload == chunking_strategy_evaluation_to_dict(evaluation)
    assert "# Chunking Strategy Candidate Evaluation" in markdown
    assert "| markdown-paragraph-v1 | implemented | 13 | stable | covered |" in markdown
    assert "| markdown-section-v1 | runnable | 2 | stable | covered-by-section |" in markdown
    assert "| token-window-v1 | runnable | 3 | stable | covered-by-window |" in markdown
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


def test_export_qdrant_bge_exact_term_smoke_evidence_uses_named_outputs(
    monkeypatch,
    tmp_path,
):
    from tests.test_qdrant_vector_store import FakeQdrantClient

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n"
        "客户三天未发货可以申请退款。\n\n"
        "退款处理需要保留订单编号。\n\n"
        "政策编号 RFD-2026-003 适用于三天未发货退款复核；售后专员需填写表单 AF-REFUND-02。",
        encoding="utf-8",
    )
    cases_path = tmp_path / "exact-cases.json"
    cases_path.write_text(
        """
[
  {
    "id": "exact-refund-policy-code",
    "category": "policy-code",
    "difficulty": "medium",
    "query": "RFD-2026-003 对应哪类退款复核？",
    "knowledge_base_ids": ["refund_policy_docs"],
    "top_k": 1,
    "expected_source_id": "refund_policy_docs",
    "expected_citation": "refund_policy_2026#exact-refund-code",
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
                "score": 0.93,
                "payload": {
                    "source_id": "refund_policy_docs",
                    "document_id": "refund_policy_2026",
                    "title": "售后退款规则",
                    "text": "政策编号 RFD-2026-003 适用于三天未发货退款复核。",
                    "citation": "refund_policy_2026#exact-refund-code",
                },
            }
        ],
    )
    monkeypatch.setattr(
        "app.services.retrieval_benchmark.create_qdrant_client",
        lambda settings: fake_client,
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

    report = export_qdrant_bge_exact_term_smoke_evidence(
        output_dir=tmp_path / "evidence",
        cases_path=cases_path,
        source_ids=["refund_policy_docs"],
        settings=settings,
    )

    assert report.candidate.id == "qdrant-bge-m3-exact-term-smoke"
    assert report.json_path == tmp_path / "evidence" / "qdrant-bge-m3-exact-term-smoke.json"
    assert report.markdown_path == tmp_path / "evidence" / "qdrant-bge-m3-exact-term-smoke.md"
    assert report.metadata["benchmark_fixture"] == "exact-term-identifier-v1"
    assert report.metadata["benchmark_cases_path"] == str(cases_path)
    assert report.report.summary.hit_rate == 1.0
    assert report.report.summary.citation_match_rate == 1.0
    assert "qdrant-bge-m3-exact-term-smoke" in report.markdown_path.read_text(
        encoding="utf-8"
    )


def test_export_qdrant_bge_hybrid_exact_term_smoke_evidence_uses_named_outputs(
    monkeypatch,
    tmp_path,
):
    from tests.test_qdrant_vector_store import FakeQdrantClient

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n"
        "客户三天未发货可以申请退款。\n\n"
        "退款处理需要保留订单编号。\n\n"
        "政策编号 RFD-2026-003 适用于三天未发货退款复核；售后专员需填写表单 AF-REFUND-02。",
        encoding="utf-8",
    )
    cases_path = tmp_path / "exact-cases.json"
    cases_path.write_text(
        """
[
  {
    "id": "exact-refund-form-name",
    "category": "form-name",
    "difficulty": "medium",
    "query": "AF-REFUND-02 表单需要关联哪些付款凭证？",
    "knowledge_base_ids": ["refund_policy_docs"],
    "top_k": 1,
    "expected_source_id": "refund_policy_docs",
    "expected_citation": "refund_policy_2026#exact-refund-code",
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
                "score": 1.0,
                "payload": {
                    "source_id": "refund_policy_docs",
                    "document_id": "refund_policy_2026",
                    "title": "售后退款规则",
                    "text": "表单 AF-REFUND-02 需要关联付款凭证。",
                    "citation": "refund_policy_2026#exact-refund-code",
                },
            }
        ],
    )
    monkeypatch.setattr(
        "app.services.retrieval_benchmark.create_qdrant_client",
        lambda settings: fake_client,
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

    report = export_qdrant_bge_hybrid_exact_term_smoke_evidence(
        output_dir=tmp_path / "evidence",
        cases_path=cases_path,
        source_ids=["refund_policy_docs"],
        settings=settings,
    )

    assert report.candidate.id == "qdrant-bge-m3-hybrid-exact-term-smoke"
    assert report.json_path == (
        tmp_path / "evidence" / "qdrant-bge-m3-hybrid-exact-term-smoke.json"
    )
    assert report.markdown_path == (
        tmp_path / "evidence" / "qdrant-bge-m3-hybrid-exact-term-smoke.md"
    )
    assert report.metadata["retrieval_mode"] == "dense+sparse-hybrid"
    assert report.metadata["sparse_vectorizer"] == "lexical-identifier-sparse-v1"
    assert report.metadata["fusion"] == "rrf"
    assert report.indexed_sources["refund_policy_docs"]["sparse_vector_name"] == (
        "text-sparse"
    )
    assert report.report.summary.backend == "qdrant-hybrid"
    assert report.report.summary.citation_match_rate == 1.0
    assert "qdrant-bge-m3-hybrid-exact-term-smoke" in (
        report.markdown_path.read_text(encoding="utf-8")
    )


def test_export_qdrant_bge_hybrid_empty_stress_evidence_records_false_positive(
    monkeypatch,
    tmp_path,
):
    from tests.test_qdrant_vector_store import FakeQdrantClient

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n"
        "客户三天未发货可以申请退款。\n\n"
        "退款处理需要保留订单编号。\n\n"
        "政策编号 RFD-2026-003 适用于三天未发货退款复核；售后专员需填写表单 AF-REFUND-02。",
        encoding="utf-8",
    )
    cases_path = tmp_path / "hybrid-empty-cases.json"
    cases_path.write_text(
        """
[
  {
    "id": "hybrid-empty-fake-refund-form",
    "category": "hybrid-empty-form-name",
    "difficulty": "hard",
    "query": "AF-REFUND-99 表单用于线下补贴退款吗？",
    "knowledge_base_ids": ["refund_policy_docs"],
    "top_k": 1,
    "expected_source_id": null,
    "expected_citation": null,
    "expect_empty": true
  }
]
""",
        encoding="utf-8",
    )
    fake_client = FakeQdrantClient(
        collection_exists=False,
        hits=[
            {
                "score": 1.0,
                "payload": {
                    "source_id": "refund_policy_docs",
                    "document_id": "refund_policy_2026",
                    "title": "售后退款规则",
                    "text": "表单 AF-REFUND-02 需要关联付款凭证。",
                    "citation": "refund_policy_2026#exact-refund-code",
                },
            }
        ],
    )
    monkeypatch.setattr(
        "app.services.retrieval_benchmark.create_qdrant_client",
        lambda settings: fake_client,
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

    report = export_qdrant_bge_hybrid_empty_stress_evidence(
        output_dir=tmp_path / "evidence",
        cases_path=cases_path,
        source_ids=["refund_policy_docs"],
        settings=settings,
    )

    assert report.candidate.id == "qdrant-bge-m3-hybrid-empty-stress"
    assert report.json_path == (
        tmp_path / "evidence" / "qdrant-bge-m3-hybrid-empty-stress.json"
    )
    assert report.markdown_path == (
        tmp_path / "evidence" / "qdrant-bge-m3-hybrid-empty-stress.md"
    )
    assert report.metadata["benchmark_fixture"] == "hybrid-empty-stress-v1"
    assert report.metadata["retrieval_mode"] == "dense+sparse-hybrid"
    assert report.report.summary.empty_handling_rate == 0.0
    assert report.report.cases[0].empty_query_handling is False
    assert report.report.cases[0].returned_citations == [
        "refund_policy_2026#exact-refund-code"
    ]
    assert "qdrant-bge-m3-hybrid-empty-stress" in (
        report.markdown_path.read_text(encoding="utf-8")
    )


def test_exact_identifier_gate_filters_unsupported_identifier_hits():
    documents = [
        EvidenceDocument(
            source_id="refund_policy_docs",
            document_id="refund_policy_2026",
            title="售后退款规则",
            snippet="表单 AF-REFUND-02 需要关联付款凭证。",
            score=1.0,
            citation="refund_policy_2026#exact-refund-code",
        )
    ]

    retained, identifiers, applied = apply_exact_identifier_containment_gate(
        "AF-REFUND-02 表单需要关联哪些付款凭证？",
        documents,
    )
    filtered, fake_identifiers, fake_applied = apply_exact_identifier_containment_gate(
        "AF-REFUND-99 表单用于线下补贴退款吗？",
        documents,
    )

    assert retained == documents
    assert identifiers == ["af-refund-02"]
    assert applied is True
    assert filtered == []
    assert fake_identifiers == ["af-refund-99"]
    assert fake_applied is True


def test_exact_identifier_gate_filters_partial_identifier_substrings():
    documents = [
        EvidenceDocument(
            source_id="refund_policy_docs",
            document_id="refund_policy_2026",
            title="售后退款规则",
            snippet="表单 AF-REFUND-02 需要关联付款凭证。",
            score=1.0,
            citation="refund_policy_2026#exact-refund-code",
        )
    ]

    filtered, identifiers, applied = apply_exact_identifier_containment_gate(
        "AF-REFUND 表单可以直接作为线下补贴退款依据吗？",
        documents,
    )

    assert identifiers == ["af-refund"]
    assert applied is True
    assert filtered == []


def test_alias_aware_identifier_extraction_normalizes_ocr_and_aliases():
    assert extract_alias_aware_identifiers("RFD-2O26-OO3") == ["rfd-2026-003"]
    assert extract_alias_aware_identifiers("AF退款02") == ["af-refund-02"]
    assert extract_alias_aware_identifiers("LST批量OPS") == ["lst-batch-ops"]
    assert extract_alias_aware_identifiers("ORD ZS 2O26 0007") == [
        "ord-zs-2026-0007"
    ]


def test_identifier_alias_catalog_exports_governance_evidence(tmp_path):
    aliases = load_identifier_alias_catalog()

    report = export_identifier_alias_governance_evidence(tmp_path / "alias-governance")
    payload = identifier_alias_governance_to_dict(report)

    assert {alias.id for alias in aliases} >= {
        "af-refund-chinese-shorthand",
        "rfd-compact-ocr",
        "lst-batch-chinese-shorthand",
        "ord-zs-compact-ocr",
    }
    assert report.json_path == (
        tmp_path / "alias-governance" / "identifier-alias-governance.json"
    )
    assert report.markdown_path == (
        tmp_path / "alias-governance" / "identifier-alias-governance.md"
    )
    assert payload["summary"]["total_aliases"] == len(aliases)
    assert payload["summary"]["status_counts"]["candidate"] == len(aliases)
    assert "production alias service" in report.decision_notes[0]
    assert "af-refund-chinese-shorthand" in report.markdown_path.read_text(
        encoding="utf-8"
    )


def test_alias_aware_identifier_gate_keeps_alias_and_filters_wrong_aliases():
    documents = [
        EvidenceDocument(
            source_id="refund_policy_docs",
            document_id="refund_policy_2026",
            title="售后退款规则",
            snippet=(
                "政策编号 RFD-2026-003 适用于三天未发货退款复核；"
                "售后专员需填写表单 AF-REFUND-02。"
            ),
            score=1.0,
            citation="refund_policy_2026#exact-refund-code",
        )
    ]

    retained, identifiers, applied = apply_alias_aware_identifier_gate(
        "AF退款02 表单需要关联哪些付款凭证？",
        documents,
    )
    filtered, fake_identifiers, fake_applied = apply_alias_aware_identifier_gate(
        "AF退款99 表单用于线下补贴退款吗？",
        documents,
    )

    assert retained == documents
    assert identifiers == ["af-refund-02"]
    assert applied is True
    assert filtered == []
    assert fake_identifiers == ["af-refund-99"]
    assert fake_applied is True


def test_export_qdrant_bge_hybrid_gating_candidate_evidence_keeps_raw_and_gated(
    monkeypatch,
    tmp_path,
):
    from tests.test_qdrant_vector_store import FakeQdrantClient

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n"
        "政策编号 RFD-2026-003 适用于三天未发货退款复核；售后专员需填写表单 AF-REFUND-02。",
        encoding="utf-8",
    )
    exact_cases_path = tmp_path / "exact-cases.json"
    exact_cases_path.write_text(
        """
[
  {
    "id": "exact-refund-form-name",
    "category": "form-name",
    "difficulty": "medium",
    "query": "AF-REFUND-02 表单需要关联哪些付款凭证？",
    "knowledge_base_ids": ["refund_policy_docs"],
    "top_k": 1,
    "expected_source_id": "refund_policy_docs",
    "expected_citation": "refund_policy_2026#exact-refund-code",
    "expect_empty": false
  }
]
""",
        encoding="utf-8",
    )
    empty_cases_path = tmp_path / "empty-cases.json"
    empty_cases_path.write_text(
        """
[
  {
    "id": "hybrid-empty-fake-refund-form",
    "category": "hybrid-empty-form-name",
    "difficulty": "hard",
    "query": "AF-REFUND-99 表单用于线下补贴退款吗？",
    "knowledge_base_ids": ["refund_policy_docs"],
    "top_k": 1,
    "expected_source_id": null,
    "expected_citation": null,
    "expect_empty": true
  }
]
""",
        encoding="utf-8",
    )
    fake_client = FakeQdrantClient(
        collection_exists=False,
        hits=[
            {
                "score": 1.0,
                "payload": {
                    "source_id": "refund_policy_docs",
                    "document_id": "refund_policy_2026",
                    "title": "售后退款规则",
                    "text": "表单 AF-REFUND-02 需要关联付款凭证。",
                    "citation": "refund_policy_2026#exact-refund-code",
                },
            }
        ],
    )
    monkeypatch.setattr(
        "app.services.retrieval_benchmark.create_qdrant_client",
        lambda settings: fake_client,
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

    report = export_qdrant_bge_hybrid_gating_candidate_evidence(
        output_dir=tmp_path / "evidence",
        exact_cases_path=exact_cases_path,
        empty_cases_path=empty_cases_path,
        source_ids=["refund_policy_docs"],
        settings=settings,
    )
    payload = qdrant_hybrid_gating_evidence_to_dict(report)

    assert report.candidate.id == "qdrant-bge-m3-hybrid-exact-identifier-gate"
    assert report.json_path == (
        tmp_path / "evidence" / "qdrant-bge-m3-hybrid-exact-identifier-gate.json"
    )
    assert report.markdown_path == (
        tmp_path / "evidence" / "qdrant-bge-m3-hybrid-exact-identifier-gate.md"
    )
    assert report.metadata["gating_policy"] == "exact-identifier-containment-gate-v1"
    assert report.report.summary.hit_rate == 1.0
    assert report.report.summary.citation_match_rate == 1.0
    assert report.report.summary.empty_handling_rate == 1.0
    assert report.cases[0].raw_returned_citations == [
        "refund_policy_2026#exact-refund-code"
    ]
    assert report.cases[1].raw_returned_citations == [
        "refund_policy_2026#exact-refund-code"
    ]
    assert report.cases[1].gated_result.returned_citations == []
    assert payload["cases"][1]["query_identifiers"] == ["af-refund-99"]
    assert "Raw And Gated Case Results" in report.markdown_path.read_text(
        encoding="utf-8"
    )


def test_export_qdrant_bge_hybrid_alias_gating_candidate_evidence(
    monkeypatch,
    tmp_path,
):
    from tests.test_qdrant_vector_store import FakeQdrantClient

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n"
        "政策编号 RFD-2026-003 适用于三天未发货退款复核；售后专员需填写表单 AF-REFUND-02。",
        encoding="utf-8",
    )
    positive_cases_path = tmp_path / "positive-cases.json"
    positive_cases_path.write_text(
        """
[
  {
    "id": "noisy-positive-refund-form-chinese-alias",
    "category": "noisy-identifier-alias",
    "difficulty": "hard",
    "query": "AF退款02 表单需要关联哪些付款凭证？",
    "knowledge_base_ids": ["refund_policy_docs"],
    "top_k": 1,
    "expected_source_id": "refund_policy_docs",
    "expected_citation": "refund_policy_2026#exact-refund-code",
    "expect_empty": false
  }
]
""",
        encoding="utf-8",
    )
    empty_cases_path = tmp_path / "empty-cases.json"
    empty_cases_path.write_text(
        """
[
  {
    "id": "noisy-empty-refund-form-chinese-alias",
    "category": "noisy-identifier-empty-alias",
    "difficulty": "hard",
    "query": "AF退款99 表单用于线下补贴退款吗？",
    "knowledge_base_ids": ["refund_policy_docs"],
    "top_k": 1,
    "expected_source_id": null,
    "expected_citation": null,
    "expect_empty": true
  }
]
""",
        encoding="utf-8",
    )
    fake_client = FakeQdrantClient(
        collection_exists=False,
        hits=[
            {
                "score": 1.0,
                "payload": {
                    "source_id": "refund_policy_docs",
                    "document_id": "refund_policy_2026",
                    "title": "售后退款规则",
                    "text": "表单 AF-REFUND-02 需要关联付款凭证。",
                    "citation": "refund_policy_2026#exact-refund-code",
                },
            }
        ],
    )
    monkeypatch.setattr(
        "app.services.retrieval_benchmark.create_qdrant_client",
        lambda settings: fake_client,
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

    report = export_qdrant_bge_hybrid_alias_gating_candidate_evidence(
        output_dir=tmp_path / "evidence",
        positive_cases_path=positive_cases_path,
        empty_cases_path=empty_cases_path,
        source_ids=["refund_policy_docs"],
        settings=settings,
    )

    assert report.candidate.id == "qdrant-bge-m3-hybrid-alias-identifier-gate"
    assert report.json_path == (
        tmp_path / "evidence" / "qdrant-bge-m3-hybrid-alias-identifier-gate.json"
    )
    assert report.markdown_path == (
        tmp_path / "evidence" / "qdrant-bge-m3-hybrid-alias-identifier-gate.md"
    )
    assert report.metadata["gating_policy"] == "alias-aware-identifier-gate-v1"
    assert report.report.summary.hit_rate == 1.0
    assert report.report.summary.citation_match_rate == 1.0
    assert report.report.summary.empty_handling_rate == 1.0
    assert report.cases[0].query_identifiers == ["af-refund-02"]
    assert report.cases[1].query_identifiers == ["af-refund-99"]
    assert report.cases[1].gated_result.returned_citations == []


def test_export_qdrant_bge_hybrid_gating_records_split_chunk_miss(
    monkeypatch,
    tmp_path,
):
    from tests.test_qdrant_vector_store import FakeQdrantClient

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "split_refund_policy_docs.md").write_text(
        "# 拆分退款编号规则\n\n"
        "政策编号 RFD-2026-003 适用于三天未发货退款复核。\n\n"
        "复核材料需要填写表单 AF-REFUND-02，并关联付款凭证。",
        encoding="utf-8",
    )
    cases_path = tmp_path / "split-cases.json"
    cases_path.write_text(
        """
[
  {
    "id": "split-chunk-refund-policy-and-form",
    "category": "split-chunk-identifier",
    "difficulty": "hard",
    "query": "RFD-2026-003 和 AF-REFUND-02 在同一个退款复核流程中分别要求什么？",
    "knowledge_base_ids": ["split_refund_policy_docs"],
    "top_k": 2,
    "expected_source_id": "split_refund_policy_docs",
    "expected_citation": "split_refund_policy_2026#form-code",
    "expect_empty": false
  }
]
""",
        encoding="utf-8",
    )
    empty_cases_path = tmp_path / "empty-cases.json"
    empty_cases_path.write_text("[]", encoding="utf-8")
    fake_client = FakeQdrantClient(
        collection_exists=False,
        hits=[
            {
                "score": 1.0,
                "payload": {
                    "source_id": "split_refund_policy_docs",
                    "document_id": "split_refund_policy_2026",
                    "title": "拆分退款编号规则",
                    "text": "政策编号 RFD-2026-003 适用于三天未发货退款复核。",
                    "citation": "split_refund_policy_2026#policy-code",
                },
            },
            {
                "score": 1.0,
                "payload": {
                    "source_id": "split_refund_policy_docs",
                    "document_id": "split_refund_policy_2026",
                    "title": "拆分退款编号规则",
                    "text": "复核材料需要填写表单 AF-REFUND-02，并关联付款凭证。",
                    "citation": "split_refund_policy_2026#form-code",
                },
            },
        ],
    )
    monkeypatch.setattr(
        "app.services.retrieval_benchmark.create_qdrant_client",
        lambda settings: fake_client,
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

    report = export_qdrant_bge_hybrid_gating_candidate_evidence(
        output_dir=tmp_path / "evidence",
        exact_cases_path=cases_path,
        empty_cases_path=empty_cases_path,
        source_ids=["split_refund_policy_docs"],
        settings=settings,
    )

    assert report.report.summary.hit_rate == 0.0
    assert report.report.summary.citation_match_rate == 0.0
    assert report.cases[0].raw_returned_citations == [
        "split_refund_policy_2026#policy-code",
        "split_refund_policy_2026#form-code",
    ]
    assert report.cases[0].query_identifiers == [
        "af-refund-02",
        "rfd-2026-003",
    ]
    assert report.cases[0].gated_result.returned_citations == []


def test_source_document_identifier_aggregation_recovers_split_chunks():
    documents = [
        EvidenceDocument(
            source_id="split_refund_policy_docs",
            document_id="split_refund_policy_2026",
            title="拆分退款编号规则",
            snippet="政策编号 RFD-2026-003 适用于三天未发货退款复核。",
            score=1.0,
            citation="split_refund_policy_2026#policy-code",
        ),
        EvidenceDocument(
            source_id="split_refund_policy_docs",
            document_id="split_refund_policy_2026",
            title="拆分退款编号规则",
            snippet="复核材料需要填写表单 AF-REFUND-02，并关联付款凭证。",
            score=1.0,
            citation="split_refund_policy_2026#form-code",
        ),
        EvidenceDocument(
            source_id="refund_policy_docs",
            document_id="refund_policy_2026",
            title="售后退款规则",
            snippet="政策编号 RFD-2026-003 适用于普通退款。",
            score=0.9,
            citation="refund_policy_2026#exact-refund-code",
        ),
    ]

    retained, identifiers, applied = apply_source_document_identifier_aggregation(
        "RFD-2026-003 和 AF-REFUND-02 分别要求什么？",
        documents,
    )

    assert applied is True
    assert identifiers == ["af-refund-02", "rfd-2026-003"]
    assert [document.citation for document in retained] == [
        "split_refund_policy_2026#policy-code",
        "split_refund_policy_2026#form-code",
    ]


def test_export_qdrant_bge_hybrid_multi_chunk_aggregation_recovers_split_chunks(
    monkeypatch,
    tmp_path,
):
    from tests.test_qdrant_vector_store import FakeQdrantClient

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "split_refund_policy_docs.md").write_text(
        "# 拆分退款编号规则\n\n"
        "政策编号 RFD-2026-003 适用于三天未发货退款复核。\n\n"
        "复核材料需要填写表单 AF-REFUND-02，并关联付款凭证。",
        encoding="utf-8",
    )
    cases_path = tmp_path / "split-cases.json"
    cases_path.write_text(
        """
[
  {
    "id": "split-chunk-refund-policy-and-form",
    "category": "split-chunk-identifier",
    "difficulty": "hard",
    "query": "RFD-2026-003 和 AF-REFUND-02 在同一个退款复核流程中分别要求什么？",
    "knowledge_base_ids": ["split_refund_policy_docs"],
    "top_k": 2,
    "expected_source_id": "split_refund_policy_docs",
    "expected_citation": "split_refund_policy_2026#form-code",
    "expect_empty": false
  }
]
""",
        encoding="utf-8",
    )
    empty_cases_path = tmp_path / "empty-cases.json"
    empty_cases_path.write_text("[]", encoding="utf-8")
    fake_client = FakeQdrantClient(
        collection_exists=False,
        hits=[
            {
                "score": 1.0,
                "payload": {
                    "source_id": "split_refund_policy_docs",
                    "document_id": "split_refund_policy_2026",
                    "title": "拆分退款编号规则",
                    "text": "政策编号 RFD-2026-003 适用于三天未发货退款复核。",
                    "citation": "split_refund_policy_2026#policy-code",
                },
            },
            {
                "score": 1.0,
                "payload": {
                    "source_id": "split_refund_policy_docs",
                    "document_id": "split_refund_policy_2026",
                    "title": "拆分退款编号规则",
                    "text": "复核材料需要填写表单 AF-REFUND-02，并关联付款凭证。",
                    "citation": "split_refund_policy_2026#form-code",
                },
            },
        ],
    )
    monkeypatch.setattr(
        "app.services.retrieval_benchmark.create_qdrant_client",
        lambda settings: fake_client,
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

    report = export_qdrant_bge_hybrid_multi_chunk_aggregation_evidence(
        output_dir=tmp_path / "evidence",
        cases_path=cases_path,
        empty_cases_path=empty_cases_path,
        source_ids=["split_refund_policy_docs"],
        settings=settings,
    )

    assert report.candidate.id == "qdrant-bge-m3-hybrid-multi-chunk-aggregation"
    assert report.json_path == (
        tmp_path / "evidence" / "qdrant-bge-m3-hybrid-multi-chunk-aggregation.json"
    )
    assert report.markdown_path == (
        tmp_path / "evidence" / "qdrant-bge-m3-hybrid-multi-chunk-aggregation.md"
    )
    assert report.metadata["aggregation_policy"] == (
        "source-document-identifier-coverage-v1"
    )
    assert report.report.summary.hit_rate == 1.0
    assert report.report.summary.citation_match_rate == 1.0
    assert report.cases[0].raw_returned_citations == [
        "split_refund_policy_2026#policy-code",
        "split_refund_policy_2026#form-code",
    ]
    assert report.cases[0].gated_result.returned_citations == [
        "split_refund_policy_2026#policy-code",
        "split_refund_policy_2026#form-code",
    ]


def test_export_qdrant_bge_hybrid_multi_chunk_aggregation_records_negative_control(
    monkeypatch,
    tmp_path,
):
    from tests.test_qdrant_vector_store import FakeQdrantClient

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "split_refund_policy_docs.md").write_text(
        "# 拆分退款编号规则\n\n"
        "政策编号 RFD-2026-003 适用于三天未发货退款复核。\n\n"
        "复核材料需要填写表单 AF-REFUND-02，并关联付款凭证。",
        encoding="utf-8",
    )
    cases_path = tmp_path / "split-cases.json"
    cases_path.write_text(
        """
[
  {
    "id": "split-chunk-refund-policy-and-form",
    "category": "split-chunk-identifier",
    "difficulty": "hard",
    "query": "RFD-2026-003 和 AF-REFUND-02 在同一个退款复核流程中分别要求什么？",
    "knowledge_base_ids": ["split_refund_policy_docs"],
    "top_k": 2,
    "expected_source_id": "split_refund_policy_docs",
    "expected_citation": "split_refund_policy_2026#form-code",
    "expect_empty": false
  }
]
""",
        encoding="utf-8",
    )
    empty_cases_path = tmp_path / "empty-cases.json"
    empty_cases_path.write_text(
        """
[
  {
    "id": "multi-chunk-empty-unsupported-form-policy-link",
    "category": "multi-chunk-aggregation-empty",
    "difficulty": "hard",
    "query": "AF-REFUND-02 是否可以直接覆盖 RFD-2026-003 的订单状态核验要求？",
    "knowledge_base_ids": ["split_refund_policy_docs"],
    "top_k": 2,
    "expected_source_id": null,
    "expected_citation": null,
    "expect_empty": true
  }
]
""",
        encoding="utf-8",
    )
    fake_client = FakeQdrantClient(
        collection_exists=False,
        hits=[
            {
                "score": 1.0,
                "payload": {
                    "source_id": "split_refund_policy_docs",
                    "document_id": "split_refund_policy_2026",
                    "title": "拆分退款编号规则",
                    "text": "政策编号 RFD-2026-003 适用于三天未发货退款复核。",
                    "citation": "split_refund_policy_2026#policy-code",
                },
            },
            {
                "score": 1.0,
                "payload": {
                    "source_id": "split_refund_policy_docs",
                    "document_id": "split_refund_policy_2026",
                    "title": "拆分退款编号规则",
                    "text": "复核材料需要填写表单 AF-REFUND-02，并关联付款凭证。",
                    "citation": "split_refund_policy_2026#form-code",
                },
            },
        ],
    )
    monkeypatch.setattr(
        "app.services.retrieval_benchmark.create_qdrant_client",
        lambda settings: fake_client,
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

    report = export_qdrant_bge_hybrid_multi_chunk_aggregation_evidence(
        output_dir=tmp_path / "evidence",
        cases_path=cases_path,
        empty_cases_path=empty_cases_path,
        source_ids=["split_refund_policy_docs"],
        settings=settings,
    )

    assert report.report.summary.total_cases == 2
    assert report.report.summary.hit_rate == 0.5
    assert report.report.summary.citation_match_rate == 0.5
    assert report.report.summary.empty_handling_rate == 0.0
    negative_case = report.cases[1]
    assert negative_case.expect_empty is True
    assert negative_case.raw_returned_citations == [
        "split_refund_policy_2026#policy-code",
        "split_refund_policy_2026#form-code",
    ]
    assert negative_case.gated_result.empty_query_handling is False
    assert negative_case.gated_result.returned_citations == [
        "split_refund_policy_2026#policy-code",
        "split_refund_policy_2026#form-code",
    ]


def test_export_qdrant_bge_hybrid_relation_aggregation_grading_labels_unsupported_relation(
    monkeypatch,
    tmp_path,
):
    from tests.test_qdrant_vector_store import FakeQdrantClient

    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "split_refund_policy_docs.md").write_text(
        "# 拆分退款编号规则\n\n"
        "政策编号 RFD-2026-003 适用于三天未发货退款复核。\n\n"
        "复核材料需要填写表单 AF-REFUND-02，并关联付款凭证。",
        encoding="utf-8",
    )
    cases_path = tmp_path / "split-cases.json"
    cases_path.write_text(
        """
[
  {
    "id": "split-chunk-refund-policy-and-form",
    "category": "split-chunk-identifier",
    "difficulty": "hard",
    "query": "RFD-2026-003 和 AF-REFUND-02 在同一个退款复核流程中分别要求什么？",
    "knowledge_base_ids": ["split_refund_policy_docs"],
    "top_k": 2,
    "expected_source_id": "split_refund_policy_docs",
    "expected_citation": "split_refund_policy_2026#form-code",
    "expect_empty": false
  }
]
""",
        encoding="utf-8",
    )
    empty_cases_path = tmp_path / "empty-cases.json"
    empty_cases_path.write_text(
        """
[
  {
    "id": "multi-chunk-empty-unsupported-form-policy-link",
    "category": "multi-chunk-aggregation-empty",
    "difficulty": "hard",
    "query": "AF-REFUND-02 是否可以直接覆盖 RFD-2026-003 的订单状态核验要求？",
    "knowledge_base_ids": ["split_refund_policy_docs"],
    "top_k": 2,
    "expected_source_id": null,
    "expected_citation": null,
    "expect_empty": true
  }
]
""",
        encoding="utf-8",
    )
    fake_client = FakeQdrantClient(
        collection_exists=False,
        hits=[
            {
                "score": 1.0,
                "payload": {
                    "source_id": "split_refund_policy_docs",
                    "document_id": "split_refund_policy_2026",
                    "title": "拆分退款编号规则",
                    "text": "政策编号 RFD-2026-003 适用于三天未发货退款复核。",
                    "citation": "split_refund_policy_2026#policy-code",
                },
            },
            {
                "score": 1.0,
                "payload": {
                    "source_id": "split_refund_policy_docs",
                    "document_id": "split_refund_policy_2026",
                    "title": "拆分退款编号规则",
                    "text": "复核材料需要填写表单 AF-REFUND-02，并关联付款凭证。",
                    "citation": "split_refund_policy_2026#form-code",
                },
            },
        ],
    )
    monkeypatch.setattr(
        "app.services.retrieval_benchmark.create_qdrant_client",
        lambda settings: fake_client,
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

    evaluation = export_qdrant_bge_hybrid_relation_aggregation_grading_evidence(
        output_dir=tmp_path / "evidence",
        cases_path=cases_path,
        empty_cases_path=empty_cases_path,
        source_ids=["split_refund_policy_docs"],
        settings=settings,
    )

    result = evaluation.results[0]
    assert result.candidate.id == "relation-aware-aggregation-grader-v1"
    assert result.total_cases == 2
    assert result.answer_bearing_rate == 1.0
    assert result.relation_unsupported_count == 1
    assert result.unexpected_evidence_count == 0
    assert result.expected_empty_pass_rate == 1.0
    assert [case.grading_label for case in result.cases] == [
        "answer_bearing",
        "relation_unsupported",
    ]
    assert evaluation.json_path == tmp_path / "evidence" / "relation-aware-aggregation-grading.json"
    assert evaluation.markdown_path == tmp_path / "evidence" / "relation-aware-aggregation-grading.md"


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
