import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE12_LOCAL_RAG_INTEGRATION_HARDENING_PROFILE_ID = (
    "phase12-local-rag-integration-hardening-profile-v1"
)
PHASE10_READINESS_PATH = Path(
    "docs/integration/myprivateagent-local-consumer-verification/"
    "phase10-myprivateagent-local-consumer-readiness.json"
)
PHASE10_PROBE_PATH = Path(
    "docs/smoke/myprivateagent-local-consumer-verification/"
    "phase10-myprivateagent-local-consumer-probe.json"
)
PHASE11_PROFILE_PATH = Path(
    "docs/integration/myprivateagent-local-provider-integration/"
    "phase11-local-provider-integration-profile.json"
)
PROVIDER_CONTRACT_SMOKE_PATH = Path("docs/smoke/provider-contract/provider-contract-smoke.json")
PROVIDER_HANDOFF_BUNDLE_PATH = Path("docs/integration/provider-handoff/provider-handoff-bundle.json")
PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_PATH = Path(
    "docs/smoke/myprivateagent-local-provider-integration/"
    "phase11-source-binding-preview-smoke.json"
)
PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_PATH = Path(
    "docs/smoke/myprivateagent-local-provider-integration/"
    "phase11-rag-retrieve-consumption-smoke.json"
)
PROFILE_JSON_FILENAME = "phase12-local-rag-integration-hardening-profile.json"
PROFILE_MARKDOWN_FILENAME = "phase12-local-rag-integration-hardening-profile.md"
LOCAL_PROVIDER_URL_DEFAULT = "http://127.0.0.1:8020"


