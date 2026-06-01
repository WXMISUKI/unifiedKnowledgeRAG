import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.config import Settings, get_settings


PHASE6_BGE_M3_ARTIFACT_READINESS_ID = "phase6-bge-m3-artifact-readiness-v1"
DEPLOYMENT_READINESS_PATH = Path("docs/operations/deployment-readiness/deployment-readiness.json")
MANIFEST_NAME = "model-manifest.json"


@dataclass(frozen=True)
class Phase6BgeM3ArtifactSignal:
    id: str
    status: str
    summary: str
    recommended_action: str
    evidence_path: str | None = None


@dataclass(frozen=True)
class Phase6BgeM3ArtifactReadinessReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    artifact: dict[str, Any]
    signals: list[Phase6BgeM3ArtifactSignal]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase6_bge_m3_artifact_readiness_report(
    settings: Settings | None = None,
    *,
    base_dir: Path = Path("."),
) -> Phase6BgeM3ArtifactReadinessReport:
    settings = settings or get_settings()
    deployment_payload = _read_json_if_present(base_dir / DEPLOYMENT_READINESS_PATH)
    artifact = _build_artifact_snapshot(settings=settings, deployment_payload=deployment_payload)
    signals = _build_signals(artifact=artifact, deployment_payload=deployment_payload)
    summary = _summary(signals)
    return Phase6BgeM3ArtifactReadinessReport(
        id=PHASE6_BGE_M3_ARTIFACT_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=_overall_status(signals),
        decision="keep_runtime_defaults",
        summary=summary,
        artifact=artifact,
        signals=signals,
        notes=[
            "This report is local, read-only artifact readiness evidence for Phase 6 deployment review.",
            "It supports Phase 3 promotion review as a bridge artifact but does not promote embedding defaults.",
            "Use matching artifact directory and manifest when copying models into private-network deployments.",
        ],
    )


