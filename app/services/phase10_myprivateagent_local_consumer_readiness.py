import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE10_LOCAL_CONSUMER_READINESS_ID = (
    "phase10-myprivateagent-local-consumer-readiness-v1"
)
PHASE10_CONTRACT_PATH = Path(
    "docs/integration/myprivateagent-local-consumer-verification/"
    "phase10-myprivateagent-local-consumer-verification-contract.md"
)
PHASE9_READINESS_PATH = Path(
    "docs/integration/myprivateagent-local-consumption/"
    "phase9-myprivateagent-local-consumption-readiness.json"
)
PHASE9_SMOKE_PATH = Path(
    "docs/smoke/myprivateagent-local-consumption/"
    "phase9-myprivateagent-local-consumption-smoke.json"
)
PROVIDER_HANDOFF_BUNDLE_PATH = Path(
    "docs/integration/provider-handoff/provider-handoff-bundle.json"
)
DEPLOYED_PROVIDER_SMOKE_PATH = Path(
    "docs/integration/deployed-provider-smoke/deployed-provider-smoke.json"
)
PHASE4_EVIDENCE_PACK_READINESS_PATH = Path(
    "docs/benchmark/chinese-seed/evidence-pack-readiness/"
    "phase4-evidence-pack-readiness.json"
)
PHASE4_CALLER_CONSUMPTION_SMOKE_PATH = Path(
    "docs/smoke/evidence-pack-consumption/phase4-caller-consumption-smoke.json"
)
PROVIDER_CONTRACT_SMOKE_PATH = Path("docs/smoke/provider-contract/provider-contract-smoke.json")
READINESS_JSON_FILENAME = "phase10-myprivateagent-local-consumer-readiness.json"
READINESS_MARKDOWN_FILENAME = "phase10-myprivateagent-local-consumer-readiness.md"
LOCAL_PROVIDER_URL_DEFAULT = "http://127.0.0.1:8020"


@dataclass(frozen=True)
class Phase10LocalConsumerSignal:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase10LocalConsumerReadinessReport:
    id: str
    generated_at: str
    status: str
    local_consumer_state: str
    decision: str
    summary: dict[str, Any]
    signals: list[Phase10LocalConsumerSignal]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase10_myprivateagent_local_consumer_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase10LocalConsumerReadinessReport:
    signals = [
        _contract_signal(base_dir),
        _phase9_readiness_signal(base_dir),
        _phase9_smoke_signal(base_dir),
        _handoff_bundle_signal(base_dir),
        _phase4_readiness_signal(base_dir),
        _phase4_caller_smoke_signal(base_dir),
        _provider_contract_smoke_signal(base_dir),
        _deployed_smoke_signal(base_dir),
    ]
    required_blocked = any(
        signal.required and signal.status == "blocked" for signal in signals
    )
    required_review = any(
        signal.required and signal.status == "review" for signal in signals
    )

    phase9_payload = _read_json_if_present(base_dir / PHASE9_READINESS_PATH)
    phase9_summary = _dict_value(phase9_payload, "summary", {})
    local_handoff_ready = bool(
        _dict_value(phase9_summary, "local_handoff_ready", False)
    )
    runtime_promotion_ready = bool(
        _dict_value(phase9_summary, "runtime_promotion_ready", False)
    )
    graph_boundary_ready = _graph_boundary_ready(base_dir)
    evidence_pack_ready = _evidence_pack_ready(base_dir)
    open_gate_ids = [s.id for s in signals if s.status in {"review", "blocked"}]

    if required_blocked:
        status = "blocked"
        local_consumer_state = "blocked"
        decision = "resolve_local_consumer_verification_blockers"
    elif required_review:
        status = "review"
        local_consumer_state = "ready_for_local_consumer_probe_review"
        decision = "run_local_consumer_probe_before_myprivateagent_integration"
    else:
        status = "ready"
        local_consumer_state = "ready_for_local_consumer_probe"
        decision = "confirm_local_consumer_probe_readiness"

    return Phase10LocalConsumerReadinessReport(
        id=PHASE10_LOCAL_CONSUMER_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        local_consumer_state=local_consumer_state,
        decision=decision,
        summary={
            "total_signals": len(signals),
            "required_signals": sum(1 for signal in signals if signal.required),
            "ready_signals": sum(1 for signal in signals if signal.status == "ready"),
            "review_signals": sum(1 for signal in signals if signal.status == "review"),
            "blocked_signals": sum(1 for signal in signals if signal.status == "blocked"),
            "local_provider_url": _local_provider_url(base_dir),
            "api_key_mode": _api_key_mode(base_dir),
            "phase9_local_handoff_ready": local_handoff_ready,
            "phase4_evidence_pack_ready": evidence_pack_ready,
            "graph_boundary_ready": graph_boundary_ready,
            "runtime_promotion_ready": runtime_promotion_ready,
            "runtime_promotion_status": "keep_runtime_defaults",
            "source_binding_policy_owner": "caller",
            "open_gate_ids": open_gate_ids,
        },
        signals=signals,
        notes=[
            "This report is provider-side read-only evidence for a MyPrivateAgent-shaped local consumer probe.",
            "Local development may keep PROVIDER_API_KEY unset; protected mode is documented for later internal or online deployment.",
            "The provider does not own source-to-agent binding, registration, heartbeat governance, audit policy, or final answer policy.",
        ],
    )


