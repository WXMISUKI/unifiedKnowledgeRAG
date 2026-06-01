import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE7_PROVIDER_RELEASE_READINESS_ID = "phase7-provider-release-readiness-v1"
PHASE7_HANDOFF_ACCEPTANCE_CONTRACT_PATH = Path(
    "docs/operations/provider-release-readiness/"
    "phase7-provider-handoff-acceptance-contract.md"
)
PHASE7_PROVIDER_INTEGRATION_PROBE_PATH = Path(
    "docs/integration/provider-binding/provider-integration-probe.json"
)
PHASE7_PROVIDER_CONTRACT_SMOKE_PATH = Path(
    "docs/smoke/provider-contract/provider-contract-smoke.json"
)
PHASE7_SOURCE_BINDING_SUMMARY_PATH = Path(
    "docs/integration/source-bindings/provider-source-bindings.json"
)
PHASE7_PHASE2_SOURCE_FORMAT_READINESS_PATH = Path(
    "docs/operations/source-format-demand/phase2-source-format-demand-readiness.json"
)
PHASE7_PHASE2_UNSUPPORTED_SMOKE_PATH = Path(
    "docs/smoke/source-format-demand/phase2-unsupported-format-negative-control-smoke.json"
)
PHASE7_PHASE3_PROMOTION_DECISION_READINESS_PATH = Path(
    "docs/benchmark/chinese-seed/hybrid-runtime-promotion/"
    "phase3-hybrid-runtime-promotion-decision-readiness.json"
)
PHASE7_PHASE3_PROMOTION_DECISION_SMOKE_PATH = Path(
    "docs/smoke/hybrid-runtime-promotion/"
    "phase3-hybrid-runtime-promotion-decision-smoke.json"
)
PHASE7_PHASE4_EVIDENCE_PACK_READINESS_PATH = Path(
    "docs/benchmark/chinese-seed/evidence-pack-readiness/phase4-evidence-pack-readiness.json"
)
PHASE7_PHASE4_CALLER_SMOKE_PATH = Path(
    "docs/smoke/evidence-pack-consumption/phase4-caller-consumption-smoke.json"
)
PHASE7_PHASE5_GRAPH_READINESS_PATH = Path(
    "docs/benchmark/chinese-seed/graph-use-case-readiness/phase5-graph-use-case-readiness.json"
)
PHASE7_PHASE5_GRAPH_SMOKE_PATH = Path(
    "docs/smoke/graph-boundary-summary/phase5-graph-boundary-smoke-summary.json"
)
PHASE7_PHASE6_DEPLOYMENT_READINESS_PATH = Path(
    "docs/operations/deployment-readiness/deployment-readiness.json"
)
PHASE7_PHASE6_DEPLOYED_FIELD_VALIDATION_PATH = Path(
    "docs/operations/deployed-field-validation/"
    "phase6-deployed-field-validation-readiness.json"
)
PHASE7_PHASE6_PRIVATE_NETWORK_READINESS_PATH = Path(
    "docs/operations/private-network-promotion/"
    "phase6-qdrant-bge-private-network-promotion-readiness.json"
)
PHASE7_PROVIDER_RELEASE_READINESS_JSON = "phase7-provider-release-readiness.json"
PHASE7_PROVIDER_RELEASE_READINESS_MARKDOWN = "phase7-provider-release-readiness.md"


