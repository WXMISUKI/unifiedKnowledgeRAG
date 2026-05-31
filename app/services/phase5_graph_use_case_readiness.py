import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.services.provider_preflight import build_provider_preflight_response


PHASE5_GRAPH_USE_CASE_READINESS_ID = "phase5-graph-use-case-readiness-v1"
PHASE5_GRAPH_USE_CASE_CONTRACT_PATH = Path(
    "docs/benchmark/chinese-seed/graph-use-case-readiness/"
    "phase5-graph-use-case-readiness-contract.md"
)
PHASE5_PROVIDER_CONTRACT_SMOKE_JSON = Path(
    "docs/smoke/provider-contract/provider-contract-smoke.json"
)
PHASE5_GRAPH_USE_CASE_READINESS_JSON = "phase5-graph-use-case-readiness.json"
PHASE5_GRAPH_USE_CASE_READINESS_MARKDOWN = "phase5-graph-use-case-readiness.md"


@dataclass(frozen=True)
class Phase5GraphUseCaseReadinessArtifact:
    id: str
    category: str
    path: str
    status: str
    summary: str
    present: bool
    required: bool
    recommended_action: str


@dataclass(frozen=True)
class Phase5GraphUseCaseReadinessReport:
    id: str
    generated_at: str
    status: str
    decision: str
    contract_path: str
    preflight_path: str
    smoke_report_path: str
    summary: dict[str, Any]
    supporting_evidence: list[Phase5GraphUseCaseReadinessArtifact]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase5_graph_use_case_readiness_report(
    *,
    base_dir: Path = Path("."),
) -> Phase5GraphUseCaseReadinessReport:
    preflight = build_provider_preflight_response()
    graph_boundary = _graph_boundary_check(preflight.checks)
    graph_boundary_details = graph_boundary.details if isinstance(graph_boundary.details, dict) else {}

    contract_artifact = _build_contract_doc_artifact(base_dir)
    preflight_artifact = _build_preflight_artifact(graph_boundary_details, graph_boundary.passed)
    smoke_artifact, smoke_payload = _build_smoke_artifact(base_dir)

    supporting_evidence = [
        contract_artifact,
        preflight_artifact,
        smoke_artifact,
    ]
    summary = _readiness_summary(
        supporting_evidence,
        graph_boundary_details,
        smoke_payload,
    )
    return Phase5GraphUseCaseReadinessReport(
        id=PHASE5_GRAPH_USE_CASE_READINESS_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=_overall_status(supporting_evidence),
        decision="keep_graph_query_planned",
        contract_path=str(PHASE5_GRAPH_USE_CASE_CONTRACT_PATH),
        preflight_path="/api/provider/preflight",
        smoke_report_path=str(PHASE5_PROVIDER_CONTRACT_SMOKE_JSON),
        summary=summary,
        supporting_evidence=supporting_evidence,
        notes=[
            "This report is local, read-only evidence for Phase 5 graph boundary review.",
            "It consolidates the graph use-case contract, provider preflight graph boundary, and provider contract smoke evidence.",
            "It does not change runtime defaults, add graph execution, or introduce graph-store dependencies.",
        ],
    )


