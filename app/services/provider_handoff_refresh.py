import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from app.services.deployment_readiness import export_deployment_readiness_report
from app.services.phase4_evidence_pack_readiness import (
    export_phase4_evidence_pack_readiness_report,
)
from app.services.phase4_caller_consumption_smoke import (
    export_phase4_caller_consumption_smoke_report,
)
from app.services.phase5_graph_use_case_readiness import (
    export_phase5_graph_use_case_readiness_report,
)
from app.services.provider_contract_smoke import export_provider_contract_smoke_report
from app.services.provider_handoff_bundle import export_provider_handoff_bundle_report
from app.services.phase3_retrieval_promotion_readiness import (
    export_phase3_retrieval_promotion_readiness_report,
)
from app.services.phase3_fp_fn_review import export_phase3_fp_fn_review_report
from app.services.provider_integration_client import export_provider_integration_probe_report
from app.services.provider_source_binding import export_provider_source_binding_summary
from app.services.reindex_readiness import export_reindex_readiness_report


PROVIDER_HANDOFF_REFRESH_ID = "provider-handoff-refresh-v1"
RefreshExporter = Callable[[Path], Any]
RefreshStatusReader = Callable[[Any], str]


@dataclass(frozen=True)
class HandoffRefreshStepSpec:
    id: str
    category: str
    output_dir: Path
    exporter: RefreshExporter
    status_reader: RefreshStatusReader


@dataclass(frozen=True)
class ProviderHandoffRefreshReport:
    id: str
    generated_at: str
    status: str
    steps: list[dict[str, Any]]
    operation_notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


@dataclass(frozen=True)
class LocalRefreshPlaceholderReport:
    status: str
    summary: dict[str, Any] | None = None
    json_path: Path | None = None
    markdown_path: Path | None = None


def default_handoff_refresh_steps(
    artifact_base_dir: Path = Path("."),
) -> list[HandoffRefreshStepSpec]:
    return [
        HandoffRefreshStepSpec(
            id="provider_integration_probe",
            category="integration",
            output_dir=artifact_base_dir / "docs/integration/provider-binding",
            exporter=export_provider_integration_probe_report,
            status_reader=lambda report: "ready" if report.bindable else "blocked",
        ),
        HandoffRefreshStepSpec(
            id="provider_contract_smoke",
            category="contract",
            output_dir=artifact_base_dir / "docs/smoke/provider-contract",
            exporter=export_provider_contract_smoke_report,
            status_reader=lambda report: "ready" if report.passed else "blocked",
        ),
        HandoffRefreshStepSpec(
            id="deployment_readiness",
            category="operations",
            output_dir=artifact_base_dir / "docs/operations/deployment-readiness",
            exporter=export_deployment_readiness_report,
            status_reader=lambda report: report.status,
        ),
        HandoffRefreshStepSpec(
            id="reindex_readiness",
            category="operations",
            output_dir=artifact_base_dir / "docs/operations/reindex-readiness",
            exporter=export_reindex_readiness_report,
            status_reader=lambda report: report.status,
        ),
        HandoffRefreshStepSpec(
            id="source_binding_summary",
            category="source-binding",
            output_dir=artifact_base_dir / "docs/integration/source-bindings",
            exporter=export_provider_source_binding_summary,
            status_reader=lambda report: report.status,
        ),
        HandoffRefreshStepSpec(
            id="phase3_fp_fn_review",
            category="retrieval-evidence",
            output_dir=artifact_base_dir / "docs/benchmark/chinese-seed/fp-fn-review",
            exporter=lambda output_dir: _export_phase3_fp_fn_review_nonblocking(
                artifact_base_dir=artifact_base_dir,
                output_dir=output_dir,
            ),
            status_reader=_phase3_fp_fn_step_status,
        ),
        HandoffRefreshStepSpec(
            id="phase3_retrieval_promotion_readiness",
            category="retrieval-evidence",
            output_dir=artifact_base_dir
            / "docs/benchmark/chinese-seed/retrieval-promotion-readiness",
            exporter=lambda output_dir: export_phase3_retrieval_promotion_readiness_report(
                output_dir=output_dir,
                base_dir=artifact_base_dir,
            ),
            status_reader=lambda report: report.status,
        ),
        HandoffRefreshStepSpec(
            id="phase4_evidence_pack_readiness",
            category="evidence-packaging",
            output_dir=artifact_base_dir
            / "docs/benchmark/chinese-seed/evidence-pack-readiness",
            exporter=lambda output_dir: export_phase4_evidence_pack_readiness_report(
                output_dir=output_dir,
                base_dir=artifact_base_dir,
            ),
            status_reader=lambda report: report.status,
        ),
        HandoffRefreshStepSpec(
            id="phase4_caller_consumption_smoke",
            category="caller-consumption",
            output_dir=artifact_base_dir / "docs/smoke/evidence-pack-consumption",
            exporter=lambda output_dir: export_phase4_caller_consumption_smoke_report(
                output_dir=output_dir,
                base_dir=artifact_base_dir,
            ),
            status_reader=lambda report: report.status,
        ),
        HandoffRefreshStepSpec(
            id="phase5_graph_use_case_readiness",
            category="graph-readiness",
            output_dir=artifact_base_dir
            / "docs/benchmark/chinese-seed/graph-use-case-readiness",
            exporter=lambda output_dir: export_phase5_graph_use_case_readiness_report(
                output_dir=output_dir,
                base_dir=artifact_base_dir,
            ),
            status_reader=lambda report: report.status,
        ),
        HandoffRefreshStepSpec(
            id="provider_handoff_bundle",
            category="handoff",
            output_dir=artifact_base_dir / "docs/integration/provider-handoff",
            exporter=lambda output_dir: export_provider_handoff_bundle_report(
                output_dir=output_dir,
                base_dir=artifact_base_dir,
            ),
            status_reader=lambda report: report.status,
        ),
    ]


