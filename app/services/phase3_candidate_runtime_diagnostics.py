import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.config import Settings, get_settings


PHASE3_CANDIDATE_RUNTIME_DIAGNOSTICS_ID = "phase3-candidate-runtime-diagnostics-v1"
PHASE3_READINESS_PATH = Path(
    "docs/benchmark/chinese-seed/retrieval-promotion-readiness/"
    "phase3-retrieval-promotion-readiness.json"
)
DEPLOYED_SMOKE_PATH = Path(
    "docs/integration/deployed-provider-smoke/deployed-provider-smoke.json"
)


@dataclass(frozen=True)
class Phase3RuntimePrerequisite:
    id: str
    status: str
    summary: str
    recommended_action: str
    evidence_path: str | None = None


@dataclass(frozen=True)
class Phase3CandidateRuntimeDiagnosticsReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    runtime_config: dict[str, Any]
    model_artifacts: dict[str, Any]
    prerequisites: list[Phase3RuntimePrerequisite]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase3_candidate_runtime_diagnostics_report(
    settings: Settings | None = None,
    *,
    base_dir: Path = Path("."),
) -> Phase3CandidateRuntimeDiagnosticsReport:
    settings = settings or get_settings()
    runtime_config = _runtime_config(settings)
    model_artifacts = _model_artifact_status(settings)
    readiness_payload = _read_json_if_present(base_dir / PHASE3_READINESS_PATH)
    deployed_smoke_payload = _read_json_if_present(base_dir / DEPLOYED_SMOKE_PATH)
    prerequisites = _build_prerequisites(
        settings=settings,
        model_artifacts=model_artifacts,
        readiness_payload=readiness_payload,
        deployed_smoke_payload=deployed_smoke_payload,
    )
    summary = _summary(prerequisites)
    return Phase3CandidateRuntimeDiagnosticsReport(
        id=PHASE3_CANDIDATE_RUNTIME_DIAGNOSTICS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=_overall_status(prerequisites),
        decision="keep_runtime_defaults",
        summary=summary,
        runtime_config=runtime_config,
        model_artifacts=model_artifacts,
        prerequisites=prerequisites,
        notes=[
            "This report is local, read-only candidate runtime evidence for Phase 3 promotion review.",
            "It summarizes runtime-adjacent prerequisites but does not change retrieval defaults.",
            "Deployment-site latency and live URL evidence still require post-deployment validation.",
        ],
    )