@dataclass(frozen=True)
class Phase7ProviderReleaseSignal:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase7ProviderReleaseReadinessReport:
    id: str
    generated_at: str
    status: str
    release_state: str
    decision: str
    summary: dict[str, Any]
    signals: list[Phase7ProviderReleaseSignal]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase7_provider_release_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase7ProviderReleaseReadinessReport:
    signals = [
        _contract_signal(base_dir),
        _integration_probe_signal(base_dir),
        _contract_smoke_signal(base_dir),
        _source_binding_signal(base_dir),
        _optional_status_signal(
            id="phase2_source_format_demand_readiness",
            path=PHASE7_PHASE2_SOURCE_FORMAT_READINESS_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase2_source_format_demand_readiness",
        ),
        _optional_status_signal(
            id="phase2_unsupported_format_negative_control_smoke",
            path=PHASE7_PHASE2_UNSUPPORTED_SMOKE_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase2_unsupported_format_negative_control_smoke",
        ),
        _optional_status_signal(
            id="phase3_hybrid_runtime_promotion_decision_readiness",
            path=PHASE7_PHASE3_PROMOTION_DECISION_READINESS_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase3_hybrid_runtime_promotion_decision_readiness",
        ),
        _optional_status_signal(
            id="phase3_hybrid_runtime_promotion_decision_smoke",
            path=PHASE7_PHASE3_PROMOTION_DECISION_SMOKE_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase3_hybrid_runtime_promotion_decision_smoke",
        ),
        _optional_status_signal(
            id="phase4_evidence_pack_readiness",
            path=PHASE7_PHASE4_EVIDENCE_PACK_READINESS_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase4_evidence_pack_readiness",
        ),
        _optional_status_signal(
            id="phase4_caller_consumption_smoke",
            path=PHASE7_PHASE4_CALLER_SMOKE_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase4_caller_consumption_smoke",
        ),
        _optional_status_signal(
            id="phase5_graph_use_case_readiness",
            path=PHASE7_PHASE5_GRAPH_READINESS_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase5_graph_use_case_readiness",
        ),
        _optional_status_signal(
            id="phase5_graph_boundary_smoke_summary",
            path=PHASE7_PHASE5_GRAPH_SMOKE_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase5_graph_boundary_smoke_summary",
        ),
        _optional_status_signal(
            id="phase6_deployment_readiness",
            path=PHASE7_PHASE6_DEPLOYMENT_READINESS_PATH,
            base_dir=base_dir,
            missing_action="regenerate_deployment_readiness",
        ),
        _optional_status_signal(
            id="phase6_deployed_field_validation_readiness",
            path=PHASE7_PHASE6_DEPLOYED_FIELD_VALIDATION_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase6_deployed_field_validation_readiness",
        ),
        _optional_status_signal(
            id="phase6_qdrant_bge_private_network_promotion_readiness",
            path=PHASE7_PHASE6_PRIVATE_NETWORK_READINESS_PATH,
            base_dir=base_dir,
            missing_action="regenerate_phase6_qdrant_bge_private_network_promotion_readiness",
        ),
    ]

    required_blocked = any(
        signal.required and signal.status == "blocked" for signal in signals
    )
    required_ready = all(
        signal.status == "ready" for signal in signals if signal.required
    )

    ready_for_local_provider_handoff = required_ready and not required_blocked
    ready_for_runtime_default_promotion = _runtime_promotion_ready(signals)

    if required_blocked:
        status = "blocked"
        release_state = "blocked"
        decision = "fix_required_handoff_gates"
    elif ready_for_local_provider_handoff and ready_for_runtime_default_promotion:
        status = "ready"
        release_state = "ready_for_runtime_promotion"
        decision = "allow_runtime_default_promotion_review"
    elif ready_for_local_provider_handoff:
        status = "review"
        release_state = "ready_for_local_handoff"
        decision = "keep_runtime_defaults"
    else:
        status = "review"
        release_state = "review"
        decision = "review_handoff_signals"

    summary = _summary(
        signals,
        ready_for_local_provider_handoff=ready_for_local_provider_handoff,
        ready_for_runtime_default_promotion=ready_for_runtime_default_promotion,
    )
    return Phase7ProviderReleaseReadinessReport(
        id=PHASE7_PROVIDER_RELEASE_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        release_state=release_state,
        decision=decision,
        summary=summary,
        signals=signals,
        notes=[
            "This report is local read-only cross-phase release evidence.",
            "Local handoff acceptance does not imply runtime default promotion.",
            "Runtime promotion remains separately gated by customer-like benchmark, deployment, and live-url evidence.",
        ],
    )


