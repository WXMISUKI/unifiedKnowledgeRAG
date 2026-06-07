import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


CLOSURE_ID = "local-rag-http-myprivateagent-call-loop-closure-v1"
DEFAULT_PROVIDER_REPORT_PATH = Path(
    "docs/local-run/rag-business-corpus-usability/local-rag-business-corpus-usability-check.json"
)
DEFAULT_MYPRIVATEAGENT_REPORT_PATH = Path(
    "D:/AI/AIcode/MyPrivateAgent/docs/integration/local-knowledge-provider-corpus-trial/local-knowledge-provider-corpus-trial.json"
)
DEFAULT_OUTPUT_DIR = Path("docs/local-run/myprivateagent-call-loop-closure")
OUTPUT_JSON_FILENAME = "local-rag-myprivateagent-call-loop-closure.json"
OUTPUT_MARKDOWN_FILENAME = "local-rag-myprivateagent-call-loop-closure.md"


@dataclass(frozen=True)
class ClosureInput:
    name: str
    path: str
    present: bool
    decision: str
    reason_code: str
    source_id: str
    summary: dict[str, Any] = field(default_factory=dict)
    error: str = ""


@dataclass(frozen=True)
class LocalRagMyPrivateAgentCallLoopClosureReport:
    id: str
    generated_at: str
    decision: str
    reason_code: str
    source_id: str
    provider_report: ClosureInput
    myprivateagent_report: ClosureInput
    summary: dict[str, Any]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


