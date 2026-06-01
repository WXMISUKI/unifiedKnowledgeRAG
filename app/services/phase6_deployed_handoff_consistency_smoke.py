import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE6_DEPLOYED_HANDOFF_CONSISTENCY_SMOKE_ID = (
    "phase6-deployed-handoff-consistency-smoke-v1"
)

DEPLOYED_FIELD_VALIDATION_READINESS_PATH = Path(
    "docs/operations/deployed-field-validation/"
    "phase6-deployed-field-validation-readiness.json"
)
PROVIDER_HANDOFF_BUNDLE_PATH = Path(
    "docs/integration/provider-handoff/provider-handoff-bundle.json"
)
READINESS_ARTIFACT_ID = "phase6_deployed_field_validation_readiness"


@dataclass(frozen=True)
class Phase6DeployedHandoffConsistencySmokeCheck:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase6DeployedHandoffConsistencySmokeReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    checks: list[Phase6DeployedHandoffConsistencySmokeCheck]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase6_deployed_handoff_consistency_smoke_report(
    *,
    base_dir: Path = Path("."),
) -> Phase6DeployedHandoffConsistencySmokeReport:
    readiness_payload = _read_json_if_present(base_dir / DEPLOYED_FIELD_VALIDATION_READINESS_PATH)
    bundle_payload = _read_json_if_present(base_dir / PROVIDER_HANDOFF_BUNDLE_PATH)
    bundle_row = _bundle_row(bundle_payload, READINESS_ARTIFACT_ID)

    readiness_signal = _artifact_signal(
        id="deployed_field_validation_readiness",
        path=DEPLOYED_FIELD_VALIDATION_READINESS_PATH,
        payload=readiness_payload,
        required=True,
        missing_action="regenerate_phase6_deployed_field_validation_readiness",
    )
    bundle_signal = _bundle_signal(bundle_payload)
    bundle_row_signal = _bundle_row_signal(bundle_row)
    status_alignment_signal = _status_alignment_signal(
        readiness_payload=readiness_payload,
        bundle_row=bundle_row,
    )
    field_validation_state_signal = _summary_alignment_signal(
        id="field_validation_state_alignment",
        label="field_validation_state",
        expected=_readiness_field_validation_state(readiness_payload),
        bundle_row=bundle_row,
        summary_key="field_validation_state",
        missing_action="regenerate_phase6_deployed_field_validation_readiness",
    )
    decision_signal = _summary_alignment_signal(
        id="decision_alignment",
        label="decision",
        expected=_readiness_decision(readiness_payload),
        bundle_row=bundle_row,
        summary_key="decision",
        missing_action="regenerate_phase6_deployed_field_validation_readiness",
    )
    live_url_signal = _summary_alignment_signal(
        id="live_url_alignment",
        label="live_url_present",
        expected=str(_readiness_live_url_present(readiness_payload)),
        bundle_row=bundle_row,
        summary_key="live_url_present",
        missing_action="regenerate_phase6_deployed_field_validation_readiness",
    )
    open_gate_signal = _summary_alignment_signal(
        id="open_gate_alignment",
        label="open_gate_count",
        expected=str(_readiness_open_gate_count(readiness_payload)),
        bundle_row=bundle_row,
        summary_key="open_gate_count",
        missing_action="regenerate_phase6_deployed_field_validation_readiness",
    )

    checks = [
        readiness_signal,
        bundle_signal,
        bundle_row_signal,
        status_alignment_signal,
        field_validation_state_signal,
        decision_signal,
        live_url_signal,
        open_gate_signal,
    ]

    status = "ready" if all(check.status == "ready" for check in checks) else "blocked"
    return Phase6DeployedHandoffConsistencySmokeReport(
        id=PHASE6_DEPLOYED_HANDOFF_CONSISTENCY_SMOKE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="keep_runtime_defaults",
        summary=_summary(readiness_payload, bundle_payload, bundle_row, checks),
        checks=checks,
        notes=[
            "This smoke report is local, read-only, and does not call the deployed provider.",
            "It only compares already-generated readiness and handoff bundle evidence.",
            "A deployed smoke report may still be needed separately for live URL validation.",
        ],
    )


