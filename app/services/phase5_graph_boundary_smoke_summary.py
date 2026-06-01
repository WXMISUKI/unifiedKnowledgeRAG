import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE5_GRAPH_BOUNDARY_SMOKE_SUMMARY_ID = "phase5-graph-boundary-smoke-summary-v1"
PHASE5_PROVIDER_CONTRACT_SMOKE_PATH = Path(
    "docs/smoke/provider-contract/provider-contract-smoke.json"
)
PHASE5_GRAPH_BOUNDARY_SMOKE_SUMMARY_JSON = "phase5-graph-boundary-smoke-summary.json"
PHASE5_GRAPH_BOUNDARY_SMOKE_SUMMARY_MARKDOWN = (
    "phase5-graph-boundary-smoke-summary.md"
)


@dataclass(frozen=True)
class Phase5GraphBoundarySmokeSummaryArtifact:
    id: str
    category: str
    path: str
    status: str
    summary: str
    present: bool
    required: bool
    recommended_action: str


@dataclass(frozen=True)
class Phase5GraphBoundarySmokeSummaryReport:
    id: str
    generated_at: str
    status: str
    decision: str
    source_smoke_path: str
    summary: dict[str, Any]
    supporting_evidence: list[Phase5GraphBoundarySmokeSummaryArtifact]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase5_graph_boundary_smoke_summary_report(
    *,
    base_dir: Path = Path("."),
) -> Phase5GraphBoundarySmokeSummaryReport:
    source_smoke_artifact, payload = _build_source_smoke_artifact(base_dir)
    graph_schema_artifact = _build_graph_schema_artifact(payload, source_smoke_artifact)
    graph_boundary_artifact = _build_graph_boundary_artifact(
        payload,
        source_smoke_artifact,
    )
    supporting_evidence = [
        source_smoke_artifact,
        graph_schema_artifact,
        graph_boundary_artifact,
    ]
    summary = _summary_from_payload(payload, supporting_evidence)
    return Phase5GraphBoundarySmokeSummaryReport(
        id=PHASE5_GRAPH_BOUNDARY_SMOKE_SUMMARY_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=_overall_status(supporting_evidence),
        decision="keep_graph_query_planned",
        source_smoke_path=str(PHASE5_PROVIDER_CONTRACT_SMOKE_PATH),
        summary=summary,
        supporting_evidence=supporting_evidence,
        notes=[
            "This report is local, read-only evidence for Phase 5 graph boundary review.",
            "It condenses the graph schema discovery and planned graph query checks from provider contract smoke.",
            "It does not change runtime defaults, add graph execution, or introduce graph-store dependencies.",
        ],
    )


