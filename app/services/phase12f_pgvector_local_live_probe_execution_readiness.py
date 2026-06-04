import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable


PHASE12F_PGVECTOR_LOCAL_LIVE_PROBE_EXECUTION_READINESS_ID = (
    "phase12f-pgvector-local-live-probe-execution-readiness-v1"
)
OUTPUT_JSON_FILENAME = "phase12f-pgvector-local-live-probe-execution-readiness.json"
OUTPUT_MARKDOWN_FILENAME = "phase12f-pgvector-local-live-probe-execution-readiness.md"
STRATEGY_VERDICT = "continue_provider_first_with_candidate_backends"


@dataclass(frozen=True)
class ExecutionArtifactSpec:
    id: str
    category: str
    path: Path
    required: bool = True
    summary_builder: Callable[[dict[str, Any] | None], str] | None = None
    missing_action: str = "review_evidence_notes"


@dataclass(frozen=True)
class ExecutionArtifact:
    id: str
    category: str
    path: str
    status: str
    summary: str
    present: bool
    required: bool
    recommended_action: str


@dataclass(frozen=True)
class ExecutionFamilySpec:
    id: str
    label: str
    required_artifact_ids: list[str]
    optional_artifact_ids: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ExecutionFamilyReadout:
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
class Phase12fPgvectorLocalLiveProbeExecutionReadinessReport:
    id: str
    generated_at: str
    status: str
    execution_state: str
    decision: str
    summary: dict[str, Any]
    supporting_artifacts: list[ExecutionArtifact]
    execution_families: list[ExecutionFamilyReadout]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


REPO_FILES: dict[str, Path] = {
    "phase12e_report": Path(
        "docs/operations/pgvector-local-probe-environment/"
        "phase12e-pgvector-local-probe-environment-readiness.json"
    ),
    "phase12d_report": Path(
        "docs/operations/pgvector-live-probe-readiness/"
        "phase12d-pgvector-live-probe-readiness.json"
    ),
    "runbook": Path(
        "docs/operations/pgvector-local-live-probe-execution/runbook.md"
    ),
    "provider_handoff_bundle": Path("docs/integration/provider-handoff/provider-handoff-bundle.json"),
    "provider_handoff_refresh": Path(
        "docs/integration/provider-handoff-refresh/provider-handoff-refresh.json"
    ),
}


SIGNAL_SPECS: list[ExecutionArtifactSpec] = [
    ExecutionArtifactSpec(
        id="phase12e_environment_readiness_report",
        category="bridge-evidence",
        path=REPO_FILES["phase12e_report"],
        summary_builder=lambda payload: _phase12e_report_summary(payload),
        missing_action="regenerate_phase12e_pgvector_local_probe_environment_readiness",
    ),
    ExecutionArtifactSpec(
        id="phase12d_live_probe_readiness_report",
        category="bridge-evidence",
        path=REPO_FILES["phase12d_report"],
        summary_builder=lambda payload: _phase12d_report_summary(payload),
        missing_action="regenerate_phase12d_pgvector_live_probe_readiness",
    ),
    ExecutionArtifactSpec(
        id="runbook",
        category="docs",
        path=REPO_FILES["runbook"],
        summary_builder=lambda payload: (
            "status=ready; rerun_target=phase12d_pgvector_live_probe_readiness; "
            "scope=local_live_probe_execution"
        ),
        missing_action="add_pgvector_local_live_probe_execution_runbook",
    ),
    ExecutionArtifactSpec(
        id="provider_handoff_bundle_visibility",
        category="handoff",
        path=REPO_FILES["provider_handoff_bundle"],
        summary_builder=lambda payload: _handoff_bundle_summary(payload),
        missing_action="regenerate_provider_handoff_bundle",
    ),
    ExecutionArtifactSpec(
        id="provider_handoff_refresh_visibility",
        category="handoff",
        path=REPO_FILES["provider_handoff_refresh"],
        summary_builder=lambda payload: _handoff_refresh_summary(payload),
        missing_action="regenerate_provider_handoff_refresh",
    ),
]


FAMILY_SPECS: list[ExecutionFamilySpec] = [
    ExecutionFamilySpec(
        id="pgvector_local_execution_pack",
        label="PGVector Local Execution Pack",
        required_artifact_ids=[
            "phase12e_environment_readiness_report",
            "phase12d_live_probe_readiness_report",
            "runbook",
        ],
        notes=[
            "This family keeps the rerun path explicit and local before any retrieval evidence is interpreted.",
        ],
    ),
    ExecutionFamilySpec(
        id="pgvector_handoff_bridge",
        label="PGVector Handoff Bridge",
        required_artifact_ids=[
            "provider_handoff_bundle_visibility",
            "provider_handoff_refresh_visibility",
        ],
        notes=[
            "This family keeps the execution-readiness artifact visible in the same handoff chain used by earlier phases.",
        ],
    ),
]


