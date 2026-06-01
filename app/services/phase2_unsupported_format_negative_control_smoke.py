import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE2_UNSUPPORTED_FORMAT_NEGATIVE_CONTROL_SMOKE_ID = (
    "phase2-unsupported-format-negative-control-smoke-v1"
)
PHASE2_SOURCE_FORMAT_DEMAND_READINESS_PATH = Path(
    "docs/operations/source-format-demand/phase2-source-format-demand-readiness.json"
)
PHASE2_UNSUPPORTED_FORMAT_NEGATIVE_CONTROL_SMOKE_JSON = (
    "phase2-unsupported-format-negative-control-smoke.json"
)
PHASE2_UNSUPPORTED_FORMAT_NEGATIVE_CONTROL_SMOKE_MARKDOWN = (
    "phase2-unsupported-format-negative-control-smoke.md"
)


@dataclass(frozen=True)
class Phase2UnsupportedFormatNegativeControlSmokeCheck:
    name: str
    passed: bool
    details: dict[str, Any]


@dataclass(frozen=True)
class Phase2UnsupportedFormatNegativeControlSmokeReport:
    id: str
    generated_at: str
    status: str
    decision: str
    readiness_report_path: str
    summary: dict[str, Any]
    checks: list[Phase2UnsupportedFormatNegativeControlSmokeCheck]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase2_unsupported_format_negative_control_smoke_report(
    *,
    base_dir: Path = Path("."),
) -> Phase2UnsupportedFormatNegativeControlSmokeReport:
    readiness_path = base_dir / PHASE2_SOURCE_FORMAT_DEMAND_READINESS_PATH
    if not readiness_path.exists():
        checks = [
            Phase2UnsupportedFormatNegativeControlSmokeCheck(
                name="phase2_source_format_demand_readiness_present",
                passed=False,
                details={"reason": "missing_readiness_report"},
            )
        ]
        return Phase2UnsupportedFormatNegativeControlSmokeReport(
            id=PHASE2_UNSUPPORTED_FORMAT_NEGATIVE_CONTROL_SMOKE_ID,
            generated_at=datetime.now(UTC).isoformat(),
            status="blocked",
            decision="keep_markdown_baseline",
            readiness_report_path=str(PHASE2_SOURCE_FORMAT_DEMAND_READINESS_PATH),
            summary=_summary_from_checks(checks, status="blocked"),
            checks=checks,
            notes=[
                "Phase 2 readiness export is required before running unsupported-format negative-control smoke.",
            ],
        )

    payload = json.loads(readiness_path.read_text(encoding="utf-8"))
    summary = payload.get("summary", {})
    if not isinstance(summary, dict):
        summary = {}
    parser_ready_documents = _int_value(summary.get("parser_ready_documents"), fallback=0)
    unsupported_documents = _int_value(summary.get("unsupported_documents"), fallback=0)
    non_markdown_sources = _int_value(summary.get("non_markdown_sources"), fallback=0)
    demand_signal = _bool_value(summary.get("format_expansion_demand_signal"))
    readiness_status = payload.get("status", "review")
    decision = payload.get("decision", "keep_markdown_baseline")

    checks = [
        Phase2UnsupportedFormatNegativeControlSmokeCheck(
            name="phase2_source_format_demand_readiness_present",
            passed=True,
            details={"readiness_status": readiness_status},
        ),
        Phase2UnsupportedFormatNegativeControlSmokeCheck(
            name="markdown_positive_control",
            passed=parser_ready_documents > 0,
            details={"parser_ready_documents": parser_ready_documents},
        ),
        Phase2UnsupportedFormatNegativeControlSmokeCheck(
            name="unsupported_document_negative_control",
            passed=unsupported_documents == 0,
            details={"unsupported_documents": unsupported_documents},
        ),
        Phase2UnsupportedFormatNegativeControlSmokeCheck(
            name="non_markdown_source_negative_control",
            passed=non_markdown_sources == 0,
            details={"non_markdown_sources": non_markdown_sources},
        ),
        Phase2UnsupportedFormatNegativeControlSmokeCheck(
            name="decision_alignment_control",
            passed=(decision == "keep_markdown_baseline" and demand_signal is False),
            details={
                "decision": decision,
                "format_expansion_demand_signal": demand_signal,
            },
        ),
    ]
    failed_required = any(
        check.name == "phase2_source_format_demand_readiness_present" and not check.passed
        for check in checks
    )
    status = _overall_status(checks, failed_required=failed_required)
    smoke_summary = _summary_from_checks(
        checks,
        status=status,
        parser_ready_documents=parser_ready_documents,
        unsupported_documents=unsupported_documents,
        non_markdown_sources=non_markdown_sources,
        demand_signal=demand_signal,
    )
    return Phase2UnsupportedFormatNegativeControlSmokeReport(
        id=PHASE2_UNSUPPORTED_FORMAT_NEGATIVE_CONTROL_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="keep_markdown_baseline",
        readiness_report_path=str(PHASE2_SOURCE_FORMAT_DEMAND_READINESS_PATH),
        summary=smoke_summary,
        checks=checks,
        notes=[
            "This smoke report is local and read-only for Phase 2 parser-expansion boundary review.",
            "It verifies unsupported-format and non-markdown-source negative controls from the Phase 2 readiness export.",
            "It does not enable non-Markdown parsers, ingestion execution, or retrieval default changes.",
        ],
    )


