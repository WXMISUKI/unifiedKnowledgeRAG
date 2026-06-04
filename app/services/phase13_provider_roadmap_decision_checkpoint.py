import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable


PHASE13_PROVIDER_ROADMAP_DECISION_CHECKPOINT_ID = (
    "phase13-provider-roadmap-decision-checkpoint-v1"
)
OUTPUT_JSON_FILENAME = "phase13-provider-roadmap-decision-checkpoint.json"
OUTPUT_MARKDOWN_FILENAME = "phase13-provider-roadmap-decision-checkpoint.md"
STRATEGY_VERDICT = "continue_provider_first_with_candidate_backends"


@dataclass(frozen=True)
class DecisionArtifactSpec:
    id: str
    category: str
    path: Path
    required: bool = True
    summary_builder: Callable[[dict[str, Any] | None], str] | None = None
    missing_action: str = "review_evidence_notes"


@dataclass(frozen=True)
class DecisionArtifact:
    id: str
    category: str
    path: str
    status: str
    summary: str
    present: bool
    required: bool
    recommended_action: str


@dataclass(frozen=True)
class DecisionFamilySpec:
    id: str
    label: str
    required_artifact_ids: list[str]
    optional_artifact_ids: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DecisionFamilyReadout:
    id: str
    label: str
    status: str
    decision: str
    summary: str
    required_artifact_ids: list[str]
    optional_artifact_ids: list[str]
    evidence_paths: list[str]
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Phase13ProviderRoadmapDecisionCheckpointReport:
    id: str
    generated_at: str
    status: str
    checkpoint_state: str
    decision: str
    summary: dict[str, Any]
    supporting_artifacts: list[DecisionArtifact]
    decision_families: list[DecisionFamilyReadout]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


REPO_FILES: dict[str, Path] = {
    "phase12b_report": Path(
        "docs/operations/candidate-backend-evaluation-readiness/"
        "phase12b-candidate-backend-evaluation-readiness.json"
    ),
    "phase12c_report": Path(
        "docs/operations/pgvector-candidate-backend-readiness/"
        "phase12c-pgvector-candidate-backend-readiness.json"
    ),
    "phase12d_report": Path(
        "docs/operations/pgvector-live-probe-readiness/"
        "phase12d-pgvector-live-probe-readiness.json"
    ),
    "phase12e_report": Path(
        "docs/operations/pgvector-local-probe-environment/"
        "phase12e-pgvector-local-probe-environment-readiness.json"
    ),
    "phase12f_report": Path(
        "docs/operations/pgvector-local-live-probe-execution/"
        "phase12f-pgvector-local-live-probe-execution-readiness.json"
    ),
    "provider_handoff_bundle": Path("docs/integration/provider-handoff/provider-handoff-bundle.json"),
    "provider_handoff_refresh": Path(
        "docs/integration/provider-handoff-refresh/provider-handoff-refresh.json"
    ),
}


SIGNAL_SPECS: list[DecisionArtifactSpec] = [
    DecisionArtifactSpec(
        id="phase12b_candidate_backend_evaluation_readiness",
        category="candidate-backend-evaluation",
        path=REPO_FILES["phase12b_report"],
        summary_builder=lambda payload: _phase12b_summary(payload),
        missing_action="regenerate_phase12b_candidate_backend_evaluation_readiness",
    ),
    DecisionArtifactSpec(
        id="phase12c_pgvector_candidate_backend_readiness",
        category="candidate-backend-evaluation",
        path=REPO_FILES["phase12c_report"],
        summary_builder=lambda payload: _phase12c_summary(payload),
        missing_action="regenerate_phase12c_pgvector_candidate_backend_readiness",
    ),
    DecisionArtifactSpec(
        id="phase12d_pgvector_live_probe_readiness",
        category="candidate-backend-evaluation",
        path=REPO_FILES["phase12d_report"],
        summary_builder=lambda payload: _phase12d_summary(payload),
        missing_action="regenerate_phase12d_pgvector_live_probe_readiness",
    ),
    DecisionArtifactSpec(
        id="phase12e_pgvector_local_probe_environment_readiness",
        category="candidate-backend-evaluation",
        path=REPO_FILES["phase12e_report"],
        summary_builder=lambda payload: _phase12e_summary(payload),
        missing_action="regenerate_phase12e_pgvector_local_probe_environment_readiness",
    ),
    DecisionArtifactSpec(
        id="phase12f_pgvector_local_live_probe_execution_readiness",
        category="candidate-backend-evaluation",
        path=REPO_FILES["phase12f_report"],
        summary_builder=lambda payload: _phase12f_summary(payload),
        missing_action="regenerate_phase12f_pgvector_local_live_probe_execution_readiness",
    ),
    DecisionArtifactSpec(
        id="provider_handoff_bundle",
        category="handoff",
        path=REPO_FILES["provider_handoff_bundle"],
        summary_builder=lambda payload: _handoff_bundle_summary(payload),
        missing_action="regenerate_provider_handoff_bundle",
    ),
    DecisionArtifactSpec(
        id="provider_handoff_refresh",
        category="handoff",
        path=REPO_FILES["provider_handoff_refresh"],
        summary_builder=lambda payload: _handoff_refresh_summary(payload),
        missing_action="regenerate_provider_handoff_refresh",
    ),
]


