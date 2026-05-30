import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.config import Settings, get_settings
from app.services.provider_contract_smoke import (
    ProviderContractSmokeReport,
    provider_contract_smoke_report_to_dict,
    run_provider_contract_smoke,
)
from app.services.provider_health import build_health_response
from app.services.provider_manifest import build_provider_integration_manifest
from app.services.provider_preflight import build_provider_preflight_response


DEPLOYMENT_READINESS_REPORT_ID = "deployment-readiness-v1"


@dataclass(frozen=True)
class DeploymentReadinessReport:
    id: str
    generated_at: str
    status: str
    provider: dict[str, Any]
    health: dict[str, Any]
    preflight: dict[str, Any]
    contract_smoke: dict[str, Any]
    runtime_config: dict[str, Any]
    model_artifacts: dict[str, Any]
    operation_notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_deployment_readiness_report(
    settings: Settings | None = None,
    *,
    smoke_report: ProviderContractSmokeReport | None = None,
) -> DeploymentReadinessReport:
    settings = settings or get_settings()
    manifest = build_provider_integration_manifest()
    health = build_health_response(settings)
    preflight = build_provider_preflight_response(settings)
    smoke_report = smoke_report or run_provider_contract_smoke()
    model_artifacts = _model_artifact_status(settings)
    notes = _operation_notes(settings, model_artifacts)
    status = _readiness_status(
        health_status=health.status,
        bindable=preflight.bindable,
        smoke_passed=smoke_report.passed,
        notes=notes,
    )
    return DeploymentReadinessReport(
        id=DEPLOYMENT_READINESS_REPORT_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        provider={
            "provider_id": manifest.provider_id,
            "provider_name": manifest.provider_name,
            "provider_version": manifest.provider_version,
            "contract_version": manifest.contract_version,
            "manifest_version": manifest.manifest_version,
            "component_role": manifest.component_role,
        },
        health=health.model_dump(),
        preflight={
            "bindable": preflight.bindable,
            "requested_contract_version": preflight.requested_contract_version,
            "requested_capability_ids": preflight.requested_capability_ids,
            "checks": [check.model_dump() for check in preflight.checks],
        },
        contract_smoke={
            "passed": smoke_report.passed,
            "summary": smoke_report.summary,
            "check_names": [check.name for check in smoke_report.checks],
        },
        runtime_config=_runtime_config(settings),
        model_artifacts=model_artifacts,
        operation_notes=notes,
    )


