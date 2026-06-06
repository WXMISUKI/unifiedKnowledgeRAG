import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PROVIDER_WORKSTREAM_REBASELINE_ID = "provider-workstream-rebaseline-v1"
OUTPUT_JSON_FILENAME = "provider-workstream-rebaseline.json"
OUTPUT_MARKDOWN_FILENAME = "provider-workstream-rebaseline.md"


@dataclass(frozen=True)
class ProviderWorkstream:
    id: str
    status: str
    trigger_condition: str
    current_basis: str
    allowed_next_actions: list[str] = field(default_factory=list)
    non_goals: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ProviderWorkstreamRebaselineReport:
    id: str
    generated_at: str
    status: str
    decision: str
    summary: dict[str, Any]
    workstreams: list[ProviderWorkstream]
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_provider_workstream_rebaseline_report() -> ProviderWorkstreamRebaselineReport:
    workstreams = _default_workstreams()
    status_counts = _status_counts(workstreams)
    return ProviderWorkstreamRebaselineReport(
        id=PROVIDER_WORKSTREAM_REBASELINE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status="ready",
        decision="close_access_readiness_and_use_triggered_workstreams",
        summary={
            "access_readiness_status": "closed",
            "access_readiness_closure_basis": "phase24_go_and_phase25_no_provider_action_required",
            "continue_phase26_access_readiness": False,
            "runtime_promotion_status": "keep_runtime_defaults",
            "retrieval_backend_promotion_status": "candidate_only",
            "parser_expansion_status": "deferred_until_real_corpus_demand",
            "graphrag_execution_status": "deferred_until_relationship_heavy_use_case",
            "workstream_count": len(workstreams),
            "status_counts": status_counts,
        },
        workstreams=workstreams,
        notes=[
            "This report rebaselines future provider work after MyPrivateAgent access readiness closure.",
            "It does not call provider HTTP endpoints, refresh all evidence artifacts, change retrieval defaults, create source bindings, add parsers, rebuild indexes, or execute GraphRAG.",
            "Future provider changes should declare a concrete trigger condition instead of continuing the access-readiness phase chain.",
        ],
    )


def provider_workstream_rebaseline_report_to_dict(
    report: ProviderWorkstreamRebaselineReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_provider_workstream_rebaseline_markdown(
    report: ProviderWorkstreamRebaselineReport,
) -> str:
    lines = [
        "# Provider Workstream Rebaseline",
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
    ]
    for key, value in report.summary.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")

    lines.extend(
        [
            "",
            "## Workstreams",
            "",
            "| Workstream | Status | Trigger Condition | Current Basis | Allowed Next Actions |",
            "|---|---|---|---|---|",
        ]
    )
    for workstream in report.workstreams:
        lines.append(
            f"| `{workstream.id}` | `{workstream.status}` | "
            f"{workstream.trigger_condition} | {workstream.current_basis} | "
            f"`{_format_value(workstream.allowed_next_actions)}` |"
        )

    lines.extend(["", "## Boundary", ""])
    for workstream in report.workstreams:
        if workstream.non_goals:
            lines.append(f"- `{workstream.id}`: {_format_value(workstream.non_goals)}")

    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    return "\n".join(lines).rstrip() + "\n"


def export_provider_workstream_rebaseline_report(
    *,
    output_dir: Path = Path("docs/roadmap/provider-workstream-rebaseline"),
) -> ProviderWorkstreamRebaselineReport:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_provider_workstream_rebaseline_report()
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = ProviderWorkstreamRebaselineReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        decision=report.decision,
        summary=report.summary,
        workstreams=report.workstreams,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            provider_workstream_rebaseline_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_provider_workstream_rebaseline_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _default_workstreams() -> list[ProviderWorkstream]:
    return [
        ProviderWorkstream(
            id="myprivateagent_access_readiness",
            status="closed",
            trigger_condition="reopen_only_if_future_real_trial_exposes_provider_issue",
            current_basis="Phase 24 returned go and Phase 25 returned no_provider_action_required.",
            allowed_next_actions=[
                "do_not_open_phase26_access_readiness",
                "keep_phase25_feedback_as_closure_point",
            ],
            non_goals=[
                "new_readiness_chain",
                "caller_trial_execution",
                "source_binding_creation",
            ],
        ),
        ProviderWorkstream(
            id="provider_bugfix",
            status="active_if_triggered",
            trigger_condition="real_trial_bug_or_provider_failure_evidence",
            current_basis="No provider-owned blocker is present in the latest live trial feedback.",
            allowed_next_actions=[
                "open_focused_provider_fix_when_trial_blocker_is_provider_owned",
                "rerun_contract_smoke_after_fix",
            ],
            non_goals=[
                "speculative_refactor",
                "platform_governance",
            ],
        ),
        ProviderWorkstream(
            id="corpus_parser_expansion",
            status="deferred",
            trigger_condition="real_non_markdown_corpus_demand_or_unsupported_format_blocker",
            current_basis="Current source-format demand evidence keeps markdown baseline sufficient.",
            allowed_next_actions=[
                "collect_real_corpus_examples",
                "propose_parser_expansion_only_after_demand_signal",
            ],
            non_goals=[
                "ocr_pdf_word_excel_dependencies_without_demand",
                "automatic_ingestion_execution",
            ],
        ),
        ProviderWorkstream(
            id="retrieval_backend_promotion",
            status="candidate_only",
            trigger_condition="quality_citation_latency_deployment_and_operations_evidence_pass",
            current_basis="Qdrant, BGE-M3, hybrid retrieval, and pgvector remain review or candidate-only.",
            allowed_next_actions=[
                "continue_candidate_evaluation_when_evidence_is_available",
                "keep_runtime_defaults_until_promotion_gate_closes",
            ],
            non_goals=[
                "promote_backend_by_popularity",
                "change_runtime_defaults_from_single_metric",
            ],
        ),
        ProviderWorkstream(
            id="graphrag_execution",
            status="deferred",
            trigger_condition="relationship_heavy_use_case_with_graph_evidence_rules_and_operations_owner",
            current_basis="GraphRAG remains a planned boundary with schema discovery only.",
            allowed_next_actions=[
                "document_graph_heavy_use_case_before_execution",
                "keep_document_rag_for_single_source_citation_lookup",
            ],
            non_goals=[
                "neo4j_default_dependency",
                "ontology_workflow_without_use_case",
                "graph_query_execution_by_default",
            ],
        ),
        ProviderWorkstream(
            id="deployment_operations",
            status="active_if_triggered",
            trigger_condition="deployment_owner_request_or_real_deployment_environment",
            current_basis="Deployment readiness remains review because local defaults still use fixture/mock posture.",
            allowed_next_actions=[
                "run_deployed_smoke_when_live_environment_exists",
                "configure_api_key_or_model_artifacts_only_when_deployment_owner_needs_them",
            ],
            non_goals=[
                "registration_governance",
                "heartbeat_policy",
                "managed_secrets_platform",
            ],
        ),
    ]


def _status_counts(workstreams: list[ProviderWorkstream]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for workstream in workstreams:
        counts[workstream.status] = counts.get(workstream.status, 0) + 1
    return counts


def _format_value(value: Any) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)