FAMILY_SPECS: list[DecisionFamilySpec] = [
    DecisionFamilySpec(
        id="roadmap_evidence_chain",
        label="Roadmap Evidence Chain",
        required_artifact_ids=[
            "phase12b_candidate_backend_evaluation_readiness",
            "phase12c_pgvector_candidate_backend_readiness",
            "phase12d_pgvector_live_probe_readiness",
            "phase12e_pgvector_local_probe_environment_readiness",
            "phase12f_pgvector_local_live_probe_execution_readiness",
        ],
        notes=[
            "This family keeps the next roadmap slice grounded in the full Phase 12 candidate chain instead of one local optimization loop.",
        ],
    ),
    DecisionFamilySpec(
        id="handoff_visibility",
        label="Handoff Visibility",
        required_artifact_ids=[
            "provider_handoff_bundle",
            "provider_handoff_refresh",
        ],
        notes=[
            "This family keeps the checkpoint visible in the same handoff path used by the rest of the provider evidence chain.",
        ],
    ),
]


def build_phase13_provider_roadmap_decision_checkpoint_report(
    *,
    base_dir: Path = Path("."),
) -> Phase13ProviderRoadmapDecisionCheckpointReport:
    artifacts = [_build_artifact(spec, base_dir=base_dir) for spec in SIGNAL_SPECS]
    artifact_map = {artifact.id: artifact for artifact in artifacts}
    families = [_build_family_readout(spec, artifact_map) for spec in FAMILY_SPECS]

    phase12b_status = _artifact_payload_status(base_dir, REPO_FILES["phase12b_report"])
    phase12c_status = _artifact_payload_status(base_dir, REPO_FILES["phase12c_report"])
    phase12d_status = _artifact_payload_status(base_dir, REPO_FILES["phase12d_report"])
    phase12e_status = _artifact_payload_status(base_dir, REPO_FILES["phase12e_report"])
    phase12f_status = _artifact_payload_status(base_dir, REPO_FILES["phase12f_report"])
    bundle_status = _artifact_payload_status(base_dir, REPO_FILES["provider_handoff_bundle"])
    refresh_status = _artifact_payload_status(base_dir, REPO_FILES["provider_handoff_refresh"])

    open_gate_ids = _merge_open_gate_ids(
        base_dir=base_dir,
        paths=[
            REPO_FILES["phase12b_report"],
            REPO_FILES["phase12c_report"],
            REPO_FILES["phase12d_report"],
            REPO_FILES["phase12e_report"],
            REPO_FILES["phase12f_report"],
        ],
    )

    ready_family_ids = [family.id for family in families if family.status == "ready"]
    review_ready_family_ids = [family.id for family in families if family.status == "review"]
    blocked_family_ids = [family.id for family in families if family.status == "blocked"]

    if any(artifact.required and artifact.status == "missing" for artifact in artifacts):
        status = "blocked"
        checkpoint_state = "global_checkpoint_missing_required_evidence"
        decision = "keep_current_default"
    elif phase12d_status != "ready" or phase12f_status != "ready":
        status = "review"
        checkpoint_state = "ready_for_provider_integration_hardening"
        decision = "resume_provider_integration_hardening"
    else:
        status = "ready"
        checkpoint_state = "ready_for_candidate_backends_review"
        decision = "continue_provider_first_with_candidate_backends"

    next_step_tasks = [
        "refresh_provider_integration_handoff_evidence",
        "keep_pgvector_candidate_only_and_pause_deeper_spikes",
        "rerun_phase12d_only_after_local_environment_is_ready",
    ]

    return Phase13ProviderRoadmapDecisionCheckpointReport(
        id=PHASE13_PROVIDER_ROADMAP_DECISION_CHECKPOINT_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        checkpoint_state=checkpoint_state,
        decision=decision,
        summary={
            "strategy_verdict": STRATEGY_VERDICT,
            "roadmap_focus": "resume_provider_integration_hardening",
            "candidate_backend_posture": "pause_pgvector_until_live_probe_executed",
            "phase12b_status": phase12b_status,
            "phase12c_status": phase12c_status,
            "phase12d_status": phase12d_status,
            "phase12e_status": phase12e_status,
            "phase12f_status": phase12f_status,
            "provider_handoff_bundle_status": bundle_status,
            "provider_handoff_refresh_status": refresh_status,
            "open_gate_ids": open_gate_ids,
            "ready_family_ids": ready_family_ids,
            "review_ready_family_ids": review_ready_family_ids,
            "blocked_family_ids": blocked_family_ids,
            "next_step_tasks": next_step_tasks,
        },
        supporting_artifacts=artifacts,
        decision_families=families,
        notes=[
            "This checkpoint is local and read-only evidence for the next global roadmap slice.",
            "It prefers a provider-integration hardening focus over a new pgvector-local tuning loop when live-probe evidence is still blocked or only rerun-ready.",
            "It keeps pgvector candidate-only and does not change runtime defaults or ownership boundaries.",
        ],
    )


