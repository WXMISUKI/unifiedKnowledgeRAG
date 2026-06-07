import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from app.services.approved_local_corpus_acceptance_smoke import DEFAULT_TOP_K
from app.services.local_approved_source_ingestion_loop import (
    export_local_approved_source_ingestion_loop_report,
)
from app.services.local_business_corpus_trial import DEFAULT_QUERY
from app.services.normalized_parser_artifact_ingestion_boundary import (
    DEFAULT_ARTIFACT_PATH,
    export_normalized_parser_artifact_ingestion_boundary_report,
)


PARSER_ARTIFACT_LOCAL_INGESTION_LOOP_ID = "parser-artifact-local-ingestion-loop-v1"
DEFAULT_OUTPUT_DIR = Path("docs/local-run/parser-artifact-local-ingestion-loop")
OUTPUT_JSON_FILENAME = "parser-artifact-local-ingestion-loop.json"
OUTPUT_MARKDOWN_FILENAME = "parser-artifact-local-ingestion-loop.md"


@dataclass(frozen=True)
class ParserArtifactLocalIngestionStep:
    id: str
    status: str
    reason_code: str
    artifacts: dict[str, str | None]
    summary: dict[str, Any]


@dataclass(frozen=True)
class ParserArtifactLocalIngestionLoopReport:
    id: str
    generated_at: str
    decision: str
    reason_code: str
    artifact_path: Path
    artifact_id: str | None
    source_id: str | None
    title: str | None
    parser_id: str | None
    materialized_markdown_path: Path | None
    source_overlay_path: Path | None
    query: str
    top_k: int
    steps: list[ParserArtifactLocalIngestionStep]
    summary: dict[str, Any]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


