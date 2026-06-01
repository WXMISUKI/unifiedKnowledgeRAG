import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE3_HYBRID_CROSS_CASE_FP_FN_SMOKE_ID = "phase3-hybrid-cross-case-fp-fn-smoke-v1"
PHASE3_BASELINE_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.json"
)
PHASE3_FP_FN_REVIEW_PATH = Path(
    "docs/benchmark/chinese-seed/fp-fn-review/phase3-fp-fn-review.json"
)
PHASE3_EVALUATION_PROTOCOL_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-candidate-evaluation-protocol/"
    "phase3-retrieval-candidate-evaluation-protocol.md"
)
PHASE3_HYBRID_CROSS_CASE_SMOKE_JSON = "phase3-hybrid-cross-case-fp-fn-smoke.json"
PHASE3_HYBRID_CROSS_CASE_SMOKE_MARKDOWN = "phase3-hybrid-cross-case-fp-fn-smoke.md"


@dataclass(frozen=True)
class Phase3HybridCrossCaseSmokeCheck:
    name: str
    passed: bool
    scenario: str
    details: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass(frozen=True)
class Phase3HybridCrossCaseSmokeReport:
    id: str
    generated_at: str
    status: str
    checks: list[Phase3HybridCrossCaseSmokeCheck]
    summary: dict[str, Any]
    source_paths: dict[str, str]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def run_phase3_hybrid_cross_case_fp_fn_smoke(
    *,
    base_dir: Path = Path("."),
) -> Phase3HybridCrossCaseSmokeReport:
    baseline_payload = _read_json(base_dir / PHASE3_BASELINE_PATH)
    fp_fn_payload = _read_json(base_dir / PHASE3_FP_FN_REVIEW_PATH)
    checks = [
        _run_check(
            "baseline_cross_case_coverage",
            "baseline risk case ids are present",
            lambda: _check_baseline_risk_case_coverage(baseline_payload),
        ),
        _run_check(
            "false_positive_alignment",
            "fp review contains expected empty trap cases",
            lambda: _check_false_positive_alignment(fp_fn_payload),
        ),
        _run_check(
            "positive_control_and_fn_guard",
            "positive controls remain successful while fn count stays zero",
            lambda: _check_positive_control_and_fn_guard(
                baseline_payload=baseline_payload,
                fp_fn_payload=fp_fn_payload,
            ),
        ),
        _run_check(
            "evaluation_protocol_artifact",
            "phase3 evaluation protocol is present",
            lambda: _check_protocol_artifact(base_dir),
        ),
    ]
    passed = sum(1 for check in checks if check.passed)
    baseline_cases = _baseline_case_map(baseline_payload)
    summary = {
        "total": len(checks),
        "passed": passed,
        "failed": len(checks) - passed,
        "risk_case_count": len(_required_risk_case_ids()),
        "baseline_total_cases": _int_value(
            baseline_payload.get("report", {}).get("summary", {}).get("total_cases"),
            fallback=len(baseline_cases),
        ),
        "false_positive_count": _int_value(
            fp_fn_payload.get("false_positive_count"),
            fallback=0,
        ),
        "false_negative_count": _int_value(
            fp_fn_payload.get("false_negative_count"),
            fallback=0,
        ),
    }
    return Phase3HybridCrossCaseSmokeReport(
        id=PHASE3_HYBRID_CROSS_CASE_FP_FN_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status="ready" if summary["failed"] == 0 else "blocked",
        checks=checks,
        summary=summary,
        source_paths={
            "baseline": str(PHASE3_BASELINE_PATH),
            "fp_fn_review": str(PHASE3_FP_FN_REVIEW_PATH),
            "evaluation_protocol": str(PHASE3_EVALUATION_PROTOCOL_PATH),
        },
        notes=[
            "This smoke validates cross-case FP/FN signal visibility from existing local evidence.",
            "It is read-only and does not execute retrieval backends.",
            "Smoke readiness reflects evidence integrity, not runtime promotion approval.",
        ],
    )


