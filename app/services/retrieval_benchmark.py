import json
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter

from app.config import Settings, get_settings
from app.services.retrieval_backends import create_document_retriever


@dataclass(frozen=True)
class RetrievalBenchmarkCase:
    id: str
    category: str
    difficulty: str
    query: str
    knowledge_base_ids: list[str]
    top_k: int
    expected_source_id: str | None
    expected_citation: str | None
    expect_empty: bool = False


@dataclass(frozen=True)
class RetrievalBenchmarkCaseResult:
    id: str
    category: str
    difficulty: str
    hit_at_k: bool
    citation_match: bool
    empty_query_handling: bool | None
    latency_ms: float
    returned_citations: list[str]
    returned_source_ids: list[str]


@dataclass(frozen=True)
class RetrievalBenchmarkSummary:
    backend: str
    total_cases: int
    hit_rate: float
    citation_match_rate: float
    empty_handling_rate: float
    category_summaries: dict[str, dict[str, float | int]]


@dataclass(frozen=True)
class RetrievalBenchmarkReport:
    summary: RetrievalBenchmarkSummary
    cases: list[RetrievalBenchmarkCaseResult]


def load_benchmark_cases(path: Path) -> list[RetrievalBenchmarkCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [RetrievalBenchmarkCase(**item) for item in payload]


def run_retrieval_benchmark(
    cases: list[RetrievalBenchmarkCase],
    settings: Settings | None = None,
) -> RetrievalBenchmarkReport:
    settings = settings or get_settings()
    retriever = create_document_retriever(settings)
    results = [_run_case(retriever, case) for case in cases]
    return RetrievalBenchmarkReport(
        summary=_summarize(retriever.backend_name, results),
        cases=results,
    )


def benchmark_report_to_dict(report: RetrievalBenchmarkReport) -> dict:
    return {
        "summary": asdict(report.summary),
        "cases": [asdict(case) for case in report.cases],
    }


def export_benchmark_report_json(
    report: RetrievalBenchmarkReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(benchmark_report_to_dict(report), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def render_benchmark_report_markdown(report: RetrievalBenchmarkReport) -> str:
    summary = report.summary
    lines = [
        "# Retrieval Benchmark Report",
        "",
        "## Summary",
        "",
        "| Backend | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |",
        "| --- | ---: | ---: | ---: | ---: |",
        (
            f"| {summary.backend} | {summary.total_cases} | {summary.hit_rate:.4f} | "
            f"{summary.citation_match_rate:.4f} | {summary.empty_handling_rate:.4f} |"
        ),
        "",
        "## Category Summary",
        "",
        "| Category | Total Cases | Hit Rate | Citation Match Rate | Empty Handling Rate |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for category, metrics in summary.category_summaries.items():
        lines.append(
            f"| {category} | {metrics['total_cases']} | {metrics['hit_rate']:.4f} | "
            f"{metrics['citation_match_rate']:.4f} | {metrics['empty_handling_rate']:.4f} |"
        )

    lines.extend([
        "",
        "## Case Results",
        "",
        "| Case | Category | Difficulty | Hit@K | Citation Match | Empty Handling | Latency ms | Returned Citations |",
        "| --- | --- | --- | --- | --- | --- | ---: | --- |",
    ])
    for case in report.cases:
        empty = "" if case.empty_query_handling is None else str(case.empty_query_handling).lower()
        lines.append(
            f"| {case.id} | {case.category} | {case.difficulty} | "
            f"{str(case.hit_at_k).lower()} | {str(case.citation_match).lower()} | "
            f"{empty} | {case.latency_ms:.3f} | {', '.join(case.returned_citations)} |"
        )
    lines.append("")
    return "\n".join(lines)


def export_benchmark_report_markdown(
    report: RetrievalBenchmarkReport,
    path: Path,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_benchmark_report_markdown(report), encoding="utf-8")
    return path


def _run_case(retriever, case: RetrievalBenchmarkCase) -> RetrievalBenchmarkCaseResult:
    started_at = perf_counter()
    unknown_sources, documents = retriever.retrieve(
        query=case.query,
        knowledge_base_ids=case.knowledge_base_ids,
        top_k=case.top_k,
    )
    latency_ms = (perf_counter() - started_at) * 1000
    if unknown_sources:
        documents = []

    returned_citations = [document.citation for document in documents]
    returned_source_ids = [document.source_id for document in documents]
    empty_query_handling = None
    if case.expect_empty:
        empty_query_handling = len(documents) == 0

    return RetrievalBenchmarkCaseResult(
        id=case.id,
        category=case.category,
        difficulty=case.difficulty,
        hit_at_k=(
            case.expected_source_id in returned_source_ids
            if case.expected_source_id is not None
            else len(documents) == 0
        ),
        citation_match=(
            case.expected_citation in returned_citations
            if case.expected_citation is not None
            else len(documents) == 0
        ),
        empty_query_handling=empty_query_handling,
        latency_ms=round(latency_ms, 3),
        returned_citations=returned_citations,
        returned_source_ids=returned_source_ids,
    )


def _summarize(
    backend: str,
    results: list[RetrievalBenchmarkCaseResult],
) -> RetrievalBenchmarkSummary:
    total = len(results)
    empty_results = [
        result.empty_query_handling
        for result in results
        if result.empty_query_handling is not None
    ]
    return RetrievalBenchmarkSummary(
        backend=backend,
        total_cases=total,
        hit_rate=_rate([result.hit_at_k for result in results]),
        citation_match_rate=_rate([result.citation_match for result in results]),
        empty_handling_rate=_rate(empty_results),
        category_summaries=_category_summaries(results),
    )


def _rate(values: list[bool]) -> float:
    if not values:
        return 0.0
    return round(sum(1 for value in values if value) / len(values), 4)


def _category_summaries(
    results: list[RetrievalBenchmarkCaseResult],
) -> dict[str, dict[str, float | int]]:
    categories = sorted({result.category for result in results})
    summaries: dict[str, dict[str, float | int]] = {}
    for category in categories:
        category_results = [
            result for result in results if result.category == category
        ]
        empty_results = [
            result.empty_query_handling
            for result in category_results
            if result.empty_query_handling is not None
        ]
        summaries[category] = {
            "total_cases": len(category_results),
            "hit_rate": _rate([result.hit_at_k for result in category_results]),
            "citation_match_rate": _rate(
                [result.citation_match for result in category_results]
            ),
            "empty_handling_rate": _rate(empty_results),
        }
    return summaries