def build_phase12f_pgvector_local_live_probe_execution_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase12fPgvectorLocalLiveProbeExecutionReadinessReport:
    artifacts = [_build_artifact(spec, base_dir=base_dir) for spec in SIGNAL_SPECS]
    artifact_map = {artifact.id: artifact for artifact in artifacts}
    families = [_build_family_readout(spec, artifact_map) for spec in FAMILY_SPECS]

    phase12e_status = _phase12e_report_status(base_dir)
    phase12d_status = _phase12d_report_status(base_dir)

    open_gate_ids: list[str] = []
    if phase12e_status != "ready":
        open_gate_ids.append("phase12e_environment_readiness_report")
    if phase12d_status != "ready":
        open_gate_ids.append("phase12d_live_probe_readiness_report")

    ready_family_ids = [family.id for family in families if family.status == "ready"]
    review_ready_family_ids = [family.id for family in families if family.status == "review"]
    blocked_family_ids = [family.id for family in families if family.status == "blocked"]

    if any(artifact.required and artifact.status == "blocked" for artifact in artifacts):
        status = "blocked"
        execution_state = "local_execution_blocked"
        decision = "keep_current_default"
    elif phase12e_status != "ready":
        status = "blocked"
        execution_state = "local_execution_blocked"
        decision = "keep_current_default"
    elif phase12d_status == "ready":
        status = "ready"
        execution_state = "local_live_probe_rerun_complete"
        decision = "continue_spike"
    else:
        status = "review"
        execution_state = "ready_for_local_live_probe_rerun"
        decision = "continue_spike"

    return Phase12fPgvectorLocalLiveProbeExecutionReadinessReport(
        id=PHASE12F_PGVECTOR_LOCAL_LIVE_PROBE_EXECUTION_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        execution_state=execution_state,
        decision=decision,
        summary={
            "strategy_verdict": STRATEGY_VERDICT,
            "candidate_backend_id": "pgvector",
            "candidate_backend_kind": "postgresql_native_vector_search_local_live_probe_execution",
            "phase12e_environment_status": phase12e_status,
            "phase12d_live_probe_status": phase12d_status,
            "execution_state": execution_state,
            "rerun_target": "python scripts/export_phase12d_pgvector_live_probe_readiness.py",
            "execution_ready": phase12e_status == "ready",
            "rerun_required": phase12d_status != "ready",
            "open_gate_ids": open_gate_ids,
            "ready_family_ids": ready_family_ids,
            "review_ready_family_ids": review_ready_family_ids,
            "blocked_family_ids": blocked_family_ids,
        },
        supporting_artifacts=artifacts,
        execution_families=families,
        notes=[
            "This report is local and read-only evidence for the optional live probe rerun path.",
            "It packages the developer-owned execution path needed to rerun Phase 12d without promoting pgvector to a runtime default.",
            "Phase 12d may remain blocked until the local execution path is applied and the live probe is refreshed again.",
        ],
    )


