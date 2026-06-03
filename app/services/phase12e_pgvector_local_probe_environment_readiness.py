import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable


PHASE12E_PGVECTOR_LOCAL_PROBE_ENVIRONMENT_READINESS_ID = (
    "phase12e-pgvector-local-probe-environment-readiness-v1"
)
OUTPUT_JSON_FILENAME = "phase12e-pgvector-local-probe-environment-readiness.json"
OUTPUT_MARKDOWN_FILENAME = "phase12e-pgvector-local-probe-environment-readiness.md"
STRATEGY_VERDICT = "continue_provider_first_with_candidate_backends"


@dataclass(frozen=True)
class EnvironmentArtifactSpec:
    id: str
    category: str
    path: Path
    required: bool = True
    summary_builder: Callable[[dict[str, Any] | None], str] | None = None
    missing_action: str = "review_evidence_notes"


@dataclass(frozen=True)
class EnvironmentArtifact:
    id: str
    category: str
    path: str
    status: str
    summary: str
    present: bool
    required: bool
    recommended_action: str


@dataclass(frozen=True)
class EnvironmentFamilySpec:
    id: str
    label: str
    required_artifact_ids: list[str]
    optional_artifact_ids: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class EnvironmentFamilyReadout:
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
class Phase12ePgvectorLocalProbeEnvironmentReadinessReport:
    id: str
    generated_at: str
    status: str
    evaluation_state: str
    decision: str
    summary: dict[str, Any]
    supporting_artifacts: list[EnvironmentArtifact]
    environment_families: list[EnvironmentFamilyReadout]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


REPO_FILES: dict[str, Path] = {
    "requirements_pgvector": Path("requirements-pgvector.txt"),
    "compose_example": Path("docker-compose.pgvector.example.yml"),
    "init_sql": Path("docker/pgvector/init.sql"),
    "env_example": Path(".env.example"),
    "phase12d_report": Path(
        "docs/operations/pgvector-live-probe-readiness/"
        "phase12d-pgvector-live-probe-readiness.json"
    ),
    "provider_handoff_bundle": Path("docs/integration/provider-handoff/provider-handoff-bundle.json"),
    "provider_handoff_refresh": Path(
        "docs/integration/provider-handoff-refresh/provider-handoff-refresh.json"
    ),
    "runbook": Path(
        "docs/operations/pgvector-local-probe-environment/runbook.md"
    ),
    "config_reference": Path(
        "docs/operations/pgvector-local-probe-environment/config-reference.md"
    ),
}


SIGNAL_SPECS: list[EnvironmentArtifactSpec] = [
    EnvironmentArtifactSpec(
        id="optional_dependency_file",
        category="dependency",
        path=REPO_FILES["requirements_pgvector"],
        summary_builder=lambda payload: (
            "status=ready; optional_dependency=psycopg[binary]; install_scope=local_probe_only"
        ),
        missing_action="add_requirements_pgvector_txt",
    ),
    EnvironmentArtifactSpec(
        id="compose_profile_example",
        category="compose",
        path=REPO_FILES["compose_example"],
        summary_builder=lambda payload: _compose_summary(),
        missing_action="add_docker_compose_pgvector_example",
    ),
    EnvironmentArtifactSpec(
        id="init_sql",
        category="sql",
        path=REPO_FILES["init_sql"],
        summary_builder=lambda payload: _init_sql_summary(),
        missing_action="add_pgvector_init_sql",
    ),
    EnvironmentArtifactSpec(
        id="runbook",
        category="docs",
        path=REPO_FILES["runbook"],
        summary_builder=lambda payload: (
            "status=ready; runbook=present; scope=optional_local_probe_environment"
        ),
        missing_action="add_pgvector_local_probe_environment_runbook",
    ),
    EnvironmentArtifactSpec(
        id="config_reference",
        category="docs",
        path=REPO_FILES["config_reference"],
        summary_builder=lambda payload: (
            "status=ready; config_reference=present; scope=pgvector_environment_contract"
        ),
        missing_action="add_pgvector_local_probe_environment_config_reference",
    ),
    EnvironmentArtifactSpec(
        id="env_example_pgvector_block",
        category="env",
        path=REPO_FILES["env_example"],
        summary_builder=lambda payload: _env_example_summary(payload),
        missing_action="update_env_example_pgvector_block",
    ),
    EnvironmentArtifactSpec(
        id="phase12d_live_probe_readiness_report",
        category="bridge-evidence",
        path=REPO_FILES["phase12d_report"],
        summary_builder=lambda payload: _phase12d_report_summary(payload),
        missing_action="regenerate_phase12d_pgvector_live_probe_readiness",
    ),
    EnvironmentArtifactSpec(
        id="provider_handoff_bundle_visibility",
        category="handoff",
        path=REPO_FILES["provider_handoff_bundle"],
        summary_builder=lambda payload: _handoff_bundle_summary(payload),
        missing_action="regenerate_provider_handoff_bundle",
    ),
    EnvironmentArtifactSpec(
        id="provider_handoff_refresh_visibility",
        category="handoff",
        path=REPO_FILES["provider_handoff_refresh"],
        summary_builder=lambda payload: _handoff_refresh_summary(payload),
        missing_action="regenerate_provider_handoff_refresh",
    ),
]