def phase5_graph_boundary_smoke_summary_report_to_dict(
    report: Phase5GraphBoundarySmokeSummaryReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase5_graph_boundary_smoke_summary_markdown(
    report: Phase5GraphBoundarySmokeSummaryReport,
) -> str:
    status = "passed" if report.status == "ready" else report.status
    lines = [
        "# Phase 5 Graph Boundary Smoke Summary",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{status}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Source Smoke: `{report.source_smoke_path}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Artifacts | `{report.summary['total_artifacts']}` |",
        f"| Ready Artifacts | `{report.summary['ready_artifacts']}` |",
        f"| Review Artifacts | `{report.summary['review_artifacts']}` |",
        f"| Blocked Artifacts | `{report.summary['blocked_artifacts']}` |",
        f"| Required Artifacts | `{report.summary['required_artifacts']}` |",
        f"| Required Ready Artifacts | `{report.summary['required_ready_artifacts']}` |",
        f"| Source Smoke Passed | `{report.summary['source_smoke_passed']}` |",
        f"| Smoke Checks Passed | `{report.summary['smoke_checks_passed']}` |",
        f"| Graph Checks Passed | `{report.summary['graph_checks_passed']}` |",
        f"| Graph Schema Count | `{report.summary['graph_schema_count']}` |",
        f"| Graph Query Status | `{report.summary['graph_query_status']}` |",
        f"| Graph Query Planned | `{report.summary['graph_query_planned']}` |",
        f"| Graph Error Code | `{report.summary['graph_error_code']}` |",
        "",
        "## Supporting Evidence",
        "",
        "| Evidence | Category | Status | Summary |",
        "|---|---|---|---|",
    ]
    for item in report.supporting_evidence:
        lines.append(
            f"| `{item.id}` | `{item.category}` | `{item.status}` | {item.summary} |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def export_phase5_graph_boundary_smoke_summary_report(
    output_dir: Path = Path("docs/smoke/graph-boundary-summary"),
    *,
    base_dir: Path = Path("."),
) -> Phase5GraphBoundarySmokeSummaryReport:
    report = build_phase5_graph_boundary_smoke_summary_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PHASE5_GRAPH_BOUNDARY_SMOKE_SUMMARY_JSON
    markdown_path = output_dir / PHASE5_GRAPH_BOUNDARY_SMOKE_SUMMARY_MARKDOWN
    exported_report = Phase5GraphBoundarySmokeSummaryReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        source_smoke_path=report.source_smoke_path,
        summary=report.summary,
        supporting_evidence=report.supporting_evidence,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase5_graph_boundary_smoke_summary_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase5_graph_boundary_smoke_summary_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _build_source_smoke_artifact(
    base_dir: Path,
) -> tuple[Phase5GraphBoundarySmokeSummaryArtifact, dict[str, Any]]:
    path = base_dir / PHASE5_PROVIDER_CONTRACT_SMOKE_PATH
    if not path.exists():
        return (
            Phase5GraphBoundarySmokeSummaryArtifact(
                id="provider_contract_smoke_source",
                category="source-smoke",
                path=str(PHASE5_PROVIDER_CONTRACT_SMOKE_PATH),
                status="blocked",
                summary="Provider contract smoke report is missing.",
                present=False,
                required=True,
                recommended_action="regenerate_provider_contract_smoke",
            ),
            {},
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    passed = payload.get("passed") is True
    summary = payload.get("summary", {})
    total = _int_value(summary.get("total"), fallback=0)
    passed_count = _int_value(summary.get("passed"), fallback=0)
    failed_count = _int_value(summary.get("failed"), fallback=0)
    status = "ready" if passed else "blocked"
    return (
        Phase5GraphBoundarySmokeSummaryArtifact(
            id="provider_contract_smoke_source",
            category="source-smoke",
            path=str(PHASE5_PROVIDER_CONTRACT_SMOKE_PATH),
            status=status,
            summary=f"passed={passed}; checks={passed_count}/{total}; failed_checks={failed_count}",
            present=True,
            required=True,
            recommended_action=_recommended_action(status),
        ),
        payload,
    )


def _build_graph_schema_artifact(
    payload: dict[str, Any],
    source_smoke_artifact: Phase5GraphBoundarySmokeSummaryArtifact,
) -> Phase5GraphBoundarySmokeSummaryArtifact:
    graph_check = _check_from_payload(payload, "graph_schema_discovery")
    if graph_check is None:
        return Phase5GraphBoundarySmokeSummaryArtifact(
            id="graph_schema_discovery_summary",
            category="graph-smoke",
            path=str(PHASE5_PROVIDER_CONTRACT_SMOKE_PATH),
            status="blocked",
            summary="graph_schema_discovery check is missing.",
            present=source_smoke_artifact.present,
            required=True,
            recommended_action=_recommended_action("blocked"),
        )
    details = graph_check.get("details", {})
    passed = graph_check.get("passed") is True
    status = "ready" if (source_smoke_artifact.status == "ready" and passed) else "blocked"
    return Phase5GraphBoundarySmokeSummaryArtifact(
        id="graph_schema_discovery_summary",
        category="graph-smoke",
        path=str(PHASE5_PROVIDER_CONTRACT_SMOKE_PATH),
        status=status,
        summary=(
            f"graph_count={_int_value(details.get('graph_count'), fallback=0)}; "
            f"graph_ids={_format_value(details.get('graph_ids', []))}; "
            f"graph_status={_safe_value(details.get('graph_status'))}; "
            f"graph_store={_safe_value(details.get('graph_store'))}; "
            f"entity_type_count={_int_value(details.get('entity_type_count'), fallback=0)}; "
            f"relation_type_count={_int_value(details.get('relation_type_count'), fallback=0)}"
        ),
        present=source_smoke_artifact.present,
        required=True,
        recommended_action=_recommended_action(status),
    )


def _build_graph_boundary_artifact(
    payload: dict[str, Any],
    source_smoke_artifact: Phase5GraphBoundarySmokeSummaryArtifact,
) -> Phase5GraphBoundarySmokeSummaryArtifact:
    graph_check = _check_from_payload(payload, "graph_planned_boundary")
    if graph_check is None:
        return Phase5GraphBoundarySmokeSummaryArtifact(
            id="graph_planned_boundary_summary",
            category="graph-smoke",
            path=str(PHASE5_PROVIDER_CONTRACT_SMOKE_PATH),
            status="blocked",
            summary="graph_planned_boundary check is missing.",
            present=source_smoke_artifact.present,
            required=True,
            recommended_action=_recommended_action("blocked"),
        )
    details = graph_check.get("details", {})
    passed = graph_check.get("passed") is True
    status = "ready" if (source_smoke_artifact.status == "ready" and passed) else "blocked"
    return Phase5GraphBoundarySmokeSummaryArtifact(
        id="graph_planned_boundary_summary",
        category="graph-smoke",
        path=str(PHASE5_PROVIDER_CONTRACT_SMOKE_PATH),
        status=status,
        summary=(
            f"error_code={_safe_value(details.get('error_code'))}; "
            f"graph_id={_safe_value(details.get('graph_id'))}; "
            f"status={_safe_value(details.get('status'))}; "
            f"capability_id={_safe_value(details.get('capability_id'))}"
        ),
        present=source_smoke_artifact.present,
        required=True,
        recommended_action=_recommended_action(status),
    )


def _summary_from_payload(
    payload: dict[str, Any],
    supporting_evidence: list[Phase5GraphBoundarySmokeSummaryArtifact],
) -> dict[str, Any]:
    source_smoke = payload.get("summary", {}) if isinstance(payload.get("summary"), dict) else {}
    graph_schema = _check_from_payload(payload, "graph_schema_discovery") or {}
    graph_boundary = _check_from_payload(payload, "graph_planned_boundary") or {}
    graph_schema_details = (
        graph_schema.get("details", {}) if isinstance(graph_schema.get("details"), dict) else {}
    )
    graph_boundary_details = (
        graph_boundary.get("details", {})
        if isinstance(graph_boundary.get("details"), dict)
        else {}
    )
    return {
        "total_artifacts": len(supporting_evidence),
        "ready_artifacts": sum(1 for item in supporting_evidence if item.status == "ready"),
        "review_artifacts": sum(1 for item in supporting_evidence if item.status == "review"),
        "blocked_artifacts": sum(1 for item in supporting_evidence if item.status == "blocked"),
        "required_artifacts": sum(1 for item in supporting_evidence if item.required),
        "required_ready_artifacts": sum(
            1 for item in supporting_evidence if item.required and item.status == "ready"
        ),
        "source_smoke_passed": payload.get("passed") is True,
        "smoke_checks_passed": _int_value(source_smoke.get("passed"), fallback=0)
        == _int_value(source_smoke.get("total"), fallback=0),
        "smoke_checks_total": _int_value(source_smoke.get("total"), fallback=0),
        "smoke_checks_ready": _int_value(source_smoke.get("passed"), fallback=0),
        "graph_checks_passed": int(
            (graph_schema.get("passed") is True) + (graph_boundary.get("passed") is True)
        ),
        "graph_schema_count": _int_value(graph_schema_details.get("graph_count"), fallback=0),
        "graph_ids": graph_schema_details.get("graph_ids", []),
        "graph_status": _safe_value(graph_schema_details.get("graph_status")),
        "graph_store": _safe_value(graph_schema_details.get("graph_store")),
        "entity_type_count": _int_value(graph_schema_details.get("entity_type_count"), fallback=0),
        "relation_type_count": _int_value(
            graph_schema_details.get("relation_type_count"),
            fallback=0,
        ),
        "graph_query_status": _safe_value(graph_boundary_details.get("status")),
        "graph_query_planned": _safe_value(graph_boundary_details.get("status")) == "planned",
        "graph_error_code": _safe_value(graph_boundary_details.get("error_code")),
    }


def _overall_status(
    supporting_evidence: list[Phase5GraphBoundarySmokeSummaryArtifact],
) -> str:
    if any(item.status == "blocked" and item.required for item in supporting_evidence):
        return "blocked"
    if any(item.status == "blocked" for item in supporting_evidence):
        return "blocked"
    if any(item.status == "review" for item in supporting_evidence):
        return "review"
    return "ready"


def _check_from_payload(payload: dict[str, Any], name: str) -> dict[str, Any] | None:
    checks = payload.get("checks", [])
    for check in checks:
        if isinstance(check, dict) and check.get("name") == name:
            return check
    return None


def _int_value(value: Any, *, fallback: int) -> int:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int) and value >= 0:
        return value
    return fallback


def _safe_value(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _format_value(value: Any) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return _safe_value(value)


def _recommended_action(status: str) -> str:
    if status == "ready":
        return "no_action_required"
    if status == "review":
        return "review_evidence_notes"
    return "regenerate_evidence"