def phase3_hybrid_cross_case_smoke_report_to_dict(
    report: Phase3HybridCrossCaseSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase3_hybrid_cross_case_smoke_markdown(
    report: Phase3HybridCrossCaseSmokeReport,
) -> str:
    lines = [
        "# Phase 3 Hybrid Cross-Case FP/FN Smoke Report",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{'passed' if report.status == 'ready' else report.status}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Baseline Source: `{report.source_paths['baseline']}`",
        f"- FP/FN Source: `{report.source_paths['fp_fn_review']}`",
        f"- Protocol Source: `{report.source_paths['evaluation_protocol']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Checks | `{report.summary['total']}` |",
        f"| Passed Checks | `{report.summary['passed']}` |",
        f"| Failed Checks | `{report.summary['failed']}` |",
        f"| Baseline Total Cases | `{report.summary['baseline_total_cases']}` |",
        f"| False Positive Count | `{report.summary['false_positive_count']}` |",
        f"| False Negative Count | `{report.summary['false_negative_count']}` |",
        "",
        "## Checks",
        "",
        "| Check | Scenario | Status | Details |",
        "|---|---|---|---|",
    ]
    for check in report.checks:
        details = json.dumps(
            check.details if check.passed else {"error": check.error or "failed"},
            ensure_ascii=False,
            sort_keys=True,
        )
        lines.append(
            f"| `{check.name}` | `{check.scenario}` | "
            f"`{'passed' if check.passed else 'failed'}` | {details} |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase3_hybrid_cross_case_fp_fn_smoke_report(
    output_dir: Path = Path("docs/smoke/hybrid-cross-case-fp-fn"),
    *,
    base_dir: Path = Path("."),
) -> Phase3HybridCrossCaseSmokeReport:
    report = run_phase3_hybrid_cross_case_fp_fn_smoke(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PHASE3_HYBRID_CROSS_CASE_SMOKE_JSON
    markdown_path = output_dir / PHASE3_HYBRID_CROSS_CASE_SMOKE_MARKDOWN
    exported = Phase3HybridCrossCaseSmokeReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        checks=report.checks,
        summary=report.summary,
        source_paths=report.source_paths,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase3_hybrid_cross_case_smoke_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase3_hybrid_cross_case_smoke_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _check_baseline_risk_case_coverage(baseline_payload: dict[str, Any]) -> dict[str, Any]:
    case_map = _baseline_case_map(baseline_payload)
    required_ids = _required_risk_case_ids()
    missing = sorted(case_id for case_id in required_ids if case_id not in case_map)
    assert not missing, f"missing risk cases: {','.join(missing)}"
    return {
        "required_case_ids": sorted(required_ids),
        "present_case_count": len(required_ids),
    }


def _check_false_positive_alignment(fp_fn_payload: dict[str, Any]) -> dict[str, Any]:
    fp_cases = fp_fn_payload.get("false_positive_cases", [])
    assert isinstance(fp_cases, list), "false_positive_cases is not a list"
    fp_ids = {case.get("id") for case in fp_cases if isinstance(case, dict)}
    expected_fp_ids = {
        "empty-refund-high-value-auto-compensation",
        "empty-refund-high-value-auto-compensation-customer-like-2",
    }
    missing = sorted(case_id for case_id in expected_fp_ids if case_id not in fp_ids)
    assert not missing, f"missing false-positive trap ids: {','.join(missing)}"
    fp_count = _int_value(fp_fn_payload.get("false_positive_count"), fallback=0)
    assert fp_count >= len(expected_fp_ids), "false_positive_count is below expected traps"
    return {
        "expected_false_positive_ids": sorted(expected_fp_ids),
        "observed_false_positive_count": fp_count,
    }


def _check_positive_control_and_fn_guard(
    *,
    baseline_payload: dict[str, Any],
    fp_fn_payload: dict[str, Any],
) -> dict[str, Any]:
    fn_count = _int_value(fp_fn_payload.get("false_negative_count"), fallback=0)
    assert fn_count == 0, "false_negative_count must stay zero for this smoke"
    case_map = _baseline_case_map(baseline_payload)
    positive_ids = [
        "logistics-exact-id-customer-like",
        "refund-high-value-review-customer-like-audit-trace-2",
    ]
    for case_id in positive_ids:
        case = case_map.get(case_id)
        assert case is not None, f"positive control case missing: {case_id}"
        assert case.get("hit_at_k") is True, f"positive control hit_at_k failed: {case_id}"
        assert (
            case.get("citation_match") is True
        ), f"positive control citation_match failed: {case_id}"
    return {
        "false_negative_count": fn_count,
        "positive_control_ids": positive_ids,
    }


def _check_protocol_artifact(base_dir: Path) -> dict[str, Any]:
    path = base_dir / PHASE3_EVALUATION_PROTOCOL_PATH
    assert path.exists(), "phase3 candidate evaluation protocol doc is missing"
    return {"present": True, "path": str(PHASE3_EVALUATION_PROTOCOL_PATH)}


def _run_check(
    name: str,
    scenario: str,
    check_fn: Any,
) -> Phase3HybridCrossCaseSmokeCheck:
    try:
        details = check_fn()
    except AssertionError as error:
        return Phase3HybridCrossCaseSmokeCheck(
            name=name,
            passed=False,
            scenario=scenario,
            error=str(error) or error.__class__.__name__,
        )
    except Exception as error:
        return Phase3HybridCrossCaseSmokeCheck(
            name=name,
            passed=False,
            scenario=scenario,
            error=f"{error.__class__.__name__}: {error}",
        )
    return Phase3HybridCrossCaseSmokeCheck(
        name=name,
        passed=True,
        scenario=scenario,
        details=details,
    )


def _baseline_case_map(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    cases = payload.get("report", {}).get("cases", [])
    result: dict[str, dict[str, Any]] = {}
    for item in cases:
        if not isinstance(item, dict):
            continue
        case_id = item.get("id")
        if isinstance(case_id, str):
            result[case_id] = item
    return result


def _required_risk_case_ids() -> set[str]:
    return {
        "empty-refund-high-value-auto-compensation",
        "empty-refund-high-value-auto-compensation-customer-like-2",
        "logistics-exact-id-customer-like",
        "refund-high-value-review-customer-like-audit-trace-2",
    }


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _int_value(value: Any, *, fallback: int) -> int:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int) and value >= 0:
        return value
    return fallback
