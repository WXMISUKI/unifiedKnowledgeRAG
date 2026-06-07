import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from app.models.contracts import IndexLifecycleJob, IndexStatusResponse
from app.services.approved_local_corpus_acceptance_smoke import (
    DEFAULT_TOP_K,
    export_approved_local_corpus_acceptance_smoke,
)
from app.services.index_lifecycle import create_ingestion_job, get_index_status
from app.services.ingestion_preflight import get_ingestion_source_preflight
from app.services.local_business_corpus_trial import (
    DEFAULT_MARKDOWN_PATH,
    DEFAULT_QUERY,
    DEFAULT_SOURCE_ID,
    DEFAULT_TITLE,
)
from app.services.local_document_source_onboarding import (
    export_local_document_source_onboarding_report,
)


LOCAL_APPROVED_SOURCE_INGESTION_LOOP_ID = "local-approved-source-ingestion-loop-v1"
DEFAULT_OUTPUT_DIR = Path("docs/local-run/approved-source-ingestion-loop")
OUTPUT_JSON_FILENAME = "local-approved-source-ingestion-loop.json"
OUTPUT_MARKDOWN_FILENAME = "local-approved-source-ingestion-loop.md"


@dataclass(frozen=True)
class IngestionLoopStep:
    id: str
    status: str
    reason_code: str
    artifacts: dict[str, str | None]
    summary: dict[str, Any]


@dataclass(frozen=True)
class LocalApprovedSourceIngestionLoopReport:
    id: str
    generated_at: str
    decision: str
    reason_code: str
    source_id: str
    title: str
    markdown_path: Path
    query: str
    top_k: int
    steps: list[IngestionLoopStep]
    summary: dict[str, Any]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path_out: Path | None = None