def phase2_unsupported_format_negative_control_smoke_report_to_dict(
    report: Phase2UnsupportedFormatNegativeControlSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase2_unsupported_format_negative_control_smoke_markdown(
    report: Phase2UnsupportedFormatNegativeControlSmokeReport,
) -> str:
    lines = [
        "# Phase 2 Unsupported Format Negative-Control Smoke",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Readiness Report: `{report.readiness_report_path}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Checks | `{report.summary['total_checks']}` |",
        f"| Passed Checks | `{report.summary['passed_checks']}` |",
        f"| Failed Checks | `{report.summary['failed_checks']}` |",
        f"| Parser-Ready Documents | `{report.summary['parser_ready_documents']}` |",
        f"| Unsupported Documents | `{report.summary['unsupported_documents']}` |",
        f"| Non-Markdown Sources | `{report.summary['non_markdown_sources']}` |",
        f"| Demand Signal | `{report.summary['format_expansion_demand_signal']}` |",
        "",
        "## Checks",
        "",
        "| Check | Passed | Details |",
        "|---|---|---|",
    ]
    for check in report.checks:
        lines.append(
            f"| `{check.name}` | `{check.passed}` | "
            f"`{json.dumps(check.details, ensure_ascii=False, sort_keys=True)}` |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase2_unsupported_format_negative_control_smoke_report(
    output_dir: Path = Path("docs/smoke/source-format-demand"),
    *,
    base_dir: Path = Path("."),
) -> Phase2UnsupportedFormatNegativeControlSmokeReport:
    report = build_phase2_unsupported_format_negative_control_smoke_report(
        base_dir=base_dir
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PHASE2_UNSUPPORTED_FORMAT_NEGATIVE_CONTROL_SMOKE_JSON
    markdown_path = (
        output_dir / PHASE2_UNSUPPORTED_FORMAT_NEGATIVE_CONTROL_SMOKE_MARKDOWN
    )
    exported_report = Phase2UnsupportedFormatNegativeControlSmokeReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        readiness_report_path=report.readiness_report_path,
        summary=report.summary,
        checks=report.checks,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase2_unsupported_format_negative_control_smoke_report_to_dict(
                exported_report
            ),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase2_unsupported_format_negative_control_smoke_markdown(
            exported_report
        ),
        encoding="utf-8",
    )
    return exported_report


def _overall_status(
    checks: list[Phase2UnsupportedFormatNegativeControlSmokeCheck],
    *,
    failed_required: bool,
) -> str:
    if failed_required:
        return "blocked"
    if all(check.passed for check in checks):
        return "ready"
    return "review"


def _summary_from_checks(
    checks: list[Phase2UnsupportedFormatNegativeControlSmokeCheck],
    *,
    status: str,
    parser_ready_documents: int = 0,
    unsupported_documents: int = 0,
    non_markdown_sources: int = 0,
    demand_signal: bool = False,
) -> dict[str, Any]:
    passed_checks = sum(1 for check in checks if check.passed)
    total_checks = len(checks)
    return {
        "status": status,
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "failed_checks": total_checks - passed_checks,
        "parser_ready_documents": parser_ready_documents,
        "unsupported_documents": unsupported_documents,
        "non_markdown_sources": non_markdown_sources,
        "format_expansion_demand_signal": demand_signal,
    }


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return False


def _int_value(value: Any, *, fallback: int) -> int:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int) and value >= 0:
        return value
    return fallback
