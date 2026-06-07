import json
import re
import shutil
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from app.services.approved_local_corpus_acceptance_smoke import DEFAULT_TOP_K
from app.services.local_approved_source_ingestion_loop import (
    export_local_approved_source_ingestion_loop_report,
)
from app.services.local_business_corpus_trial import (
    DEFAULT_QUERY,
    DEFAULT_SOURCE_ID,
    DEFAULT_TITLE,
)


LOCAL_ENTERPRISE_CORPUS_INGESTION_QA_LOOP_ID = "local-enterprise-corpus-ingestion-qa-loop-v1"
DEFAULT_INPUT_PATH = Path("docs/local-run/pdf-derived-corpus/company_profile_2025_trial.md")
DEFAULT_OUTPUT_DIR = Path("docs/local-run/local-enterprise-corpus-ingestion-qa-loop")
OUTPUT_JSON_FILENAME = "local-enterprise-corpus-ingestion-qa-loop.json"
OUTPUT_MARKDOWN_FILENAME = "local-enterprise-corpus-ingestion-qa-loop.md"
SUPPORTED_MARKDOWN_SUFFIXES = {".md", ".markdown"}
SUPPORTED_TEXT_SUFFIXES = {".txt"}


@dataclass(frozen=True)
class LocalEnterpriseCorpusIngestionQaLoopReport:
    id: str
    generated_at: str
    decision: str
    reason_code: str
    source_id: str
    title: str
    query: str
    top_k: int
    input_path: Path
    input_format: str
    materialized_markdown_path: Path | None
    downstream: dict[str, Any]
    summary: dict[str, Any]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


