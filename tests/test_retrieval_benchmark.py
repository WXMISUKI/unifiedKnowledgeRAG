import json
from pathlib import Path

from app.config import Settings

from app.services.retrieval_benchmark import (
    benchmark_report_to_dict,
    candidate_evaluation_to_dict,
    default_embedding_candidates,
    embedding_candidate_result_to_dict,
    EmbeddingCandidate,
    export_chinese_seed_evidence_bundle,
    export_qdrant_bge_smoke_evidence,
    export_qdrant_bge_threshold_sweep_evidence,
    evaluate_retrieval_candidates,
    evaluate_embedding_candidates,
    export_benchmark_report_json,
    export_benchmark_report_markdown,
    load_benchmark_cases,
    render_embedding_candidate_markdown,
    render_benchmark_report_markdown,
    render_qdrant_threshold_sweep_evidence_markdown,
    fixture_chinese_seed_retrieval_candidate,
    RetrievalCandidate,
    run_retrieval_benchmark,
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
    assert bundle.retrieval_evaluations[0].report.summary.total_cases == 15
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
    assert retrieval_payload["report"]["summary"]["total_cases"] == 15

    embedding_payload = json.loads(embedding_json.read_text(encoding="utf-8"))
    assert embedding_payload["candidate"]["id"] == "bge-m3-local-candidate"
    assert embedding_payload["readiness_status"] == "review_required"


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