def phase13_provider_roadmap_decision_checkpoint_report_to_dict(
    report: Phase13ProviderRoadmapDecisionCheckpointReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase13_provider_roadmap_decision_checkpoint_markdown(
    report: Phase13ProviderRoadmapDecisionCheckpointReport,
) -> str:
    lines = [
        "# Phase 13 Provider Roadmap Decision Checkpoint",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Checkpoint State: `{report.checkpoint_state}`",
        f"- Decision: `{report.decision}`",
        f"- Strategy Verdict: `{STRATEGY_VERDICT}`",
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
            "## Decision Families",
            "",
            "| Family | Status | Decision | Evidence Paths | Summary |",
            "|---|---|---|---|---|",
        ]
    )
    for family in report.decision_families:
        lines.append(
            "| "
            f"`{family.label}` | `{family.status}` | `{family.decision}` | "
            f"`{_format_value(family.evidence_paths)}` | `{family.summary}` |"
        )
    lines.extend(
        [
            "",
            "## Supporting Artifacts",
            "",
            "| Artifact | Category | Present | Status | Summary | Recommended Action |",
            "|---|---|---|---|---|---|",
        ]
    )
    for artifact in report.supporting_artifacts:
        lines.append(
            "| "
            f"`{artifact.id}` | `{artifact.category}` | `{artifact.present}` | "
            f"`{artifact.status}` | `{artifact.summary}` | "
            f"`{artifact.recommended_action}` |"
        )
    if report.notes:
        lines.extend(["", "## Notes", ""])
        for note in report.notes:
            lines.append(f"- {note}")
    return "\n".join(lines).rstrip() + "\n"


def export_phase13_provider_roadmap_decision_checkpoint_report(
    *,
    output_dir: Path = Path("docs/operations/provider-roadmap-decision-checkpoint"),
    base_dir: Path = Path("."),
) -> Phase13ProviderRoadmapDecisionCheckpointReport:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_phase13_provider_roadmap_decision_checkpoint_report(base_dir=base_dir)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    report = Phase13ProviderRoadmapDecisionCheckpointReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        checkpoint_state=report.checkpoint_state,
        decision=report.decision,
        summary=report.summary,
        supporting_artifacts=report.supporting_artifacts,
        decision_families=report.decision_families,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase13_provider_roadmap_decision_checkpoint_report_to_dict(report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase13_provider_roadmap_decision_checkpoint_markdown(report),
        encoding="utf-8",
    )
    return report