def export_local_enterprise_corpus_ingestion_qa_loop_report(
    *,
    input_path: Path = DEFAULT_INPUT_PATH,
    source_id: str = DEFAULT_SOURCE_ID,
    title: str = DEFAULT_TITLE,
    query: str = DEFAULT_QUERY,
    top_k: int = DEFAULT_TOP_K,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    ingestion_loop_exporter: Callable[..., Any] = export_local_approved_source_ingestion_loop_report,
) -> LocalEnterpriseCorpusIngestionQaLoopReport:
    report = run_local_enterprise_corpus_ingestion_qa_loop(
        input_path=input_path,
        source_id=source_id,
        title=title,
        query=query,
        top_k=top_k,
        output_dir=output_dir,
        ingestion_loop_exporter=ingestion_loop_exporter,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = LocalEnterpriseCorpusIngestionQaLoopReport(
        id=report.id,
        generated_at=report.generated_at,
        decision=report.decision,
        reason_code=report.reason_code,
        source_id=report.source_id,
        title=report.title,
        query=report.query,
        top_k=report.top_k,
        input_path=report.input_path,
        input_format=report.input_format,
        materialized_markdown_path=report.materialized_markdown_path,
        downstream=report.downstream,
        summary=report.summary,
        recommended_actions=report.recommended_actions,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            local_enterprise_corpus_ingestion_qa_loop_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_local_enterprise_corpus_ingestion_qa_loop_markdown(exported),
        encoding="utf-8",
    )
    return exported


def run_local_enterprise_corpus_ingestion_qa_loop(
    *,
    input_path: Path = DEFAULT_INPUT_PATH,
    source_id: str = DEFAULT_SOURCE_ID,
    title: str = DEFAULT_TITLE,
    query: str = DEFAULT_QUERY,
    top_k: int = DEFAULT_TOP_K,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    ingestion_loop_exporter: Callable[..., Any] = export_local_approved_source_ingestion_loop_report,
) -> LocalEnterpriseCorpusIngestionQaLoopReport:
    normalized_input_path = input_path.expanduser().resolve()
    input_format = _input_format(normalized_input_path)
    if not normalized_input_path.exists():
        return _blocked_report(
            input_path=normalized_input_path,
            input_format=input_format,
            source_id=source_id,
            title=title,
            query=query,
            top_k=top_k,
            reason_code="input_file_missing",
            summary={"input_status": "missing"},
        )
    if normalized_input_path.suffix.lower() == ".pdf":
        return _blocked_report(
            input_path=normalized_input_path,
            input_format="pdf",
            source_id=source_id,
            title=title,
            query=query,
            top_k=top_k,
            reason_code="raw_pdf_requires_parser_artifact",
            summary={"input_status": "unsupported_direct_pdf"},
        )
    if normalized_input_path.suffix.lower() not in SUPPORTED_MARKDOWN_SUFFIXES | SUPPORTED_TEXT_SUFFIXES:
        return _blocked_report(
            input_path=normalized_input_path,
            input_format=input_format,
            source_id=source_id,
            title=title,
            query=query,
            top_k=top_k,
            reason_code="unsupported_input_format",
            summary={"input_status": "unsupported_format"},
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    materialized_markdown_path = _materialize_markdown(
        input_path=normalized_input_path,
        input_format=input_format,
        output_dir=output_dir,
        source_id=source_id,
        title=title,
    )
    downstream_report = ingestion_loop_exporter(
        markdown_path=materialized_markdown_path,
        source_id=source_id,
        title=title,
        query=query,
        top_k=top_k,
        output_dir=output_dir / "approved-source-ingestion-loop",
    )
    downstream = _downstream_summary(downstream_report)
    downstream_decision = str(getattr(downstream_report, "decision", "") or "blocked")
    downstream_reason = str(getattr(downstream_report, "reason_code", "") or "downstream_unknown")
    if downstream_decision == "go":
        decision = "go"
        reason_code = "local_enterprise_corpus_qa_ready"
    elif downstream_decision == "review":
        decision = "review"
        reason_code = f"downstream_{downstream_reason}"
    else:
        decision = "blocked"
        reason_code = f"downstream_{downstream_reason}"

    return LocalEnterpriseCorpusIngestionQaLoopReport(
        id=LOCAL_ENTERPRISE_CORPUS_INGESTION_QA_LOOP_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision=decision,
        reason_code=reason_code,
        source_id=source_id,
        title=title,
        query=query,
        top_k=top_k,
        input_path=normalized_input_path,
        input_format=input_format,
        materialized_markdown_path=materialized_markdown_path,
        downstream=downstream,
        summary={
            "input_status": "ready",
            "input_format": input_format,
            "materialized_markdown_status": "ready",
            "downstream_decision": downstream_decision,
            "downstream_reason_code": downstream_reason,
            "final_decision": decision,
            "source_binding_status": "not_created",
            "runtime_promotion_status": "keep_runtime_defaults",
            "retrieval_backend_promotion_status": "not_changed",
            "graph_execution_status": "not_executed",
        },
        recommended_actions=_recommended_actions(decision, reason_code),
        non_goals=_non_goals(),
    )


def local_enterprise_corpus_ingestion_qa_loop_report_to_dict(
    report: LocalEnterpriseCorpusIngestionQaLoopReport,
) -> dict[str, Any]:
    payload = asdict(report)
    for key in ["input_path", "materialized_markdown_path", "json_path", "markdown_path"]:
        if payload[key] is not None:
            payload[key] = str(payload[key])
    return payload


def render_local_enterprise_corpus_ingestion_qa_loop_markdown(
    report: LocalEnterpriseCorpusIngestionQaLoopReport,
) -> str:
    lines = [
        "# Local Enterprise Corpus Ingestion QA Loop",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Source ID: `{report.source_id}`",
        f"- Title: `{report.title}`",
        f"- Query: `{report.query}`",
        f"- Input Path: `{report.input_path}`",
        f"- Input Format: `{report.input_format}`",
        f"- Materialized Markdown: `{report.materialized_markdown_path}`",
        "",
        "## Downstream",
        "",
        "| Field | Value |",
        "|---|---|",
    ]
    for key, value in report.downstream.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")
    lines.extend(["", "## Summary", "", "| Metric | Value |", "|---|---|"])
    for key, value in report.summary.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in report.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def _materialize_markdown(
    *,
    input_path: Path,
    input_format: str,
    output_dir: Path,
    source_id: str,
    title: str,
) -> Path:
    if input_format == "markdown":
        return input_path
    staging_dir = output_dir / "materialized-input"
    staging_dir.mkdir(parents=True, exist_ok=True)
    materialized_path = staging_dir / f"{_safe_source_id(source_id)}.md"
    text = input_path.read_text(encoding="utf-8")
    materialized_path.write_text(f"# {title}\n\n{text.strip()}\n", encoding="utf-8")
    return materialized_path


def _downstream_summary(report: Any) -> dict[str, Any]:
    return {
        "decision": getattr(report, "decision", None),
        "reason_code": getattr(report, "reason_code", None),
        "source_id": getattr(report, "source_id", None),
        "title": getattr(report, "title", None),
        "query": getattr(report, "query", None),
        "top_k": getattr(report, "top_k", None),
        "json_path": _path_string(getattr(report, "json_path", None)),
        "markdown_path": _path_string(getattr(report, "markdown_path_out", None)),
        "summary": dict(getattr(report, "summary", {}) or {}),
    }


def _blocked_report(
    *,
    input_path: Path,
    input_format: str,
    source_id: str,
    title: str,
    query: str,
    top_k: int,
    reason_code: str,
    summary: dict[str, Any],
) -> LocalEnterpriseCorpusIngestionQaLoopReport:
    return LocalEnterpriseCorpusIngestionQaLoopReport(
        id=LOCAL_ENTERPRISE_CORPUS_INGESTION_QA_LOOP_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision="blocked",
        reason_code=reason_code,
        source_id=source_id,
        title=title,
        query=query,
        top_k=top_k,
        input_path=input_path,
        input_format=input_format,
        materialized_markdown_path=None,
        downstream={},
        summary={
            **summary,
            "final_decision": "blocked",
            "source_binding_status": "not_created",
            "runtime_promotion_status": "keep_runtime_defaults",
            "retrieval_backend_promotion_status": "not_changed",
            "graph_execution_status": "not_executed",
        },
        recommended_actions=_recommended_actions("blocked", reason_code),
        non_goals=_non_goals(),
    )


def _recommended_actions(decision: str, reason_code: str) -> list[str]:
    if decision == "go":
        return [
            "use_source_for_local_enterprise_rag_questions",
            "call_provider_rag_answer_with_registered_source_id",
            "keep_source_binding_decisions_in_myprivateagent_control_plane",
        ]
    if reason_code == "input_file_missing":
        return ["check_input_path_and_rerun"]
    if reason_code == "raw_pdf_requires_parser_artifact":
        return [
            "convert_pdf_to_markdown_with_parser_or_ocr",
            "or_export_normalized_parser_artifact_then_run_parser_artifact_ingestion_loop",
            "rerun_local_enterprise_corpus_ingestion_qa_loop_with_markdown_or_txt",
        ]
    if reason_code == "unsupported_input_format":
        return [
            "provide_markdown_or_txt_for_direct_local_ingestion",
            "convert_source_file_to_markdown_with_parser_or_ocr",
        ]
    if decision == "review":
        return [
            "review_downstream_ingestion_or_acceptance_warning",
            "adjust_query_or_source_content_and_rerun",
        ]
    return [
        "inspect_downstream_blocking_reason",
        "fix_source_registration_ingestion_index_or_acceptance_issue",
        "rerun_local_enterprise_corpus_ingestion_qa_loop",
    ]


def _non_goals() -> list[str]:
    return [
        "does_not_parse_raw_pdf_as_supported_direct_ingestion",
        "does_not_start_ocr_services",
        "does_not_start_parser_services",
        "does_not_call_myprivateagent",
        "does_not_create_source_to_agent_binding",
        "does_not_mutate_chat_runtime",
        "does_not_promote_retrieval_backend",
        "does_not_add_background_worker",
        "does_not_execute_graphrag",
    ]


def _input_format(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in SUPPORTED_MARKDOWN_SUFFIXES:
        return "markdown"
    if suffix in SUPPORTED_TEXT_SUFFIXES:
        return "txt"
    if suffix == ".pdf":
        return "pdf"
    return suffix.lstrip(".") or "unknown"


def _safe_source_id(source_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", source_id.strip())
    return cleaned or "local_enterprise_source"


def _path_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _format_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
