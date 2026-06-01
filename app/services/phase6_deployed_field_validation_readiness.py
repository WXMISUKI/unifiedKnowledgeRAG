import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE6_DEPLOYED_FIELD_VALIDATION_READINESS_ID = (
    "phase6-deployed-field-validation-readiness-v1"
)

CONTRACT_PATH = Path(
    "docs/operations/deployed-field-validation/"
    "phase6-deployed-field-validation-contract.md"
)
DEPLOYMENT_READINESS_PATH = Path(
    "docs/operations/deployment-readiness/deployment-readiness.json"
)
HANDOFF_BUNDLE_PATH = Path("docs/integration/provider-handoff/provider-handoff-bundle.json")
DEPLOYED_SMOKE_PATH = Path(
    "docs/integration/deployed-provider-smoke/deployed-provider-smoke.json"
)


@dataclass(frozen=True)
class Phase6DeployedFieldValidationSignal:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase6DeployedFieldValidationReadinessReport:
    id: str
    generated_at: str
    status: str
    field_validation_state: str
    decision: str
    summary: dict[str, Any]
    signals: list[Phase6DeployedFieldValidationSignal]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase6_deployed_field_validation_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase6DeployedFieldValidationReadinessReport:
    signals = [
        _contract_signal(base_dir),
        _required_artifact_signal(
            id="deployment_readiness",
            path=DEPLOYMENT_READINESS_PATH,
            base_dir=base_dir,
            missing_action="regenerate_deployment_readiness",
        ),
        _required_artifact_signal(
            id="provider_handoff_bundle",
            path=HANDOFF_BUNDLE_PATH,
            base_dir=base_dir,
            missing_action="regenerate_provider_handoff_bundle",
        ),
        _optional_artifact_signal(
            id="deployed_provider_smoke",
            path=DEPLOYED_SMOKE_PATH,
            base_dir=base_dir,
            missing_action="run_deployed_provider_smoke_after_deployment",
        ),
    ]

    required_blocked = any(
        signal.required and signal.status == "blocked" for signal in signals
    )
    required_review = any(
        signal.required and signal.status == "review" for signal in signals
    )
    optional_blocked = any(
        (not signal.required) and signal.status == "blocked" for signal in signals
    )

    deployed_smoke_present = signals[-1].status != "review" or (
        base_dir / DEPLOYED_SMOKE_PATH
    ).exists()
    live_url_present = _live_url_present(base_dir / DEPLOYED_SMOKE_PATH)

    if required_blocked or optional_blocked:
        status = "blocked"
        field_validation_state = "blocked"
        decision = "blocked"
    elif not deployed_smoke_present:
        status = "review"
        field_validation_state = "await_live_url"
        decision = "keep_local_review_until_deployed_smoke"
    elif required_review:
        status = "review"
        field_validation_state = "review"
        decision = "keep_local_review_until_deployed_smoke"
    elif live_url_present:
        status = "ready"
        field_validation_state = "ready_for_live_validation"
        decision = "confirm_deployed_field_validation"
    else:
        status = "review"
        field_validation_state = "review"
        decision = "keep_local_review_until_deployed_smoke"

    return Phase6DeployedFieldValidationReadinessReport(
        id=PHASE6_DEPLOYED_FIELD_VALIDATION_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        field_validation_state=field_validation_state,
        decision=decision,
        summary=_summary(signals, live_url_present=live_url_present),
        signals=signals,
        notes=[
            "This report is local read-only field validation evidence.",
            "It only summarizes existing deployment, handoff, and deployed smoke artifacts.",
            "A live URL is required before the field validation posture can be considered ready.",
        ],
    )