def phase6_bge_m3_artifact_readiness_report_to_dict(
    report: Phase6BgeM3ArtifactReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase6_bge_m3_artifact_readiness_markdown(
    report: Phase6BgeM3ArtifactReadinessReport,
) -> str:
    lines = [
        "# Phase 6 BGE-M3 Artifact Readiness",
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
        f"| Total Signals | `{report.summary['total_signals']}` |",
        f"| Ready Signals | `{report.summary['ready_signals']}` |",
        f"| Review Signals | `{report.summary['review_signals']}` |",
        f"| Blocked Signals | `{report.summary['blocked_signals']}` |",
        f"| Open Signal IDs | `{json.dumps(report.summary['open_signal_ids'])}` |",
        "",
        "## Artifact Snapshot",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Embedding Provider | `{report.artifact['embedding_provider']}` |",
        f"| Embedding Model | `{report.artifact['embedding_model']}` |",
        f"| Embedding Local Files Only | `{report.artifact['embedding_local_files_only']}` |",
        f"| Model Path | `{report.artifact['model_path']}` |",
        f"| Path Exists | `{report.artifact['path_exists']}` |",
        f"| Manifest Exists | `{report.artifact['manifest_exists']}` |",
        f"| Required Files Present | `{report.artifact['required_files_present_count']}/{report.artifact['required_files_total']}` |",
        f"| Weight Files Count | `{report.artifact['weight_files_count']}` |",
        f"| Checksum Coverage | `{report.artifact['checksum_coverage_count']}/{report.artifact['checksum_target_count']}` |",
        f"| Checksum Algorithm | `{report.artifact['checksum_algorithm']}` |",
        f"| Deployment Readiness Status | `{report.artifact['deployment_readiness_status']}` |",
        "",
        "## Signals",
        "",
        "| Signal | Status | Summary | Recommended Action |",
        "|---|---|---|---|",
    ]
    for signal in report.signals:
        lines.append(
            f"| `{signal.id}` | `{signal.status}` | {signal.summary} | "
            f"`{signal.recommended_action}` |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase6_bge_m3_artifact_readiness_report(
    output_dir: Path = Path("docs/operations/bge-m3-artifact-readiness"),
    *,
    settings: Settings | None = None,
    base_dir: Path = Path("."),
) -> Phase6BgeM3ArtifactReadinessReport:
    report = build_phase6_bge_m3_artifact_readiness_report(
        settings=settings,
        base_dir=base_dir,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase6-bge-m3-artifact-readiness.json"
    markdown_path = output_dir / "phase6-bge-m3-artifact-readiness.md"
    exported = Phase6BgeM3ArtifactReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        summary=report.summary,
        artifact=report.artifact,
        signals=report.signals,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase6_bge_m3_artifact_readiness_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase6_bge_m3_artifact_readiness_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _build_artifact_snapshot(
    *,
    settings: Settings,
    deployment_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    runtime_config = _dict_value(deployment_payload, "runtime_config", {})
    model_artifacts = _dict_value(deployment_payload, "model_artifacts", {})
    model_path_raw = _dict_value(model_artifacts, "model_path", None)
    if model_path_raw is None and settings.embedding_model_path is not None:
        model_path_raw = str(settings.embedding_model_path)
    model_path = Path(model_path_raw) if isinstance(model_path_raw, str) else None
    manifest_path = model_path / MANIFEST_NAME if model_path is not None else None
    manifest_payload = (
        _read_json_if_present(manifest_path)
        if manifest_path is not None
        else None
    )
    required_files = _list_of_strings(_dict_value(_dict_value(manifest_payload, "validation", {}), "required_files", []))
    weight_files = _list_of_strings(_dict_value(_dict_value(manifest_payload, "validation", {}), "weight_files", []))
    checksums = _dict_value(_dict_value(manifest_payload, "validation", {}), "checksums", {})
    required_present = sum(
        1
        for file_name in required_files
        if model_path is not None and (model_path / file_name).is_file()
    )
    checksum_target_count = len(required_files) + len(weight_files)
    checksum_coverage_count = 0
    if isinstance(checksums, dict):
        checksum_coverage_count = sum(
            1 for key, value in checksums.items()
            if isinstance(key, str) and isinstance(value, str) and len(value) == 64
        )
    return {
        "embedding_provider": _dict_value(runtime_config, "embedding_provider", settings.embedding_provider),
        "embedding_model": _dict_value(runtime_config, "embedding_model", settings.embedding_model),
        "embedding_local_files_only": bool(
            _dict_value(
                runtime_config,
                "embedding_local_files_only",
                settings.embedding_local_files_only,
            )
        ),
        "deployment_readiness_status": _dict_value(deployment_payload, "status", "missing"),
        "model_path": str(model_path) if model_path is not None else None,
        "path_exists": bool(model_path and model_path.exists()),
        "manifest_exists": bool(manifest_path and manifest_path.exists()),
        "required_files": required_files,
        "required_files_total": len(required_files),
        "required_files_present_count": required_present,
        "weight_files": weight_files,
        "weight_files_count": len(weight_files),
        "checksum_algorithm": _dict_value(_dict_value(manifest_payload, "validation", {}), "checksum_algorithm", "unknown"),
        "checksum_target_count": checksum_target_count,
        "checksum_coverage_count": checksum_coverage_count,
        "manifest_local_files_only": bool(_dict_value(manifest_payload, "local_files_only", False)),
    }


def _build_signals(
    *,
    artifact: dict[str, Any],
    deployment_payload: dict[str, Any] | None,
) -> list[Phase6BgeM3ArtifactSignal]:
    signals: list[Phase6BgeM3ArtifactSignal] = []
    signals.append(
        _signal(
            id="embedding_provider_candidate",
            ready=artifact["embedding_provider"] == "bge_m3_local",
            summary=f"embedding_provider={artifact['embedding_provider']}",
            ready_action="no_action_required",
            review_action="set_embedding_provider_to_bge_m3_local_for_candidate_review",
            evidence_path=str(DEPLOYMENT_READINESS_PATH),
        )
    )
    signals.append(
        _signal(
            id="model_path_and_manifest_presence",
            ready=artifact["path_exists"] and artifact["manifest_exists"],
            summary=(
                f"path_exists={artifact['path_exists']}; "
                f"manifest_exists={artifact['manifest_exists']}"
            ),
            ready_action="no_action_required",
            review_action="configure_embedding_model_path_and_manifest",
            evidence_path=str(DEPLOYMENT_READINESS_PATH),
        )
    )
    signals.append(
        _signal(
            id="required_file_inventory",
            ready=artifact["required_files_total"] > 0
            and artifact["required_files_present_count"] == artifact["required_files_total"]
            and artifact["weight_files_count"] > 0,
            summary=(
                f"required_files={artifact['required_files_present_count']}/{artifact['required_files_total']}; "
                f"weight_files={artifact['weight_files_count']}"
            ),
            ready_action="no_action_required",
            review_action="rebuild_or_copy_complete_bge_m3_artifact",
            evidence_path="model-manifest.json",
        )
    )
    signals.append(
        _signal(
            id="checksum_coverage",
            ready=artifact["checksum_target_count"] > 0
            and artifact["checksum_coverage_count"] >= artifact["checksum_target_count"]
            and artifact["checksum_algorithm"] == "sha256",
            summary=(
                f"checksum_coverage={artifact['checksum_coverage_count']}/"
                f"{artifact['checksum_target_count']}; "
                f"algorithm={artifact['checksum_algorithm']}"
            ),
            ready_action="no_action_required",
            review_action="regenerate_manifest_with_sha256_checksums",
            evidence_path="model-manifest.json",
        )
    )
    deployment_status = _dict_value(deployment_payload, "status", "missing")
    signals.append(
        _signal(
            id="deployment_readiness_linkage",
            ready=deployment_status in {"ready", "review"},
            summary=f"deployment_readiness_status={deployment_status}",
            ready_action="no_action_required",
            review_action="regenerate_deployment_readiness_report",
            evidence_path=str(DEPLOYMENT_READINESS_PATH),
        )
    )
    signals.append(
        _signal(
            id="private_network_copy_posture",
            ready=artifact["embedding_local_files_only"] and artifact["manifest_local_files_only"],
            summary=(
                f"runtime_local_files_only={artifact['embedding_local_files_only']}; "
                f"manifest_local_files_only={artifact['manifest_local_files_only']}"
            ),
            ready_action="no_action_required",
            review_action="enable_local_files_only_for_private_network_artifacts",
            evidence_path=str(DEPLOYMENT_READINESS_PATH),
        )
    )
    return signals


def _summary(signals: list[Phase6BgeM3ArtifactSignal]) -> dict[str, Any]:
    return {
        "total_signals": len(signals),
        "ready_signals": sum(1 for signal in signals if signal.status == "ready"),
        "review_signals": sum(1 for signal in signals if signal.status == "review"),
        "blocked_signals": sum(1 for signal in signals if signal.status == "blocked"),
        "open_signal_ids": [
            signal.id for signal in signals if signal.status in {"review", "blocked"}
        ],
    }


def _overall_status(signals: list[Phase6BgeM3ArtifactSignal]) -> str:
    if any(signal.status == "blocked" for signal in signals):
        return "blocked"
    if any(signal.status == "review" for signal in signals):
        return "review"
    return "ready"


def _signal(
    *,
    id: str,
    ready: bool,
    summary: str,
    ready_action: str,
    review_action: str,
    evidence_path: str | None = None,
) -> Phase6BgeM3ArtifactSignal:
    return Phase6BgeM3ArtifactSignal(
        id=id,
        status="ready" if ready else "review",
        summary=summary,
        recommended_action=ready_action if ready else review_action,
        evidence_path=evidence_path,
    )


def _read_json_if_present(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _dict_value(value: Any, key: str, fallback: Any) -> Any:
    if not isinstance(value, dict):
        return fallback
    return value.get(key, fallback)


def _list_of_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]
