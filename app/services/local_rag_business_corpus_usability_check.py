import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from app.services.approved_local_corpus_acceptance_smoke import (
    DEFAULT_SOURCE_ID,
    DEFAULT_TOP_K,
    run_approved_local_corpus_acceptance_smoke,
)
from app.services.approved_local_corpus_live_http_smoke import (
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT_SECONDS,
    run_approved_local_corpus_live_http_smoke,
)
from app.services.local_business_corpus_trial import (
    DEFAULT_MARKDOWN_PATH,
    DEFAULT_QUERY,
    DEFAULT_TITLE,
    run_local_business_corpus_trial,
)


LOCAL_RAG_BUSINESS_CORPUS_USABILITY_CHECK_ID = (
    "local-rag-business-corpus-usability-check-v1"
)
DEFAULT_OUTPUT_DIR = Path("docs/local-run/rag-business-corpus-usability")
OUTPUT_JSON_FILENAME = "local-rag-business-corpus-usability-check.json"
OUTPUT_MARKDOWN_FILENAME = "local-rag-business-corpus-usability-check.md"


@dataclass(frozen=True)
class UsabilityCheckResult:
    name: str
    required: bool
    decision: str
    reason_code: str
    summary: dict[str, Any] = field(default_factory=dict)
    json_path: str = ""
    markdown_path: str = ""


@dataclass(frozen=True)
class LocalRagBusinessCorpusUsabilityCheckReport:
    id: str
    generated_at: str
    decision: str
    reason_code: str
    source_id: str
    title: str
    query: str
    base_url: str
    include_live_http: bool
    summary: dict[str, Any]
    checks: list[UsabilityCheckResult]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


