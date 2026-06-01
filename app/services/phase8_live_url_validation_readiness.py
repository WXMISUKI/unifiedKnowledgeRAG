import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE8_LIVE_URL_VALIDATION_READINESS_ID = "phase8-live-url-validation-readiness-v1"
PHASE8_CONTRACT_PATH = Path(
    "docs/operations/live-url-validation/"
    "phase8-live-url-validation-execution-contract.md"
)
PHASE6_DEPLOYED_FIELD_VALIDATION_PATH = Path(
    "docs/operations/deployed-field-validation/"
    "phase6-deployed-field-validation-readiness.json"
)
PHASE7_PROVIDER_RELEASE_READINESS_PATH = Path(
    "docs/operations/provider-release-readiness/"
    "phase7-provider-release-readiness.json"
)
DEPLOYED_PROVIDER_SMOKE_PATH = Path(
    "docs/integration/deployed-provider-smoke/deployed-provider-smoke.json"
)
PHASE8_LIVE_URL_VALIDATION_READINESS_JSON = "phase8-live-url-validation-readiness.json"
PHASE8_LIVE_URL_VALIDATION_READINESS_MARKDOWN = (
    "phase8-live-url-validation-readiness.md"
)


@dataclass(frozen=True)
class Phase8LiveUrlValidationSignal:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase8LiveUrlValidationReadinessReport:
    id: str
    generated_at: str
    status: str
    live_validation_state: str
    decision: str
    summary: dict[str, Any]
    signals: list[Phase8LiveUrlValidationSignal]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase8_live_url_validation_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase8LiveUrlValidationReadinessReport:
    contract_signal = _contract_signal(base_dir)
    phase6_signal = _phase6_deployed_field_validation_signal(base_dir)
    phase7_signal = _phase7_provider_release_signal(base_dir)
    deployed_smoke_signal = _deployed_smoke_signal(base_dir)
    signals = [contract_signal, phase6_signal, phase7_signal, deployed_smoke_signal]

    required_blocked = any(
        signal.required and signal.status == "blocked" for signal in signals
    )
    required_review = any(
        signal.required and signal.status == "review" for signal in signals
    )
    deployed_smoke_present = (base_dir / DEPLOYED_PROVIDER_SMOKE_PATH).exists()
    live_url_present = _live_url_present(base_dir / DEPLOYED_PROVIDER_SMOKE_PATH)
    deployed_smoke_status = deployed_smoke_signal.status

    if required_blocked or deployed_smoke_status == "blocked":
        status = "blocked"
        live_validation_state = "blocked"
        decision = "resolve_live_url_validation_blockers"
    elif not deployed_smoke_present:
        status = "review"
        live_validation_state = "await_live_url_validation"
        decision = "keep_runtime_defaults_until_live_url_validation"
    elif required_review or deployed_smoke_status == "review":
        status = "review"
        live_validation_state = "review"
        decision = "keep_runtime_defaults_until_live_url_validation"
    elif live_url_present:
        status = "ready"
        live_validation_state = "ready_for_live_url_validation"
        decision = "confirm_live_url_validation_evidence"
    else:
        status = "review"
        live_validation_state = "review"
        decision = "keep_runtime_defaults_until_live_url_validation"

    return Phase8LiveUrlValidationReadinessReport(
        id=PHASE8_LIVE_URL_VALIDATION_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        live_validation_state=live_validation_state,
        decision=decision,
        summary=_summary(
            signals,
            live_url_present=live_url_present,
            deployed_smoke_present=deployed_smoke_present,
            deployed_smoke_status=deployed_smoke_status,
        ),
        signals=signals,
        notes=[
            "This report is local read-only evidence for deployed live URL validation.",
            "It summarizes existing Phase 6/Phase 7/read-only deployed smoke artifacts.",
            "It does not promote runtime defaults or replace caller-side release decisions.",
        ],
    )