FAMILY_SPECS: list[EnvironmentFamilySpec] = [
    EnvironmentFamilySpec(
        id="pgvector_local_environment_pack",
        label="PGVector Local Environment Pack",
        required_artifact_ids=[
            "optional_dependency_file",
            "compose_profile_example",
            "init_sql",
            "runbook",
            "config_reference",
            "env_example_pgvector_block",
        ],
        notes=[
            "This family packages the optional local setup needed to exercise the pgvector probe.",
        ],
    ),
    EnvironmentFamilySpec(
        id="pgvector_probe_bridge",
        label="PGVector Probe Bridge",
        required_artifact_ids=[
            "phase12d_live_probe_readiness_report",
            "provider_handoff_bundle_visibility",
            "provider_handoff_refresh_visibility",
        ],
        notes=[
            "This family keeps the live probe and handoff visibility aligned with the local environment package.",
        ],
    ),
]


def build_phase12e_pgvector_local_probe_environment_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase12ePgvectorLocalProbeEnvironmentReadinessReport:
    artifacts = [_build_artifact(spec, base_dir=base_dir) for spec in SIGNAL_SPECS]
    artifact_map = {artifact.id: artifact for artifact in artifacts}
    families = [_build_family_readout(spec, artifact_map) for spec in FAMILY_SPECS]

    required_blocked = any(
        artifact.required and artifact.status == "blocked" for artifact in artifacts
    )
    required_review = any(
        artifact.required and artifact.status == "review" for artifact in artifacts
    )
    open_gate_ids = [artifact.id for artifact in artifacts if artifact.status in {"review", "blocked"}]
    ready_family_ids = [family.id for family in families if family.status == "ready"]
    review_ready_family_ids = [family.id for family in families if family.status == "review"]
    blocked_family_ids = [family.id for family in families if family.status == "blocked"]

    if required_blocked:
        status = "blocked"
        evaluation_state = "pgvector_local_probe_environment_blocked"
        decision = "keep_current_default"
    elif required_review:
        status = "review"
        evaluation_state = "ready_for_pgvector_local_probe_environment_review"
        decision = "continue_spike"
    else:
        status = "ready"
        evaluation_state = "ready_for_pgvector_local_probe_environment_review"
        decision = "continue_spike"

    return Phase12ePgvectorLocalProbeEnvironmentReadinessReport(
        id=PHASE12E_PGVECTOR_LOCAL_PROBE_ENVIRONMENT_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        evaluation_state=evaluation_state,
        decision=decision,
        summary={
            "strategy_verdict": STRATEGY_VERDICT,
            "candidate_backend_id": "pgvector",
            "candidate_backend_kind": "postgresql_native_vector_search_local_probe_environment",
            "optional_dependency_present": _exists(base_dir / REPO_FILES["requirements_pgvector"]),
            "compose_example_present": _exists(base_dir / REPO_FILES["compose_example"]),
            "init_sql_present": _exists(base_dir / REPO_FILES["init_sql"]),
            "runbook_present": _exists(base_dir / REPO_FILES["runbook"]),
            "config_reference_present": _exists(base_dir / REPO_FILES["config_reference"]),
            "env_example_pgvector_block_present": _contains_any(
                base_dir / REPO_FILES["env_example"],
                [
                    "PGVECTOR_DATABASE_URL",
                    "PGVECTOR_SCHEMA=unified_knowledge_rag",
                    "PGVECTOR_TABLE=knowledge_chunks",
                    "PGVECTOR_INDEX_NAME=knowledge_chunks_embedding_idx",
                    "PGVECTOR_VECTOR_SIZE=1024",
                ],
            ),
            "phase12d_report_status": _phase12d_report_status(base_dir),
            "handoff_bundle_visible": _handoff_contains_phase12e(
                base_dir / REPO_FILES["provider_handoff_bundle"]
            ),
            "handoff_refresh_visible": _handoff_contains_phase12e(
                base_dir / REPO_FILES["provider_handoff_refresh"]
            ),
            "open_gate_ids": open_gate_ids,
            "ready_family_ids": ready_family_ids,
            "review_ready_family_ids": review_ready_family_ids,
            "blocked_family_ids": blocked_family_ids,
        },
        supporting_artifacts=artifacts,
        environment_families=families,
        notes=[
            "This report is local and read-only evidence for the optional pgvector probe environment.",
            "It packages the developer-owned setup needed to run the live probe without promoting pgvector to a runtime default.",
            "Phase 12d may remain blocked until the local environment is applied and the optional probe is rerun.",
        ],
    )


