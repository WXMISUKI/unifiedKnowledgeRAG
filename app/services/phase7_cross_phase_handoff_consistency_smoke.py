import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE7_CROSS_PHASE_HANDOFF_CONSISTENCY_SMOKE_ID = (
    "phase7-cross-phase-handoff-consistency-smoke-v1"
)
PHASE7_PROVIDER_RELEASE_READINESS_PATH = Path(
    "docs/operations/provider-release-readiness/phase7-provider-release-readiness.json"
)
PHASE2_DECISION_RECORD_PATH = Path(
    "docs/operations/source-format-demand/phase2-parser-expansion-decision-record.md"
)
PHASE3_DECISION_RECORD_PATH = Path(
    "docs/benchmark/chinese-seed/hybrid-runtime-promotion/"
    "phase3-hybrid-runtime-promotion-decision-record.md"
)
PHASE4_CALLER_SMOKE_PATH = Path(
    "docs/smoke/evidence-pack-consumption/phase4-caller-consumption-smoke.json"
)
PHASE5_GRAPH_SMOKE_PATH = Path(
    "docs/smoke/graph-boundary-summary/phase5-graph-boundary-smoke-summary.json"
)
PHASE6_DEPLOYED_FIELD_VALIDATION_PATH = Path(
    "docs/operations/deployed-field-validation/"
    "phase6-deployed-field-validation-readiness.json"
)
PHASE7_CROSS_PHASE_HANDOFF_CONSISTENCY_SMOKE_JSON = (
    "phase7-cross-phase-handoff-consistency-smoke.json"
)
PHASE7_CROSS_PHASE_HANDOFF_CONSISTENCY_SMOKE_MARKDOWN = (
    "phase7-cross-phase-handoff-consistency-smoke.md"
)


@dataclass(frozen=True)
class Phase7CrossPhaseConsistencyCheck:
    name: str
    passed: bool
    details: dict[str, Any]


@dataclass(frozen=True)
class Phase7CrossPhaseHandoffConsistencySmokeReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    checks: list[Phase7CrossPhaseConsistencyCheck]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase7_cross_phase_handoff_consistency_smoke_report(
    *,
    base_dir: Path = Path("."),
) -> Phase7CrossPhaseHandoffConsistencySmokeReport:
    readiness_payload = _read_json_if_present(base_dir / PHASE7_PROVIDER_RELEASE_READINESS_PATH)
    if readiness_payload is None:
        checks = [
            Phase7CrossPhaseConsistencyCheck(
                name="phase7_provider_release_readiness_present",
                passed=False,
                details={"reason": "missing_release_readiness_report"},
            )
        ]
        return Phase7CrossPhaseHandoffConsistencySmokeReport(
            id=PHASE7_CROSS_PHASE_HANDOFF_CONSISTENCY_SMOKE_ID,
            generated_at=datetime.now(UTC).isoformat(),
            status="blocked",
            decision="regenerate_phase7_release_readiness_first",
            summary=_summary_from_checks(checks),
            checks=checks,
            notes=[
                "Phase 7 provider release readiness is required before cross-phase consistency smoke.",
            ],
        )

    checks = [
        _check_phase7_release_readiness(readiness_payload),
        _check_phase2_decision_record(base_dir),
        _check_phase3_decision_record(base_dir),
        _check_phase4_caller_smoke(base_dir),
        _check_phase5_graph_smoke(base_dir),
        _check_phase6_deployed_field_validation(base_dir),
    ]
    status = _overall_status(checks)
    decision = (
        "keep_runtime_defaults_until_live_validation"
        if status in {"ready", "review"}
        else "resolve_cross_phase_inconsistency"
    )
    return Phase7CrossPhaseHandoffConsistencySmokeReport(
        id=PHASE7_CROSS_PHASE_HANDOFF_CONSISTENCY_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision=decision,
        summary=_summary_from_checks(checks),
        checks=checks,
        notes=[
            "This smoke is local read-only cross-phase consistency evidence.",
            "It validates that phase decisions and key smoke/readiness outputs remain aligned.",
            "It does not promote runtime defaults or replace deployed live-url validation.",
        ],
    )


