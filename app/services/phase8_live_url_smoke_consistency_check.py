import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE8_LIVE_URL_SMOKE_CONSISTENCY_CHECK_ID = (
    "phase8-live-url-smoke-consistency-check-v1"
)
PHASE8_LIVE_URL_VALIDATION_READINESS_PATH = Path(
    "docs/operations/live-url-validation/"
    "phase8-live-url-validation-readiness.json"
)
PROVIDER_HANDOFF_BUNDLE_PATH = Path(
    "docs/integration/provider-handoff/provider-handoff-bundle.json"
)
READINESS_ARTIFACT_ID = "phase8_live_url_validation_readiness"
PHASE8_LIVE_URL_SMOKE_CONSISTENCY_CHECK_JSON = (
    "phase8-live-url-smoke-consistency-check.json"
)
PHASE8_LIVE_URL_SMOKE_CONSISTENCY_CHECK_MARKDOWN = (
    "phase8-live-url-smoke-consistency-check.md"
)


@dataclass(frozen=True)
class Phase8LiveUrlSmokeConsistencyCheck:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase8LiveUrlSmokeConsistencyReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    checks: list[Phase8LiveUrlSmokeConsistencyCheck]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase8_live_url_smoke_consistency_check_report(
    *,
    base_dir: Path = Path("."),
) -> Phase8LiveUrlSmokeConsistencyReport:
    readiness_payload = _read_json_if_present(
        base_dir / PHASE8_LIVE_URL_VALIDATION_READINESS_PATH
    )
    bundle_payload = _read_json_if_present(base_dir / PROVIDER_HANDOFF_BUNDLE_PATH)
    bundle_row = _bundle_row(bundle_payload, READINESS_ARTIFACT_ID)

    checks = [
        _artifact_signal(
            id="phase8_live_url_validation_readiness",
            path=PHASE8_LIVE_URL_VALIDATION_READINESS_PATH,
            payload=readiness_payload,
            required=True,
            missing_action="regenerate_phase8_live_url_validation_readiness",
        ),
        _bundle_signal(bundle_payload),
        _bundle_row_signal(bundle_row),
        _status_alignment_signal(
            readiness_payload=readiness_payload,
            bundle_row=bundle_row,
        ),
        _summary_alignment_signal(
            id="live_validation_state_alignment",
            label="live_validation_state",
            expected=_readiness_live_validation_state(readiness_payload),
            bundle_row=bundle_row,
            summary_key="live_validation_state",
            missing_action="regenerate_phase8_live_url_validation_readiness",
        ),
        _summary_alignment_signal(
            id="decision_alignment",
            label="decision",
            expected=_readiness_decision(readiness_payload),
            bundle_row=bundle_row,
            summary_key="decision",
            missing_action="regenerate_phase8_live_url_validation_readiness",
        ),
        _summary_alignment_signal(
            id="deployed_smoke_present_alignment",
            label="deployed_smoke_present",
            expected=str(_readiness_deployed_smoke_present(readiness_payload)),
            bundle_row=bundle_row,
            summary_key="deployed_smoke_present",
            missing_action="regenerate_phase8_live_url_validation_readiness",
        ),
        _summary_alignment_signal(
            id="deployed_smoke_status_alignment",
            label="deployed_smoke_status",
            expected=_readiness_deployed_smoke_status(readiness_payload),
            bundle_row=bundle_row,
            summary_key="deployed_smoke_status",
            missing_action="regenerate_phase8_live_url_validation_readiness",
        ),
        _summary_alignment_signal(
            id="live_url_present_alignment",
            label="live_url_present",
            expected=str(_readiness_live_url_present(readiness_payload)),
            bundle_row=bundle_row,
            summary_key="live_url_present",
            missing_action="regenerate_phase8_live_url_validation_readiness",
        ),
        _summary_alignment_signal(
            id="open_gate_count_alignment",
            label="open_gate_count",
            expected=str(_readiness_open_gate_count(readiness_payload)),
            bundle_row=bundle_row,
            summary_key="open_gate_count",
            missing_action="regenerate_phase8_live_url_validation_readiness",
        ),
    ]

    status = "ready" if all(check.status == "ready" for check in checks) else "blocked"
    return Phase8LiveUrlSmokeConsistencyReport(
        id=PHASE8_LIVE_URL_SMOKE_CONSISTENCY_CHECK_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        decision="keep_runtime_defaults_until_live_url_validation",
        summary=_summary(readiness_payload, bundle_payload, bundle_row, checks),
        checks=checks,
        notes=[
            "This smoke is local read-only consistency evidence.",
            "It compares the current Phase 8 readiness export with the handoff bundle row.",
            "It does not call deployed endpoints or promote runtime defaults.",
        ],
    )