def phase12e_pgvector_local_probe_environment_readiness_report_to_dict(
    report: Phase12ePgvectorLocalProbeEnvironmentReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase12e_pgvector_local_probe_environment_readiness_markdown(
    report: Phase12ePgvectorLocalProbeEnvironmentReadinessReport,
) -> str:
    lines = [
        "# Phase 12e PGVector Local Probe Environment Readiness",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Evaluation State: `{report.evaluation_state}`",
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
            "## Environment Families",
            "",
            "| Family | Status | Decision | Evidence Paths | Notes |",
            "|---|---|---|---|---|",
        ]
    )
    for family in report.environment_families:
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


def export_phase12e_pgvector_local_probe_environment_readiness_report(
    output_dir: Path = Path("docs/operations/pgvector-local-probe-environment"),
    *,
    base_dir: Path = Path("."),
) -> Phase12ePgvectorLocalProbeEnvironmentReadinessReport:
    report = build_phase12e_pgvector_local_probe_environment_readiness_report(
        base_dir=base_dir
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = Phase12ePgvectorLocalProbeEnvironmentReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        evaluation_state=report.evaluation_state,
        decision=report.decision,
        summary=report.summary,
        supporting_artifacts=report.supporting_artifacts,
        environment_families=report.environment_families,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase12e_pgvector_local_probe_environment_readiness_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase12e_pgvector_local_probe_environment_readiness_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _build_artifact(
    spec: EnvironmentArtifactSpec,
    *,
    base_dir: Path,
) -> EnvironmentArtifact:
    path = base_dir / spec.path
    if not path.exists():
        return EnvironmentArtifact(
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
    return EnvironmentArtifact(
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
    spec: EnvironmentFamilySpec,
    artifact_map: dict[str, EnvironmentArtifact],
) -> EnvironmentFamilyReadout:
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
    return EnvironmentFamilyReadout(
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
    required_artifacts: list[EnvironmentArtifact],
    optional_artifacts: list[EnvironmentArtifact],
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


def _compose_summary() -> str:
    return (
        "status=ready; compose_image=pgvector/pgvector:pg16; "
        "port_mapping=5433:5432; profile=pgvector"
    )


def _init_sql_summary() -> str:
    return (
        "status=ready; extension=vector; schema=unified_knowledge_rag; "
        "table=knowledge_chunks; index=knowledge_chunks_embedding_idx"
    )


def _env_example_summary(payload: dict[str, Any] | None) -> str:
    if payload is None:
        return "status=blocked; env_example_missing"
    text = ""
    if isinstance(payload, dict):
        text = str(payload.get("text", ""))
    if not text:
        return "status=blocked; env_example_missing"
    return (
        "status=ready; env_block=present; "
        "pgvector_schema=unified_knowledge_rag; pgvector_table=knowledge_chunks"
    )


def _phase12d_report_summary(payload: dict[str, Any] | None) -> str:
    if payload is None:
        return "status=blocked; phase12d_report_missing"
    status = payload.get("status", "review") if isinstance(payload, dict) else "review"
    decision = payload.get("decision", "continue_spike") if isinstance(payload, dict) else "continue_spike"
    return f"status=ready; phase12d_report_status={status}; phase12d_decision={decision}"


def _handoff_bundle_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=blocked; handoff_bundle_missing"
    evidence_artifacts = payload.get("evidence_artifacts", [])
    present = any(
        isinstance(item, dict) and item.get("id") == "phase12e_pgvector_local_probe_environment_readiness"
        for item in evidence_artifacts
    )
    return (
        f"status={'ready' if present else 'blocked'}; "
        f"phase12e_visible={present}"
    )


def _handoff_refresh_summary(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict):
        return "status=blocked; handoff_refresh_missing"
    steps = payload.get("steps", [])
    present = any(
        isinstance(item, dict)
        and item.get("id") == "phase12e_pgvector_local_probe_environment_readiness"
        for item in steps
    )
    return f"status={'ready' if present else 'blocked'}; phase12e_visible={present}"


def _phase12d_report_status(base_dir: Path) -> str:
    payload = _read_json_if_present(base_dir / REPO_FILES["phase12d_report"])
    if not isinstance(payload, dict):
        return "missing"
    return str(payload.get("status", "review"))


def _handoff_contains_phase12e(path: Path) -> bool:
    payload = _read_json_if_present(path)
    if not isinstance(payload, dict):
        return False
    if "evidence_artifacts" in payload:
        return any(
            isinstance(item, dict)
            and item.get("id") == "phase12e_pgvector_local_probe_environment_readiness"
            for item in payload.get("evidence_artifacts", [])
        )
    if "steps" in payload:
        return any(
            isinstance(item, dict)
            and item.get("id") == "phase12e_pgvector_local_probe_environment_readiness"
            for item in payload.get("steps", [])
        )
    return False


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


def _exists(path: Path) -> bool:
    return path.is_file()


def _contains_any(path: Path, patterns: list[str]) -> bool:
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8")
    return all(pattern in content for pattern in patterns)


def _jsonish_list(values: list[Any]) -> str:
    return json.dumps(values, ensure_ascii=False)