def phase7_provider_release_readiness_report_to_dict(
    report: Phase7ProviderReleaseReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase7_provider_release_readiness_markdown(
    report: Phase7ProviderReleaseReadinessReport,
) -> str:
    lines = [
        "# Phase 7 Provider Release Readiness",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Release State: `{report.release_state}`",
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
        f"| Local Handoff Ready | `{report.summary['ready_for_local_provider_handoff']}` |",
        f"| Runtime Promotion Ready | `{report.summary['ready_for_runtime_default_promotion']}` |",
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


def export_phase7_provider_release_readiness_report(
    output_dir: Path = Path("docs/operations/provider-release-readiness"),
    *,
    base_dir: Path = Path("."),
) -> Phase7ProviderReleaseReadinessReport:
    report = build_phase7_provider_release_readiness_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PHASE7_PROVIDER_RELEASE_READINESS_JSON
    markdown_path = output_dir / PHASE7_PROVIDER_RELEASE_READINESS_MARKDOWN
    exported = Phase7ProviderReleaseReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        release_state=report.release_state,
        decision=report.decision,
        summary=report.summary,
        signals=report.signals,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase7_provider_release_readiness_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase7_provider_release_readiness_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _contract_signal(base_dir: Path) -> Phase7ProviderReleaseSignal:
    path = base_dir / PHASE7_HANDOFF_ACCEPTANCE_CONTRACT_PATH
    if path.exists():
        return Phase7ProviderReleaseSignal(
            id="phase7_provider_handoff_acceptance_contract",
            required=True,
            status="ready",
            summary="contract_present=true",
            recommended_action="no_action_required",
            evidence_path=str(PHASE7_HANDOFF_ACCEPTANCE_CONTRACT_PATH),
        )
    return Phase7ProviderReleaseSignal(
        id="phase7_provider_handoff_acceptance_contract",
        required=True,
        status="blocked",
        summary="contract_present=false",
        recommended_action="restore_phase7_provider_handoff_acceptance_contract",
        evidence_path=str(PHASE7_HANDOFF_ACCEPTANCE_CONTRACT_PATH),
    )


def _integration_probe_signal(base_dir: Path) -> Phase7ProviderReleaseSignal:
    path = base_dir / PHASE7_PROVIDER_INTEGRATION_PROBE_PATH
    payload = _read_json_if_present(path)
    if payload is None:
        return Phase7ProviderReleaseSignal(
            id="provider_integration_probe",
            required=True,
            status="blocked",
            summary="artifact_present=false",
            recommended_action="regenerate_provider_integration_probe",
            evidence_path=str(PHASE7_PROVIDER_INTEGRATION_PROBE_PATH),
        )
    bindable = bool(payload.get("bindable"))
    status = "ready" if bindable else "blocked"
    return Phase7ProviderReleaseSignal(
        id="provider_integration_probe",
        required=True,
        status=status,
        summary=f"artifact_present=true; bindable={bindable}",
        recommended_action=(
            "no_action_required" if status == "ready" else "resolve_binding_blockers"
        ),
        evidence_path=str(PHASE7_PROVIDER_INTEGRATION_PROBE_PATH),
    )


def _contract_smoke_signal(base_dir: Path) -> Phase7ProviderReleaseSignal:
    path = base_dir / PHASE7_PROVIDER_CONTRACT_SMOKE_PATH
    payload = _read_json_if_present(path)
    if payload is None:
        return Phase7ProviderReleaseSignal(
            id="provider_contract_smoke",
            required=True,
            status="blocked",
            summary="artifact_present=false",
            recommended_action="regenerate_provider_contract_smoke",
            evidence_path=str(PHASE7_PROVIDER_CONTRACT_SMOKE_PATH),
        )
    passed = payload.get("passed") is True
    smoke_summary = payload.get("summary", {})
    status = "ready" if passed else "blocked"
    return Phase7ProviderReleaseSignal(
        id="provider_contract_smoke",
        required=True,
        status=status,
        summary=(
            "artifact_present=true; "
            f"checks={_int_value(_dict_value(smoke_summary, 'passed', 0), fallback=0)}/"
            f"{_int_value(_dict_value(smoke_summary, 'total', 0), fallback=0)}"
        ),
        recommended_action=(
            "no_action_required" if status == "ready" else "resolve_contract_failures"
        ),
        evidence_path=str(PHASE7_PROVIDER_CONTRACT_SMOKE_PATH),
    )


def _source_binding_signal(base_dir: Path) -> Phase7ProviderReleaseSignal:
    path = base_dir / PHASE7_SOURCE_BINDING_SUMMARY_PATH
    payload = _read_json_if_present(path)
    if payload is None:
        return Phase7ProviderReleaseSignal(
            id="source_binding_summary",
            required=True,
            status="blocked",
            summary="artifact_present=false",
            recommended_action="regenerate_source_binding_summary",
            evidence_path=str(PHASE7_SOURCE_BINDING_SUMMARY_PATH),
        )
    status = _normalize_status(payload.get("status"))
    source_count = _int_value(payload.get("total_source_count"), fallback=0)
    bindable_count = _int_value(payload.get("bindable_source_count"), fallback=0)
    return Phase7ProviderReleaseSignal(
        id="source_binding_summary",
        required=True,
        status="ready" if status == "ready" else "blocked",
        summary=(
            f"artifact_present=true; status={status}; "
            f"bindable_sources={bindable_count}/{source_count}"
        ),
        recommended_action=(
            "no_action_required" if status == "ready" else "resolve_source_binding_blockers"
        ),
        evidence_path=str(PHASE7_SOURCE_BINDING_SUMMARY_PATH),
    )


def _optional_status_signal(
    *,
    id: str,
    path: Path,
    base_dir: Path,
    missing_action: str,
) -> Phase7ProviderReleaseSignal:
    payload = _read_json_if_present(base_dir / path)
    if payload is None:
        return Phase7ProviderReleaseSignal(
            id=id,
            required=False,
            status="review",
            summary="artifact_present=false",
            recommended_action=missing_action,
            evidence_path=str(path),
        )
    status = _normalize_status(payload.get("status"))
    return Phase7ProviderReleaseSignal(
        id=id,
        required=False,
        status=status,
        summary=f"artifact_present=true; status={status}",
        recommended_action=(
            "no_action_required" if status == "ready" else "review_evidence_notes"
        ),
        evidence_path=str(path),
    )


def _summary(
    signals: list[Phase7ProviderReleaseSignal],
    *,
    ready_for_local_provider_handoff: bool,
    ready_for_runtime_default_promotion: bool,
) -> dict[str, Any]:
    return {
        "total_signals": len(signals),
        "required_signals": sum(1 for signal in signals if signal.required),
        "ready_signals": sum(1 for signal in signals if signal.status == "ready"),
        "review_signals": sum(1 for signal in signals if signal.status == "review"),
        "blocked_signals": sum(1 for signal in signals if signal.status == "blocked"),
        "ready_for_local_provider_handoff": ready_for_local_provider_handoff,
        "ready_for_runtime_default_promotion": ready_for_runtime_default_promotion,
        "open_gate_ids": [
            signal.id for signal in signals if signal.status in {"review", "blocked"}
        ],
    }


def _runtime_promotion_ready(signals: list[Phase7ProviderReleaseSignal]) -> bool:
    phase3_ready = _signal_ready(
        signals, "phase3_hybrid_runtime_promotion_decision_readiness"
    )
    phase3_smoke_ready = _signal_ready(signals, "phase3_hybrid_runtime_promotion_decision_smoke")
    phase6_private_ready = _signal_ready(
        signals, "phase6_qdrant_bge_private_network_promotion_readiness"
    )
    phase6_deployed_ready = _signal_ready(
        signals, "phase6_deployed_field_validation_readiness"
    )
    # Promotion remains conservative: all core promotion-facing signals must be ready.
    return phase3_ready and phase3_smoke_ready and phase6_private_ready and phase6_deployed_ready


def _signal_ready(signals: list[Phase7ProviderReleaseSignal], signal_id: str) -> bool:
    signal = next((item for item in signals if item.id == signal_id), None)
    return signal is not None and signal.status == "ready"


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
