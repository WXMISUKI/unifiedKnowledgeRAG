import json
from pathlib import Path

from app.config import Settings

from app.services.retrieval_benchmark import (
    benchmark_report_to_dict,
    export_benchmark_report_json,
    export_benchmark_report_markdown,
    load_benchmark_cases,
    render_benchmark_report_markdown,
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
        "empty-membership-points",
    ]
    assert cases[0].expected_citation == "refund_policy_2026#section-3"
    assert cases[-1].expect_empty is True
    assert cases[-1].category == "empty"


def test_fixture_backend_benchmark_reports_success_metrics():
    cases = load_benchmark_cases(FIXTURE_PATH)
    report = run_retrieval_benchmark(cases, Settings(rag_retrieval_backend="fixture"))

    assert report.summary.backend == "fixture"
    assert report.summary.total_cases == 8
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
        "empty",
    }
    assert {case.difficulty for case in cases} >= {"easy", "medium"}


def test_benchmark_report_includes_category_summaries():
    cases = load_benchmark_cases(FIXTURE_PATH)
    report = run_retrieval_benchmark(cases, Settings(rag_retrieval_backend="fixture"))

    summaries = report.summary.category_summaries
    assert summaries["policy"]["total_cases"] == 1
    assert summaries["paraphrase"]["total_cases"] == 2
    assert summaries["empty"]["total_cases"] == 2
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
    assert payload["summary"]["category_summaries"]["empty"]["total_cases"] == 2
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