def export_local_approved_source_ingestion_loop_report(
    *,
    markdown_path: Path = DEFAULT_MARKDOWN_PATH,
    source_id: str = DEFAULT_SOURCE_ID,
    title: str = DEFAULT_TITLE,
    query: str = DEFAULT_QUERY,
    top_k: int = DEFAULT_TOP_K,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    onboarding_exporter: Callable[..., Any] = export_local_document_source_onboarding_report,
    preflight_getter: Callable[..., Any] = get_ingestion_source_preflight,
    ingestion_job_creator: Callable[..., Any] = create_ingestion_job,
    index_status_getter: Callable[..., Any] = get_index_status,
    acceptance_exporter: Callable[..., Any] = export_approved_local_corpus_acceptance_smoke,
) -> LocalApprovedSourceIngestionLoopReport:
    report = run_local_approved_source_ingestion_loop(
        markdown_path=markdown_path,
        source_id=source_id,
        title=title,
        query=query,
        top_k=top_k,
        output_dir=output_dir,
        onboarding_exporter=onboarding_exporter,
        preflight_getter=preflight_getter,
        ingestion_job_creator=ingestion_job_creator,
        index_status_getter=index_status_getter,
        acceptance_exporter=acceptance_exporter,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path_out = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = LocalApprovedSourceIngestionLoopReport(
        id=report.id,
        generated_at=report.generated_at,
        decision=report.decision,
        reason_code=report.reason_code,
        source_id=report.source_id,
        title=report.title,
        markdown_path=report.markdown_path,
        query=report.query,
        top_k=report.top_k,
        steps=report.steps,
        summary=report.summary,
        recommended_actions=report.recommended_actions,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path_out=markdown_path_out,
    )
    json_path.write_text(
        json.dumps(local_approved_source_ingestion_loop_report_to_dict(exported), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    markdown_path_out.write_text(
        render_local_approved_source_ingestion_loop_markdown(exported),
        encoding="utf-8",
    )
    return exported


def run_local_approved_source_ingestion_loop(
    *,
    markdown_path: Path = DEFAULT_MARKDOWN_PATH,
    source_id: str = DEFAULT_SOURCE_ID,
    title: str = DEFAULT_TITLE,
    query: str = DEFAULT_QUERY,
    top_k: int = DEFAULT_TOP_K,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    onboarding_exporter: Callable[..., Any] = export_local_document_source_onboarding_report,
    preflight_getter: Callable[..., Any] = get_ingestion_source_preflight,
    ingestion_job_creator: Callable[..., Any] = create_ingestion_job,
    index_status_getter: Callable[..., Any] = get_index_status,
    acceptance_exporter: Callable[..., Any] = export_approved_local_corpus_acceptance_smoke,
) -> LocalApprovedSourceIngestionLoopReport:
    output_dir.mkdir(parents=True, exist_ok=True)
    steps: list[IngestionLoopStep] = []

    onboarding = onboarding_exporter(
        markdown_path=markdown_path,
        source_id=source_id,
        title=title,
        query=query,
        top_k=top_k,
        output_dir=output_dir / "document-source-onboarding",
    )
    steps.append(_onboarding_step(onboarding))
    if onboarding.decision != "go":
        decision = "review" if onboarding.decision == "review" else "blocked"
        return _report(decision=decision, reason_code=f"onboarding_{decision}", source_id=source_id, title=title, markdown_path=Path(markdown_path), query=query, top_k=top_k, steps=steps)

    preflight = preflight_getter(source_id)
    steps.append(_preflight_step(preflight))
    preflight_status = _preflight_status(preflight)
    if preflight_status != "ready":
        return _report(decision="blocked", reason_code="ingestion_preflight_blocked", source_id=source_id, title=title, markdown_path=Path(markdown_path), query=query, top_k=top_k, steps=steps)

    ok, job, error = ingestion_job_creator(source_id)
    steps.append(_ingestion_job_step(ok, job, error))
    if not ok or job is None or getattr(job, "status", None) != "completed":
        return _report(decision="blocked", reason_code="ingestion_job_blocked", source_id=source_id, title=title, markdown_path=Path(markdown_path), query=query, top_k=top_k, steps=steps)

    index_status = index_status_getter(source_id)
    steps.append(_index_status_step(index_status))
    if getattr(index_status, "status", None) != "ready":
        return _report(decision="blocked", reason_code="index_status_not_ready", source_id=source_id, title=title, markdown_path=Path(markdown_path), query=query, top_k=top_k, steps=steps)

    acceptance = acceptance_exporter(
        source_id=source_id,
        top_k=top_k,
        output_dir=output_dir / "approved-local-corpus-acceptance",
    )
    steps.append(_acceptance_step(acceptance))
    if acceptance.decision != "go":
        decision = "review" if acceptance.decision == "review" else "blocked"
        return _report(decision=decision, reason_code=f"acceptance_smoke_{decision}", source_id=source_id, title=title, markdown_path=Path(markdown_path), query=query, top_k=top_k, steps=steps)

    return _report(decision="go", reason_code="local_approved_source_ingestion_ready", source_id=source_id, title=title, markdown_path=Path(markdown_path), query=query, top_k=top_k, steps=steps)


def local_approved_source_ingestion_loop_report_to_dict(
    report: LocalApprovedSourceIngestionLoopReport,
) -> dict[str, Any]:
    payload = asdict(report)
    for key in ["markdown_path", "json_path", "markdown_path_out"]:
        if payload[key] is not None:
            payload[key] = str(payload[key])
    return payload


def render_local_approved_source_ingestion_loop_markdown(
    report: LocalApprovedSourceIngestionLoopReport,
) -> str:
    lines = [
        "# Local Approved Source Ingestion Loop",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Source ID: `{report.source_id}`",
        f"- Title: `{report.title}`",
        f"- Markdown Path: `{report.markdown_path}`",
        f"- Query: `{report.query}`",
        "",
        "## Steps",
        "",
        "| Step | Status | Reason | Artifacts |",
        "|---|---|---|---|",
    ]
    for step in report.steps:
        artifacts = ", ".join(f"{key}={value}" for key, value in step.artifacts.items() if value) or "n/a"
        lines.append(f"| `{step.id}` | `{step.status}` | `{step.reason_code}` | `{artifacts}` |")
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
    source_id: str,
    title: str,
    markdown_path: Path,
    query: str,
    top_k: int,
    steps: list[IngestionLoopStep],
) -> LocalApprovedSourceIngestionLoopReport:
    return LocalApprovedSourceIngestionLoopReport(
        id=LOCAL_APPROVED_SOURCE_INGESTION_LOOP_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision=decision,
        reason_code=reason_code,
        source_id=source_id,
        title=title,
        markdown_path=markdown_path,
        query=query,
        top_k=top_k,
        steps=steps,
        summary={
            "step_count": len(steps),
            "ready_step_count": sum(1 for step in steps if step.status in {"go", "ready", "completed"}),
            "review_step_count": sum(1 for step in steps if step.status == "review"),
            "blocked_step_count": sum(1 for step in steps if step.status in {"blocked", "failed", "not_ready", "unknown"}),
            "final_decision": decision,
            "explicit_ingestion_job_created": any(step.id == "ingestion_job" for step in steps),
            "source_binding_status": "not_created",
            "runtime_promotion_status": "keep_runtime_defaults",
            "graph_execution_status": "not_executed",
        },
        recommended_actions=_recommended_actions(decision),
        non_goals=_non_goals(),
    )


def _onboarding_step(onboarding: Any) -> IngestionLoopStep:
    return IngestionLoopStep(
        id="document_source_onboarding",
        status=str(onboarding.decision),
        reason_code=str(onboarding.reason_code),
        artifacts={
            "json": _path_string(getattr(onboarding, "json_path", None)),
            "markdown": _path_string(getattr(onboarding, "markdown_path_out", None)),
        },
        summary=dict(getattr(onboarding, "summary", {}) or {}),
    )


def _preflight_step(preflight: Any) -> IngestionLoopStep:
    if getattr(preflight, "ok", False) is not True:
        error = getattr(preflight, "error", None)
        return IngestionLoopStep(
            id="ingestion_preflight",
            status="blocked",
            reason_code=str(getattr(error, "code", None) or "preflight_not_ok"),
            artifacts={},
            summary={"ok": False},
        )
    result = getattr(preflight, "result", None)
    status = str(getattr(result, "status", "") or "unknown")
    return IngestionLoopStep(
        id="ingestion_preflight",
        status=status,
        reason_code="preflight_ready" if status == "ready" else "preflight_not_ready",
        artifacts={},
        summary={
            "source_id": getattr(result, "source_id", None),
            "retrieval_backend": getattr(result, "retrieval_backend", None),
            "index_status": getattr(result, "index_status", None),
            "latest_index_job_id": getattr(result, "latest_index_job_id", None),
            "document_count": len(getattr(result, "documents", []) or []),
            "recommended_action": getattr(result, "recommended_action", None),
        },
    )


def _preflight_status(preflight: Any) -> str:
    if getattr(preflight, "ok", False) is not True:
        return "blocked"
    result = getattr(preflight, "result", None)
    return str(getattr(result, "status", "") or "blocked")


def _ingestion_job_step(ok: bool, job: IndexLifecycleJob | None, error: Any) -> IngestionLoopStep:
    if not ok or job is None:
        return IngestionLoopStep(
            id="ingestion_job",
            status="blocked",
            reason_code=str(getattr(error, "code", None) or "ingestion_job_not_created"),
            artifacts={},
            summary={"ok": False},
        )
    status = str(job.status)
    return IngestionLoopStep(
        id="ingestion_job",
        status=status,
        reason_code="ingestion_job_completed" if status == "completed" else "ingestion_job_not_completed",
        artifacts={},
        summary={
            "job_id": job.job_id,
            "source_id": job.source_id,
            "status": job.status,
            "requested_at": job.requested_at,
            "completed_at": job.completed_at,
            "error_code": getattr(job.error, "code", None) if job.error else None,
        },
    )


def _index_status_step(index_status: IndexStatusResponse) -> IngestionLoopStep:
    status = str(index_status.status)
    return IngestionLoopStep(
        id="index_status",
        status=status,
        reason_code="index_ready" if status == "ready" else "index_not_ready",
        artifacts={},
        summary={
            "source_id": index_status.source_id,
            "status": index_status.status,
            "backend": index_status.backend,
            "indexed_at": index_status.indexed_at,
            "latest_job_id": index_status.latest_job_id,
            "reason": index_status.reason,
            "error_code": getattr(index_status.error, "code", None) if index_status.error else None,
        },
    )


def _acceptance_step(acceptance: Any) -> IngestionLoopStep:
    return IngestionLoopStep(
        id="acceptance_smoke",
        status=str(acceptance.decision),
        reason_code=str(acceptance.reason_code),
        artifacts={
            "json": _path_string(getattr(acceptance, "json_path", None)),
            "markdown": _path_string(getattr(acceptance, "markdown_path", None)),
        },
        summary=dict(getattr(acceptance, "summary", {}) or {}),
    )


def _recommended_actions(decision: str) -> list[str]:
    if decision == "go":
        return [
            "use_source_for_local_rag_business_trials",
            "keep_source_binding_decisions_in_caller_control_plane",
            "move_next_to_parser_adapter_boundary_only_if_new_file_formats_are_needed",
        ]
    if decision == "review":
        return [
            "review_acceptance_cases_or_retrieval_quality",
            "rerun_local_approved_source_ingestion_loop_after_adjustment",
        ]
    return [
        "inspect_blocking_step_reason_code",
        "fix_onboarding_preflight_ingestion_index_or_acceptance_issue",
        "rerun_local_approved_source_ingestion_loop",
    ]


def _non_goals() -> list[str]:
    return [
        "does_not_parse_raw_pdf_as_supported_ingestion",
        "does_not_start_ocr_services",
        "does_not_call_myprivateagent",
        "does_not_create_source_to_agent_binding",
        "does_not_mutate_chat_runtime",
        "does_not_promote_retrieval_backend",
        "does_not_introduce_background_worker",
        "does_not_execute_graphrag",
    ]


def _path_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _format_value(value: Any) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)