def deployment_readiness_report_to_dict(
    report: DeploymentReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_deployment_readiness_markdown(
    report: DeploymentReadinessReport,
) -> str:
    config = report.runtime_config
    artifacts = report.model_artifacts
    smoke = report.contract_smoke
    lines = [
        "# Deployment Readiness Report",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Provider: `{report.provider['provider_id']}`",
        f"- Contract: `{report.provider['contract_version']}`",
        "",
        "## Core Checks",
        "",
        "| Check | Status | Details |",
        "|---|---|---|",
        f"| Health | `{report.health['status']}` | RAG `{report.health['rag']['status']}`, Answer `{report.health['answer']['status']}`, Graph `{report.health['graph']['status']}` |",
        f"| Preflight | `{'bindable' if report.preflight['bindable'] else 'blocked'}` | `{_passed_count(report.preflight['checks'])}/{len(report.preflight['checks'])}` checks passed |",
        f"| Contract Smoke | `{'passed' if smoke['passed'] else 'failed'}` | `{smoke['summary']['passed']}/{smoke['summary']['total']}` checks passed |",
        "",
        "## Runtime Configuration",
        "",
        "| Setting | Value |",
        "|---|---|",
        f"| Retrieval Backend | `{config['rag_retrieval_backend']}` |",
        f"| Source Dir | `{config['rag_source_dir']}` |",
        f"| Index Dir | `{config['rag_index_dir']}` |",
        f"| Embedding Provider | `{config['embedding_provider']}` |",
        f"| Embedding Model | `{config['embedding_model']}` |",
        f"| Embedding Local Files Only | `{config['embedding_local_files_only']}` |",
        f"| Qdrant URL | `{config['qdrant_url']}` |",
        f"| Qdrant Collection | `{config['qdrant_collection']}` |",
        f"| Qdrant API Key Configured | `{config['qdrant_api_key_configured']}` |",
        f"| Answer Composer | `{config['rag_answer_composer']}` |",
        "",
        "## Model Artifacts",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Status | `{artifacts['status']}` |",
        f"| Model Path | `{artifacts['model_path']}` |",
        f"| Path Exists | `{artifacts['path_exists']}` |",
        f"| Manifest Exists | `{artifacts['manifest_exists']}` |",
        "",
        "## Operation Notes",
        "",
    ]
    lines.extend(f"- {note}" for note in report.operation_notes)
    lines.append("")
    return "\n".join(lines)


def export_deployment_readiness_report(
    output_dir: Path = Path("docs/operations/deployment-readiness"),
    *,
    settings: Settings | None = None,
    smoke_report: ProviderContractSmokeReport | None = None,
) -> DeploymentReadinessReport:
    report = build_deployment_readiness_report(
        settings=settings,
        smoke_report=smoke_report,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "deployment-readiness.json"
    markdown_path = output_dir / "deployment-readiness.md"
    exported_report = DeploymentReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        provider=report.provider,
        health=report.health,
        preflight=report.preflight,
        contract_smoke=report.contract_smoke,
        runtime_config=report.runtime_config,
        model_artifacts=report.model_artifacts,
        operation_notes=report.operation_notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            deployment_readiness_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_deployment_readiness_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _runtime_config(settings: Settings) -> dict[str, Any]:
    return {
        "rag_retrieval_backend": settings.rag_retrieval_backend,
        "rag_source_dir": str(settings.rag_source_dir),
        "rag_index_dir": str(settings.rag_index_dir),
        "rag_score_threshold": settings.rag_score_threshold,
        "embedding_provider": settings.embedding_provider,
        "embedding_model": settings.embedding_model,
        "embedding_model_path": (
            str(settings.embedding_model_path)
            if settings.embedding_model_path is not None
            else None
        ),
        "embedding_vector_size": settings.embedding_vector_size,
        "embedding_local_files_only": settings.embedding_local_files_only,
        "qdrant_url": settings.qdrant_url,
        "qdrant_collection": settings.qdrant_collection,
        "qdrant_vector_name": settings.qdrant_vector_name,
        "qdrant_vector_size": settings.qdrant_vector_size,
        "qdrant_api_key_configured": bool(settings.qdrant_api_key),
        "rag_answer_composer": settings.rag_answer_composer,
        "rag_answer_composer_model": settings.rag_answer_composer_model,
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


def _operation_notes(
    settings: Settings,
    model_artifacts: dict[str, Any],
) -> list[str]:
    notes = [
        "This report is local readiness evidence; external control planes still own binding and governance decisions.",
        "Contract smoke evidence should be regenerated after configuration or dependency changes.",
    ]
    if settings.embedding_provider == "mock":
        notes.append(
            "Embedding provider is mock; use a real local or hosted embedding candidate before production retrieval promotion."
        )
    if settings.rag_retrieval_backend != "qdrant":
        notes.append(
            "Retrieval backend is not qdrant; vector-store deployment readiness remains a separate review."
        )
    if model_artifacts["status"] == "missing":
        notes.append(
            "Configured embedding model path is missing required local artifact files."
        )
    if settings.qdrant_api_key:
        notes.append("Qdrant API key is configured; the report intentionally redacts secrets.")
    return notes


def _readiness_status(
    *,
    health_status: str,
    bindable: bool,
    smoke_passed: bool,
    notes: list[str],
) -> str:
    if health_status != "ok" or not bindable or not smoke_passed:
        return "blocked"
    if notes:
        return "review"
    return "ready"


def _passed_count(checks: list[dict[str, Any]]) -> int:
    return sum(1 for check in checks if check.get("passed") is True)