def phase8_live_url_validation_readiness_report_to_dict(
    report: Phase8LiveUrlValidationReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase8_live_url_validation_readiness_markdown(
    report: Phase8LiveUrlValidationReadinessReport,
) -> str:
    lines = [
        "# Phase 8 Live URL Validation Readiness",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Live Validation State: `{report.live_validation_state}`",
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
        f"| Deployed Smoke Present | `{report.summary['deployed_smoke_present']}` |",
        f"| Deployed Smoke Status | `{report.summary['deployed_smoke_status']}` |",
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


def export_phase8_live_url_validation_readiness_report(
    output_dir: Path = Path("docs/operations/live-url-validation"),
    *,
    base_dir: Path = Path("."),
) -> Phase8LiveUrlValidationReadinessReport:
    report = build_phase8_live_url_validation_readiness_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PHASE8_LIVE_URL_VALIDATION_READINESS_JSON
    markdown_path = output_dir / PHASE8_LIVE_URL_VALIDATION_READINESS_MARKDOWN
    exported = Phase8LiveUrlValidationReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        live_validation_state=report.live_validation_state,
        decision=report.decision,
        summary=report.summary,
        signals=report.signals,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase8_live_url_validation_readiness_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase8_live_url_validation_readiness_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _contract_signal(base_dir: Path) -> Phase8LiveUrlValidationSignal:
    path = base_dir / PHASE8_CONTRACT_PATH
    if path.exists():
        return Phase8LiveUrlValidationSignal(
            id="phase8_live_url_validation_execution_contract",
            required=True,
            status="ready",
            summary="contract_present=true",
            recommended_action="no_action_required",
            evidence_path=str(PHASE8_CONTRACT_PATH),
        )
    return Phase8LiveUrlValidationSignal(
        id="phase8_live_url_validation_execution_contract",
        required=True,
        status="blocked",
        summary="contract_present=false",
        recommended_action="restore_phase8_live_url_validation_execution_contract",
        evidence_path=str(PHASE8_CONTRACT_PATH),
    )


def _phase6_deployed_field_validation_signal(
    base_dir: Path,
) -> Phase8LiveUrlValidationSignal:
    path = base_dir / PHASE6_DEPLOYED_FIELD_VALIDATION_PATH
    payload = _read_json_if_present(path)
    if payload is None:
        return Phase8LiveUrlValidationSignal(
            id="phase6_deployed_field_validation_readiness",
            required=True,
            status="blocked",
            summary="artifact_present=false",
            recommended_action="regenerate_phase6_deployed_field_validation_readiness",
            evidence_path=str(PHASE6_DEPLOYED_FIELD_VALIDATION_PATH),
        )
    status = _normalize_status(payload.get("status"))
    summary = payload.get("summary", {})
    open_gate_ids = summary.get("open_gate_ids", []) if isinstance(summary, dict) else []
    return Phase8LiveUrlValidationSignal(
        id="phase6_deployed_field_validation_readiness",
        required=True,
        status=status,
        summary=(
            f"artifact_present=true; status={status}; "
            f"field_validation_state={payload.get('field_validation_state', 'review')}; "
            f"decision={payload.get('decision', 'keep_local_review_until_deployed_smoke')}; "
            f"live_url_present={bool(_dict_value(summary, 'live_url_present', False))}; "
            f"open_gate_count={_int_value(len(open_gate_ids), fallback=0)}"
        ),
        recommended_action=(
            "no_action_required" if status == "ready" else "review_evidence_notes"
        ),
        evidence_path=str(PHASE6_DEPLOYED_FIELD_VALIDATION_PATH),
    )


def _phase7_provider_release_signal(base_dir: Path) -> Phase8LiveUrlValidationSignal:
    path = base_dir / PHASE7_PROVIDER_RELEASE_READINESS_PATH
    payload = _read_json_if_present(path)
    if payload is None:
        return Phase8LiveUrlValidationSignal(
            id="phase7_provider_release_readiness",
            required=True,
            status="blocked",
            summary="artifact_present=false",
            recommended_action="regenerate_phase7_provider_release_readiness",
            evidence_path=str(PHASE7_PROVIDER_RELEASE_READINESS_PATH),
        )
    status = _normalize_status(payload.get("status"))
    summary = payload.get("summary", {})
    open_gate_ids = summary.get("open_gate_ids", []) if isinstance(summary, dict) else []
    return Phase8LiveUrlValidationSignal(
        id="phase7_provider_release_readiness",
        required=True,
        status=status,
        summary=(
            f"artifact_present=true; status={status}; "
            f"release_state={payload.get('release_state', 'review')}; "
            f"decision={payload.get('decision', 'keep_runtime_defaults')}; "
            f"local_handoff_ready={bool(_dict_value(summary, 'ready_for_local_provider_handoff', False))}; "
            f"runtime_promotion_ready={bool(_dict_value(summary, 'ready_for_runtime_default_promotion', False))}; "
            f"open_gate_count={_int_value(len(open_gate_ids), fallback=0)}"
        ),
        recommended_action=(
            "no_action_required" if status == "ready" else "review_evidence_notes"
        ),
        evidence_path=str(PHASE7_PROVIDER_RELEASE_READINESS_PATH),
    )


def _deployed_smoke_signal(base_dir: Path) -> Phase8LiveUrlValidationSignal:
    path = base_dir / DEPLOYED_PROVIDER_SMOKE_PATH
    payload = _read_json_if_present(path)
    if payload is None:
        return Phase8LiveUrlValidationSignal(
            id="deployed_provider_smoke",
            required=False,
            status="review",
            summary="artifact_present=false",
            recommended_action="run_deployed_provider_smoke_after_deployment",
            evidence_path=str(DEPLOYED_PROVIDER_SMOKE_PATH),
        )
    status = _normalize_status(payload.get("status"))
    handoff_status = _dict_value(_dict_value(payload, "handoff", {}), "status", "unknown")
    checks = payload.get("checks", [])
    check_count = len(checks) if isinstance(checks, list) else 0
    return Phase8LiveUrlValidationSignal(
        id="deployed_provider_smoke",
        required=False,
        status=status,
        summary=(
            f"artifact_present=true; status={status}; "
            f"base_url={payload.get('base_url', 'missing')}; "
            f"handoff_status={handoff_status}; "
            f"check_count={_int_value(check_count, fallback=0)}"
        ),
        recommended_action=(
            "no_action_required" if status == "ready" else "review_evidence_notes"
        ),
        evidence_path=str(DEPLOYED_PROVIDER_SMOKE_PATH),
    )


def _summary(
    signals: list[Phase8LiveUrlValidationSignal],
    *,
    live_url_present: bool,
    deployed_smoke_present: bool,
    deployed_smoke_status: str,
) -> dict[str, Any]:
    return {
        "total_signals": len(signals),
        "required_signals": sum(1 for signal in signals if signal.required),
        "ready_signals": sum(1 for signal in signals if signal.status == "ready"),
        "review_signals": sum(1 for signal in signals if signal.status == "review"),
        "blocked_signals": sum(1 for signal in signals if signal.status == "blocked"),
        "deployed_smoke_present": deployed_smoke_present,
        "deployed_smoke_status": deployed_smoke_status,
        "live_url_present": live_url_present,
        "open_gate_ids": [
            signal.id for signal in signals if signal.status in {"review", "blocked"}
        ],
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