def _build_artifact(
    spec: DecisionArtifactSpec,
    *,
    base_dir: Path,
) -> DecisionArtifact:
    payload = _load_json_payload(base_dir / spec.path)
    present = payload is not None
    if payload is None:
        return DecisionArtifact(
            id=spec.id,
            category=spec.category,
            path=str(spec.path),
            status="missing",
            summary="status=missing",
            present=False,
            required=spec.required,
            recommended_action=spec.missing_action,
        )

    status = _normalize_status(payload.get("status", "review"))
    summary_builder = spec.summary_builder or (lambda current: f"status={status}")
    summary = summary_builder(payload)
    return DecisionArtifact(
        id=spec.id,
        category=spec.category,
        path=str(spec.path),
        status=status,
        summary=summary,
        present=present,
        required=spec.required,
        recommended_action=_recommended_action_for_status(status, spec.missing_action),
    )


def _build_family_readout(
    spec: DecisionFamilySpec,
    artifacts: dict[str, DecisionArtifact],
) -> DecisionFamilyReadout:
    required_statuses = [artifacts[artifact_id].status for artifact_id in spec.required_artifact_ids]
    optional_statuses = [
        artifacts[artifact_id].status for artifact_id in spec.optional_artifact_ids if artifact_id in artifacts
    ]
    if any(status == "missing" for status in required_statuses):
        status = "blocked"
        decision = "keep_current_default"
    elif any(status == "blocked" for status in required_statuses):
        status = "review"
        decision = "resume_provider_integration_hardening"
    elif any(status == "review" for status in required_statuses + optional_statuses):
        status = "review"
        decision = "resume_provider_integration_hardening"
    else:
        status = "ready"
        decision = "continue_provider_first_with_candidate_backends"

    evidence_paths = [
        artifacts[artifact_id].path for artifact_id in spec.required_artifact_ids if artifact_id in artifacts
    ]
    evidence_paths.extend(
        artifacts[artifact_id].path for artifact_id in spec.optional_artifact_ids if artifact_id in artifacts
    )
    summary = (
        f"required_ready={_count_status(required_statuses, 'ready')}/{len(required_statuses)}; "
        f"required_review={_count_status(required_statuses, 'review')}; "
        f"required_blocked={_count_status(required_statuses, 'blocked')}; "
        f"optional_review={_count_status(optional_statuses, 'review')}; "
        f"optional_blocked={_count_status(optional_statuses, 'blocked')}"
    )
    return DecisionFamilyReadout(
        id=spec.id,
        label=spec.label,
        status=status,
        decision=decision,
        summary=summary,
        required_artifact_ids=spec.required_artifact_ids,
        optional_artifact_ids=spec.optional_artifact_ids,
        evidence_paths=evidence_paths,
        notes=spec.notes,
    )


def _phase12b_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    summary = payload.get("summary", {})
    open_gate_ids = summary.get("open_gate_ids", [])
    review_ready_family_ids = summary.get("review_ready_family_ids", [])
    reference_only_family_ids = summary.get("reference_only_family_ids", [])
    return (
        f"status={_normalize_status(payload.get('status'))}; "
        f"decision={payload.get('decision', 'continue_spike')}; "
        f"strategy_verdict={_dict_value(summary, 'strategy_verdict', STRATEGY_VERDICT)}; "
        f"review_ready_families={_jsonish_list(review_ready_family_ids if isinstance(review_ready_family_ids, list) else [])}; "
        f"reference_only_families={_jsonish_list(reference_only_family_ids if isinstance(reference_only_family_ids, list) else [])}; "
        f"open_gate_count={_int_value(len(open_gate_ids) if isinstance(open_gate_ids, list) else 0, fallback=0)}"
    )


