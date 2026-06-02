import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE11_LOCAL_PROVIDER_INTEGRATION_PROFILE_ID = (
    "phase11-local-provider-integration-profile-v1"
)
PHASE10_READINESS_PATH = Path(
    "docs/integration/myprivateagent-local-consumer-verification/"
    "phase10-myprivateagent-local-consumer-readiness.json"
)
PHASE10_PROBE_PATH = Path(
    "docs/smoke/myprivateagent-local-consumer-verification/"
    "phase10-myprivateagent-local-consumer-probe.json"
)
PROVIDER_INTEGRATION_PROBE_PATH = Path(
    "docs/integration/provider-binding/provider-integration-probe.json"
)
PROVIDER_HANDOFF_BUNDLE_PATH = Path(
    "docs/integration/provider-handoff/provider-handoff-bundle.json"
)
PROFILE_JSON_FILENAME = "phase11-local-provider-integration-profile.json"
PROFILE_MARKDOWN_FILENAME = "phase11-local-provider-integration-profile.md"
LOCAL_PROVIDER_URL_DEFAULT = "http://127.0.0.1:8020"


@dataclass(frozen=True)
class Phase11LocalIntegrationSignal:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase11LocalProviderIntegrationProfileReport:
    id: str
    generated_at: str
    status: str
    integration_state: str
    decision: str
    summary: dict[str, Any]
    signals: list[Phase11LocalIntegrationSignal]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase11_local_provider_integration_profile_report(
    *,
    base_dir: Path = Path("."),
) -> Phase11LocalProviderIntegrationProfileReport:
    signals = [
        _phase10_readiness_signal(base_dir),
        _phase10_probe_signal(base_dir),
        _integration_probe_signal(base_dir),
        _handoff_bundle_signal(base_dir),
    ]
    required_blocked = any(
        signal.required and signal.status == "blocked" for signal in signals
    )
    required_review = any(
        signal.required and signal.status == "review" for signal in signals
    )
    phase10_payload = _read_json_if_present(base_dir / PHASE10_READINESS_PATH)
    phase10_summary = _dict_value(phase10_payload, "summary", {})
    open_gate_ids = [signal.id for signal in signals if signal.status in {"review", "blocked"}]

    if required_blocked:
        status = "blocked"
        integration_state = "blocked"
        decision = "resolve_local_integration_blockers"
    elif required_review:
        status = "review"
        integration_state = "ready_for_local_provider_integration_review"
        decision = "run_phase11_local_integration_smokes"
    else:
        status = "ready"
        integration_state = "ready_for_local_provider_integration"
        decision = "confirm_local_provider_integration_profile"

    return Phase11LocalProviderIntegrationProfileReport(
        id=PHASE11_LOCAL_PROVIDER_INTEGRATION_PROFILE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        integration_state=integration_state,
        decision=decision,
        summary={
            "total_signals": len(signals),
            "required_signals": sum(1 for signal in signals if signal.required),
            "ready_signals": sum(1 for signal in signals if signal.status == "ready"),
            "review_signals": sum(1 for signal in signals if signal.status == "review"),
            "blocked_signals": sum(1 for signal in signals if signal.status == "blocked"),
            "local_provider_url": _dict_value(
                phase10_summary, "local_provider_url", LOCAL_PROVIDER_URL_DEFAULT
            ),
            "api_key_mode": _dict_value(
                phase10_summary, "api_key_mode", "not_configured_local_dev"
            ),
            "runtime_promotion_status": _dict_value(
                phase10_summary, "runtime_promotion_status", "keep_runtime_defaults"
            ),
            "source_binding_policy_owner": _dict_value(
                phase10_summary, "source_binding_policy_owner", "caller"
            ),
            "open_gate_ids": open_gate_ids,
        },
        signals=signals,
        notes=[
            "Phase 11 profile is read-only local integration evidence for MyPrivateAgent-style consumption.",
            "It does not mutate source bindings, switch runtime defaults, or enable GraphRAG execution.",
        ],
    )