def phase5_graph_use_case_readiness_report_to_dict(
    report: Phase5GraphUseCaseReadinessReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase5_graph_use_case_readiness_markdown(
    report: Phase5GraphUseCaseReadinessReport,
) -> str:
    status = "passed" if report.status == "ready" else report.status
    lines = [
        "# Phase 5 Graph Use-Case Readiness Report",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{status}`",
        f"- Decision: `{report.decision}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Contract Doc: `{report.contract_path}`",
        f"- Preflight Snapshot: `{report.preflight_path}`",
        f"- Smoke Report: `{report.smoke_report_path}`",
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
        f"| Graph Schema Count | `{report.summary['graph_schema_count']}` |",
        f"| Graph Query Status | `{report.summary['graph_query_status']}` |",
        f"| Graph Query Planned | `{report.summary['graph_query_planned']}` |",
        f"| Preflight Graph Boundary Ready | `{report.summary['preflight_graph_boundary_ready']}` |",
        f"| Smoke Graph Check Passed | `{report.summary['smoke_graph_check_passed']}` |",
        f"| Smoke Checks Passed | `{report.summary['smoke_checks_passed']}` |",
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


def export_phase5_graph_use_case_readiness_report(
    output_dir: Path = Path("docs/benchmark/chinese-seed/graph-use-case-readiness"),
    *,
    base_dir: Path = Path("."),
) -> Phase5GraphUseCaseReadinessReport:
    report = build_phase5_graph_use_case_readiness_report(base_dir=base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PHASE5_GRAPH_USE_CASE_READINESS_JSON
    markdown_path = output_dir / PHASE5_GRAPH_USE_CASE_READINESS_MARKDOWN
    exported_report = Phase5GraphUseCaseReadinessReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        contract_path=report.contract_path,
        preflight_path=report.preflight_path,
        smoke_report_path=report.smoke_report_path,
        summary=report.summary,
        supporting_evidence=report.supporting_evidence,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase5_graph_use_case_readiness_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase5_graph_use_case_readiness_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _build_contract_doc_artifact(base_dir: Path) -> Phase5GraphUseCaseReadinessArtifact:
    path = base_dir / PHASE5_GRAPH_USE_CASE_CONTRACT_PATH
    if not path.exists():
        return Phase5GraphUseCaseReadinessArtifact(
            id="graph_use_case_contract_doc",
            category="contract",
            path=str(PHASE5_GRAPH_USE_CASE_CONTRACT_PATH),
            status="blocked",
            summary="Graph use-case readiness contract document is missing.",
            present=False,
            required=True,
            recommended_action="regenerate_graph_use_case_contract_doc",
        )
    return Phase5GraphUseCaseReadinessArtifact(
        id="graph_use_case_contract_doc",
        category="contract",
        path=str(PHASE5_GRAPH_USE_CASE_CONTRACT_PATH),
        status="ready",
        summary="contract_doc_present=True",
        present=True,
        required=True,
        recommended_action="no_action_required",
    )


def _build_preflight_artifact(
    graph_boundary_details: dict[str, Any],
    graph_boundary_passed: bool,
) -> Phase5GraphUseCaseReadinessArtifact:
    graph_schema_count = _int_value(graph_boundary_details.get("graph_schema_count"), fallback=0)
    graph_ids = graph_boundary_details.get("graph_ids", [])
    graph_stores = graph_boundary_details.get("graph_stores", {})
    capability_status = _safe_value(graph_boundary_details.get("capability_status"))
    execution_status = _safe_value(graph_boundary_details.get("execution_status"))
    status = "ready" if graph_boundary_passed else "blocked"
    return Phase5GraphUseCaseReadinessArtifact(
        id="provider_preflight_graph_boundary",
        category="runtime-snapshot",
        path="/api/provider/preflight",
        status=status,
        summary=(
            f"graph_schema_count={graph_schema_count}; "
            f"graph_ids={_format_value(graph_ids)}; "
            f"graph_stores={_format_value(graph_stores)}; "
            f"graph_query_status={capability_status}; "
            f"execution_status={execution_status}"
        ),
        present=True,
        required=True,
        recommended_action=_recommended_action(status),
    )


def _build_smoke_artifact(
    base_dir: Path,
) -> tuple[Phase5GraphUseCaseReadinessArtifact, dict[str, Any]]:
    path = base_dir / PHASE5_PROVIDER_CONTRACT_SMOKE_JSON
    if not path.exists():
        return (
            Phase5GraphUseCaseReadinessArtifact(
                id="provider_contract_smoke",
                category="smoke",
                path=str(PHASE5_PROVIDER_CONTRACT_SMOKE_JSON),
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
    graph_check = _graph_smoke_check(payload)
    graph_check_passed = graph_check is not None and graph_check.get("passed") is True
    graph_query_status = _safe_value(
        (graph_check.get("details", {}) if graph_check is not None else {}).get("status")
    )
    graph_error_code = _safe_value(
        (graph_check.get("details", {}) if graph_check is not None else {}).get("error_code")
    )
    status = "ready" if passed else "blocked"
    return (
        Phase5GraphUseCaseReadinessArtifact(
            id="provider_contract_smoke",
            category="smoke",
            path=str(PHASE5_PROVIDER_CONTRACT_SMOKE_JSON),
            status=status,
            summary=(
                f"passed={passed}; checks={passed_count}/{total}; failed_checks={failed_count}; "
                f"graph_check_status={'passed' if graph_check_passed else 'failed'}; "
                f"graph_query_status={graph_query_status}; graph_error_code={graph_error_code}"
            ),
            present=True,
            required=True,
            recommended_action=_recommended_action(status),
        ),
        payload,
    )


def _readiness_summary(
    supporting_evidence: list[Phase5GraphUseCaseReadinessArtifact],
    graph_boundary_details: dict[str, Any],
    smoke_payload: dict[str, Any],
) -> dict[str, Any]:
    smoke_summary = smoke_payload.get("summary", {}) if isinstance(smoke_payload.get("summary"), dict) else {}
    smoke_checks_passed = bool(smoke_payload.get("passed") is True)
    smoke_check = _graph_smoke_check(smoke_payload)
    graph_schema_count = _int_value(graph_boundary_details.get("graph_schema_count"), fallback=0)
    graph_query_status = _safe_value(graph_boundary_details.get("capability_status"))
    graph_query_planned = _safe_value(graph_boundary_details.get("execution_status")) == "planned"
    return {
        "total_artifacts": len(supporting_evidence),
        "ready_artifacts": sum(1 for item in supporting_evidence if item.status == "ready"),
        "review_artifacts": sum(1 for item in supporting_evidence if item.status == "review"),
        "blocked_artifacts": sum(1 for item in supporting_evidence if item.status == "blocked"),
        "required_artifacts": sum(1 for item in supporting_evidence if item.required),
        "required_ready_artifacts": sum(
            1 for item in supporting_evidence if item.required and item.status == "ready"
        ),
        "graph_schema_count": graph_schema_count,
        "graph_ids": graph_boundary_details.get("graph_ids", []),
        "graph_stores": graph_boundary_details.get("graph_stores", {}),
        "graph_query_status": graph_query_status,
        "graph_query_planned": graph_query_planned,
        "preflight_graph_boundary_ready": True,
        "smoke_checks_passed": smoke_checks_passed,
        "smoke_check_count": _int_value(smoke_summary.get("passed"), fallback=0),
        "smoke_graph_check_passed": smoke_check is not None and smoke_check.get("passed") is True,
    }


def _overall_status(
    supporting_evidence: list[Phase5GraphUseCaseReadinessArtifact],
) -> str:
    if any(item.status == "blocked" and item.required for item in supporting_evidence):
        return "blocked"
    if any(item.status == "blocked" for item in supporting_evidence):
        return "blocked"
    if any(item.status == "review" for item in supporting_evidence):
        return "review"
    return "ready"


def _graph_boundary_check(checks: list[Any]) -> Any:
    for check in checks:
        if getattr(check, "name", None) == "graph_boundary":
            return check
    raise RuntimeError("Provider preflight graph boundary check is missing.")


def _graph_smoke_check(payload: dict[str, Any]) -> dict[str, Any] | None:
    checks = payload.get("checks", [])
    for check in checks:
        if isinstance(check, dict) and check.get("name") == "graph_planned_boundary":
            details = check.get("details", {})
            return {
                "passed": check.get("passed") is True,
                "details": details if isinstance(details, dict) else {},
            }
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