def _phase12c_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    summary = payload.get("summary", {})
    open_gate_ids = summary.get("open_gate_ids", [])
    review_ready_family_ids = summary.get("review_ready_family_ids", [])
    ready_family_ids = summary.get("ready_family_ids", [])
    blocked_family_ids = summary.get("blocked_family_ids", [])
    return (
        f"status={_normalize_status(payload.get('status'))}; "
        f"evaluation_state={payload.get('evaluation_state', 'review')}; "
        f"decision={payload.get('decision', 'continue_spike')}; "
        f"strategy_verdict={_dict_value(summary, 'strategy_verdict', STRATEGY_VERDICT)}; "
        f"pgvector_database_url_present={_bool_value(summary.get('pgvector_database_url_present', False))}; "
        f"review_ready_families={_jsonish_list(review_ready_family_ids if isinstance(review_ready_family_ids, list) else [])}; "
        f"ready_families={_jsonish_list(ready_family_ids if isinstance(ready_family_ids, list) else [])}; "
        f"blocked_families={_jsonish_list(blocked_family_ids if isinstance(blocked_family_ids, list) else [])}; "
        f"open_gate_count={_int_value(len(open_gate_ids) if isinstance(open_gate_ids, list) else 0, fallback=0)}"
    )


def _phase12d_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    summary = payload.get("summary", {})
    open_gate_ids = summary.get("open_gate_ids", [])
    review_ready_family_ids = summary.get("review_ready_family_ids", [])
    ready_family_ids = summary.get("ready_family_ids", [])
    blocked_family_ids = summary.get("blocked_family_ids", [])
    return (
        f"status={_normalize_status(payload.get('status'))}; "
        f"evaluation_state={payload.get('evaluation_state', 'review')}; "
        f"decision={payload.get('decision', 'continue_spike')}; "
        f"strategy_verdict={_dict_value(summary, 'strategy_verdict', STRATEGY_VERDICT)}; "
        f"pgvector_database_url_present={_bool_value(summary.get('pgvector_database_url_present', False))}; "
        f"pgvector_driver_available={_bool_value(summary.get('pgvector_driver_available', False))}; "
        f"review_ready_families={_jsonish_list(review_ready_family_ids if isinstance(review_ready_family_ids, list) else [])}; "
        f"ready_families={_jsonish_list(ready_family_ids if isinstance(ready_family_ids, list) else [])}; "
        f"blocked_families={_jsonish_list(blocked_family_ids if isinstance(blocked_family_ids, list) else [])}; "
        f"open_gate_count={_int_value(len(open_gate_ids) if isinstance(open_gate_ids, list) else 0, fallback=0)}"
    )


def _phase12e_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    summary = payload.get("summary", {})
    open_gate_ids = summary.get("open_gate_ids", [])
    ready_family_ids = summary.get("ready_family_ids", [])
    review_ready_family_ids = summary.get("review_ready_family_ids", [])
    blocked_family_ids = summary.get("blocked_family_ids", [])
    return (
        f"status={_normalize_status(payload.get('status'))}; "
        f"evaluation_state={payload.get('evaluation_state', 'review')}; "
        f"decision={payload.get('decision', 'continue_spike')}; "
        f"strategy_verdict={_dict_value(summary, 'strategy_verdict', STRATEGY_VERDICT)}; "
        f"phase12d_report_status={_dict_value(summary, 'phase12d_report_status', 'missing')}; "
        f"optional_dependency_present={_bool_value(summary.get('optional_dependency_present', False))}; "
        f"ready_families={_jsonish_list(ready_family_ids if isinstance(ready_family_ids, list) else [])}; "
        f"review_ready_families={_jsonish_list(review_ready_family_ids if isinstance(review_ready_family_ids, list) else [])}; "
        f"blocked_families={_jsonish_list(blocked_family_ids if isinstance(blocked_family_ids, list) else [])}; "
        f"open_gate_count={_int_value(len(open_gate_ids) if isinstance(open_gate_ids, list) else 0, fallback=0)}"
    )