def phase12f_pgvector_local_live_probe_execution_readiness_report_to_dict(
    report: Phase12fPgvectorLocalLiveProbeExecutionReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase12f_pgvector_local_live_probe_execution_readiness_markdown(
    report: Phase12fPgvectorLocalLiveProbeExecutionReadinessReport,
) -> str:
    lines = [
        "# Phase 12f PGVector Local Live Probe Execution Readiness",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Execution State: `{report.execution_state}`",
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
        rendered = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
        lines.append(f"| {key} | `{rendered}` |")

    lines.extend(
        [
            "",
            "## Execution Families",
            "",
            "| Family | Status | Decision | Evidence Paths | Notes |",
            "|---|---|---|---|---|",
        ]
    )
    for family in report.execution_families:
        evidence_paths = _jsonish_list(family.evidence_paths)
        notes = _jsonish_list(family.notes)
        lines.append(
            f"| `{family.label}` | `{family.status}` | `{family.decision}` | {evidence_paths} | {notes} |"
        )

    lines.extend(
        [
            "",
            "## Supporting Artifacts",
            "",
            "| Artifact | Category | Status | Summary | Recommended Action |",
            "|---|---|---|---|---|",
        ]
    )
    for artifact in report.supporting_artifacts:
        lines.append(
            f"| `{artifact.id}` | `{artifact.category}` | `{artifact.status}` | "
            f"{artifact.summary} | `{artifact.recommended_action}` |"
        )

    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase12f_pgvector_local_live_probe_execution_readiness_report(
    output_dir: Path = Path("docs/operations/pgvector-local-live-probe-execution"),
    *,
    base_dir: Path = Path("."),
) -> Phase12fPgvectorLocalLiveProbeExecutionReadinessReport:
    report = build_phase12f_pgvector_local_live_probe_execution_readiness_report(
        base_dir=base_dir
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = Phase12fPgvectorLocalLiveProbeExecutionReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        execution_state=report.execution_state,
        decision=report.decision,
        summary=report.summary,
        supporting_artifacts=report.supporting_artifacts,
        execution_families=report.execution_families,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase12f_pgvector_local_live_probe_execution_readiness_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase12f_pgvector_local_live_probe_execution_readiness_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _build_artifact(
    spec: ExecutionArtifactSpec,
    *,
    base_dir: Path,
) -> ExecutionArtifact:
    path = base_dir / spec.path
    if not path.exists():
        return ExecutionArtifact(
            id=spec.id,
            category=spec.category,
            path=str(spec.path.as_posix()),
            status="blocked",
            summary=f"missing_local_evidence={spec.path.as_posix()}",
            present=False,
            required=spec.required,
            recommended_action=spec.missing_action,
        )
    payload = _read_content_if_present(path)
    summary_builder = spec.summary_builder
    summary = summary_builder(payload) if summary_builder is not None else "status=ready"
    return ExecutionArtifact(
        id=spec.id,
        category=spec.category,
        path=str(spec.path.as_posix()),
        status="ready",
        summary=summary,
        present=True,
        required=spec.required,
        recommended_action="no_action_required",
    )


def _build_family_readout(
    spec: ExecutionFamilySpec,
    artifact_map: dict[str, ExecutionArtifact],
) -> ExecutionFamilyReadout:
    required_artifacts = [artifact_map[artifact_id] for artifact_id in spec.required_artifact_ids]
    optional_artifacts = [
        artifact_map[artifact_id]
        for artifact_id in spec.optional_artifact_ids
        if artifact_id in artifact_map
    ]
    if any(artifact.status == "blocked" for artifact in required_artifacts):
        status = "blocked"
        decision = "keep_current_default"
    elif any(artifact.status == "review" for artifact in required_artifacts):
        status = "review"
        decision = "continue_spike"
    elif any(artifact.status == "review" for artifact in optional_artifacts):
        status = "review"
        decision = "continue_spike"
    else:
        status = "ready"
        decision = "continue_spike"
    evidence_paths = [artifact.path for artifact in required_artifacts + optional_artifacts]
    return ExecutionFamilyReadout(
        id=spec.id,
        label=spec.label,
        status=status,
        decision=decision,
        summary=_family_summary(required_artifacts, optional_artifacts),
        required_artifact_ids=spec.required_artifact_ids,
        optional_artifact_ids=spec.optional_artifact_ids,
        evidence_paths=evidence_paths,
        notes=spec.notes,
    )


def _family_summary(
    required_artifacts: list[ExecutionArtifact],
    optional_artifacts: list[ExecutionArtifact],
) -> str:
    required_ready = sum(1 for artifact in required_artifacts if artifact.status == "ready")
    required_total = len(required_artifacts)
    optional_open = sum(
        1 for artifact in optional_artifacts if artifact.status in {"review", "blocked"}
    )
    return (
        f"required_ready={required_ready}/{required_total}; "
        f"optional_open={optional_open}; "
        f"required_ids={_jsonish_list([artifact.id for artifact in required_artifacts])}"
    )


def _phase12e_report_summary(payload: dict[str, Any] | None) -> str:
    if payload is None:
        return "status=blocked; phase12e_report_missing"
    status = payload.get("status", "review") if isinstance(payload, dict) else "review"
    decision = payload.get("decision", "continue_spike") if isinstance(payload, dict) else "continue_spike"
    return f"status=ready; phase12e_report_status={status}; phase12e_decision={decision}"


def _phase12d_report_summary(payload: dict[str, Any] | None) -> str:
    if payload is None:
        return "status=blocked; phase12d_report_missing"
    status = payload.get("status", "review") if isinstance(payload, dict) else "review"
    decision = payload.get("decision", "continue_spike") if isinstance(payload, dict) else "continue_spike"
    summary = payload.get("summary", {}) if isinstance(payload, dict) else {}
    return (
        f"status=ready; phase12d_report_status={status}; phase12d_decision={decision}; "
        f"phase12d_connection_status={summary.get('pgvector_connection_status', 'unknown')}"
    )


def _handoff_bundle_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=blocked; handoff_bundle_missing"
    evidence_artifacts = payload.get("evidence_artifacts", [])
    present = any(
        isinstance(item, dict)
        and item.get("id") == "phase12f_pgvector_local_live_probe_execution_readiness"
        for item in evidence_artifacts
    )
    return f"status={'ready' if present else 'blocked'}; phase12f_visible={present}"


def _handoff_refresh_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=blocked; handoff_refresh_missing"
    steps = payload.get("steps", [])
    present = any(
        isinstance(item, dict)
        and item.get("id") == "phase12f_pgvector_local_live_probe_execution_readiness"
        for item in steps
    )
    return f"status={'ready' if present else 'blocked'}; phase12f_visible={present}"


def _phase12e_report_status(base_dir: Path) -> str:
    payload = _read_json_if_present(base_dir / REPO_FILES["phase12e_report"])
    if not isinstance(payload, dict):
        return "missing"
    return str(payload.get("status", "review"))


def _phase12d_report_status(base_dir: Path) -> str:
    payload = _read_json_if_present(base_dir / REPO_FILES["phase12d_report"])
    if not isinstance(payload, dict):
        return "missing"
    return str(payload.get("status", "review"))


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _read_content_if_present(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    return {"text": path.read_text(encoding="utf-8")}


def _jsonish_list(values: list[Any]) -> str:
    return json.dumps(values, ensure_ascii=False)
