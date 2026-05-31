import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE3_FP_FN_REVIEW_ID = "phase3-fp-fn-review-v1"


@dataclass(frozen=True)
class Phase3FpFnReviewCase:
    id: str
    category: str
    expect_empty: bool
    hit_at_k: bool
    citation_match: bool
    empty_query_handling: bool | None
    returned_citations: list[str]


@dataclass(frozen=True)
class Phase3FpFnReviewReport:
    id: str
    generated_at: str
    source_report_path: str
    total_cases: int
    false_positive_count: int
    false_negative_count: int
    false_positive_rate: float
    false_negative_rate: float
    false_positive_cases: list[Phase3FpFnReviewCase]
    false_negative_cases: list[Phase3FpFnReviewCase]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase3_fp_fn_review_report(
    benchmark_report_path: Path,
) -> Phase3FpFnReviewReport:
    payload = json.loads(benchmark_report_path.read_text(encoding="utf-8"))
    report = payload.get("report")
    if not isinstance(report, dict):
        raise ValueError("Invalid benchmark evidence: missing report")
    cases = report.get("cases")
    if not isinstance(cases, list):
        raise ValueError("Invalid benchmark evidence: missing report.cases")

    fp_cases: list[Phase3FpFnReviewCase] = []
    fn_cases: list[Phase3FpFnReviewCase] = []
    for item in cases:
        if not isinstance(item, dict):
            continue
        case = _to_review_case(item)
        if case is None:
            continue
        is_false_positive = case.expect_empty and (
            case.empty_query_handling is False or bool(case.returned_citations)
        )
        is_false_negative = (not case.expect_empty) and (
            (not case.hit_at_k) or (not case.citation_match)
        )
        if is_false_positive:
            fp_cases.append(case)
        if is_false_negative:
            fn_cases.append(case)

    total_cases = len(cases)
    fp_rate = round(len(fp_cases) / total_cases, 4) if total_cases > 0 else 0.0
    fn_rate = round(len(fn_cases) / total_cases, 4) if total_cases > 0 else 0.0
    return Phase3FpFnReviewReport(
        id=PHASE3_FP_FN_REVIEW_ID,
        generated_at=datetime.now(UTC).isoformat(),
        source_report_path=str(benchmark_report_path),
        total_cases=total_cases,
        false_positive_count=len(fp_cases),
        false_negative_count=len(fn_cases),
        false_positive_rate=fp_rate,
        false_negative_rate=fn_rate,
        false_positive_cases=fp_cases,
        false_negative_cases=fn_cases,
        notes=[
            "This report is a read-only review view over existing benchmark evidence.",
            "It does not change retrieval defaults, thresholds, or runtime promotion status.",
        ],
    )


def phase3_fp_fn_review_report_to_dict(
    report: Phase3FpFnReviewReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase3_fp_fn_review_markdown(
    report: Phase3FpFnReviewReport,
) -> str:
    lines = [
        "# Phase 3 FP/FN Review Report",
        "",
        f"- Report: `{report.id}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Source Benchmark Report: `{report.source_report_path}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Cases | `{report.total_cases}` |",
        f"| False Positive Count | `{report.false_positive_count}` |",
        f"| False Negative Count | `{report.false_negative_count}` |",
        f"| False Positive Rate | `{report.false_positive_rate:.4f}` |",
        f"| False Negative Rate | `{report.false_negative_rate:.4f}` |",
        "",
        "## False Positive Cases",
        "",
        "| Case ID | Category | Returned Citations |",
        "|---|---|---|",
    ]
    if not report.false_positive_cases:
        lines.append("| `none` | `n/a` | `[]` |")
    else:
        for case in report.false_positive_cases:
            lines.append(
                f"| `{case.id}` | `{case.category}` | "
                f"`{', '.join(case.returned_citations)}` |"
            )
    lines.extend(
        [
            "",
            "## False Negative Cases",
            "",
            "| Case ID | Category | Hit At K | Citation Match |",
            "|---|---|---|---|",
        ]
    )
    if not report.false_negative_cases:
        lines.append("| `none` | `n/a` | `n/a` | `n/a` |")
    else:
        for case in report.false_negative_cases:
            lines.append(
                f"| `{case.id}` | `{case.category}` | "
                f"`{case.hit_at_k}` | `{case.citation_match}` |"
            )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase3_fp_fn_review_report(
    *,
    benchmark_report_path: Path = Path(
        "docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.json"
    ),
    output_dir: Path = Path("docs/benchmark/chinese-seed/fp-fn-review"),
) -> Phase3FpFnReviewReport:
    report = build_phase3_fp_fn_review_report(benchmark_report_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3-fp-fn-review.json"
    markdown_path = output_dir / "phase3-fp-fn-review.md"
    exported_report = Phase3FpFnReviewReport(
        id=report.id,
        generated_at=report.generated_at,
        source_report_path=report.source_report_path,
        total_cases=report.total_cases,
        false_positive_count=report.false_positive_count,
        false_negative_count=report.false_negative_count,
        false_positive_rate=report.false_positive_rate,
        false_negative_rate=report.false_negative_rate,
        false_positive_cases=report.false_positive_cases,
        false_negative_cases=report.false_negative_cases,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase3_fp_fn_review_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase3_fp_fn_review_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _to_review_case(item: dict[str, Any]) -> Phase3FpFnReviewCase | None:
    case_id = item.get("id")
    category = item.get("category")
    hit_at_k = item.get("hit_at_k")
    citation_match = item.get("citation_match")
    returned_citations = item.get("returned_citations")
    if not isinstance(case_id, str) or not isinstance(category, str):
        return None
    if not isinstance(hit_at_k, bool) or not isinstance(citation_match, bool):
        return None
    if not isinstance(returned_citations, list):
        return None
    empty_query_handling = item.get("empty_query_handling")
    if empty_query_handling is not None and not isinstance(empty_query_handling, bool):
        empty_query_handling = None
    expect_empty_value = item.get("expect_empty")
    if isinstance(expect_empty_value, bool):
        expect_empty = expect_empty_value
    else:
        # Benchmark report cases do not always include expect_empty. For those rows,
        # empty_query_handling is only present on expected-empty benchmark cases.
        expect_empty = empty_query_handling is not None
    citations = [citation for citation in returned_citations if isinstance(citation, str)]
    return Phase3FpFnReviewCase(
        id=case_id,
        category=category,
        expect_empty=expect_empty,
        hit_at_k=hit_at_k,
        citation_match=citation_match,
        empty_query_handling=empty_query_handling,
        returned_citations=citations,
    )