def export_local_rag_business_corpus_usability_check(
    *,
    markdown_path: Path = DEFAULT_MARKDOWN_PATH,
    source_id: str = DEFAULT_SOURCE_ID,
    title: str = DEFAULT_TITLE,
    query: str = DEFAULT_QUERY,
    top_k: int = DEFAULT_TOP_K,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    base_url: str = DEFAULT_BASE_URL,
    include_live_http: bool = False,
    provider_api_key: str | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    local_trial_runner: Callable[..., Any] | None = None,
    acceptance_runner: Callable[..., Any] | None = None,
    live_http_runner: Callable[..., Any] | None = None,
) -> LocalRagBusinessCorpusUsabilityCheckReport:
    report = run_local_rag_business_corpus_usability_check(
        markdown_path=markdown_path,
        source_id=source_id,
        title=title,
        query=query,
        top_k=top_k,
        output_dir=output_dir,
        base_url=base_url,
        include_live_http=include_live_http,
        provider_api_key=provider_api_key,
        timeout_seconds=timeout_seconds,
        local_trial_runner=local_trial_runner,
        acceptance_runner=acceptance_runner,
        live_http_runner=live_http_runner,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path_out = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = LocalRagBusinessCorpusUsabilityCheckReport(
        id=report.id,
        generated_at=report.generated_at,
        decision=report.decision,
        reason_code=report.reason_code,
        source_id=report.source_id,
        title=report.title,
        query=report.query,
        base_url=report.base_url,
        include_live_http=report.include_live_http,
        summary=report.summary,
        checks=report.checks,
        recommended_actions=report.recommended_actions,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path=markdown_path_out,
    )
    json_path.write_text(
        json.dumps(
            local_rag_business_corpus_usability_check_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path_out.write_text(
        render_local_rag_business_corpus_usability_check_markdown(exported),
        encoding="utf-8",
    )
    return exported


def run_local_rag_business_corpus_usability_check(
    *,
    markdown_path: Path = DEFAULT_MARKDOWN_PATH,
    source_id: str = DEFAULT_SOURCE_ID,
    title: str = DEFAULT_TITLE,
    query: str = DEFAULT_QUERY,
    top_k: int = DEFAULT_TOP_K,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    base_url: str = DEFAULT_BASE_URL,
    include_live_http: bool = False,
    provider_api_key: str | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    local_trial_runner: Callable[..., Any] | None = None,
    acceptance_runner: Callable[..., Any] | None = None,
    live_http_runner: Callable[..., Any] | None = None,
) -> LocalRagBusinessCorpusUsabilityCheckReport:
    local_runner = local_trial_runner or run_local_business_corpus_trial

    local_output_dir = output_dir / "local-business-corpus-trial"
    acceptance_output_dir = output_dir / "approved-local-corpus-acceptance"
    live_output_dir = output_dir / "approved-local-corpus-live-http"

    local_report = local_runner(
        markdown_path=markdown_path,
        output_dir=local_output_dir,
        source_id=source_id,
        title=title,
        query=query,
        top_k=top_k,
    )
    if acceptance_runner is None:
        acceptance_report = run_approved_local_corpus_acceptance_smoke(
            source_id=source_id,
            top_k=top_k,
        )
    else:
        acceptance_report = acceptance_runner(
            source_id=source_id,
            output_dir=acceptance_output_dir,
            top_k=top_k,
        )

    checks = [
        _check_result("local_business_corpus_trial", local_report, required=True),
        _check_result("approved_local_corpus_acceptance", acceptance_report, required=True),
    ]

    if include_live_http:
        if live_http_runner is None:
            live_report = run_approved_local_corpus_live_http_smoke(
                base_url=base_url,
                source_id=source_id,
                top_k=top_k,
                provider_api_key=provider_api_key,
                timeout_seconds=timeout_seconds,
            )
        else:
            live_report = live_http_runner(
                base_url=base_url,
                source_id=source_id,
                output_dir=live_output_dir,
                top_k=top_k,
                provider_api_key=provider_api_key,
                timeout_seconds=timeout_seconds,
            )
        checks.append(_check_result("approved_local_corpus_live_http", live_report, required=True))
    else:
        checks.append(
            UsabilityCheckResult(
                name="approved_local_corpus_live_http",
                required=False,
                decision="skipped",
                reason_code="live_http_not_requested",
                summary={
                    "base_url": base_url,
                    "transport_mode": "live_http",
                },
            )
        )

    decision, reason_code = _decision(checks)
    return LocalRagBusinessCorpusUsabilityCheckReport(
        id=LOCAL_RAG_BUSINESS_CORPUS_USABILITY_CHECK_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision=decision,
        reason_code=reason_code,
        source_id=source_id,
        title=title,
        query=query,
        base_url=base_url,
        include_live_http=include_live_http,
        summary={
            "required_check_count": sum(1 for check in checks if check.required),
            "go_check_count": sum(1 for check in checks if check.decision == "go"),
            "review_check_count": sum(1 for check in checks if check.decision == "review"),
            "blocked_check_count": sum(1 for check in checks if check.decision == "blocked"),
            "skipped_check_count": sum(1 for check in checks if check.decision == "skipped"),
            "live_http_required": include_live_http,
            "default_rag_api_behavior": "unchanged",
            "myprivateagent_behavior": "unchanged",
            "source_binding_status": "not_created",
            "runtime_promotion_status": "keep_runtime_defaults",
            "graph_execution_status": "not_executed",
        },
        checks=checks,
        recommended_actions=_recommended_actions(decision, reason_code, include_live_http),
        non_goals=_non_goals(),
    )


def local_rag_business_corpus_usability_check_report_to_dict(
    report: LocalRagBusinessCorpusUsabilityCheckReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_local_rag_business_corpus_usability_check_markdown(
    report: LocalRagBusinessCorpusUsabilityCheckReport,
) -> str:
    lines = [
        "# Local RAG Business Corpus Usability Check",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Source ID: `{report.source_id}`",
        f"- Base URL: `{report.base_url}`",
        f"- Live HTTP Included: `{report.include_live_http}`",
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
            "## Checks",
            "",
            "| Check | Required | Decision | Reason |",
            "|---|---:|---|---|",
        ]
    )
    for check in report.checks:
        lines.append(
            f"| `{check.name}` | `{check.required}` | `{check.decision}` | `{check.reason_code}` |"
        )
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in report.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def _check_result(name: str, report: Any, *, required: bool) -> UsabilityCheckResult:
    return UsabilityCheckResult(
        name=name,
        required=required,
        decision=str(getattr(report, "decision", "blocked") or "blocked"),
        reason_code=str(getattr(report, "reason_code", "missing_reason_code") or "missing_reason_code"),
        summary=dict(getattr(report, "summary", {}) or {}),
        json_path=str(getattr(report, "json_path", "") or ""),
        markdown_path=str(
            getattr(report, "markdown_path", None)
            or getattr(report, "report_markdown_path", "")
            or ""
        ),
    )


def _decision(checks: list[UsabilityCheckResult]) -> tuple[str, str]:
    required_checks = [check for check in checks if check.required]
    blocked = next((check for check in required_checks if check.decision == "blocked"), None)
    if blocked is not None:
        return "blocked", f"{blocked.name}_{blocked.reason_code}"
    review = next((check for check in required_checks if check.decision == "review"), None)
    if review is not None:
        return "review", f"{review.name}_{review.reason_code}"
    return "go", "local_rag_business_corpus_usable"


def _recommended_actions(
    decision: str,
    reason_code: str,
    include_live_http: bool,
) -> list[str]:
    if decision == "go":
        actions = [
            "use_local_business_corpus_for_myprivateagent_trial",
            "keep_default_rag_behavior_unchanged",
        ]
        if not include_live_http:
            actions.append("run_with_include_live_http_before_claiming_http_access")
        return actions
    if decision == "review":
        return [
            "review_business_corpus_markdown_page_range_or_queries",
            "rerun_usability_check_after_corpus_adjustment",
        ]
    if "local_provider_unreachable" in reason_code:
        return [
            "start_provider_with_uvicorn_app_main_app_reload_port_8020",
            "rerun_usability_check_with_include_live_http",
        ]
    return [
        "inspect_blocked_check_reason",
        "fix_source_catalog_manifest_retrieve_or_answer_contract",
        "rerun_usability_check",
    ]


def _non_goals() -> list[str]:
    return [
        "does_not_start_server",
        "does_not_register_sources",
        "does_not_create_source_to_agent_binding",
        "does_not_create_formal_ingestion_job",
        "does_not_start_ocr_services",
        "does_not_promote_retrieval_backend",
        "does_not_run_myprivateagent_orchestration",
        "does_not_call_vector_databases",
        "does_not_execute_graphrag",
        "does_not_change_default_rag_api_behavior",
    ]


def _format_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
