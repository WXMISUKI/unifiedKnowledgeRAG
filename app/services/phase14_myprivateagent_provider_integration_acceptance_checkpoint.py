import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from app.services.myprivateagent_access_gate import build_myprivateagent_access_gate


PHASE14_MYPRIVATEAGENT_PROVIDER_INTEGRATION_ACCEPTANCE_CHECKPOINT_ID = (
    "phase14-myprivateagent-provider-integration-acceptance-checkpoint-v1"
)
OUTPUT_JSON_FILENAME = "phase14-myprivateagent-provider-integration-acceptance-checkpoint.json"
OUTPUT_MARKDOWN_FILENAME = "phase14-myprivateagent-provider-integration-acceptance-checkpoint.md"
LOCAL_PROVIDER_URL_DEFAULT = "http://127.0.0.1:8020"


@dataclass(frozen=True)
class AcceptanceSignalSpec:
    id: str
    path: Path
    required: bool = True
    summary_builder: Callable[[dict[str, Any] | None], str] | None = None
    missing_action: str = "review_evidence_notes"


@dataclass(frozen=True)
class AcceptanceSignal:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase14MyPrivateAgentProviderIntegrationAcceptanceCheckpointReport:
    id: str
    generated_at: str
    status: str
    acceptance_state: str
    decision: str
    summary: dict[str, Any]
    signals: list[AcceptanceSignal]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


PHASE10_READINESS_PATH = Path(
    "docs/integration/myprivateagent-local-consumer-verification/"
    "phase10-myprivateagent-local-consumer-readiness.json"
)
PROVIDER_CONTRACT_SMOKE_PATH = Path("docs/smoke/provider-contract/provider-contract-smoke.json")
PHASE10_PROBE_PATH = Path(
    "docs/smoke/myprivateagent-local-consumer-verification/"
    "phase10-myprivateagent-local-consumer-probe.json"
)
PHASE11_PROFILE_PATH = Path(
    "docs/integration/myprivateagent-local-provider-integration/"
    "phase11-local-provider-integration-profile.json"
)
PHASE11_PROVIDER_DISCOVERY_SMOKE_PATH = Path(
    "docs/smoke/myprivateagent-local-provider-integration/"
    "phase11-provider-discovery-smoke.json"
)
PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_PATH = Path(
    "docs/smoke/myprivateagent-local-provider-integration/"
    "phase11-rag-retrieve-consumption-smoke.json"
)
PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_PATH = Path(
    "docs/smoke/myprivateagent-local-provider-integration/"
    "phase11-source-binding-preview-smoke.json"
)
PHASE13_ROADMAP_CHECKPOINT_PATH = Path(
    "docs/operations/provider-roadmap-decision-checkpoint/"
    "phase13-provider-roadmap-decision-checkpoint.json"
)
PROVIDER_HANDOFF_BUNDLE_PATH = Path(
    "docs/integration/provider-handoff/provider-handoff-bundle.json"
)
PROVIDER_HANDOFF_REFRESH_PATH = Path(
    "docs/integration/provider-handoff-refresh/provider-handoff-refresh.json"
)