@dataclass(frozen=True)
class Phase12LocalRagIntegrationSignal:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase12LocalRagIntegrationHardeningProfileReport:
    id: str
    generated_at: str
    status: str
    hardening_state: str
    decision: str
    summary: dict[str, Any]
    signals: list[Phase12LocalRagIntegrationSignal]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase12_local_rag_integration_hardening_profile_report(
    *,
    base_dir: Path = Path("."),
) -> Phase12LocalRagIntegrationHardeningProfileReport:
    signals = [
        _phase10_readiness_signal(base_dir),
        _phase10_probe_signal(base_dir),
        _phase11_local_provider_integration_profile_signal(base_dir),
        _provider_contract_smoke_signal(base_dir),
        _provider_handoff_bundle_signal(base_dir),
        _phase11_source_binding_preview_smoke_signal(base_dir),
        _phase11_rag_retrieve_consumption_smoke_signal(base_dir),
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
    local_provider_url = _dict_value(phase10_summary, "local_provider_url", LOCAL_PROVIDER_URL_DEFAULT)
    api_key_mode = _dict_value(phase10_summary, "api_key_mode", "not_configured_local_dev")

    if required_blocked:
        status = "blocked"
        hardening_state = "hardening_blocked"
        decision = "resolve_phase12_hardening_blockers"
    elif required_review:
        status = "review"
        hardening_state = "ready_for_local_rag_hardening_review"
        decision = "run_phase12_local_rag_integration_hardening_smoke"
    else:
        status = "ready"
        hardening_state = "ready_for_local_rag_hardening"
        decision = "confirm_phase12_local_rag_hardening_readiness"

    return Phase12LocalRagIntegrationHardeningProfileReport(
        id=PHASE12_LOCAL_RAG_INTEGRATION_HARDENING_PROFILE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        hardening_state=hardening_state,
        decision=decision,
        summary={
            "total_signals": len(signals),
            "required_signals": sum(1 for signal in signals if signal.required),
            "ready_signals": sum(1 for signal in signals if signal.status == "ready"),
            "review_signals": sum(1 for signal in signals if signal.status == "review"),
            "blocked_signals": sum(1 for signal in signals if signal.status == "blocked"),
            "local_provider_url": local_provider_url,
            "api_key_mode": api_key_mode,
            "source_binding_preview_required": True,
            "rag_retrieve_consumption_required": True,
            "open_gate_ids": open_gate_ids,
        },
        signals=signals,
        notes=[
            "Phase 12 hardening report is read-only and intended for local MyPrivateAgent consumption review.",
            "It does not switch runtime defaults or mutate source bindings.",
        ],
    )


def phase12_local_rag_integration_hardening_profile_report_to_dict(
    report: Phase12LocalRagIntegrationHardeningProfileReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase12_local_rag_integration_hardening_profile_markdown(
    report: Phase12LocalRagIntegrationHardeningProfileReport,
) -> str:
    lines = [
        "# Phase 12 Local RAG Integration Hardening Profile",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Hardening State: `{report.hardening_state}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in report.summary.items():
        rendered = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
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


def export_phase12_local_rag_integration_hardening_profile_report(
    output_dir: Path = Path(
        "docs/integration/myprivateagent-local-rag-integration-hardening"
    ),
    *,
    base_dir: Path = Path("."),
) -> Phase12LocalRagIntegrationHardeningProfileReport:
    report = build_phase12_local_rag_integration_hardening_profile_report(
        base_dir=base_dir
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PROFILE_JSON_FILENAME
    markdown_path = output_dir / PROFILE_MARKDOWN_FILENAME
    exported = Phase12LocalRagIntegrationHardeningProfileReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        hardening_state=report.hardening_state,
        decision=report.decision,
        summary=report.summary,
        signals=report.signals,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase12_local_rag_integration_hardening_profile_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase12_local_rag_integration_hardening_profile_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _phase10_readiness_signal(base_dir: Path) -> Phase12LocalRagIntegrationSignal:
    payload = _read_json_if_present(base_dir / PHASE10_READINESS_PATH)
    if payload is None:
        return _missing_signal(
            id="phase10_local_consumer_readiness",
            path=PHASE10_READINESS_PATH,
            action="regenerate_phase10_myprivateagent_local_consumer_readiness",
        )
    status = _normalize_status(payload.get("status"))
    summary = _dict_value(payload, "summary", {})
    return Phase12LocalRagIntegrationSignal(
        id="phase10_local_consumer_readiness",
        required=True,
        status=status,
        summary=(
            f"status={status}; local_consumer_state="
            f"{payload.get('local_consumer_state', 'review')}; "
            f"api_key_mode={_dict_value(summary, 'api_key_mode', 'not_configured_local_dev')}"
        ),
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(PHASE10_READINESS_PATH),
    )


def _phase10_probe_signal(base_dir: Path) -> Phase12LocalRagIntegrationSignal:
    payload = _read_json_if_present(base_dir / PHASE10_PROBE_PATH)
    if payload is None:
        return _missing_signal(
            id="phase10_local_consumer_probe",
            path=PHASE10_PROBE_PATH,
            action="regenerate_phase10_myprivateagent_local_consumer_probe",
        )
    status = _normalize_status(payload.get("status"))
    summary = payload.get("summary", {})
    passed_checks = _dict_value(summary, "passed_checks", 0)
    total_checks = _dict_value(summary, "total_checks", 0)
    return Phase12LocalRagIntegrationSignal(
        id="phase10_local_consumer_probe",
        required=True,
        status=status,
        summary=(
            f"status={status}; passed_checks={passed_checks}/{total_checks}"
        ),
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(PHASE10_PROBE_PATH),
    )


def _phase11_local_provider_integration_profile_signal(
    base_dir: Path,
) -> Phase12LocalRagIntegrationSignal:
    payload = _read_json_if_present(base_dir / PHASE11_PROFILE_PATH)
    if payload is None:
        return _missing_signal(
            id="phase11_local_provider_integration_profile",
            path=PHASE11_PROFILE_PATH,
            action="regenerate_phase11_local_provider_integration_profile",
        )
    status = _normalize_status(payload.get("status"))
    return Phase12LocalRagIntegrationSignal(
        id="phase11_local_provider_integration_profile",
        required=True,
        status=status,
        summary=f"status={status}; id={payload.get('id', 'unknown')}",
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(PHASE11_PROFILE_PATH),
    )


def _provider_contract_smoke_signal(
    base_dir: Path,
) -> Phase12LocalRagIntegrationSignal:
    payload = _read_json_if_present(base_dir / PROVIDER_CONTRACT_SMOKE_PATH)
    if payload is None:
        return _missing_signal(
            id="provider_contract_smoke",
            path=PROVIDER_CONTRACT_SMOKE_PATH,
            action="regenerate_provider_contract_smoke",
        )
    passed = bool(payload.get("passed"))
    summary = payload.get("summary", {})
    return Phase12LocalRagIntegrationSignal(
        id="provider_contract_smoke",
        required=True,
        status="ready" if passed else "blocked",
        summary=f"passed={passed}; checks={summary.get('passed', 0)}/{summary.get('total', 0)}",
        recommended_action="no_action_required" if passed else "regenerate_provider_contract_smoke",
        evidence_path=str(PROVIDER_CONTRACT_SMOKE_PATH),
    )


def _provider_handoff_bundle_signal(
    base_dir: Path,
) -> Phase12LocalRagIntegrationSignal:
    payload = _read_json_if_present(base_dir / PROVIDER_HANDOFF_BUNDLE_PATH)
    if payload is None:
        return _missing_signal(
            id="provider_handoff_bundle",
            path=PROVIDER_HANDOFF_BUNDLE_PATH,
            action="regenerate_provider_handoff_bundle",
        )
    status = _normalize_status(payload.get("status"))
    return Phase12LocalRagIntegrationSignal(
        id="provider_handoff_bundle",
        required=True,
        status=status,
        summary=f"status={status}; evidence_artifacts={payload.get('evidence_artifacts', 0)}",
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(PROVIDER_HANDOFF_BUNDLE_PATH),
    )


def _phase11_source_binding_preview_smoke_signal(
    base_dir: Path,
) -> Phase12LocalRagIntegrationSignal:
    payload = _read_json_if_present(base_dir / PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_PATH)
    if payload is None:
        return _missing_signal(
            id="phase11_source_binding_preview_smoke",
            path=PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_PATH,
            action="regenerate_phase11_source_binding_preview_smoke",
        )
    status = _normalize_status(payload.get("status"))
    summary = payload.get("summary", {})
    return Phase12LocalRagIntegrationSignal(
        id="phase11_source_binding_preview_smoke",
        required=True,
        status=status,
        summary=f"status={status}; passed_checks={summary.get('passed_checks', 0)}/{summary.get('total_checks', 0)}",
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_PATH),
    )


def _phase11_rag_retrieve_consumption_smoke_signal(
    base_dir: Path,
) -> Phase12LocalRagIntegrationSignal:
    payload = _read_json_if_present(base_dir / PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_PATH)
    if payload is None:
        return _missing_signal(
            id="phase11_rag_retrieve_consumption_smoke",
            path=PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_PATH,
            action="regenerate_phase11_rag_retrieve_consumption_smoke",
        )
    status = _normalize_status(payload.get("status"))
    summary = payload.get("summary", {})
    return Phase12LocalRagIntegrationSignal(
        id="phase11_rag_retrieve_consumption_smoke",
        required=True,
        status=status,
        summary=f"status={status}; passed_checks={summary.get('passed_checks', 0)}/{summary.get('total_checks', 0)}",
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_PATH),
    )


def _missing_signal(
    *,
    id: str,
    path: Path,
    action: str,
) -> Phase12LocalRagIntegrationSignal:
    return Phase12LocalRagIntegrationSignal(
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