def phase7_cross_phase_handoff_consistency_smoke_report_to_dict(
    report: Phase7CrossPhaseHandoffConsistencySmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase7_cross_phase_handoff_consistency_smoke_markdown(
    report: Phase7CrossPhaseHandoffConsistencySmokeReport,
) -> str:
    lines = [
        "# Phase 7 Cross-Phase Handoff Consistency Smoke",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Checks | `{report.summary['total_checks']}` |",
        f"| Passed Checks | `{report.summary['passed_checks']}` |",
        f"| Failed Checks | `{report.summary['failed_checks']}` |",
        f"| Open Gate IDs | `{json.dumps(report.summary['open_gate_ids'])}` |",
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


def export_phase7_cross_phase_handoff_consistency_smoke_report(
    output_dir: Path = Path("docs/smoke/cross-phase-handoff"),
    *,
    base_dir: Path = Path("."),
) -> Phase7CrossPhaseHandoffConsistencySmokeReport:
    report = build_phase7_cross_phase_handoff_consistency_smoke_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PHASE7_CROSS_PHASE_HANDOFF_CONSISTENCY_SMOKE_JSON
    markdown_path = output_dir / PHASE7_CROSS_PHASE_HANDOFF_CONSISTENCY_SMOKE_MARKDOWN
    exported = Phase7CrossPhaseHandoffConsistencySmokeReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        summary=report.summary,
        checks=report.checks,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase7_cross_phase_handoff_consistency_smoke_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase7_cross_phase_handoff_consistency_smoke_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _check_phase7_release_readiness(payload: dict[str, Any]) -> Phase7CrossPhaseConsistencyCheck:
    summary = payload.get("summary", {})
    local_handoff_ready = bool(_dict_value(summary, "ready_for_local_provider_handoff", False))
    runtime_ready = bool(_dict_value(summary, "ready_for_runtime_default_promotion", False))
    release_state = str(payload.get("release_state", "review"))
    decision = str(payload.get("decision", "keep_runtime_defaults"))
    passed = local_handoff_ready and (not runtime_ready) and decision == "keep_runtime_defaults"
    return Phase7CrossPhaseConsistencyCheck(
        name="phase7_release_readiness_decision_alignment",
        passed=passed,
        details={
            "release_state": release_state,
            "decision": decision,
            "ready_for_local_provider_handoff": local_handoff_ready,
            "ready_for_runtime_default_promotion": runtime_ready,
        },
    )


def _check_phase2_decision_record(base_dir: Path) -> Phase7CrossPhaseConsistencyCheck:
    path = base_dir / PHASE2_DECISION_RECORD_PATH
    if not path.exists():
        return Phase7CrossPhaseConsistencyCheck(
            name="phase2_decision_record_alignment",
            passed=False,
            details={"reason": "missing_phase2_decision_record"},
        )
    content = path.read_text(encoding="utf-8")
    passed = "keep_markdown_baseline" in content
    return Phase7CrossPhaseConsistencyCheck(
        name="phase2_decision_record_alignment",
        passed=passed,
        details={"contains_keep_markdown_baseline": passed},
    )


def _check_phase3_decision_record(base_dir: Path) -> Phase7CrossPhaseConsistencyCheck:
    path = base_dir / PHASE3_DECISION_RECORD_PATH
    if not path.exists():
        return Phase7CrossPhaseConsistencyCheck(
            name="phase3_decision_record_alignment",
            passed=False,
            details={"reason": "missing_phase3_decision_record"},
        )
    content = path.read_text(encoding="utf-8")
    passed = "keep_runtime_defaults" in content
    return Phase7CrossPhaseConsistencyCheck(
        name="phase3_decision_record_alignment",
        passed=passed,
        details={"contains_keep_runtime_defaults": passed},
    )


def _check_phase4_caller_smoke(base_dir: Path) -> Phase7CrossPhaseConsistencyCheck:
    payload = _read_json_if_present(base_dir / PHASE4_CALLER_SMOKE_PATH)
    if payload is None:
        return Phase7CrossPhaseConsistencyCheck(
            name="phase4_caller_consumption_smoke_alignment",
            passed=False,
            details={"reason": "missing_phase4_caller_smoke"},
        )
    status = _normalize_status(payload.get("status"))
    passed = status == "ready"
    return Phase7CrossPhaseConsistencyCheck(
        name="phase4_caller_consumption_smoke_alignment",
        passed=passed,
        details={"status": status},
    )


def _check_phase5_graph_smoke(base_dir: Path) -> Phase7CrossPhaseConsistencyCheck:
    payload = _read_json_if_present(base_dir / PHASE5_GRAPH_SMOKE_PATH)
    if payload is None:
        return Phase7CrossPhaseConsistencyCheck(
            name="phase5_graph_boundary_alignment",
            passed=False,
            details={"reason": "missing_phase5_graph_smoke"},
        )
    status = _normalize_status(payload.get("status"))
    summary = payload.get("summary", {})
    graph_query_planned = bool(_dict_value(summary, "graph_query_planned", False))
    passed = status == "ready" and graph_query_planned
    return Phase7CrossPhaseConsistencyCheck(
        name="phase5_graph_boundary_alignment",
        passed=passed,
        details={"status": status, "graph_query_planned": graph_query_planned},
    )


def _check_phase6_deployed_field_validation(
    base_dir: Path,
) -> Phase7CrossPhaseConsistencyCheck:
    payload = _read_json_if_present(base_dir / PHASE6_DEPLOYED_FIELD_VALIDATION_PATH)
    if payload is None:
        return Phase7CrossPhaseConsistencyCheck(
            name="phase6_deployed_field_validation_alignment",
            passed=False,
            details={"reason": "missing_phase6_deployed_field_validation_readiness"},
        )
    status = _normalize_status(payload.get("status"))
    field_validation_state = str(payload.get("field_validation_state", "review"))
    passed = status in {"review", "ready"} and field_validation_state in {
        "await_live_url",
        "review",
        "ready_for_live_validation",
    }
    return Phase7CrossPhaseConsistencyCheck(
        name="phase6_deployed_field_validation_alignment",
        passed=passed,
        details={
            "status": status,
            "field_validation_state": field_validation_state,
        },
    )


def _overall_status(checks: list[Phase7CrossPhaseConsistencyCheck]) -> str:
    if not checks or checks[0].name == "phase7_provider_release_readiness_present":
        return "blocked"
    if all(check.passed for check in checks):
        return "ready"
    return "review"


def _summary_from_checks(
    checks: list[Phase7CrossPhaseConsistencyCheck],
) -> dict[str, Any]:
    total_checks = len(checks)
    passed_checks = sum(1 for check in checks if check.passed)
    return {
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "failed_checks": total_checks - passed_checks,
        "open_gate_ids": [check.name for check in checks if not check.passed],
    }


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_status(value: Any) -> str:
    if value in {"ready", "review", "blocked"}:
        return str(value)
    return "review"


def _dict_value(value: Any, key: str, fallback: Any) -> Any:
    if not isinstance(value, dict):
        return fallback
    return value.get(key, fallback)