def phase6_deployed_field_validation_readiness_report_to_dict(
    report: Phase6DeployedFieldValidationReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase6_deployed_field_validation_readiness_markdown(
    report: Phase6DeployedFieldValidationReadinessReport,
) -> str:
    lines = [
        "# Phase 6 Deployed Field Validation Readiness",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Field Validation State: `{report.field_validation_state}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Signals | `{report.summary['total_signals']}` |",
        f"| Required Signals | `{report.summary['required_signals']}` |",
        f"| Ready Signals | `{report.summary['ready_signals']}` |",
        f"| Review Signals | `{report.summary['review_signals']}` |",
        f"| Blocked Signals | `{report.summary['blocked_signals']}` |",
        f"| Live URL Present | `{report.summary['live_url_present']}` |",
        f"| Open Gate IDs | `{json.dumps(report.summary['open_gate_ids'])}` |",
        "",
        "## Signals",
        "",
        "| Signal | Required | Status | Summary | Recommended Action |",
        "|---|---|---|---|---|",
    ]
    for signal in report.signals:
        lines.append(
            f"| `{signal.id}` | `{signal.required}` | `{signal.status}` | "
            f"{signal.summary} | `{signal.recommended_action}` |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase6_deployed_field_validation_readiness_report(
    output_dir: Path = Path("docs/operations/deployed-field-validation"),
    *,
    base_dir: Path = Path("."),
) -> Phase6DeployedFieldValidationReadinessReport:
    report = build_phase6_deployed_field_validation_readiness_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase6-deployed-field-validation-readiness.json"
    markdown_path = output_dir / "phase6-deployed-field-validation-readiness.md"
    exported = Phase6DeployedFieldValidationReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        field_validation_state=report.field_validation_state,
        decision=report.decision,
        summary=report.summary,
        signals=report.signals,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase6_deployed_field_validation_readiness_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase6_deployed_field_validation_readiness_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _contract_signal(base_dir: Path) -> Phase6DeployedFieldValidationSignal:
    path = base_dir / CONTRACT_PATH
    if path.exists():
        return Phase6DeployedFieldValidationSignal(
            id="deployed_field_validation_contract",
            required=True,
            status="ready",
            summary="contract_present=true",
            recommended_action="no_action_required",
            evidence_path=str(CONTRACT_PATH),
        )
    return Phase6DeployedFieldValidationSignal(
        id="deployed_field_validation_contract",
        required=True,
        status="blocked",
        summary="contract_present=false",
        recommended_action="restore_deployed_field_validation_contract",
        evidence_path=str(CONTRACT_PATH),
    )


def _required_artifact_signal(
    *,
    id: str,
    path: Path,
    base_dir: Path,
    missing_action: str,
) -> Phase6DeployedFieldValidationSignal:
    return _artifact_signal(
        id=id,
        required=True,
        path=path,
        base_dir=base_dir,
        missing_action=missing_action,
    )


def _optional_artifact_signal(
    *,
    id: str,
    path: Path,
    base_dir: Path,
    missing_action: str,
) -> Phase6DeployedFieldValidationSignal:
    return _artifact_signal(
        id=id,
        required=False,
        path=path,
        base_dir=base_dir,
        missing_action=missing_action,
    )


def _artifact_signal(
    *,
    id: str,
    required: bool,
    path: Path,
    base_dir: Path,
    missing_action: str,
) -> Phase6DeployedFieldValidationSignal:
    full_path = base_dir / path
    if not full_path.exists():
        return Phase6DeployedFieldValidationSignal(
            id=id,
            required=required,
            status="blocked" if required else "review",
            summary="artifact_present=false",
            recommended_action=missing_action,
            evidence_path=str(path),
        )

    payload = _read_json_if_present(full_path)
    status = _normalize_status(_dict_value(payload, "status", "review"))
    if id == "deployment_readiness":
        summary = (
            f"artifact_present=true; status={status}; "
            f"retrieval_backend={_dict_value(_dict_value(payload, 'runtime_config', {}), 'rag_retrieval_backend', 'unknown')}"
        )
        recommended_action = (
            "no_action_required" if status == "ready" else "review_evidence_notes"
        )
        return Phase6DeployedFieldValidationSignal(
            id=id,
            required=required,
            status=status,
            summary=summary,
            recommended_action=recommended_action,
            evidence_path=str(path),
        )

    if id == "provider_handoff_bundle":
        summary = (
            f"artifact_present=true; status={status}; "
            f"artifact_count={_int_value(len(_dict_value(payload, 'evidence_artifacts', [])), fallback=0)}"
        )
        recommended_action = (
            "no_action_required" if status == "ready" else "review_evidence_notes"
        )
        return Phase6DeployedFieldValidationSignal(
            id=id,
            required=required,
            status=status,
            summary=summary,
            recommended_action=recommended_action,
            evidence_path=str(path),
        )

    smoke_base_url = _dict_value(payload, "base_url", "")
    handoff_status = _dict_value(_dict_value(payload, "handoff", {}), "status", "unknown")
    smoke_status = status
    if smoke_status == "blocked" or not smoke_base_url:
        signal_status = "blocked"
    else:
        signal_status = smoke_status
    summary = (
        f"artifact_present=true; status={smoke_status}; "
        f"base_url={smoke_base_url or 'missing'}; handoff_status={handoff_status}"
    )
    recommended_action = (
        "no_action_required" if signal_status == "ready" else "review_evidence_notes"
    )
    return Phase6DeployedFieldValidationSignal(
        id=id,
        required=required,
        status=signal_status,
        summary=summary,
        recommended_action=recommended_action,
        evidence_path=str(path),
    )


def _summary(
    signals: list[Phase6DeployedFieldValidationSignal],
    *,
    live_url_present: bool,
) -> dict[str, Any]:
    return {
        "total_signals": len(signals),
        "required_signals": sum(1 for signal in signals if signal.required),
        "ready_signals": sum(1 for signal in signals if signal.status == "ready"),
        "review_signals": sum(1 for signal in signals if signal.status == "review"),
        "blocked_signals": sum(1 for signal in signals if signal.status == "blocked"),
        "open_gate_ids": [
            signal.id for signal in signals if signal.status in {"review", "blocked"}
        ],
        "live_url_present": live_url_present,
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


def _int_value(value: Any, *, fallback: int) -> int:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int) and value >= 0:
        return value
    return fallback


def _live_url_present(path: Path) -> bool:
    payload = _read_json_if_present(path)
    if not isinstance(payload, dict):
        return False
    base_url = payload.get("base_url")
    return isinstance(base_url, str) and bool(base_url.strip())
