import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE9_LOCAL_CONSUMPTION_READINESS_ID = (
    "phase9-myprivateagent-local-consumption-readiness-v1"
)
PHASE9_CONTRACT_PATH = Path(
    "docs/integration/myprivateagent-local-consumption/"
    "phase9-myprivateagent-local-consumption-contract.md"
)
PHASE7_PROVIDER_RELEASE_READINESS_PATH = Path(
    "docs/operations/provider-release-readiness/"
    "phase7-provider-release-readiness.json"
)
PHASE8_LIVE_URL_VALIDATION_READINESS_PATH = Path(
    "docs/operations/live-url-validation/"
    "phase8-live-url-validation-readiness.json"
)
PROVIDER_INTEGRATION_PROBE_PATH = Path(
    "docs/integration/provider-binding/provider-integration-probe.json"
)
DEPLOYED_PROVIDER_SMOKE_PATH = Path(
    "docs/integration/deployed-provider-smoke/deployed-provider-smoke.json"
)
SOURCE_BINDING_SUMMARY_PATH = Path(
    "docs/integration/source-bindings/provider-source-bindings.json"
)
PHASE4_EVIDENCE_PACK_READINESS_PATH = Path(
    "docs/benchmark/chinese-seed/evidence-pack-readiness/"
    "phase4-evidence-pack-readiness.json"
)
PHASE4_CALLER_CONSUMPTION_SMOKE_PATH = Path(
    "docs/smoke/evidence-pack-consumption/phase4-caller-consumption-smoke.json"
)
READINESS_JSON_FILENAME = "phase9-myprivateagent-local-consumption-readiness.json"
READINESS_MARKDOWN_FILENAME = "phase9-myprivateagent-local-consumption-readiness.md"
LOCAL_PROVIDER_URL_DEFAULT = "http://127.0.0.1:8020"


@dataclass(frozen=True)
class Phase9LocalConsumptionSignal:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase9LocalConsumptionReadinessReport:
    id: str
    generated_at: str
    status: str
    local_consumption_state: str
    decision: str
    summary: dict[str, Any]
    signals: list[Phase9LocalConsumptionSignal]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase9_myprivateagent_local_consumption_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase9LocalConsumptionReadinessReport:
    signals = [
        _contract_signal(base_dir),
        _phase7_release_signal(base_dir),
        _phase8_live_url_signal(base_dir),
        _integration_probe_signal(base_dir),
        _deployed_smoke_signal(base_dir),
        _source_binding_signal(base_dir),
        _phase4_pack_signal(base_dir),
        _phase4_caller_smoke_signal(base_dir),
    ]

    required_blocked = any(
        signal.required and signal.status == "blocked" for signal in signals
    )
    required_review = any(
        signal.required and signal.status == "review" for signal in signals
    )

    phase7_payload = _read_json_if_present(base_dir / PHASE7_PROVIDER_RELEASE_READINESS_PATH)
    phase7_summary = _dict_value(phase7_payload, "summary", {})
    local_handoff_ready = bool(
        _dict_value(phase7_summary, "ready_for_local_provider_handoff", False)
    )
    runtime_promotion_ready = bool(
        _dict_value(phase7_summary, "ready_for_runtime_default_promotion", False)
    )
    open_gate_ids = [s.id for s in signals if s.status in {"review", "blocked"}]

    if required_blocked:
        status = "blocked"
        local_consumption_state = "blocked"
        decision = "resolve_local_consumption_blockers"
    elif required_review or not local_handoff_ready:
        status = "review"
        local_consumption_state = "review"
        decision = "keep_local_consumption_review"
    else:
        status = "ready"
        local_consumption_state = "ready_for_local_consumption"
        decision = "confirm_local_consumption_readiness"

    return Phase9LocalConsumptionReadinessReport(
        id=PHASE9_LOCAL_CONSUMPTION_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        local_consumption_state=local_consumption_state,
        decision=decision,
        summary={
            "total_signals": len(signals),
            "required_signals": sum(1 for signal in signals if signal.required),
            "ready_signals": sum(1 for signal in signals if signal.status == "ready"),
            "review_signals": sum(1 for signal in signals if signal.status == "review"),
            "blocked_signals": sum(1 for signal in signals if signal.status == "blocked"),
            "local_provider_url": _local_provider_url(base_dir),
            "local_handoff_ready": local_handoff_ready,
            "runtime_promotion_ready": runtime_promotion_ready,
            "api_key_mode": _api_key_mode(base_dir),
            "open_gate_ids": open_gate_ids,
        },
        signals=signals,
        notes=[
            "This report is local read-only evidence for MyPrivateAgent local consumption.",
            "It does not change runtime defaults or control-plane ownership boundaries.",
            "Source-to-agent binding policy and final answer governance remain MyPrivateAgent responsibilities.",
        ],
    )


