import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE24_DOCUMENT_RAG_TRIAL_READINESS_ID = (
    "phase24-document-rag-trial-readiness-v1"
)
OUTPUT_JSON_FILENAME = "phase24-document-rag-trial-readiness.json"
OUTPUT_MARKDOWN_FILENAME = "phase24-document-rag-trial-readiness.md"
LOCAL_PROVIDER_URL_DEFAULT = "http://127.0.0.1:8020"


@dataclass(frozen=True)
class TrialReadinessSignalSpec:
    id: str
    path: Path
    required: bool
    missing_action: str


@dataclass(frozen=True)
class TrialReadinessSignal:
    id: str
    required: bool
    status: str
    summary: str
    recommended_action: str
    evidence_path: str


@dataclass(frozen=True)
class Phase24DocumentRagTrialReadinessReport:
    id: str
    generated_at: str
    status: str
    trial_readiness_state: str
    decision: str
    summary: dict[str, Any]
    primitive_signals: list[TrialReadinessSignal]
    review_context_signals: list[TrialReadinessSignal]
    caller_next_actions: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


PROVIDER_CONTRACT_SMOKE_PATH = Path("docs/smoke/provider-contract/provider-contract-smoke.json")
PHASE10_PROBE_PATH = Path(
    "docs/smoke/myprivateagent-local-consumer-verification/"
    "phase10-myprivateagent-local-consumer-probe.json"
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

PHASE10_READINESS_PATH = Path(
    "docs/integration/myprivateagent-local-consumer-verification/"
    "phase10-myprivateagent-local-consumer-readiness.json"
)
PHASE11_PROFILE_PATH = Path(
    "docs/integration/myprivateagent-local-provider-integration/"
    "phase11-local-provider-integration-profile.json"
)
PHASE14_ACCEPTANCE_PATH = Path(
    "docs/integration/myprivateagent-provider-integration-acceptance/"
    "phase14-myprivateagent-provider-integration-acceptance-checkpoint.json"
)
PHASE15_DISPATCH_PATH = Path(
    "docs/integration/myprivateagent-repo-side-trial-dispatch/"
    "phase15-myprivateagent-repo-side-trial-dispatch-package.json"
)
PHASE16_ACCESS_LOOP_PATH = Path(
    "docs/integration/myprivateagent-minimal-access-loop/"
    "phase16-myprivateagent-minimal-access-loop.json"
)
PROVIDER_HANDOFF_BUNDLE_PATH = Path(
    "docs/integration/provider-handoff/provider-handoff-bundle.json"
)
PROVIDER_HANDOFF_REFRESH_PATH = Path(
    "docs/integration/provider-handoff-refresh/provider-handoff-refresh.json"
)


PRIMITIVE_SIGNAL_SPECS: list[TrialReadinessSignalSpec] = [
    TrialReadinessSignalSpec(
        id="provider_contract_smoke",
        path=PROVIDER_CONTRACT_SMOKE_PATH,
        required=True,
        missing_action="regenerate_provider_contract_smoke",
    ),
    TrialReadinessSignalSpec(
        id="phase10_myprivateagent_local_consumer_probe",
        path=PHASE10_PROBE_PATH,
        required=True,
        missing_action="regenerate_phase10_myprivateagent_local_consumer_probe",
    ),
    TrialReadinessSignalSpec(
        id="phase11_provider_discovery_smoke",
        path=PHASE11_PROVIDER_DISCOVERY_SMOKE_PATH,
        required=True,
        missing_action="regenerate_phase11_provider_discovery_smoke",
    ),
    TrialReadinessSignalSpec(
        id="phase11_rag_retrieve_consumption_smoke",
        path=PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_PATH,
        required=True,
        missing_action="regenerate_phase11_rag_retrieve_consumption_smoke",
    ),
    TrialReadinessSignalSpec(
        id="phase11_source_binding_preview_smoke",
        path=PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_PATH,
        required=True,
        missing_action="regenerate_phase11_source_binding_preview_smoke",
    ),
]

REVIEW_CONTEXT_SIGNAL_SPECS: list[TrialReadinessSignalSpec] = [
    TrialReadinessSignalSpec(
        id="phase10_myprivateagent_local_consumer_readiness",
        path=PHASE10_READINESS_PATH,
        required=False,
        missing_action="regenerate_phase10_myprivateagent_local_consumer_readiness",
    ),
    TrialReadinessSignalSpec(
        id="phase11_local_provider_integration_profile",
        path=PHASE11_PROFILE_PATH,
        required=False,
        missing_action="regenerate_phase11_local_provider_integration_profile",
    ),
    TrialReadinessSignalSpec(
        id="phase14_myprivateagent_provider_integration_acceptance_checkpoint",
        path=PHASE14_ACCEPTANCE_PATH,
        required=False,
        missing_action="regenerate_phase14_myprivateagent_provider_integration_acceptance_checkpoint",
    ),
    TrialReadinessSignalSpec(
        id="phase15_myprivateagent_repo_side_trial_dispatch_package",
        path=PHASE15_DISPATCH_PATH,
        required=False,
        missing_action="regenerate_phase15_myprivateagent_repo_side_trial_dispatch_package",
    ),
    TrialReadinessSignalSpec(
        id="phase16_myprivateagent_minimal_access_loop",
        path=PHASE16_ACCESS_LOOP_PATH,
        required=False,
        missing_action="regenerate_phase16_myprivateagent_minimal_access_loop",
    ),
    TrialReadinessSignalSpec(
        id="provider_handoff_bundle",
        path=PROVIDER_HANDOFF_BUNDLE_PATH,
        required=False,
        missing_action="regenerate_provider_handoff_bundle",
    ),
    TrialReadinessSignalSpec(
        id="provider_handoff_refresh",
        path=PROVIDER_HANDOFF_REFRESH_PATH,
        required=False,
        missing_action="regenerate_provider_handoff_refresh",
    ),
]


def build_phase24_document_rag_trial_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase24DocumentRagTrialReadinessReport:
    primitive_signals = [
        _build_signal(spec, base_dir=base_dir) for spec in PRIMITIVE_SIGNAL_SPECS
    ]
    review_context_signals = [
        _build_signal(spec, base_dir=base_dir) for spec in REVIEW_CONTEXT_SIGNAL_SPECS
    ]
    blocked_primitive_ids = [
        signal.id for signal in primitive_signals if signal.status == "blocked"
    ]
    review_primitive_ids = [
        signal.id for signal in primitive_signals if signal.status == "review"
    ]
    ready_primitive_ids = [
        signal.id for signal in primitive_signals if signal.status == "ready"
    ]
    open_review_context_ids = [
        signal.id for signal in review_context_signals if signal.status != "ready"
    ]

    if blocked_primitive_ids:
        status = "blocked"
        trial_readiness_state = "blocked_for_repo_side_document_rag_trial"
        decision = "blocked"
    elif review_primitive_ids:
        status = "review"
        trial_readiness_state = "review_for_repo_side_document_rag_trial"
        decision = "review"
    else:
        status = "ready"
        trial_readiness_state = "ready_for_repo_side_document_rag_trial"
        decision = "go"

    return Phase24DocumentRagTrialReadinessReport(
        id=PHASE24_DOCUMENT_RAG_TRIAL_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        trial_readiness_state=trial_readiness_state,
        decision=decision,
        summary={
            "roadmap_phase": "Phase 24",
            "roadmap_focus": "external_knowledge_provider_document_rag_readiness_closure",
            "local_provider_url": LOCAL_PROVIDER_URL_DEFAULT,
            "primitive_gate_status": status,
            "primitive_signal_count": len(primitive_signals),
            "ready_primitive_signal_ids": ready_primitive_ids,
            "review_primitive_signal_ids": review_primitive_ids,
            "blocked_primitive_signal_ids": blocked_primitive_ids,
            "review_context_signal_count": len(review_context_signals),
            "open_review_context_signal_ids": open_review_context_ids,
            "runtime_promotion_status": "keep_runtime_defaults",
            "retrieval_backend_promotion_status": "not_promoted_by_this_report",
            "graph_execution_status": "planned_boundary_only",
            "source_binding_policy_owner": "caller",
            "trial_execution_owner": "MyPrivateAgent",
        },
        primitive_signals=primitive_signals,
        review_context_signals=review_context_signals,
        caller_next_actions=_caller_next_actions(decision),
        notes=[
            "This report is a local read-only provider closure artifact for MyPrivateAgent document RAG trial readiness.",
            "Review-context signals remain visible but do not block the primitive access gate.",
            "MyPrivateAgent owns repo-side trial execution, source-to-agent binding, audit policy, and final answer behavior.",
            "This report does not promote retrieval defaults, execute GraphRAG, start a server, rebuild indexes, or download models.",
        ],
    )


def phase24_document_rag_trial_readiness_report_to_dict(
    report: Phase24DocumentRagTrialReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase24_document_rag_trial_readiness_markdown(
    report: Phase24DocumentRagTrialReadinessReport,
) -> str:
    lines = [
        "# Phase 24 Document RAG Trial Readiness",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Trial Readiness State: `{report.trial_readiness_state}`",
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
    lines.extend(["", "## Caller Next Actions", ""])
    lines.extend(f"- {action}" for action in report.caller_next_actions)
    lines.extend(
        [
            "",
            "## Primitive Signals",
            "",
            "| Signal | Status | Summary | Recommended Action |",
            "|---|---|---|---|",
        ]
    )
    for signal in report.primitive_signals:
        lines.append(
            f"| `{signal.id}` | `{signal.status}` | "
            f"{signal.summary} | `{signal.recommended_action}` |"
        )
    lines.extend(
        [
            "",
            "## Review Context Signals",
            "",
            "| Signal | Status | Summary | Recommended Action |",
            "|---|---|---|---|",
        ]
    )
    for signal in report.review_context_signals:
        lines.append(
            f"| `{signal.id}` | `{signal.status}` | "
            f"{signal.summary} | `{signal.recommended_action}` |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    return "\n".join(lines).rstrip() + "\n"


def export_phase24_document_rag_trial_readiness_report(
    *,
    output_dir: Path = Path("docs/integration/myprivateagent-document-rag-trial-readiness"),
    base_dir: Path = Path("."),
) -> Phase24DocumentRagTrialReadinessReport:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_phase24_document_rag_trial_readiness_report(base_dir=base_dir)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = Phase24DocumentRagTrialReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        trial_readiness_state=report.trial_readiness_state,
        decision=report.decision,
        summary=report.summary,
        primitive_signals=report.primitive_signals,
        review_context_signals=report.review_context_signals,
        caller_next_actions=report.caller_next_actions,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase24_document_rag_trial_readiness_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase24_document_rag_trial_readiness_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _build_signal(
    spec: TrialReadinessSignalSpec,
    *,
    base_dir: Path,
) -> TrialReadinessSignal:
    payload = _read_json_if_present(base_dir / spec.path)
    if payload is None:
        return TrialReadinessSignal(
            id=spec.id,
            required=spec.required,
            status="blocked" if spec.required else "review",
            summary="status=missing",
            recommended_action=spec.missing_action,
            evidence_path=str(spec.path),
        )

    status = _signal_status(spec.id, payload)
    return TrialReadinessSignal(
        id=spec.id,
        required=spec.required,
        status=status,
        summary=_signal_summary(spec.id, payload, status),
        recommended_action=_recommended_action(status, spec.missing_action),
        evidence_path=str(spec.path),
    )


def _signal_status(signal_id: str, payload: dict[str, Any]) -> str:
    if signal_id == "provider_contract_smoke":
        return "ready" if payload.get("passed") is True else "blocked"
    if signal_id in {"provider_handoff_bundle", "provider_handoff_refresh"}:
        visibility = payload.get("access_focused_visibility")
        if isinstance(visibility, dict):
            return _normalize_status(visibility.get("status"))
    return _normalize_status(payload.get("status"))


def _signal_summary(signal_id: str, payload: dict[str, Any], status: str) -> str:
    summary = payload.get("summary")
    summary = summary if isinstance(summary, dict) else {}
    if signal_id == "provider_contract_smoke":
        smoke_summary = payload.get("summary")
        smoke_summary = smoke_summary if isinstance(smoke_summary, dict) else {}
        failed = smoke_summary.get("failed", smoke_summary.get("failed_checks", "unknown"))
        total = smoke_summary.get("total", smoke_summary.get("total_checks", "unknown"))
        return f"status={status}; passed={payload.get('passed', 'unknown')}; failed={failed}; total={total}"
    if "decision" in payload:
        return f"status={status}; decision={payload.get('decision')}"
    if summary:
        compact = {
            key: summary.get(key)
            for key in (
                "passed_checks",
                "total_checks",
                "access_gate_status",
                "primitive_gate_status",
                "runtime_promotion_status",
            )
            if key in summary
        }
        if compact:
            return f"status={status}; summary={json.dumps(compact, ensure_ascii=False, sort_keys=True)}"
    return f"status={status}"


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_status(value: Any) -> str:
    if value in {"ready", "review", "blocked"}:
        return str(value)
    if value in {"passed", "bindable"}:
        return "ready"
    return "review"


def _recommended_action(status: str, missing_action: str) -> str:
    if status == "ready":
        return "no_action_required"
    if status == "blocked":
        return missing_action
    return "review_evidence_notes"


def _caller_next_actions(decision: str) -> list[str]:
    if decision == "go":
        return [
            "begin_myprivateagent_repo_side_document_rag_trial",
            "capture_trial_outcome_in_myprivateagent",
        ]
    if decision == "review":
        return [
            "review_open_primitive_signal_notes",
            "refresh_phase24_document_rag_trial_readiness",
        ]
    return [
        "resolve_blocked_primitive_signals",
        "regenerate_provider_contract_phase10_phase11_smokes",
        "rerun_phase24_document_rag_trial_readiness",
    ]


def _format_value(value: Any) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)