def phase6_deployed_handoff_consistency_smoke_report_to_dict(
    report: Phase6DeployedHandoffConsistencySmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase6_deployed_handoff_consistency_smoke_markdown(
    report: Phase6DeployedHandoffConsistencySmokeReport,
) -> str:
    lines = [
        "# Phase 6 Deployed Handoff Consistency Smoke",
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
        f"| Readiness Status | `{report.summary['readiness_status']}` |",
        f"| Bundle Status | `{report.summary['bundle_status']}` |",
        f"| Bundle Row Status | `{report.summary['bundle_row_status']}` |",
        f"| Field Validation State | `{report.summary['field_validation_state']}` |",
        f"| Live URL Present | `{report.summary['live_url_present']}` |",
        f"| Open Gate Count | `{report.summary['open_gate_count']}` |",
        "",
        "## Checks",
        "",
        "| Check | Required | Status | Summary | Recommended Action |",
        "|---|---|---|---|---|",
    ]
    for check in report.checks:
        lines.append(
            f"| `{check.id}` | `{check.required}` | `{check.status}` | "
            f"{check.summary} | `{check.recommended_action}` |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase6_deployed_handoff_consistency_smoke_report(
    output_dir: Path = Path("docs/smoke/deployed-field-validation"),
    *,
    base_dir: Path = Path("."),
) -> Phase6DeployedHandoffConsistencySmokeReport:
    report = build_phase6_deployed_handoff_consistency_smoke_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase6-deployed-handoff-consistency-smoke.json"
    markdown_path = output_dir / "phase6-deployed-handoff-consistency-smoke.md"
    exported_report = Phase6DeployedHandoffConsistencySmokeReport(
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
            phase6_deployed_handoff_consistency_smoke_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase6_deployed_handoff_consistency_smoke_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _artifact_signal(
    *,
    id: str,
    path: Path,
    payload: dict[str, Any] | None,
    required: bool,
    missing_action: str,
) -> Phase6DeployedHandoffConsistencySmokeCheck:
    if not isinstance(payload, dict):
        return Phase6DeployedHandoffConsistencySmokeCheck(
            id=id,
            required=required,
            status="blocked",
            summary="artifact_present=false",
            recommended_action=missing_action,
            evidence_path=str(path),
        )
    raw_status = _normalize_status(payload.get("status", "review"))
    summary = (
        f"artifact_present=true; status={raw_status}; "
        f"field_validation_state={payload.get('field_validation_state', 'review')}; "
        f"decision={payload.get('decision', 'keep_runtime_defaults')}; "
        f"live_url_present={_readiness_live_url_present(payload)}; "
        f"open_gate_count={_readiness_open_gate_count(payload)}"
    )
    return Phase6DeployedHandoffConsistencySmokeCheck(
        id=id,
        required=required,
        status="ready",
        summary=summary,
        recommended_action="no_action_required",
        evidence_path=str(path),
    )


def _bundle_row_signal(
    bundle_row: dict[str, Any] | None,
) -> Phase6DeployedHandoffConsistencySmokeCheck:
    if not isinstance(bundle_row, dict):
        return Phase6DeployedHandoffConsistencySmokeCheck(
            id="provider_handoff_bundle_row",
            required=True,
            status="blocked",
            summary="bundle_row_present=false",
            recommended_action="regenerate_provider_handoff_bundle",
            evidence_path=str(PROVIDER_HANDOFF_BUNDLE_PATH),
        )
    return Phase6DeployedHandoffConsistencySmokeCheck(
        id="provider_handoff_bundle_row",
        required=True,
        status="ready",
        summary=(
            f"bundle_row_present=true; bundle_row_status={bundle_row.get('status', 'review')}; "
            f"bundle_row_summary={bundle_row.get('summary', 'unknown')}"
        ),
        recommended_action="no_action_required",
        evidence_path=str(PROVIDER_HANDOFF_BUNDLE_PATH),
    )


def _bundle_signal(
    payload: dict[str, Any] | None,
) -> Phase6DeployedHandoffConsistencySmokeCheck:
    if not isinstance(payload, dict):
        return Phase6DeployedHandoffConsistencySmokeCheck(
            id="provider_handoff_bundle",
            required=True,
            status="blocked",
            summary="artifact_present=false",
            recommended_action="regenerate_provider_handoff_bundle",
            evidence_path=str(PROVIDER_HANDOFF_BUNDLE_PATH),
        )
    evidence_artifacts = payload.get("evidence_artifacts", [])
    artifact_count = len(evidence_artifacts) if isinstance(evidence_artifacts, list) else 0
    raw_status = _normalize_status(payload.get("status", "review"))
    return Phase6DeployedHandoffConsistencySmokeCheck(
        id="provider_handoff_bundle",
        required=True,
        status="ready",
        summary=f"artifact_present=true; status={raw_status}; artifact_count={artifact_count}",
        recommended_action="no_action_required",
        evidence_path=str(PROVIDER_HANDOFF_BUNDLE_PATH),
    )


def _status_alignment_signal(
    *,
    readiness_payload: dict[str, Any] | None,
    bundle_row: dict[str, Any] | None,
) -> Phase6DeployedHandoffConsistencySmokeCheck:
    if not isinstance(readiness_payload, dict) or not isinstance(bundle_row, dict):
        return Phase6DeployedHandoffConsistencySmokeCheck(
            id="status_alignment",
            required=True,
            status="blocked",
            summary="status_alignment=unavailable",
            recommended_action="regenerate_phase6_deployed_field_validation_readiness",
            evidence_path=str(DEPLOYED_FIELD_VALIDATION_READINESS_PATH),
        )
    readiness_status = _normalize_status(readiness_payload.get("status", "review"))
    bundle_status = _normalize_status(bundle_row.get("status", "review"))
    passed = readiness_status == bundle_status
    return Phase6DeployedHandoffConsistencySmokeCheck(
        id="status_alignment",
        required=True,
        status="ready" if passed else "blocked",
        summary=(
            f"readiness_status={readiness_status}; bundle_row_status={bundle_status}"
        ),
        recommended_action=_recommended_action("ready" if passed else "blocked"),
        evidence_path=str(PROVIDER_HANDOFF_BUNDLE_PATH),
    )


def _summary_alignment_signal(
    *,
    id: str,
    label: str,
    expected: str,
    bundle_row: dict[str, Any] | None,
    summary_key: str,
    missing_action: str,
) -> Phase6DeployedHandoffConsistencySmokeCheck:
    if not isinstance(bundle_row, dict):
        return Phase6DeployedHandoffConsistencySmokeCheck(
            id=id,
            required=True,
            status="blocked",
            summary=f"{label}=unavailable",
            recommended_action=missing_action,
            evidence_path=str(PROVIDER_HANDOFF_BUNDLE_PATH),
        )
    row_summary = str(bundle_row.get("summary", ""))
    passed = f"{summary_key}={expected}" in row_summary
    return Phase6DeployedHandoffConsistencySmokeCheck(
        id=id,
        required=True,
        status="ready" if passed else "blocked",
        summary=f"expected={expected}; bundle_summary={row_summary}",
        recommended_action=_recommended_action("ready" if passed else "blocked"),
        evidence_path=str(PROVIDER_HANDOFF_BUNDLE_PATH),
    )


def _bundle_row(
    payload: dict[str, Any] | None,
    artifact_id: str,
) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    artifacts = payload.get("evidence_artifacts", [])
    if not isinstance(artifacts, list):
        return None
    for artifact in artifacts:
        if isinstance(artifact, dict) and artifact.get("id") == artifact_id:
            return artifact
    return None


def _summary(
    readiness_payload: dict[str, Any] | None,
    bundle_payload: dict[str, Any] | None,
    bundle_row: dict[str, Any] | None,
    checks: list[Phase6DeployedHandoffConsistencySmokeCheck],
) -> dict[str, Any]:
    return {
        "total_checks": len(checks),
        "passed_checks": sum(1 for check in checks if check.status == "ready"),
        "failed_checks": sum(1 for check in checks if check.status == "blocked"),
        "readiness_status": _normalize_status(_readiness_status(readiness_payload)),
        "bundle_status": _normalize_status(_bundle_status(bundle_payload)),
        "bundle_row_status": _normalize_status(
            bundle_row.get("status", "review") if isinstance(bundle_row, dict) else "review"
        ),
        "field_validation_state": _readiness_field_validation_state(readiness_payload),
        "live_url_present": _readiness_live_url_present(readiness_payload),
        "open_gate_count": _readiness_open_gate_count(readiness_payload),
    }


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _readiness_status(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "review"
    return str(payload.get("status", "review"))


def _readiness_decision(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "keep_local_review_until_deployed_smoke"
    return str(payload.get("decision", "keep_local_review_until_deployed_smoke"))


def _readiness_field_validation_state(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "review"
    return str(payload.get("field_validation_state", "review"))


def _readiness_live_url_present(payload: dict[str, Any] | None) -> bool:
    if not isinstance(payload, dict):
        return False
    summary = payload.get("summary", {})
    if not isinstance(summary, dict):
        return False
    return bool(summary.get("live_url_present", False))


def _readiness_open_gate_count(payload: dict[str, Any] | None) -> int:
    if not isinstance(payload, dict):
        return 0
    summary = payload.get("summary", {})
    if not isinstance(summary, dict):
        return 0
    open_gate_ids = summary.get("open_gate_ids", [])
    if isinstance(open_gate_ids, list):
        return len(open_gate_ids)
    return 0


def _bundle_status(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "review"
    return str(payload.get("status", "review"))


def _normalize_status(value: Any) -> str:
    if value in {"ready", "review", "blocked"}:
        return str(value)
    return "review"


def _recommended_action(status: str) -> str:
    if status == "ready":
        return "no_action_required"
    if status == "review":
        return "review_evidence_notes"
    return "regenerate_evidence"