def phase8_live_url_smoke_consistency_check_report_to_dict(
    report: Phase8LiveUrlSmokeConsistencyReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase8_live_url_smoke_consistency_check_markdown(
    report: Phase8LiveUrlSmokeConsistencyReport,
) -> str:
    lines = [
        "# Phase 8 Live URL Smoke Consistency Check",
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
        f"| Live Validation State | `{report.summary['live_validation_state']}` |",
        f"| Deployed Smoke Present | `{report.summary['deployed_smoke_present']}` |",
        f"| Deployed Smoke Status | `{report.summary['deployed_smoke_status']}` |",
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


def export_phase8_live_url_smoke_consistency_check_report(
    output_dir: Path = Path("docs/smoke/live-url-validation"),
    *,
    base_dir: Path = Path("."),
) -> Phase8LiveUrlSmokeConsistencyReport:
    report = build_phase8_live_url_smoke_consistency_check_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PHASE8_LIVE_URL_SMOKE_CONSISTENCY_CHECK_JSON
    markdown_path = output_dir / PHASE8_LIVE_URL_SMOKE_CONSISTENCY_CHECK_MARKDOWN
    exported = Phase8LiveUrlSmokeConsistencyReport(
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
            phase8_live_url_smoke_consistency_check_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase8_live_url_smoke_consistency_check_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _artifact_signal(
    *,
    id: str,
    path: Path,
    payload: dict[str, Any] | None,
    required: bool,
    missing_action: str,
) -> Phase8LiveUrlSmokeConsistencyCheck:
    if not isinstance(payload, dict):
        return Phase8LiveUrlSmokeConsistencyCheck(
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
        f"live_validation_state={payload.get('live_validation_state', 'review')}; "
        f"decision={payload.get('decision', 'keep_runtime_defaults_until_live_url_validation')}; "
        f"deployed_smoke_present={_readiness_deployed_smoke_present(payload)}; "
        f"deployed_smoke_status={_readiness_deployed_smoke_status(payload)}; "
        f"live_url_present={_readiness_live_url_present(payload)}; "
        f"open_gate_count={_readiness_open_gate_count(payload)}"
    )
    return Phase8LiveUrlSmokeConsistencyCheck(
        id=id,
        required=required,
        status="ready",
        summary=summary,
        recommended_action="no_action_required",
        evidence_path=str(path),
    )


def _bundle_signal(
    payload: dict[str, Any] | None,
) -> Phase8LiveUrlSmokeConsistencyCheck:
    if not isinstance(payload, dict):
        return Phase8LiveUrlSmokeConsistencyCheck(
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
    return Phase8LiveUrlSmokeConsistencyCheck(
        id="provider_handoff_bundle",
        required=True,
        status="ready",
        summary=f"artifact_present=true; status={raw_status}; artifact_count={artifact_count}",
        recommended_action="no_action_required",
        evidence_path=str(PROVIDER_HANDOFF_BUNDLE_PATH),
    )


def _bundle_row_signal(
    bundle_row: dict[str, Any] | None,
) -> Phase8LiveUrlSmokeConsistencyCheck:
    if not isinstance(bundle_row, dict):
        return Phase8LiveUrlSmokeConsistencyCheck(
            id="provider_handoff_bundle_row",
            required=True,
            status="blocked",
            summary="bundle_row_present=false",
            recommended_action="regenerate_provider_handoff_bundle",
            evidence_path=str(PROVIDER_HANDOFF_BUNDLE_PATH),
        )
    return Phase8LiveUrlSmokeConsistencyCheck(
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


def _status_alignment_signal(
    *,
    readiness_payload: dict[str, Any] | None,
    bundle_row: dict[str, Any] | None,
) -> Phase8LiveUrlSmokeConsistencyCheck:
    if not isinstance(readiness_payload, dict) or not isinstance(bundle_row, dict):
        return Phase8LiveUrlSmokeConsistencyCheck(
            id="status_alignment",
            required=True,
            status="blocked",
            summary="status_alignment=unavailable",
            recommended_action="regenerate_phase8_live_url_validation_readiness",
            evidence_path=str(PHASE8_LIVE_URL_VALIDATION_READINESS_PATH),
        )
    readiness_status = _normalize_status(readiness_payload.get("status", "review"))
    bundle_status = _normalize_status(bundle_row.get("status", "review"))
    passed = readiness_status == bundle_status
    return Phase8LiveUrlSmokeConsistencyCheck(
        id="status_alignment",
        required=True,
        status="ready" if passed else "blocked",
        summary=f"readiness_status={readiness_status}; bundle_row_status={bundle_status}",
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
) -> Phase8LiveUrlSmokeConsistencyCheck:
    if not isinstance(bundle_row, dict):
        return Phase8LiveUrlSmokeConsistencyCheck(
            id=id,
            required=True,
            status="blocked",
            summary=f"{label}=unavailable",
            recommended_action=missing_action,
            evidence_path=str(PROVIDER_HANDOFF_BUNDLE_PATH),
        )
    row_summary = str(bundle_row.get("summary", ""))
    passed = f"{summary_key}={expected}" in row_summary
    return Phase8LiveUrlSmokeConsistencyCheck(
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
    checks: list[Phase8LiveUrlSmokeConsistencyCheck],
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
        "live_validation_state": _readiness_live_validation_state(readiness_payload),
        "deployed_smoke_present": _readiness_deployed_smoke_present(readiness_payload),
        "deployed_smoke_status": _readiness_deployed_smoke_status(readiness_payload),
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
        return "keep_runtime_defaults_until_live_url_validation"
    return str(payload.get("decision", "keep_runtime_defaults_until_live_url_validation"))


def _readiness_live_validation_state(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "review"
    return str(payload.get("live_validation_state", "review"))


def _readiness_deployed_smoke_present(payload: dict[str, Any] | None) -> bool:
    summary = _dict_value(payload, "summary", {})
    return bool(_dict_value(summary, "deployed_smoke_present", False))


def _readiness_deployed_smoke_status(payload: dict[str, Any] | None) -> str:
    summary = _dict_value(payload, "summary", {})
    return str(_dict_value(summary, "deployed_smoke_status", "review"))


def _readiness_live_url_present(payload: dict[str, Any] | None) -> bool:
    summary = _dict_value(payload, "summary", {})
    return bool(_dict_value(summary, "live_url_present", False))


def _readiness_open_gate_count(payload: dict[str, Any] | None) -> int:
    summary = _dict_value(payload, "summary", {})
    open_gate_ids = _dict_value(summary, "open_gate_ids", [])
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


def _dict_value(value: Any, key: str, fallback: Any) -> Any:
    if not isinstance(value, dict):
        return fallback
    return value.get(key, fallback)


def _recommended_action(status: str) -> str:
    if status == "ready":
        return "no_action_required"
    if status == "review":
        return "review_evidence_notes"
    return "regenerate_evidence"
