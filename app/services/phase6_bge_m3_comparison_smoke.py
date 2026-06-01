import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE6_BGE_M3_COMPARISON_SMOKE_ID = "phase6-bge-m3-comparison-smoke-v1"


@dataclass(frozen=True)
class Phase6BgeM3ComparisonSmokeReport:
    id: str
    generated_at: str
    status: str
    decision: str
    checks: list[dict[str, Any]]
    summary: dict[str, int]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase6_bge_m3_comparison_smoke_report(
    *,
    base_dir: Path = Path("."),
) -> Phase6BgeM3ComparisonSmokeReport:
    checks = [
        _file_check(
            check_id="comparison_contract_present",
            path=base_dir
            / "docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-quality-latency-comparison-contract.md",
            required=True,
        ),
        _json_check(
            check_id="comparison_diagnostics_present",
            path=base_dir
            / "docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-vs-mock-fixture-diagnostics.json",
            required=True,
        ),
        _json_check(
            check_id="artifact_readiness_present",
            path=base_dir
            / "docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json",
            required=True,
        ),
        _json_check(
            check_id="phase3_runtime_diagnostics_present",
            path=base_dir
            / "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/phase3-candidate-runtime-diagnostics.json",
            required=True,
        ),
        _json_check(
            check_id="phase3_latency_diagnostics_present",
            path=base_dir
            / "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/phase3-candidate-latency-resource-diagnostics.json",
            required=True,
        ),
        _json_check(
            check_id="deployment_readiness_present",
            path=base_dir / "docs/operations/deployment-readiness/deployment-readiness.json",
            required=True,
        ),
    ]
    passed = sum(1 for check in checks if check["passed"] is True)
    total = len(checks)
    failed = total - passed
    status = "ready" if failed == 0 else "review"
    return Phase6BgeM3ComparisonSmokeReport(
        id=PHASE6_BGE_M3_COMPARISON_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="keep_runtime_defaults",
        checks=checks,
        summary={"total_checks": total, "passed_checks": passed, "failed_checks": failed},
        notes=[
            "This smoke report is read-only and validates evidence-chain completeness only.",
            "No embedding execution, retrieval switching, or runtime promotion is performed.",
            "Use this artifact before starting private-network promotion review.",
        ],
    )


def phase6_bge_m3_comparison_smoke_report_to_dict(
    report: Phase6BgeM3ComparisonSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase6_bge_m3_comparison_smoke_markdown(
    report: Phase6BgeM3ComparisonSmokeReport,
) -> str:
    lines = [
        "# Phase 6 BGE-M3 Comparison Smoke",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        "",
        "## Checks",
        "",
        "| Check | Passed | Summary | Recommended Action |",
        "|---|---|---|---|",
    ]
    for check in report.checks:
        lines.append(
            f"| `{check['id']}` | `{check['passed']}` | {check['summary']} | `{check['recommended_action']}` |"
        )
    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Total checks: `{report.summary['total_checks']}`",
            f"- Passed checks: `{report.summary['passed_checks']}`",
            f"- Failed checks: `{report.summary['failed_checks']}`",
            "",
            "## Notes",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase6_bge_m3_comparison_smoke_report(
    output_dir: Path = Path("docs/smoke/bge-m3-comparison"),
    *,
    base_dir: Path = Path("."),
) -> Phase6BgeM3ComparisonSmokeReport:
    report = build_phase6_bge_m3_comparison_smoke_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase6-bge-m3-comparison-smoke.json"
    markdown_path = output_dir / "phase6-bge-m3-comparison-smoke.md"
    exported = Phase6BgeM3ComparisonSmokeReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        checks=report.checks,
        summary=report.summary,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase6_bge_m3_comparison_smoke_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase6_bge_m3_comparison_smoke_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _file_check(*, check_id: str, path: Path, required: bool) -> dict[str, Any]:
    present = path.exists()
    return {
        "id": check_id,
        "path": str(path),
        "required": required,
        "passed": present,
        "summary": "present" if present else "missing",
        "recommended_action": "no_action_required" if present else "restore_required_evidence",
    }


def _json_check(*, check_id: str, path: Path, required: bool) -> dict[str, Any]:
    if not path.exists():
        return {
            "id": check_id,
            "path": str(path),
            "required": required,
            "passed": False,
            "summary": "missing",
            "recommended_action": "regenerate_required_evidence",
        }
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return {
            "id": check_id,
            "path": str(path),
            "required": required,
            "passed": True,
            "summary": "json_parse_ok",
            "recommended_action": "no_action_required",
        }
    except json.JSONDecodeError as error:
        return {
            "id": check_id,
            "path": str(path),
            "required": required,
            "passed": False,
            "summary": f"invalid_json: {error.msg}",
            "recommended_action": "regenerate_required_evidence",
        }