def phase11_local_provider_integration_profile_report_to_dict(
    report: Phase11LocalProviderIntegrationProfileReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase11_local_provider_integration_profile_markdown(
    report: Phase11LocalProviderIntegrationProfileReport,
) -> str:
    lines = [
        "# Phase 11 Local Provider Integration Profile",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Integration State: `{report.integration_state}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in report.summary.items():
        rendered = json.dumps(value, ensure_ascii=False) if isinstance(value, list) else value
        lines.append(f"| {key} | `{rendered}` |")
    lines.extend(
        [
            "",
            "## Signals",
            "",
            "| Signal | Required | Status | Summary | Recommended Action |",
            "|---|---|---|---|---|",
        ]
    )
    for signal in report.signals:
        lines.append(
            f"| `{signal.id}` | `{signal.required}` | `{signal.status}` | "
            f"{signal.summary} | `{signal.recommended_action}` |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase11_local_provider_integration_profile_report(
    output_dir: Path = Path("docs/integration/myprivateagent-local-provider-integration"),
    *,
    base_dir: Path = Path("."),
) -> Phase11LocalProviderIntegrationProfileReport:
    report = build_phase11_local_provider_integration_profile_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PROFILE_JSON_FILENAME
    markdown_path = output_dir / PROFILE_MARKDOWN_FILENAME
    exported = Phase11LocalProviderIntegrationProfileReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        integration_state=report.integration_state,
        decision=report.decision,
        summary=report.summary,
        signals=report.signals,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase11_local_provider_integration_profile_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase11_local_provider_integration_profile_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _phase10_readiness_signal(base_dir: Path) -> Phase11LocalIntegrationSignal:
    payload = _read_json_if_present(base_dir / PHASE10_READINESS_PATH)
    if payload is None:
        return _missing_signal(
            id="phase10_local_consumer_readiness",
            path=PHASE10_READINESS_PATH,
            action="regenerate_phase10_local_consumer_readiness",
        )
    status = _normalize_status(payload.get("status"))
    return Phase11LocalIntegrationSignal(
        id="phase10_local_consumer_readiness",
        required=True,
        status=status,
        summary=(
            f"status={status}; local_consumer_state="
            f"{payload.get('local_consumer_state', 'review')}"
        ),
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(PHASE10_READINESS_PATH),
    )


def _phase10_probe_signal(base_dir: Path) -> Phase11LocalIntegrationSignal:
    payload = _read_json_if_present(base_dir / PHASE10_PROBE_PATH)
    if payload is None:
        return _missing_signal(
            id="phase10_local_consumer_probe",
            path=PHASE10_PROBE_PATH,
            action="regenerate_phase10_local_consumer_probe",
        )
    status = _normalize_status(payload.get("status"))
    summary = _dict_value(payload, "summary", {})
    return Phase11LocalIntegrationSignal(
        id="phase10_local_consumer_probe",
        required=True,
        status=status,
        summary=(
            f"status={status}; passed_checks={_dict_value(summary, 'passed_checks', 0)}/"
            f"{_dict_value(summary, 'total_checks', 0)}"
        ),
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(PHASE10_PROBE_PATH),
    )


def _integration_probe_signal(base_dir: Path) -> Phase11LocalIntegrationSignal:
    payload = _read_json_if_present(base_dir / PROVIDER_INTEGRATION_PROBE_PATH)
    if payload is None:
        return _missing_signal(
            id="provider_integration_probe",
            path=PROVIDER_INTEGRATION_PROBE_PATH,
            action="regenerate_provider_integration_probe",
        )
    bindable = bool(payload.get("bindable", False))
    status = "ready" if bindable else "blocked"
    return Phase11LocalIntegrationSignal(
        id="provider_integration_probe",
        required=True,
        status=status,
        summary=f"bindable={bindable}",
        recommended_action="no_action_required" if bindable else "review_evidence_notes",
        evidence_path=str(PROVIDER_INTEGRATION_PROBE_PATH),
    )


def _handoff_bundle_signal(base_dir: Path) -> Phase11LocalIntegrationSignal:
    payload = _read_json_if_present(base_dir / PROVIDER_HANDOFF_BUNDLE_PATH)
    if payload is None:
        return _missing_signal(
            id="provider_handoff_bundle",
            path=PROVIDER_HANDOFF_BUNDLE_PATH,
            action="regenerate_provider_handoff_bundle",
        )
    status = _normalize_status(payload.get("status"))
    return Phase11LocalIntegrationSignal(
        id="provider_handoff_bundle",
        required=True,
        status=status,
        summary=f"status={status}",
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(PROVIDER_HANDOFF_BUNDLE_PATH),
    )


def _missing_signal(
    *,
    id: str,
    path: Path,
    action: str,
) -> Phase11LocalIntegrationSignal:
    return Phase11LocalIntegrationSignal(
        id=id,
        required=True,
        status="blocked",
        summary="artifact_present=false",
        recommended_action=action,
        evidence_path=str(path),
    )


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