def phase9_myprivateagent_local_consumption_readiness_report_to_dict(
    report: Phase9LocalConsumptionReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase9_myprivateagent_local_consumption_readiness_markdown(
    report: Phase9LocalConsumptionReadinessReport,
) -> str:
    lines = [
        "# Phase 9 MyPrivateAgent Local Consumption Readiness",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Local Consumption State: `{report.local_consumption_state}`",
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
        f"| Local Provider URL | `{report.summary['local_provider_url']}` |",
        f"| Local Handoff Ready | `{report.summary['local_handoff_ready']}` |",
        f"| Runtime Promotion Ready | `{report.summary['runtime_promotion_ready']}` |",
        f"| API Key Mode | `{report.summary['api_key_mode']}` |",
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


def export_phase9_myprivateagent_local_consumption_readiness_report(
    output_dir: Path = Path("docs/integration/myprivateagent-local-consumption"),
    *,
    base_dir: Path = Path("."),
) -> Phase9LocalConsumptionReadinessReport:
    report = build_phase9_myprivateagent_local_consumption_readiness_report(
        base_dir=base_dir
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / READINESS_JSON_FILENAME
    markdown_path = output_dir / READINESS_MARKDOWN_FILENAME
    exported = Phase9LocalConsumptionReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        local_consumption_state=report.local_consumption_state,
        decision=report.decision,
        summary=report.summary,
        signals=report.signals,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase9_myprivateagent_local_consumption_readiness_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase9_myprivateagent_local_consumption_readiness_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _contract_signal(base_dir: Path) -> Phase9LocalConsumptionSignal:
    path = base_dir / PHASE9_CONTRACT_PATH
    if path.exists():
        return Phase9LocalConsumptionSignal(
            id="phase9_myprivateagent_local_consumption_contract",
            required=True,
            status="ready",
            summary="contract_present=true",
            recommended_action="no_action_required",
            evidence_path=str(PHASE9_CONTRACT_PATH),
        )
    return Phase9LocalConsumptionSignal(
        id="phase9_myprivateagent_local_consumption_contract",
        required=True,
        status="blocked",
        summary="contract_present=false",
        recommended_action="restore_phase9_myprivateagent_local_consumption_contract",
        evidence_path=str(PHASE9_CONTRACT_PATH),
    )


def _phase7_release_signal(base_dir: Path) -> Phase9LocalConsumptionSignal:
    payload = _read_json_if_present(base_dir / PHASE7_PROVIDER_RELEASE_READINESS_PATH)
    if payload is None:
        return Phase9LocalConsumptionSignal(
            id="phase7_provider_release_readiness",
            required=True,
            status="blocked",
            summary="artifact_present=false",
            recommended_action="regenerate_phase7_provider_release_readiness",
            evidence_path=str(PHASE7_PROVIDER_RELEASE_READINESS_PATH),
        )
    status = _normalize_status(payload.get("status"))
    summary = _dict_value(payload, "summary", {})
    return Phase9LocalConsumptionSignal(
        id="phase7_provider_release_readiness",
        required=True,
        status=status,
        summary=(
            f"artifact_present=true; status={status}; "
            f"release_state={payload.get('release_state', 'review')}; "
            f"local_handoff_ready={bool(_dict_value(summary, 'ready_for_local_provider_handoff', False))}; "
            f"runtime_promotion_ready={bool(_dict_value(summary, 'ready_for_runtime_default_promotion', False))}"
        ),
        recommended_action=(
            "no_action_required" if status == "ready" else "review_evidence_notes"
        ),
        evidence_path=str(PHASE7_PROVIDER_RELEASE_READINESS_PATH),
    )


def _phase8_live_url_signal(base_dir: Path) -> Phase9LocalConsumptionSignal:
    payload = _read_json_if_present(base_dir / PHASE8_LIVE_URL_VALIDATION_READINESS_PATH)
    if payload is None:
        return Phase9LocalConsumptionSignal(
            id="phase8_live_url_validation_readiness",
            required=True,
            status="blocked",
            summary="artifact_present=false",
            recommended_action="regenerate_phase8_live_url_validation_readiness",
            evidence_path=str(PHASE8_LIVE_URL_VALIDATION_READINESS_PATH),
        )
    status = _normalize_status(payload.get("status"))
    summary = _dict_value(payload, "summary", {})
    return Phase9LocalConsumptionSignal(
        id="phase8_live_url_validation_readiness",
        required=True,
        status=status,
        summary=(
            f"artifact_present=true; status={status}; "
            f"live_validation_state={payload.get('live_validation_state', 'review')}; "
            f"deployed_smoke_status={_dict_value(summary, 'deployed_smoke_status', 'review')}; "
            f"live_url_present={bool(_dict_value(summary, 'live_url_present', False))}"
        ),
        recommended_action=(
            "no_action_required" if status == "ready" else "review_evidence_notes"
        ),
        evidence_path=str(PHASE8_LIVE_URL_VALIDATION_READINESS_PATH),
    )


def _integration_probe_signal(base_dir: Path) -> Phase9LocalConsumptionSignal:
    payload = _read_json_if_present(base_dir / PROVIDER_INTEGRATION_PROBE_PATH)
    if payload is None:
        return Phase9LocalConsumptionSignal(
            id="provider_integration_probe",
            required=True,
            status="blocked",
            summary="artifact_present=false",
            recommended_action="regenerate_provider_integration_probe",
            evidence_path=str(PROVIDER_INTEGRATION_PROBE_PATH),
        )
    status = "ready" if bool(payload.get("bindable", False)) else "blocked"
    compatible = _compatible_control_planes(payload)
    return Phase9LocalConsumptionSignal(
        id="provider_integration_probe",
        required=True,
        status=status,
        summary=(
            f"artifact_present=true; bindable={bool(payload.get('bindable', False))}; "
            f"compatible_control_planes={compatible}"
        ),
        recommended_action=(
            "no_action_required" if status == "ready" else "review_evidence_notes"
        ),
        evidence_path=str(PROVIDER_INTEGRATION_PROBE_PATH),
    )


def _deployed_smoke_signal(base_dir: Path) -> Phase9LocalConsumptionSignal:
    payload = _read_json_if_present(base_dir / DEPLOYED_PROVIDER_SMOKE_PATH)
    if payload is None:
        return Phase9LocalConsumptionSignal(
            id="deployed_provider_smoke",
            required=False,
            status="review",
            summary="artifact_present=false",
            recommended_action="run_deployed_provider_smoke_after_deployment",
            evidence_path=str(DEPLOYED_PROVIDER_SMOKE_PATH),
        )
    status = _normalize_status(payload.get("status"))
    handoff = _dict_value(_dict_value(payload, "handoff", {}), "status", "unknown")
    return Phase9LocalConsumptionSignal(
        id="deployed_provider_smoke",
        required=False,
        status=status,
        summary=(
            f"artifact_present=true; status={status}; "
            f"base_url={payload.get('base_url', 'missing')}; handoff_status={handoff}"
        ),
        recommended_action=(
            "no_action_required" if status == "ready" else "review_evidence_notes"
        ),
        evidence_path=str(DEPLOYED_PROVIDER_SMOKE_PATH),
    )


def _source_binding_signal(base_dir: Path) -> Phase9LocalConsumptionSignal:
    payload = _read_json_if_present(base_dir / SOURCE_BINDING_SUMMARY_PATH)
    if payload is None:
        return Phase9LocalConsumptionSignal(
            id="source_binding_summary",
            required=False,
            status="review",
            summary="artifact_present=false",
            recommended_action="regenerate_provider_source_bindings",
            evidence_path=str(SOURCE_BINDING_SUMMARY_PATH),
        )
    status = _normalize_status(payload.get("status"))
    return Phase9LocalConsumptionSignal(
        id="source_binding_summary",
        required=False,
        status=status,
        summary=(
            f"artifact_present=true; status={status}; "
            f"bindable_sources={payload.get('bindable_source_count', 0)}/"
            f"{payload.get('total_source_count', 0)}"
        ),
        recommended_action=(
            "no_action_required" if status == "ready" else "review_evidence_notes"
        ),
        evidence_path=str(SOURCE_BINDING_SUMMARY_PATH),
    )


def _phase4_pack_signal(base_dir: Path) -> Phase9LocalConsumptionSignal:
    payload = _read_json_if_present(base_dir / PHASE4_EVIDENCE_PACK_READINESS_PATH)
    if payload is None:
        return Phase9LocalConsumptionSignal(
            id="phase4_evidence_pack_readiness",
            required=False,
            status="review",
            summary="artifact_present=false",
            recommended_action="regenerate_phase4_evidence_pack_readiness",
            evidence_path=str(PHASE4_EVIDENCE_PACK_READINESS_PATH),
        )
    status = _normalize_status(payload.get("status"))
    return Phase9LocalConsumptionSignal(
        id="phase4_evidence_pack_readiness",
        required=False,
        status=status,
        summary=(
            f"artifact_present=true; status={status}; "
            f"decision={payload.get('decision', 'keep_caller_ownership')}"
        ),
        recommended_action=(
            "no_action_required" if status == "ready" else "review_evidence_notes"
        ),
        evidence_path=str(PHASE4_EVIDENCE_PACK_READINESS_PATH),
    )


def _phase4_caller_smoke_signal(base_dir: Path) -> Phase9LocalConsumptionSignal:
    payload = _read_json_if_present(base_dir / PHASE4_CALLER_CONSUMPTION_SMOKE_PATH)
    if payload is None:
        return Phase9LocalConsumptionSignal(
            id="phase4_caller_consumption_smoke",
            required=False,
            status="review",
            summary="artifact_present=false",
            recommended_action="regenerate_phase4_caller_consumption_smoke",
            evidence_path=str(PHASE4_CALLER_CONSUMPTION_SMOKE_PATH),
        )
    status = _normalize_status(payload.get("status"))
    summary = _dict_value(payload, "summary", {})
    return Phase9LocalConsumptionSignal(
        id="phase4_caller_consumption_smoke",
        required=False,
        status=status,
        summary=(
            f"artifact_present=true; status={status}; "
            f"passed_checks={_dict_value(summary, 'passed', 0)}/"
            f"{_dict_value(summary, 'total', 0)}"
        ),
        recommended_action=(
            "no_action_required" if status == "ready" else "review_evidence_notes"
        ),
        evidence_path=str(PHASE4_CALLER_CONSUMPTION_SMOKE_PATH),
    )


def _local_provider_url(base_dir: Path) -> str:
    payload = _read_json_if_present(base_dir / DEPLOYED_PROVIDER_SMOKE_PATH)
    if isinstance(payload, dict):
        value = payload.get("base_url")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return LOCAL_PROVIDER_URL_DEFAULT


def _api_key_mode(base_dir: Path) -> str:
    payload = _read_json_if_present(base_dir / DEPLOYED_PROVIDER_SMOKE_PATH)
    if not isinstance(payload, dict):
        return "not_configured_local_dev"
    notes = payload.get("operation_notes", [])
    if isinstance(notes, list) and any(
        isinstance(note, str)
        and "no provider api credentials were supplied" in note.lower()
        for note in notes
    ):
        return "not_configured_local_dev"
    if isinstance(notes, list) and any(
        isinstance(note, str) and "credentials were supplied" in note.lower()
        for note in notes
    ):
        return "configured_protected_api"
    return "not_configured_local_dev"


def _compatible_control_planes(payload: dict[str, Any]) -> str:
    checks = payload.get("checks", [])
    if not isinstance(checks, list):
        return "unknown"
    for check in checks:
        if not isinstance(check, dict):
            continue
        if check.get("name") != "manifest_identity":
            continue
        details = _dict_value(check, "details", {})
        planes = _dict_value(details, "compatible_control_planes", [])
        if isinstance(planes, list):
            return ",".join(str(item) for item in planes)
    return "unknown"


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