def export_local_rag_myprivateagent_call_loop_closure(
    *,
    provider_report_path: Path = DEFAULT_PROVIDER_REPORT_PATH,
    myprivateagent_report_path: Path = DEFAULT_MYPRIVATEAGENT_REPORT_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> LocalRagMyPrivateAgentCallLoopClosureReport:
    report = build_local_rag_myprivateagent_call_loop_closure(
        provider_report_path=provider_report_path,
        myprivateagent_report_path=myprivateagent_report_path,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = LocalRagMyPrivateAgentCallLoopClosureReport(
        id=report.id,
        generated_at=report.generated_at,
        decision=report.decision,
        reason_code=report.reason_code,
        source_id=report.source_id,
        provider_report=report.provider_report,
        myprivateagent_report=report.myprivateagent_report,
        summary=report.summary,
        recommended_actions=report.recommended_actions,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            local_rag_myprivateagent_call_loop_closure_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_local_rag_myprivateagent_call_loop_closure_markdown(exported),
        encoding="utf-8",
    )
    return exported


def build_local_rag_myprivateagent_call_loop_closure(
    *,
    provider_report_path: Path = DEFAULT_PROVIDER_REPORT_PATH,
    myprivateagent_report_path: Path = DEFAULT_MYPRIVATEAGENT_REPORT_PATH,
) -> LocalRagMyPrivateAgentCallLoopClosureReport:
    provider = _load_input("provider_live_http_usability", provider_report_path)
    caller = _load_input("myprivateagent_caller_trial", myprivateagent_report_path)
    decision, reason_code, source_id = _decision(provider, caller)
    return LocalRagMyPrivateAgentCallLoopClosureReport(
        id=CLOSURE_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision=decision,
        reason_code=reason_code,
        source_id=source_id,
        provider_report=provider,
        myprivateagent_report=caller,
        summary={
            "provider_report_present": provider.present,
            "myprivateagent_report_present": caller.present,
            "provider_decision": provider.decision,
            "myprivateagent_decision": caller.decision,
            "provider_live_http_included": bool(provider.summary.get("live_http_required")),
            "source_ids_match": bool(provider.source_id and provider.source_id == caller.source_id),
            "default_rag_api_behavior": "unchanged",
            "myprivateagent_default_chat_behavior": "unchanged",
            "source_binding_status": "not_created",
            "graph_execution_status": "not_executed",
        },
        recommended_actions=_recommended_actions(decision, reason_code),
        non_goals=_non_goals(),
    )


def local_rag_myprivateagent_call_loop_closure_to_dict(
    report: LocalRagMyPrivateAgentCallLoopClosureReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_local_rag_myprivateagent_call_loop_closure_markdown(
    report: LocalRagMyPrivateAgentCallLoopClosureReport,
) -> str:
    lines = [
        "# Local RAG MyPrivateAgent Call Loop Closure",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Source ID: `{report.source_id or '-'}`",
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
            "## Inputs",
            "",
            "| Input | Present | Decision | Reason | Source ID |",
            "|---|---:|---|---|---|",
        ]
    )
    for item in [report.provider_report, report.myprivateagent_report]:
        lines.append(
            f"| `{item.name}` | `{item.present}` | `{item.decision}` | `{item.reason_code}` | `{item.source_id}` |"
        )
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in report.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def _load_input(name: str, path: Path) -> ClosureInput:
    normalized_path = path.expanduser().resolve()
    if not normalized_path.exists():
        return ClosureInput(
            name=name,
            path=str(normalized_path),
            present=False,
            decision="blocked",
            reason_code="report_missing",
            source_id="",
            error="Report file does not exist.",
        )
    try:
        payload = json.loads(normalized_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return ClosureInput(
            name=name,
            path=str(normalized_path),
            present=True,
            decision="blocked",
            reason_code="report_malformed",
            source_id="",
            error=f"{error.__class__.__name__}: {error}",
        )
    if not isinstance(payload, dict):
        return ClosureInput(
            name=name,
            path=str(normalized_path),
            present=True,
            decision="blocked",
            reason_code="report_not_object",
            source_id="",
        )
    return ClosureInput(
        name=name,
        path=str(normalized_path),
        present=True,
        decision=str(payload.get("decision") or "blocked"),
        reason_code=str(payload.get("reason_code") or "missing_reason_code"),
        source_id=str(payload.get("source_id") or ""),
        summary=dict(payload.get("summary") or {}),
    )


def _decision(provider: ClosureInput, caller: ClosureInput) -> tuple[str, str, str]:
    source_id = provider.source_id or caller.source_id
    for item in [provider, caller]:
        if not item.present:
            return "blocked", f"{item.name}_report_missing", source_id
        if item.decision == "blocked":
            return "blocked", f"{item.name}_{item.reason_code}", source_id
    if provider.source_id and caller.source_id and provider.source_id != caller.source_id:
        return "blocked", "source_id_mismatch", source_id
    if provider.summary.get("live_http_required") is not True:
        return "review", "provider_live_http_not_included", source_id
    if provider.decision != "go":
        return "review", f"provider_live_http_usability_{provider.reason_code}", source_id
    if caller.decision != "go":
        return "review", f"myprivateagent_caller_trial_{caller.reason_code}", source_id
    return "go", "local_rag_http_myprivateagent_call_loop_closed", source_id


def _recommended_actions(decision: str, reason_code: str) -> list[str]:
    if decision == "go":
        return [
            "stop_provider_side_readiness_expansion",
            "use_company_profile_source_in_myprivateagent_local_trial",
            "only_reopen_provider_work_for_concrete_trial_bugs_or_new_corpus_demand",
        ]
    if reason_code == "provider_live_http_not_included":
        return [
            "rerun_provider_usability_check_with_include_live_http",
            "rerun_closure_report",
        ]
    if decision == "review":
        return [
            "review_non_go_trial_report",
            "rerun_provider_or_myprivateagent_trial_after_fix",
        ]
    return [
        "fix_missing_blocked_or_mismatched_trial_report",
        "rerun_provider_live_http_and_myprivateagent_caller_trial",
    ]


def _non_goals() -> list[str]:
    return [
        "does_not_call_provider_http",
        "does_not_run_myprivateagent_orchestration",
        "does_not_change_rag_api_behavior",
        "does_not_enable_default_chat_retrieval",
        "does_not_create_source_to_agent_binding",
        "does_not_start_services",
        "does_not_promote_retrieval_backend",
        "does_not_start_ocr_services",
        "does_not_execute_graphrag",
    ]


def _format_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