def phase10_myprivateagent_local_consumer_readiness_report_to_dict(
    report: Phase10LocalConsumerReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase10_myprivateagent_local_consumer_readiness_markdown(
    report: Phase10LocalConsumerReadinessReport,
) -> str:
    lines = [
        "# Phase 10 MyPrivateAgent Local Consumer Readiness",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Local Consumer State: `{report.local_consumer_state}`",
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


def export_phase10_myprivateagent_local_consumer_readiness_report(
    output_dir: Path = Path("docs/integration/myprivateagent-local-consumer-verification"),
    *,
    base_dir: Path = Path("."),
) -> Phase10LocalConsumerReadinessReport:
    report = build_phase10_myprivateagent_local_consumer_readiness_report(
        base_dir=base_dir
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / READINESS_JSON_FILENAME
    markdown_path = output_dir / READINESS_MARKDOWN_FILENAME
    exported = Phase10LocalConsumerReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        local_consumer_state=report.local_consumer_state,
        decision=report.decision,
        summary=report.summary,
        signals=report.signals,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase10_myprivateagent_local_consumer_readiness_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase10_myprivateagent_local_consumer_readiness_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _contract_signal(base_dir: Path) -> Phase10LocalConsumerSignal:
    path = base_dir / PHASE10_CONTRACT_PATH
    if path.exists():
        return Phase10LocalConsumerSignal(
            id="phase10_local_consumer_verification_contract",
            required=True,
            status="ready",
            summary="contract_present=true",
            recommended_action="no_action_required",
            evidence_path=str(PHASE10_CONTRACT_PATH),
        )
    return Phase10LocalConsumerSignal(
        id="phase10_local_consumer_verification_contract",
        required=True,
        status="blocked",
        summary="contract_present=false",
        recommended_action="restore_phase10_local_consumer_verification_contract",
        evidence_path=str(PHASE10_CONTRACT_PATH),
    )


def _phase9_readiness_signal(base_dir: Path) -> Phase10LocalConsumerSignal:
    payload = _read_json_if_present(base_dir / PHASE9_READINESS_PATH)
    if payload is None:
        return _missing_signal(
            "phase9_myprivateagent_local_consumption_readiness",
            PHASE9_READINESS_PATH,
            True,
            "regenerate_phase9_myprivateagent_local_consumption_readiness",
        )
    status = _normalize_status(payload.get("status"))
    summary = _dict_value(payload, "summary", {})
    return Phase10LocalConsumerSignal(
        id="phase9_myprivateagent_local_consumption_readiness",
        required=True,
        status=status,
        summary=(
            f"status={status}; local_consumption_state="
            f"{payload.get('local_consumption_state', 'review')}; "
            f"local_handoff_ready={bool(_dict_value(summary, 'local_handoff_ready', False))}"
        ),
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(PHASE9_READINESS_PATH),
    )


def _phase9_smoke_signal(base_dir: Path) -> Phase10LocalConsumerSignal:
    payload = _read_json_if_present(base_dir / PHASE9_SMOKE_PATH)
    if payload is None:
        return _missing_signal(
            "phase9_myprivateagent_local_consumption_smoke",
            PHASE9_SMOKE_PATH,
            True,
            "regenerate_phase9_myprivateagent_local_consumption_smoke",
        )
    status = _normalize_status(payload.get("status"))
    summary = _dict_value(payload, "summary", {})
    return Phase10LocalConsumerSignal(
        id="phase9_myprivateagent_local_consumption_smoke",
        required=True,
        status=status,
        summary=(
            f"status={status}; passed_checks={_dict_value(summary, 'passed_checks', 0)}/"
            f"{_dict_value(summary, 'total_checks', 0)}"
        ),
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(PHASE9_SMOKE_PATH),
    )


def _handoff_bundle_signal(base_dir: Path) -> Phase10LocalConsumerSignal:
    payload = _read_json_if_present(base_dir / PROVIDER_HANDOFF_BUNDLE_PATH)
    if payload is None:
        return _missing_signal(
            "provider_handoff_bundle",
            PROVIDER_HANDOFF_BUNDLE_PATH,
            True,
            "regenerate_provider_handoff_bundle",
        )
    status = _normalize_status(payload.get("status"))
    artifacts = payload.get("evidence_artifacts", [])
    artifact_count = len(artifacts) if isinstance(artifacts, list) else 0
    return Phase10LocalConsumerSignal(
        id="provider_handoff_bundle",
        required=True,
        status=status,
        summary=f"status={status}; evidence_artifacts={artifact_count}",
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(PROVIDER_HANDOFF_BUNDLE_PATH),
    )


def _phase4_readiness_signal(base_dir: Path) -> Phase10LocalConsumerSignal:
    payload = _read_json_if_present(base_dir / PHASE4_EVIDENCE_PACK_READINESS_PATH)
    if payload is None:
        return _missing_signal(
            "phase4_evidence_pack_readiness",
            PHASE4_EVIDENCE_PACK_READINESS_PATH,
            True,
            "regenerate_phase4_evidence_pack_readiness",
        )
    status = _normalize_status(payload.get("status"))
    return Phase10LocalConsumerSignal(
        id="phase4_evidence_pack_readiness",
        required=True,
        status=status,
        summary=f"status={status}; decision={payload.get('decision', 'keep_caller_ownership')}",
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(PHASE4_EVIDENCE_PACK_READINESS_PATH),
    )


def _phase4_caller_smoke_signal(base_dir: Path) -> Phase10LocalConsumerSignal:
    payload = _read_json_if_present(base_dir / PHASE4_CALLER_CONSUMPTION_SMOKE_PATH)
    if payload is None:
        return _missing_signal(
            "phase4_caller_consumption_smoke",
            PHASE4_CALLER_CONSUMPTION_SMOKE_PATH,
            True,
            "regenerate_phase4_caller_consumption_smoke",
        )
    status = _normalize_status(payload.get("status"))
    summary = _dict_value(payload, "summary", {})
    return Phase10LocalConsumerSignal(
        id="phase4_caller_consumption_smoke",
        required=True,
        status=status,
        summary=(
            f"status={status}; passed_checks={_dict_value(summary, 'passed_checks', _dict_value(summary, 'passed', 0))}/"
            f"{_dict_value(summary, 'total_checks', _dict_value(summary, 'total', 0))}"
        ),
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(PHASE4_CALLER_CONSUMPTION_SMOKE_PATH),
    )


def _provider_contract_smoke_signal(base_dir: Path) -> Phase10LocalConsumerSignal:
    payload = _read_json_if_present(base_dir / PROVIDER_CONTRACT_SMOKE_PATH)
    if payload is None:
        return _missing_signal(
            "provider_contract_smoke",
            PROVIDER_CONTRACT_SMOKE_PATH,
            True,
            "regenerate_provider_contract_smoke",
        )
    passed = payload.get("passed") is True
    status = "ready" if passed else "blocked"
    summary = _dict_value(payload, "summary", {})
    return Phase10LocalConsumerSignal(
        id="provider_contract_smoke",
        required=True,
        status=status,
        summary=(
            f"passed={passed}; checks={_dict_value(summary, 'passed', 0)}/"
            f"{_dict_value(summary, 'total', 0)}"
        ),
        recommended_action="no_action_required" if passed else "regenerate_provider_contract_smoke",
        evidence_path=str(PROVIDER_CONTRACT_SMOKE_PATH),
    )


def _deployed_smoke_signal(base_dir: Path) -> Phase10LocalConsumerSignal:
    payload = _read_json_if_present(base_dir / DEPLOYED_PROVIDER_SMOKE_PATH)
    if payload is None:
        return _missing_signal(
            "deployed_provider_smoke",
            DEPLOYED_PROVIDER_SMOKE_PATH,
            False,
            "run_deployed_provider_smoke_after_starting_local_provider",
        )
    status = _normalize_status(payload.get("status"))
    return Phase10LocalConsumerSignal(
        id="deployed_provider_smoke",
        required=False,
        status=status,
        summary=f"status={status}; base_url={payload.get('base_url', LOCAL_PROVIDER_URL_DEFAULT)}",
        recommended_action="no_action_required" if status == "ready" else "review_evidence_notes",
        evidence_path=str(DEPLOYED_PROVIDER_SMOKE_PATH),
    )


def _missing_signal(
    id: str,
    path: Path,
    required: bool,
    action: str,
) -> Phase10LocalConsumerSignal:
    return Phase10LocalConsumerSignal(
        id=id,
        required=required,
        status="blocked" if required else "review",
        summary="artifact_present=false",
        recommended_action=action,
        evidence_path=str(path),
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


def _graph_boundary_ready(base_dir: Path) -> bool:
    payload = _read_json_if_present(base_dir / PROVIDER_CONTRACT_SMOKE_PATH)
    checks = _dict_value(payload, "checks", [])
    if not isinstance(checks, list):
        return False
    return any(
        isinstance(check, dict)
        and check.get("name") == "graph_planned_boundary"
        and check.get("passed") is True
        for check in checks
    )


def _evidence_pack_ready(base_dir: Path) -> bool:
    readiness = _read_json_if_present(base_dir / PHASE4_EVIDENCE_PACK_READINESS_PATH)
    smoke = _read_json_if_present(base_dir / PHASE4_CALLER_CONSUMPTION_SMOKE_PATH)
    return (
        _normalize_status(_dict_value(readiness, "status", "review")) == "ready"
        and _normalize_status(_dict_value(smoke, "status", "review")) == "ready"
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