def refresh_provider_handoff_evidence(
    *,
    output_dir: Path = Path("docs/integration/provider-handoff-refresh"),
    artifact_base_dir: Path = Path("."),
    steps: list[HandoffRefreshStepSpec] | None = None,
) -> ProviderHandoffRefreshReport:
    step_specs = steps or default_handoff_refresh_steps(artifact_base_dir)
    step_rows: list[dict[str, Any]] = []
    blocked = False
    for step in step_specs:
        if blocked:
            step_rows.append(_skipped_step(step))
            continue
        row = _run_step(step)
        step_rows.append(row)
        blocked = row["status"] == "blocked"

    report = ProviderHandoffRefreshReport(
        id=PROVIDER_HANDOFF_REFRESH_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=_overall_status(step_rows),
        steps=step_rows,
        operation_notes=_operation_notes(step_rows),
    )
    return _export_refresh_report(report, output_dir)


def provider_handoff_refresh_report_to_dict(
    report: ProviderHandoffRefreshReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_provider_handoff_refresh_markdown(
    report: ProviderHandoffRefreshReport,
) -> str:
    lines = [
        "# Provider Handoff Evidence Refresh",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Generated At: `{report.generated_at}`",
        "",
        "## Refresh Steps",
        "",
        "| Step | Category | Status | Output Paths | Recommended Action | Summary |",
        "|---|---|---|---|---|---|",
    ]
    for step in report.steps:
        output_paths = ", ".join(f"`{path}`" for path in step["output_paths"]) or "`none`"
        lines.append(
            f"| `{step['id']}` | `{step['category']}` | `{step['status']}` | "
            f"{output_paths} | `{step['recommended_action']}` | {step['summary']} |"
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


def _run_step(step: HandoffRefreshStepSpec) -> dict[str, Any]:
    try:
        report = step.exporter(step.output_dir)
        status = _normalize_status(step.status_reader(report))
    except Exception as error:
        return {
            "id": step.id,
            "category": step.category,
            "status": "blocked",
            "output_paths": [],
            "recommended_action": "resolve_step_failure",
            "summary": f"{error.__class__.__name__}: {error}",
            "error": {
                "type": error.__class__.__name__,
                "message": str(error),
            },
        }
    return {
        "id": step.id,
        "category": step.category,
        "status": status,
        "output_paths": _output_paths(report),
        "recommended_action": _recommended_action(status),
        "summary": _step_summary(status, report),
        "error": None,
    }


def _skipped_step(step: HandoffRefreshStepSpec) -> dict[str, Any]:
    return {
        "id": step.id,
        "category": step.category,
        "status": "skipped",
        "output_paths": [],
        "recommended_action": "not_run_due_to_previous_failure",
        "summary": "Skipped because an earlier refresh step was blocked.",
        "error": None,
    }


def _export_refresh_report(
    report: ProviderHandoffRefreshReport,
    output_dir: Path,
) -> ProviderHandoffRefreshReport:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "provider-handoff-refresh.json"
    markdown_path = output_dir / "provider-handoff-refresh.md"
    exported_report = ProviderHandoffRefreshReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        steps=report.steps,
        operation_notes=report.operation_notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            provider_handoff_refresh_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_provider_handoff_refresh_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _normalize_status(status: str) -> str:
    if status in {"ready", "review", "blocked"}:
        return status
    if status in {"passed", "bindable"}:
        return "ready"
    return "review"


def _overall_status(steps: list[dict[str, Any]]) -> str:
    statuses = {step["status"] for step in steps}
    if statuses & {"blocked", "skipped"}:
        return "blocked"
    if statuses - {"ready"}:
        return "review"
    return "ready"


def _recommended_action(status: str) -> str:
    if status == "ready":
        return "no_action_required"
    if status == "review":
        return "review_evidence_notes"
    return "resolve_step_failure"


def _step_summary(status: str, report: Any) -> str:
    if hasattr(report, "summary"):
        summary = json.dumps(
            getattr(report, "summary"),
            ensure_ascii=False,
            sort_keys=True,
        )
        return f"status={status}; summary={summary}"
    if hasattr(report, "status"):
        return f"status={status}; report_status={getattr(report, 'status')}"
    if hasattr(report, "bindable"):
        return f"status={status}; bindable={getattr(report, 'bindable')}"
    if hasattr(report, "passed"):
        return f"status={status}; passed={getattr(report, 'passed')}"
    return f"status={status}"


def _output_paths(report: Any) -> list[str]:
    paths = []
    json_path = getattr(report, "json_path", None)
    markdown_path = getattr(report, "markdown_path", None)
    if json_path is not None:
        paths.append(str(json_path))
    if markdown_path is not None:
        paths.append(str(markdown_path))
    return paths


def _operation_notes(steps: list[dict[str, Any]]) -> list[str]:
    notes = [
        "This refresh workflow only regenerates local evidence files.",
        "External control planes still own provider registration, heartbeat governance, audit policy, source-to-agent binding decisions, and final answer policy.",
    ]
    if any(step["status"] == "review" for step in steps):
        notes.append("At least one refreshed report requires human review before promotion.")
    if any(step["status"] in {"blocked", "skipped"} for step in steps):
        notes.append("Refresh stopped or skipped later steps because a blocking issue was detected.")
    return notes


def _export_phase3_fp_fn_review_nonblocking(
    *,
    artifact_base_dir: Path,
    output_dir: Path,
) -> Any:
    benchmark_path = (
        artifact_base_dir
        / "docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.json"
    )
    try:
        return export_phase3_fp_fn_review_report(
            benchmark_report_path=benchmark_path,
            output_dir=output_dir,
        )
    except FileNotFoundError:
        return LocalRefreshPlaceholderReport(
            status="review",
            summary={"reason": "phase3_seed_retrieval_baseline_missing"},
        )


def _phase3_fp_fn_step_status(report: Any) -> str:
    if hasattr(report, "status"):
        return getattr(report, "status")
    fp_count = getattr(report, "false_positive_count", 0)
    fn_count = getattr(report, "false_negative_count", 0)
    return "review" if (fp_count > 0 or fn_count > 0) else "ready"