def export_parser_artifact_local_ingestion_loop_report(
    *,
    artifact_path: Path = DEFAULT_ARTIFACT_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    query: str = DEFAULT_QUERY,
    top_k: int = DEFAULT_TOP_K,
    artifact_boundary_exporter: Callable[..., Any] = export_normalized_parser_artifact_ingestion_boundary_report,
    ingestion_loop_exporter: Callable[..., Any] = export_local_approved_source_ingestion_loop_report,
) -> ParserArtifactLocalIngestionLoopReport:
    report = run_parser_artifact_local_ingestion_loop(
        artifact_path=artifact_path,
        output_dir=output_dir,
        query=query,
        top_k=top_k,
        artifact_boundary_exporter=artifact_boundary_exporter,
        ingestion_loop_exporter=ingestion_loop_exporter,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = ParserArtifactLocalIngestionLoopReport(
        id=report.id,
        generated_at=report.generated_at,
        decision=report.decision,
        reason_code=report.reason_code,
        artifact_path=report.artifact_path,
        artifact_id=report.artifact_id,
        source_id=report.source_id,
        title=report.title,
        parser_id=report.parser_id,
        materialized_markdown_path=report.materialized_markdown_path,
        source_overlay_path=report.source_overlay_path,
        query=report.query,
        top_k=report.top_k,
        steps=report.steps,
        summary=report.summary,
        recommended_actions=report.recommended_actions,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            parser_artifact_local_ingestion_loop_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_parser_artifact_local_ingestion_loop_markdown(exported),
        encoding="utf-8",
    )
    return exported


def run_parser_artifact_local_ingestion_loop(
    *,
    artifact_path: Path = DEFAULT_ARTIFACT_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    query: str = DEFAULT_QUERY,
    top_k: int = DEFAULT_TOP_K,
    artifact_boundary_exporter: Callable[..., Any] = export_normalized_parser_artifact_ingestion_boundary_report,
    ingestion_loop_exporter: Callable[..., Any] = export_local_approved_source_ingestion_loop_report,
) -> ParserArtifactLocalIngestionLoopReport:
    output_dir.mkdir(parents=True, exist_ok=True)
    steps: list[ParserArtifactLocalIngestionStep] = []
    artifact_report = artifact_boundary_exporter(
        artifact_path=artifact_path,
        output_dir=output_dir / "normalized-parser-artifact-boundary",
    )
    steps.append(_artifact_step(artifact_report))
    if artifact_report.decision != "go":
        decision = "review" if artifact_report.decision == "review" else "blocked"
        return _report(
            decision=decision,
            reason_code=f"parser_artifact_boundary_{decision}",
            artifact_path=Path(artifact_path),
            artifact_id=getattr(artifact_report, "artifact_id", None),
            source_id=getattr(artifact_report, "source_id", None),
            title=getattr(artifact_report, "title", None),
            parser_id=getattr(artifact_report, "parser_id", None),
            materialized_markdown_path=getattr(artifact_report, "markdown_artifact_path", None),
            source_overlay_path=getattr(artifact_report, "source_overlay_path", None),
            query=query,
            top_k=top_k,
            steps=steps,
        )

    markdown_path = getattr(artifact_report, "markdown_artifact_path", None)
    source_id = getattr(artifact_report, "source_id", None)
    title = getattr(artifact_report, "title", None)
    if markdown_path is None or source_id is None or title is None:
        return _report(
            decision="blocked",
            reason_code="parser_artifact_boundary_missing_ingestion_inputs",
            artifact_path=Path(artifact_path),
            artifact_id=getattr(artifact_report, "artifact_id", None),
            source_id=source_id,
            title=title,
            parser_id=getattr(artifact_report, "parser_id", None),
            materialized_markdown_path=markdown_path,
            source_overlay_path=getattr(artifact_report, "source_overlay_path", None),
            query=query,
            top_k=top_k,
            steps=steps,
        )

    ingestion_report = ingestion_loop_exporter(
        markdown_path=Path(markdown_path),
        source_id=str(source_id),
        title=str(title),
        query=query,
        top_k=top_k,
        output_dir=output_dir / "approved-source-ingestion-loop",
    )
    steps.append(_ingestion_step(ingestion_report))
    if ingestion_report.decision != "go":
        decision = "review" if ingestion_report.decision == "review" else "blocked"
        return _report(
            decision=decision,
            reason_code=f"approved_source_ingestion_loop_{decision}",
            artifact_path=Path(artifact_path),
            artifact_id=getattr(artifact_report, "artifact_id", None),
            source_id=str(source_id),
            title=str(title),
            parser_id=getattr(artifact_report, "parser_id", None),
            materialized_markdown_path=Path(markdown_path),
            source_overlay_path=getattr(artifact_report, "source_overlay_path", None),
            query=query,
            top_k=top_k,
            steps=steps,
        )

    return _report(
        decision="go",
        reason_code="parser_artifact_local_ingestion_ready",
        artifact_path=Path(artifact_path),
        artifact_id=getattr(artifact_report, "artifact_id", None),
        source_id=str(source_id),
        title=str(title),
        parser_id=getattr(artifact_report, "parser_id", None),
        materialized_markdown_path=Path(markdown_path),
        source_overlay_path=getattr(artifact_report, "source_overlay_path", None),
        query=query,
        top_k=top_k,
        steps=steps,
    )


def parser_artifact_local_ingestion_loop_report_to_dict(
    report: ParserArtifactLocalIngestionLoopReport,
) -> dict[str, Any]:
    payload = asdict(report)
    for key in [
        "artifact_path",
        "materialized_markdown_path",
        "source_overlay_path",
        "json_path",
        "markdown_path",
    ]:
        if payload[key] is not None:
            payload[key] = str(payload[key])
    return payload


def render_parser_artifact_local_ingestion_loop_markdown(
    report: ParserArtifactLocalIngestionLoopReport,
) -> str:
    lines = [
        "# Parser Artifact Local Ingestion Loop",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Artifact Path: `{report.artifact_path}`",
        f"- Artifact ID: `{report.artifact_id}`",
        f"- Source ID: `{report.source_id}`",
        f"- Parser ID: `{report.parser_id}`",
        f"- Materialized Markdown: `{report.materialized_markdown_path}`",
        f"- Source Overlay: `{report.source_overlay_path}`",
        "",
        "## Steps",
        "",
        "| Step | Status | Reason | Artifacts |",
        "|---|---|---|---|",
    ]
    for step in report.steps:
        artifacts = ", ".join(
            f"{key}={value}" for key, value in step.artifacts.items() if value
        ) or "n/a"
        lines.append(
            f"| `{step.id}` | `{step.status}` | `{step.reason_code}` | `{artifacts}` |"
        )
    lines.extend(["", "## Summary", "", "| Metric | Value |", "|---|---|"])
    for key, value in report.summary.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in report.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def _report(
    *,
    decision: str,
    reason_code: str,
    artifact_path: Path,
    artifact_id: str | None,
    source_id: str | None,
    title: str | None,
    parser_id: str | None,
    materialized_markdown_path: Path | None,
    source_overlay_path: Path | None,
    query: str,
    top_k: int,
    steps: list[ParserArtifactLocalIngestionStep],
) -> ParserArtifactLocalIngestionLoopReport:
    return ParserArtifactLocalIngestionLoopReport(
        id=PARSER_ARTIFACT_LOCAL_INGESTION_LOOP_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision=decision,
        reason_code=reason_code,
        artifact_path=artifact_path,
        artifact_id=artifact_id,
        source_id=source_id,
        title=title,
        parser_id=parser_id,
        materialized_markdown_path=materialized_markdown_path,
        source_overlay_path=source_overlay_path,
        query=query,
        top_k=top_k,
        steps=steps,
        summary={
            "step_count": len(steps),
            "artifact_materialized": materialized_markdown_path is not None,
            "approved_source_ingestion_decision": _step_status(
                steps,
                "approved_source_ingestion_loop",
            ),
            "source_binding_status": "not_created",
            "runtime_promotion_status": "keep_runtime_defaults",
            "raw_parser_execution_status": "not_executed",
            "ocr_service_status": "not_started",
            "myprivateagent_call_status": "not_called",
            "vector_database_status": "not_promoted",
            "graph_execution_status": "not_executed",
            "final_decision": decision,
        },
        recommended_actions=_recommended_actions(decision),
        non_goals=_non_goals(),
    )


def _artifact_step(report: Any) -> ParserArtifactLocalIngestionStep:
    return ParserArtifactLocalIngestionStep(
        id="parser_artifact_boundary",
        status=str(report.decision),
        reason_code=str(report.reason_code),
        artifacts={
            "json": _path_string(getattr(report, "json_path", None)),
            "markdown": _path_string(getattr(report, "markdown_path", None)),
            "materialized_markdown": _path_string(
                getattr(report, "markdown_artifact_path", None)
            ),
            "source_overlay": _path_string(getattr(report, "source_overlay_path", None)),
        },
        summary=dict(getattr(report, "summary", {}) or {}),
    )


def _ingestion_step(report: Any) -> ParserArtifactLocalIngestionStep:
    return ParserArtifactLocalIngestionStep(
        id="approved_source_ingestion_loop",
        status=str(report.decision),
        reason_code=str(report.reason_code),
        artifacts={
            "json": _path_string(getattr(report, "json_path", None)),
            "markdown": _path_string(getattr(report, "markdown_path_out", None)),
        },
        summary=dict(getattr(report, "summary", {}) or {}),
    )


def _step_status(
    steps: list[ParserArtifactLocalIngestionStep],
    step_id: str,
) -> str | None:
    for step in steps:
        if step.id == step_id:
            return step.status
    return None


def _recommended_actions(decision: str) -> list[str]:
    if decision == "go":
        return [
            "use_parser_derived_source_for_local_business_rag_trial",
            "keep_parser_engines_outside_provider_defaults",
            "evaluate_retrieval_quality_with_customer_like_cases_next",
        ]
    if decision == "review":
        return [
            "review_parser_artifact_citations_or_ingestion_smoke",
            "rerun_parser_artifact_local_ingestion_loop_after_adjustment",
        ]
    return [
        "inspect_blocking_step_reason_code",
        "fix_parser_artifact_or_ingestion_blocker",
        "rerun_parser_artifact_local_ingestion_loop",
    ]


def _non_goals() -> list[str]:
    return [
        "does_not_parse_raw_pdf",
        "does_not_start_ocr_services",
        "does_not_call_paddleocr_or_parser_engines",
        "does_not_call_myprivateagent",
        "does_not_create_source_to_agent_binding",
        "does_not_mutate_chat_runtime",
        "does_not_promote_retrieval_backend",
        "does_not_promote_vector_database",
        "does_not_execute_graphrag",
    ]


def _path_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _format_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