def phase3_candidate_runtime_diagnostics_report_to_dict(
    report: Phase3CandidateRuntimeDiagnosticsReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase3_candidate_runtime_diagnostics_markdown(
    report: Phase3CandidateRuntimeDiagnosticsReport,
) -> str:
    lines = [
        "# Phase 3 Candidate Runtime Diagnostics",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Checks | `{report.summary['total_checks']}` |",
        f"| Ready Checks | `{report.summary['ready_checks']}` |",
        f"| Review Checks | `{report.summary['review_checks']}` |",
        f"| Blocked Checks | `{report.summary['blocked_checks']}` |",
        f"| Open Prerequisites | `{json.dumps(report.summary['open_prerequisite_ids'])}` |",
        "",
        "## Runtime Snapshot",
        "",
        "| Setting | Value |",
        "|---|---|",
        f"| Retrieval Backend | `{report.runtime_config['rag_retrieval_backend']}` |",
        f"| Embedding Provider | `{report.runtime_config['embedding_provider']}` |",
        f"| Embedding Model | `{report.runtime_config['embedding_model']}` |",
        f"| Embedding Model Path | `{report.runtime_config['embedding_model_path']}` |",
        f"| Provider API Key Configured | `{report.runtime_config['provider_api_key_configured']}` |",
        f"| Qdrant URL | `{report.runtime_config['qdrant_url']}` |",
        f"| Qdrant Collection | `{report.runtime_config['qdrant_collection']}` |",
        "",
        "## Prerequisites",
        "",
        "| Prerequisite | Status | Summary | Recommended Action |",
        "|---|---|---|---|",
    ]
    for item in report.prerequisites:
        lines.append(
            f"| `{item.id}` | `{item.status}` | {item.summary} | "
            f"`{item.recommended_action}` |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase3_candidate_runtime_diagnostics_report(
    output_dir: Path = Path("docs/benchmark/chinese-seed/retrieval-runtime-diagnostics"),
    *,
    settings: Settings | None = None,
    base_dir: Path = Path("."),
) -> Phase3CandidateRuntimeDiagnosticsReport:
    report = build_phase3_candidate_runtime_diagnostics_report(
        settings=settings,
        base_dir=base_dir,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3-candidate-runtime-diagnostics.json"
    markdown_path = output_dir / "phase3-candidate-runtime-diagnostics.md"
    exported = Phase3CandidateRuntimeDiagnosticsReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        summary=report.summary,
        runtime_config=report.runtime_config,
        model_artifacts=report.model_artifacts,
        prerequisites=report.prerequisites,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase3_candidate_runtime_diagnostics_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase3_candidate_runtime_diagnostics_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _runtime_config(settings: Settings) -> dict[str, Any]:
    return {
        "rag_retrieval_backend": settings.rag_retrieval_backend,
        "rag_score_threshold": settings.rag_score_threshold,
        "embedding_provider": settings.embedding_provider,
        "embedding_model": settings.embedding_model,
        "embedding_model_path": (
            str(settings.embedding_model_path)
            if settings.embedding_model_path is not None
            else None
        ),
        "embedding_local_files_only": settings.embedding_local_files_only,
        "qdrant_url": settings.qdrant_url,
        "qdrant_collection": settings.qdrant_collection,
        "qdrant_vector_name": settings.qdrant_vector_name,
        "qdrant_vector_size": settings.qdrant_vector_size,
        "provider_api_key_configured": bool(settings.provider_api_key),
        "qdrant_api_key_configured": bool(settings.qdrant_api_key),
    }


def _model_artifact_status(settings: Settings) -> dict[str, Any]:
    model_path = settings.embedding_model_path
    if model_path is None:
        return {
            "status": "not_configured",
            "model_path": None,
            "path_exists": False,
            "manifest_exists": False,
        }
    manifest_path = model_path / "model-manifest.json"
    path_exists = model_path.exists()
    manifest_exists = manifest_path.exists()
    return {
        "status": "ready" if path_exists and manifest_exists else "missing",
        "model_path": str(model_path),
        "path_exists": path_exists,
        "manifest_exists": manifest_exists,
    }


def _build_prerequisites(
    *,
    settings: Settings,
    model_artifacts: dict[str, Any],
    readiness_payload: dict[str, Any] | None,
    deployed_smoke_payload: dict[str, Any] | None,
) -> list[Phase3RuntimePrerequisite]:
    items: list[Phase3RuntimePrerequisite] = []
    items.append(
        _prerequisite(
            id="candidate_retrieval_backend",
            ready=settings.rag_retrieval_backend in {"qdrant", "qdrant-hybrid"},
            summary=(
                f"backend={settings.rag_retrieval_backend}; "
                "candidate_backends=qdrant,qdrant-hybrid"
            ),
            ready_action="no_action_required",
            review_action="run_candidate_backend_benchmark_review",
        )
    )
    items.append(
        _prerequisite(
            id="candidate_embedding_provider",
            ready=settings.embedding_provider != "mock",
            summary=(
                f"embedding_provider={settings.embedding_provider}; "
                "mock_provider_requires_promotion_evidence=true"
            ),
            ready_action="no_action_required",
            review_action="switch_to_candidate_embedding_for_evaluation",
        )
    )
    artifact_status = model_artifacts.get("status", "not_configured")
    items.append(
        _prerequisite(
            id="local_embedding_artifact",
            ready=artifact_status == "ready",
            summary=(
                f"artifact_status={artifact_status}; "
                f"path_exists={model_artifacts.get('path_exists', False)}; "
                f"manifest_exists={model_artifacts.get('manifest_exists', False)}"
            ),
            ready_action="no_action_required",
            review_action="validate_local_embedding_artifact",
        )
    )
    items.append(
        _prerequisite(
            id="provider_api_guard",
            ready=bool(settings.provider_api_key),
            summary=f"provider_api_key_configured={bool(settings.provider_api_key)}",
            ready_action="no_action_required",
            review_action="configure_provider_api_key_for_deployment_review",
        )
    )
    items.append(_phase3_readiness_prerequisite(readiness_payload))
    items.append(_deployed_smoke_prerequisite(deployed_smoke_payload))
    return items


def _phase3_readiness_prerequisite(
    readiness_payload: dict[str, Any] | None,
) -> Phase3RuntimePrerequisite:
    if readiness_payload is None:
        return Phase3RuntimePrerequisite(
            id="phase3_readiness_export",
            status="review",
            summary="Phase 3 readiness export is missing.",
            recommended_action="regenerate_phase3_retrieval_promotion_readiness",
            evidence_path=str(PHASE3_READINESS_PATH),
        )
    status = _normalize_status(readiness_payload.get("status", "review"))
    decision = str(readiness_payload.get("decision", "keep_runtime_defaults"))
    summary = readiness_payload.get("summary")
    open_gates = 0
    if isinstance(summary, dict):
        open_gates = _int_value(summary.get("open_gates"), fallback=0)
    return Phase3RuntimePrerequisite(
        id="phase3_readiness_export",
        status=status,
        summary=f"status={status}; decision={decision}; open_gates={open_gates}",
        recommended_action=(
            "review_evidence_notes" if status != "ready" else "no_action_required"
        ),
        evidence_path=str(PHASE3_READINESS_PATH),
    )


def _deployed_smoke_prerequisite(
    deployed_smoke_payload: dict[str, Any] | None,
) -> Phase3RuntimePrerequisite:
    if deployed_smoke_payload is None:
        return Phase3RuntimePrerequisite(
            id="deployed_smoke_evidence",
            status="review",
            summary="Deployed smoke evidence is not present in local workspace.",
            recommended_action="run_deployed_provider_smoke_after_deployment",
            evidence_path=str(DEPLOYED_SMOKE_PATH),
        )
    status = _normalize_status(deployed_smoke_payload.get("status", "review"))
    base_url = str(deployed_smoke_payload.get("base_url", "unknown"))
    return Phase3RuntimePrerequisite(
        id="deployed_smoke_evidence",
        status=status,
        summary=f"status={status}; base_url={base_url}",
        recommended_action=(
            "review_evidence_notes" if status != "ready" else "no_action_required"
        ),
        evidence_path=str(DEPLOYED_SMOKE_PATH),
    )


def _summary(prerequisites: list[Phase3RuntimePrerequisite]) -> dict[str, Any]:
    return {
        "total_checks": len(prerequisites),
        "ready_checks": sum(1 for item in prerequisites if item.status == "ready"),
        "review_checks": sum(1 for item in prerequisites if item.status == "review"),
        "blocked_checks": sum(1 for item in prerequisites if item.status == "blocked"),
        "open_prerequisite_ids": [
            item.id for item in prerequisites if item.status in {"review", "blocked"}
        ],
    }


def _overall_status(prerequisites: list[Phase3RuntimePrerequisite]) -> str:
    if any(item.status == "blocked" for item in prerequisites):
        return "blocked"
    if any(item.status == "review" for item in prerequisites):
        return "review"
    return "ready"


def _prerequisite(
    *,
    id: str,
    ready: bool,
    summary: str,
    ready_action: str,
    review_action: str,
) -> Phase3RuntimePrerequisite:
    status = "ready" if ready else "review"
    return Phase3RuntimePrerequisite(
        id=id,
        status=status,
        summary=summary,
        recommended_action=ready_action if ready else review_action,
    )


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_status(value: Any) -> str:
    if value in {"ready", "review", "blocked"}:
        return str(value)
    return "review"


def _int_value(value: Any, *, fallback: int) -> int:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int) and value >= 0:
        return value
    return fallback