SIGNAL_SPECS: list[AcceptanceSignalSpec] = [
    AcceptanceSignalSpec(
        id="provider_contract_smoke",
        path=PROVIDER_CONTRACT_SMOKE_PATH,
        summary_builder=lambda payload: _provider_contract_smoke_summary(payload),
        missing_action="regenerate_provider_contract_smoke",
    ),
    AcceptanceSignalSpec(
        id="phase10_myprivateagent_local_consumer_readiness",
        path=PHASE10_READINESS_PATH,
        required=False,
        summary_builder=lambda payload: _phase10_readiness_summary(payload),
        missing_action="regenerate_phase10_myprivateagent_local_consumer_readiness",
    ),
    AcceptanceSignalSpec(
        id="phase10_myprivateagent_local_consumer_probe",
        path=PHASE10_PROBE_PATH,
        summary_builder=lambda payload: _phase10_probe_summary(payload),
        missing_action="regenerate_phase10_myprivateagent_local_consumer_probe",
    ),
    AcceptanceSignalSpec(
        id="phase11_local_provider_integration_profile",
        path=PHASE11_PROFILE_PATH,
        required=False,
        summary_builder=lambda payload: _phase11_profile_summary(payload),
        missing_action="regenerate_phase11_local_provider_integration_profile",
    ),
    AcceptanceSignalSpec(
        id="phase11_provider_discovery_smoke",
        path=PHASE11_PROVIDER_DISCOVERY_SMOKE_PATH,
        summary_builder=lambda payload: _phase11_smoke_summary(
            payload, "provider_discovery_state"
        ),
        missing_action="regenerate_phase11_provider_discovery_smoke",
    ),
    AcceptanceSignalSpec(
        id="phase11_rag_retrieve_consumption_smoke",
        path=PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_PATH,
        summary_builder=lambda payload: _phase11_smoke_summary(
            payload, "rag_retrieve_state"
        ),
        missing_action="regenerate_phase11_rag_retrieve_consumption_smoke",
    ),
    AcceptanceSignalSpec(
        id="phase11_source_binding_preview_smoke",
        path=PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_PATH,
        summary_builder=lambda payload: _phase11_smoke_summary(
            payload, "source_binding_preview_state"
        ),
        missing_action="regenerate_phase11_source_binding_preview_smoke",
    ),
    AcceptanceSignalSpec(
        id="phase13_provider_roadmap_decision_checkpoint",
        path=PHASE13_ROADMAP_CHECKPOINT_PATH,
        required=False,
        summary_builder=lambda payload: _phase13_summary(payload),
        missing_action="regenerate_phase13_provider_roadmap_decision_checkpoint",
    ),
    AcceptanceSignalSpec(
        id="provider_handoff_bundle",
        path=PROVIDER_HANDOFF_BUNDLE_PATH,
        required=False,
        summary_builder=lambda payload: _handoff_bundle_summary(payload),
        missing_action="regenerate_provider_handoff_bundle",
    ),
    AcceptanceSignalSpec(
        id="provider_handoff_refresh",
        path=PROVIDER_HANDOFF_REFRESH_PATH,
        required=False,
        summary_builder=lambda payload: _handoff_refresh_summary(payload),
        missing_action="regenerate_provider_handoff_refresh",
    ),
]