def _phase12f_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    summary = payload.get("summary", {})
    open_gate_ids = summary.get("open_gate_ids", [])
    ready_family_ids = summary.get("ready_family_ids", [])
    review_ready_family_ids = summary.get("review_ready_family_ids", [])
    blocked_family_ids = summary.get("blocked_family_ids", [])
    return (
        f"status={_normalize_status(payload.get('status'))}; "
        f"execution_state={payload.get('execution_state', 'review')}; "
        f"decision={payload.get('decision', 'continue_spike')}; "
        f"strategy_verdict={_dict_value(summary, 'strategy_verdict', STRATEGY_VERDICT)}; "
        f"phase12e_environment_status={_dict_value(summary, 'phase12e_environment_status', 'missing')}; "
        f"phase12d_live_probe_status={_dict_value(summary, 'phase12d_live_probe_status', 'missing')}; "
        f"rerun_required={_bool_value(summary.get('rerun_required', False))}; "
        f"ready_families={_jsonish_list(ready_family_ids if isinstance(ready_family_ids, list) else [])}; "
        f"review_ready_families={_jsonish_list(review_ready_family_ids if isinstance(review_ready_family_ids, list) else [])}; "
        f"blocked_families={_jsonish_list(blocked_family_ids if isinstance(blocked_family_ids, list) else [])}; "
        f"open_gate_count={_int_value(len(open_gate_ids) if isinstance(open_gate_ids, list) else 0, fallback=0)}"
    )


def _handoff_bundle_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    evidence_artifacts = payload.get("evidence_artifacts", [])
    evidence_artifacts_count = len(evidence_artifacts) if isinstance(evidence_artifacts, list) else 0
    phase13_present = _artifact_present(evidence_artifacts, "phase13_provider_roadmap_decision_checkpoint")
    return (
        f"status={_normalize_status(payload.get('status'))}; "
        f"decision={payload.get('decision', 'review_evidence_notes')}; "
        f"evidence_artifacts={evidence_artifacts_count}; "
        f"phase13_present={_bool_value(phase13_present)}"
    )


def _handoff_refresh_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=missing"
    steps = payload.get("steps", [])
    steps_count = len(steps) if isinstance(steps, list) else 0
    phase13_present = _artifact_present(steps, "phase13_provider_roadmap_decision_checkpoint")
    return (
        f"status={_normalize_status(payload.get('status'))}; "
        f"decision={payload.get('decision', 'review_evidence_notes')}; "
        f"steps={steps_count}; "
        f"phase13_present={_bool_value(phase13_present)}"
    )


def _artifact_present(items: Any, artifact_id: str) -> bool:
    if not isinstance(items, list):
        return False
    return any(isinstance(item, dict) and item.get("id") == artifact_id for item in items)


def _merge_open_gate_ids(*, base_dir: Path, paths: list[Path]) -> list[str]:
    gate_ids: list[str] = []
    for path in paths:
        payload = _load_json_payload(base_dir / path)
        if not isinstance(payload, dict):
            continue
        summary = payload.get("summary", {})
        if not isinstance(summary, dict):
            continue
        open_gates = summary.get("open_gate_ids", [])
        if isinstance(open_gates, list):
            for gate in open_gates:
                if isinstance(gate, str) and gate not in gate_ids:
                    gate_ids.append(gate)
    return gate_ids


def _artifact_payload_status(base_dir: Path, path: Path) -> str:
    payload = _load_json_payload(base_dir / path)
    if not isinstance(payload, dict):
        return "missing"
    return _normalize_status(payload.get("status", "review"))


def _load_json_payload(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if isinstance(payload, dict):
        return payload
    return None


def _normalize_status(value: Any) -> str:
    if isinstance(value, str) and value in {"ready", "review", "blocked"}:
        return value
    return "review"


def _recommended_action_for_status(status: str, missing_action: str) -> str:
    if status == "ready":
        return "no_action_required"
    if status == "blocked":
        return "resolve_failed_evidence"
    return "review_evidence_notes"


def _count_status(statuses: list[str], target: str) -> int:
    return sum(1 for status in statuses if status == target)


def _bool_value(value: Any) -> str:
    return "True" if bool(value) else "False"


def _int_value(value: Any, fallback: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _jsonish_list(items: list[Any]) -> str:
    values = [str(item) for item in items]
    return "[" + ", ".join(f'"{item}"' for item in values) + "]"


def _dict_value(payload: dict[str, Any], key: str, default: Any) -> Any:
    value = payload.get(key, default)
    return value if value is not None else default


def _format_value(value: Any) -> str:
    if isinstance(value, list):
        return _jsonish_list(value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
