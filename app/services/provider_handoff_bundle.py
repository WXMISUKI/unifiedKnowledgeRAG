import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.services.provider_manifest import build_provider_integration_manifest


PROVIDER_HANDOFF_BUNDLE_ID = "provider-handoff-bundle-v1"


@dataclass(frozen=True)
class HandoffEvidenceSpec:
    id: str
    category: str
    path: Path


@dataclass(frozen=True)
class ProviderHandoffBundleReport:
    id: str
    generated_at: str
    status: str
    provider: dict[str, Any]
    evidence_artifacts: list[dict[str, Any]]
    operation_notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


DEFAULT_EVIDENCE_SPECS = [
    HandoffEvidenceSpec(
        id="provider_integration_probe",
        category="integration",
        path=Path("docs/integration/provider-binding/provider-integration-probe.json"),
    ),
    HandoffEvidenceSpec(
        id="provider_contract_smoke",
        category="contract",
        path=Path("docs/smoke/provider-contract/provider-contract-smoke.json"),
    ),
    HandoffEvidenceSpec(
        id="deployment_readiness",
        category="operations",
        path=Path("docs/operations/deployment-readiness/deployment-readiness.json"),
    ),
    HandoffEvidenceSpec(
        id="reindex_readiness",
        category="operations",
        path=Path("docs/operations/reindex-readiness/reindex-readiness.json"),
    ),
]


def build_provider_handoff_bundle_report(
    *,
    base_dir: Path = Path("."),
    evidence_specs: list[HandoffEvidenceSpec] | None = None,
) -> ProviderHandoffBundleReport:
    manifest = build_provider_integration_manifest()
    specs = evidence_specs or DEFAULT_EVIDENCE_SPECS
    artifact_rows = [
        _artifact_row(base_dir=base_dir, spec=spec)
        for spec in specs
    ]
    return ProviderHandoffBundleReport(
        id=PROVIDER_HANDOFF_BUNDLE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=_overall_status(artifact_rows),
        provider={
            "provider_id": manifest.provider_id,
            "provider_name": manifest.provider_name,
            "provider_version": manifest.provider_version,
            "contract_version": manifest.contract_version,
            "manifest_version": manifest.manifest_version,
            "component_role": manifest.component_role,
            "compatible_control_planes": manifest.compatible_control_planes,
        },
        evidence_artifacts=artifact_rows,
        operation_notes=_operation_notes(artifact_rows),
    )


def provider_handoff_bundle_report_to_dict(
    report: ProviderHandoffBundleReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_provider_handoff_bundle_markdown(
    report: ProviderHandoffBundleReport,
) -> str:
    lines = [
        "# Provider Handoff Bundle",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Provider: `{report.provider['provider_id']}`",
        f"- Contract: `{report.provider['contract_version']}`",
        f"- Manifest: `{report.provider['manifest_version']}`",
        "",
        "## Evidence Artifacts",
        "",
        "| Artifact | Category | Present | Status | Summary | Recommended Action |",
        "|---|---|---|---|---|---|",
    ]
    for artifact in report.evidence_artifacts:
        lines.append(
            f"| `{artifact['id']}` | `{artifact['category']}` | "
            f"`{artifact['present']}` | `{artifact['status']}` | "
            f"{artifact['summary']} | `{artifact['recommended_action']}` |"
        )
    lines.extend(
        [
            "",
            "## Operation Notes",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in report.operation_notes)
    lines.append("")
    return "\n".join(lines)


def export_provider_handoff_bundle_report(
    output_dir: Path = Path("docs/integration/provider-handoff"),
    *,
    base_dir: Path = Path("."),
    evidence_specs: list[HandoffEvidenceSpec] | None = None,
) -> ProviderHandoffBundleReport:
    report = build_provider_handoff_bundle_report(
        base_dir=base_dir,
        evidence_specs=evidence_specs,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "provider-handoff-bundle.json"
    markdown_path = output_dir / "provider-handoff-bundle.md"
    exported_report = ProviderHandoffBundleReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        provider=report.provider,
        evidence_artifacts=report.evidence_artifacts,
        operation_notes=report.operation_notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            provider_handoff_bundle_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_provider_handoff_bundle_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _artifact_row(
    *,
    base_dir: Path,
    spec: HandoffEvidenceSpec,
) -> dict[str, Any]:
    path = base_dir / spec.path
    if not path.exists():
        return {
            "id": spec.id,
            "category": spec.category,
            "path": str(spec.path),
            "present": False,
            "status": "missing",
            "summary": "Evidence artifact is missing.",
            "recommended_action": f"regenerate_{spec.id}",
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    status, summary = _artifact_status_and_summary(spec.id, payload)
    return {
        "id": spec.id,
        "category": spec.category,
        "path": str(spec.path),
        "present": True,
        "status": status,
        "summary": summary,
        "recommended_action": _recommended_action(status),
    }


def _artifact_status_and_summary(
    artifact_id: str,
    payload: dict[str, Any],
) -> tuple[str, str]:
    if artifact_id == "provider_integration_probe":
        bindable = payload.get("bindable") is True
        check_count = len(payload.get("checks", []))
        capability_count = len(payload.get("capability_bindings", []))
        return (
            "ready" if bindable else "blocked",
            f"bindable={bindable}; checks={check_count}; capabilities={capability_count}",
        )
    if artifact_id == "provider_contract_smoke":
        passed = payload.get("passed") is True
        summary = payload.get("summary", {})
        return (
            "ready" if passed else "blocked",
            (
                f"passed={passed}; "
                f"checks={summary.get('passed', 0)}/{summary.get('total', 0)}"
            ),
        )
    if artifact_id in {"deployment_readiness", "reindex_readiness"}:
        status = payload.get("status", "review")
        return (
            status if status in {"ready", "review", "blocked"} else "review",
            f"status={status}",
        )
    return "review", "Unknown evidence artifact shape."


def _recommended_action(status: str) -> str:
    if status == "ready":
        return "no_action_required"
    if status == "review":
        return "review_evidence_notes"
    if status == "missing":
        return "regenerate_evidence"
    return "resolve_failed_evidence"


def _overall_status(artifact_rows: list[dict[str, Any]]) -> str:
    statuses = {artifact["status"] for artifact in artifact_rows}
    if statuses & {"missing", "blocked"}:
        return "blocked"
    if statuses - {"ready"}:
        return "review"
    return "ready"


def _operation_notes(artifact_rows: list[dict[str, Any]]) -> list[str]:
    notes = [
        "This bundle is a read-only handoff index over existing local evidence files.",
        "Regenerate prerequisite evidence reports after configuration, dependency, source, or index lifecycle changes.",
        "External control planes still own provider registration, heartbeat governance, audit policy, and source-to-agent binding decisions.",
    ]
    if any(artifact["status"] == "missing" for artifact in artifact_rows):
        notes.append("At least one required evidence artifact is missing.")
    if any(artifact["status"] == "review" for artifact in artifact_rows):
        notes.append("At least one evidence artifact requires human review before promotion.")
    return notes