def build_phase14_myprivateagent_provider_integration_acceptance_checkpoint_report(
    *,
    base_dir: Path = Path("."),
) -> Phase14MyPrivateAgentProviderIntegrationAcceptanceCheckpointReport:
    signals = [_build_signal(spec, base_dir=base_dir) for spec in SIGNAL_SPECS]
    signal_map = {signal.id: signal for signal in signals}

    phase10_status = _aggregate_status(
        [
            signal_map["phase10_myprivateagent_local_consumer_readiness"].status,
            signal_map["phase10_myprivateagent_local_consumer_probe"].status,
        ]
    )
    phase11_status = _aggregate_status(
        [
            signal_map["phase11_local_provider_integration_profile"].status,
            signal_map["phase11_provider_discovery_smoke"].status,
            signal_map["phase11_rag_retrieve_consumption_smoke"].status,
            signal_map["phase11_source_binding_preview_smoke"].status,
        ]
    )
    phase13_status = signal_map["phase13_provider_roadmap_decision_checkpoint"].status
    handoff_status = _aggregate_status(
        [
            signal_map["provider_handoff_bundle"].status,
            signal_map["provider_handoff_refresh"].status,
        ]
    )

    any_missing_required = any(
        signal.required and signal.status == "blocked" and signal.summary == "status=missing"
        for signal in signals
    )
    any_blocked_required = any(signal.required and signal.status == "blocked" for signal in signals)
    any_review_required = any(signal.required and signal.status == "review" for signal in signals)

    if any_missing_required or any_blocked_required:
        status = "blocked"
        acceptance_state = "blocked_for_myprivateagent_repo_side_trial"
        decision = "resolve_provider_contract_or_environment_blockers"
    elif any_review_required:
        status = "review"
        acceptance_state = "review_for_myprivateagent_repo_side_trial"
        decision = "refresh_provider_integration_evidence"
    else:
        status = "ready"
        acceptance_state = "ready_for_myprivateagent_repo_side_trial"
        decision = "approve_myprivateagent_repo_side_trial"

    blocker_category = _blocker_category(signals=signals)
    access_gate = build_myprivateagent_access_gate(
        [{"id": signal.id, "status": signal.status} for signal in signals]
    )
    ready_signal_ids = [signal.id for signal in signals if signal.status == "ready"]
    review_signal_ids = [signal.id for signal in signals if signal.status == "review"]
    blocked_signal_ids = [signal.id for signal in signals if signal.status == "blocked"]
    open_gate_ids = [signal.id for signal in signals if signal.status in {"review", "blocked"}]

    return Phase14MyPrivateAgentProviderIntegrationAcceptanceCheckpointReport(
        id=PHASE14_MYPRIVATEAGENT_PROVIDER_INTEGRATION_ACCEPTANCE_CHECKPOINT_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        acceptance_state=acceptance_state,
        decision=decision,
        summary={
            "roadmap_focus": "myprivateagent_repo_side_trial",
            "trial_readiness": acceptance_state,
            "blocker_category": blocker_category,
            "access_gate_status": access_gate.status,
            "primitive_signal_ids": access_gate.primitive_ids,
            "ready_primitive_signal_ids": access_gate.ready_primitive_ids,
            "review_primitive_signal_ids": access_gate.review_primitive_ids,
            "blocked_primitive_signal_ids": access_gate.blocked_primitive_ids,
            "missing_primitive_signal_ids": access_gate.missing_primitive_ids,
            "open_review_context_signal_ids": access_gate.review_context_open_ids,
            "phase10_status": phase10_status,
            "phase11_status": phase11_status,
            "phase13_status": phase13_status,
            "handoff_status": handoff_status,
            "total_signals": len(signals),
            "required_signals": len([signal for signal in signals if signal.required]),
            "ready_signals": len(ready_signal_ids),
            "review_signals": len(review_signal_ids),
            "blocked_signals": len(blocked_signal_ids),
            "ready_signal_ids": ready_signal_ids,
            "review_signal_ids": review_signal_ids,
            "blocked_signal_ids": blocked_signal_ids,
            "open_gate_ids": open_gate_ids,
            "local_provider_url": LOCAL_PROVIDER_URL_DEFAULT,
            "source_binding_policy_owner": "caller",
            "runtime_promotion_status": "keep_runtime_defaults",
        },
        signals=signals,
        notes=[
            "This checkpoint is local, read-only evidence for a MyPrivateAgent repo-side trial decision.",
            "It keeps runtime defaults unchanged and does not create source-to-agent binding or control-plane ownership.",
            "The verdict is conservative and separates provider evidence gaps from external environment blockers.",
        ],
    )


def phase14_myprivateagent_provider_integration_acceptance_checkpoint_report_to_dict(
    report: Phase14MyPrivateAgentProviderIntegrationAcceptanceCheckpointReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase14_myprivateagent_provider_integration_acceptance_checkpoint_markdown(
    report: Phase14MyPrivateAgentProviderIntegrationAcceptanceCheckpointReport,
) -> str:
    lines = [
        "# Phase 14 MyPrivateAgent Provider Integration Acceptance Checkpoint",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Acceptance State: `{report.acceptance_state}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in report.summary.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")
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
            "| "
            f"`{signal.id}` | `{signal.required}` | `{signal.status}` | "
            f"{signal.summary} | `{signal.recommended_action}` |"
        )
    if report.notes:
        lines.extend(["", "## Notes", ""])
        for note in report.notes:
            lines.append(f"- {note}")
    return "\n".join(lines).rstrip() + "\n"


def export_phase14_myprivateagent_provider_integration_acceptance_checkpoint_report(
    *,
    output_dir: Path = Path("docs/integration/myprivateagent-provider-integration-acceptance"),
    base_dir: Path = Path("."),
) -> Phase14MyPrivateAgentProviderIntegrationAcceptanceCheckpointReport:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_phase14_myprivateagent_provider_integration_acceptance_checkpoint_report(
        base_dir=base_dir
    )
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = Phase14MyPrivateAgentProviderIntegrationAcceptanceCheckpointReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        acceptance_state=report.acceptance_state,
        decision=report.decision,
        summary=report.summary,
        signals=report.signals,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase14_myprivateagent_provider_integration_acceptance_checkpoint_report_to_dict(
                exported
            ),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase14_myprivateagent_provider_integration_acceptance_checkpoint_markdown(
            exported
        ),
        encoding="utf-8",
    )
    return exported


def _build_signal(
    spec: AcceptanceSignalSpec,
    *,
    base_dir: Path,
) -> AcceptanceSignal:
    payload = _read_json_if_present(base_dir / spec.path)
    if payload is None:
        return AcceptanceSignal(
            id=spec.id,
            required=spec.required,
            status="blocked",
            summary="status=missing",
            recommended_action=spec.missing_action,
            evidence_path=str(spec.path),
        )

    status = _access_focused_status_for_signal(spec.id, payload)
    summary_builder = spec.summary_builder or (lambda current: f"status={status}")
    summary = summary_builder(payload)
    return AcceptanceSignal(
        id=spec.id,
        required=spec.required,
        status=status,
        summary=summary,
        recommended_action=_recommended_action_for_status(status, spec.missing_action),
        evidence_path=str(spec.path),
    )


def _phase10_readiness_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    summary = _summary_dict(payload)
    return (
        f"status={_normalize_status(payload.get('status'))}; "
        f"local_consumer_state={payload.get('local_consumer_state', 'review')}; "
        f"runtime_promotion_status={_dict_value(summary, 'runtime_promotion_status', 'keep_runtime_defaults')}; "
        f"source_binding_policy_owner={_dict_value(summary, 'source_binding_policy_owner', 'caller')}"
    )


def _provider_contract_smoke_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    summary = _summary_dict(payload)
    return (
        f"status={_access_focused_status_for_signal('provider_contract_smoke', payload)}; "
        f"passed={payload.get('passed', 'unknown')}; "
        f"total_checks={_dict_value(summary, 'total_checks', 'unknown')}; "
        f"failed_checks={_dict_value(summary, 'failed_checks', 'unknown')}"
    )


def _phase10_probe_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    summary = _summary_dict(payload)
    total_checks = _int_value(_dict_value(summary, "total_checks", 0), fallback=0)
    passed_checks = _int_value(_dict_value(summary, "passed_checks", 0), fallback=0)
    return (
        f"status={_normalize_status(payload.get('status'))}; "
        f"passed_checks={passed_checks}/{total_checks}; "
        f"decision={payload.get('decision', 'continue_local_consumer_probe')}"
    )


def _phase11_profile_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    summary = _summary_dict(payload)
    return (
        f"status={_normalize_status(payload.get('status'))}; "
        f"integration_state={payload.get('integration_state', 'review')}; "
        f"local_provider_url={_dict_value(summary, 'local_provider_url', LOCAL_PROVIDER_URL_DEFAULT)}; "
        f"api_key_mode={_dict_value(summary, 'api_key_mode', 'not_configured_local_dev')}"
    )


def _phase11_smoke_summary(payload: dict[str, Any] | None, state_key: str) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    summary = _summary_dict(payload)
    passed_checks = _int_value(_dict_value(summary, "passed_checks", 0), fallback=0)
    total_checks = _int_value(_dict_value(summary, "total_checks", 0), fallback=0)
    state_value = _dict_value(summary, state_key, payload.get("status", "review"))
    return (
        f"status={_normalize_status(payload.get('status'))}; "
        f"{state_key}={state_value}; "
        f"passed_checks={passed_checks}/{total_checks}"
    )


def _phase13_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    summary = _summary_dict(payload)
    return (
        f"status={_normalize_status(payload.get('status'))}; "
        f"checkpoint_state={payload.get('checkpoint_state', 'review')}; "
        f"decision={payload.get('decision', 'review_evidence_notes')}; "
        f"roadmap_focus={_dict_value(summary, 'roadmap_focus', 'resume_provider_integration_hardening')}; "
        f"candidate_backend_posture={_dict_value(summary, 'candidate_backend_posture', 'pause_pgvector_until_live_probe_executed')}; "
        f"phase12d_status={_dict_value(summary, 'phase12d_status', 'missing')}; "
        f"phase12f_status={_dict_value(summary, 'phase12f_status', 'missing')}"
    )


def _handoff_bundle_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    evidence_artifacts = payload.get("evidence_artifacts", [])
    access_focused_visibility = _access_focused_visibility_payload(payload)
    access_focused_status = (
        _normalize_status(access_focused_visibility.get("status", "review"))
        if isinstance(access_focused_visibility, dict)
        else _normalize_status(payload.get("status"))
    )
    return (
        f"status={access_focused_status}; "
        f"overall_status={_normalize_status(payload.get('status'))}; "
        f"access_focused_status={access_focused_status}; "
        f"decision={payload.get('decision', 'review_evidence_notes')}; "
        f"evidence_artifacts={len(evidence_artifacts) if isinstance(evidence_artifacts, list) else 0}"
    )


def _handoff_refresh_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    steps = payload.get("steps", [])
    access_focused_visibility = _access_focused_visibility_payload(payload)
    access_focused_status = (
        _normalize_status(access_focused_visibility.get("status", "review"))
        if isinstance(access_focused_visibility, dict)
        else _normalize_status(payload.get("status"))
    )
    return (
        f"status={access_focused_status}; "
        f"overall_status={_normalize_status(payload.get('status'))}; "
        f"access_focused_status={access_focused_status}; "
        f"decision={payload.get('decision', 'review_evidence_notes')}; "
        f"steps={len(steps) if isinstance(steps, list) else 0}"
    )


def _blocker_category(*, signals: list[AcceptanceSignal]) -> str:
    access_gate = build_myprivateagent_access_gate(
        [{"id": signal.id, "status": signal.status} for signal in signals]
    )
    if access_gate.status != "ready":
        return "provider_contract_evidence"
    return "none"


def _aggregate_status(statuses: list[str]) -> str:
    if any(status == "blocked" for status in statuses):
        return "blocked"
    if any(status == "review" for status in statuses):
        return "review"
    return "ready"


def _recommended_action_for_status(status: str, missing_action: str) -> str:
    if status == "ready":
        return "no_action_required"
    if status == "blocked":
        return missing_action
    return "review_evidence_notes"


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_status(value: Any) -> str:
    if value in {"ready", "review", "blocked"}:
        return str(value)
    return "review"


def _summary_dict(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    summary = payload.get("summary", {})
    return summary if isinstance(summary, dict) else {}


def _dict_value(payload: dict[str, Any], key: str, default: Any) -> Any:
    return payload.get(key, default) if isinstance(payload, dict) else default


def _access_focused_status_for_signal(artifact_id: str, payload: dict[str, Any]) -> str:
    if artifact_id == "provider_contract_smoke":
        return "ready" if payload.get("passed") is True else "blocked"
    if artifact_id not in {"provider_handoff_bundle", "provider_handoff_refresh"}:
        return _normalize_status(payload.get("status", "review"))
    access_focused_visibility = _access_focused_visibility_payload(payload)
    if isinstance(access_focused_visibility, dict):
        return _normalize_status(access_focused_visibility.get("status", "review"))
    return _normalize_status(payload.get("status", "review"))


def _access_focused_visibility_payload(
    payload: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    visibility = payload.get("access_focused_visibility")
    return visibility if isinstance(visibility, dict) else None


def _int_value(value: Any, *, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _format_value(value: Any) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)
