import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


LOCAL_CORPUS_CALLER_HANDOFF_ID = "local-corpus-caller-handoff-v1"
DEFAULT_TRIAL_REPORT_PATH = Path(
    "docs/local-run/business-corpus-trial/local-business-corpus-trial.json"
)
DEFAULT_OUTPUT_DIR = Path("docs/local-run/corpus-caller-handoff")
OUTPUT_JSON_FILENAME = "local-corpus-caller-handoff.json"
OUTPUT_MARKDOWN_FILENAME = "local-corpus-caller-handoff.md"
REQUIRED_ARTIFACT_FIELDS = ["markdown_path", "overlay_path", "chunks_path"]


@dataclass(frozen=True)
class LocalCorpusCallerHandoff:
    id: str
    generated_at: str
    status: str
    reason_code: str
    trial_report_path: Path
    source_id: str | None
    title: str | None
    recommended_query: str | None
    registration_status: str
    citation_policy: str
    caller_next_action: str
    artifacts: dict[str, str | None]
    summary: dict[str, Any]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


def export_local_corpus_caller_handoff(
    *,
    trial_report_path: Path = DEFAULT_TRIAL_REPORT_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> LocalCorpusCallerHandoff:
    handoff = build_local_corpus_caller_handoff(
        trial_report_path=trial_report_path,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = LocalCorpusCallerHandoff(
        id=handoff.id,
        generated_at=handoff.generated_at,
        status=handoff.status,
        reason_code=handoff.reason_code,
        trial_report_path=handoff.trial_report_path,
        source_id=handoff.source_id,
        title=handoff.title,
        recommended_query=handoff.recommended_query,
        registration_status=handoff.registration_status,
        citation_policy=handoff.citation_policy,
        caller_next_action=handoff.caller_next_action,
        artifacts=handoff.artifacts,
        summary=handoff.summary,
        recommended_actions=handoff.recommended_actions,
        non_goals=handoff.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            local_corpus_caller_handoff_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_local_corpus_caller_handoff_markdown(exported),
        encoding="utf-8",
    )
    return exported


def build_local_corpus_caller_handoff(
    *,
    trial_report_path: Path = DEFAULT_TRIAL_REPORT_PATH,
) -> LocalCorpusCallerHandoff:
    normalized_path = trial_report_path.expanduser().resolve()
    if not normalized_path.exists():
        return _blocked_handoff(
            trial_report_path=normalized_path,
            reason_code="trial_report_missing",
            error="Local business corpus trial report does not exist.",
        )

    try:
        payload = json.loads(normalized_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return _blocked_handoff(
            trial_report_path=normalized_path,
            reason_code="trial_report_unreadable",
            error=f"{error.__class__.__name__}: {error}",
        )
    if not isinstance(payload, dict):
        return _blocked_handoff(
            trial_report_path=normalized_path,
            reason_code="trial_report_invalid",
            error="Trial report must be a JSON object.",
        )

    trial_decision = _string_value(payload.get("decision"))
    missing_artifacts = [
        field for field in REQUIRED_ARTIFACT_FIELDS if not _string_value(payload.get(field))
    ]
    if missing_artifacts:
        return _handoff_from_payload(
            payload=payload,
            trial_report_path=normalized_path,
            status="blocked",
            reason_code="trial_artifact_pointers_missing",
            caller_next_action="rerun_local_business_corpus_trial_before_caller_review",
            extra_summary={"missing_artifact_fields": missing_artifacts},
        )

    status, reason_code, next_action = _status_from_trial_decision(trial_decision)
    return _handoff_from_payload(
        payload=payload,
        trial_report_path=normalized_path,
        status=status,
        reason_code=reason_code,
        caller_next_action=next_action,
        extra_summary={},
    )


def local_corpus_caller_handoff_to_dict(
    handoff: LocalCorpusCallerHandoff,
) -> dict[str, Any]:
    payload = asdict(handoff)
    for key in ["trial_report_path", "json_path", "markdown_path"]:
        if payload[key] is not None:
            payload[key] = str(payload[key])
    return payload


def render_local_corpus_caller_handoff_markdown(
    handoff: LocalCorpusCallerHandoff,
) -> str:
    lines = [
        "# Local Corpus Caller Handoff",
        "",
        f"- Report: `{handoff.id}`",
        f"- Status: `{handoff.status}`",
        f"- Reason: `{handoff.reason_code}`",
        f"- Generated At: `{handoff.generated_at}`",
        f"- Source ID: `{handoff.source_id or 'n/a'}`",
        f"- Title: `{handoff.title or 'n/a'}`",
        f"- Recommended Query: `{handoff.recommended_query or 'n/a'}`",
        f"- Registration Status: `{handoff.registration_status}`",
        f"- Caller Next Action: `{handoff.caller_next_action}`",
        "",
        "## Artifacts",
        "",
        "| Artifact | Path |",
        "|---|---|",
    ]
    for key, value in handoff.artifacts.items():
        lines.append(f"| `{key}` | `{value or 'n/a'}` |")

    lines.extend(["", "## Summary", "", "| Metric | Value |", "|---|---|"])
    for key, value in handoff.summary.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")

    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in handoff.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in handoff.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def _handoff_from_payload(
    *,
    payload: dict[str, Any],
    trial_report_path: Path,
    status: str,
    reason_code: str,
    caller_next_action: str,
    extra_summary: dict[str, Any],
) -> LocalCorpusCallerHandoff:
    summary = _dict_value(payload.get("summary"))
    artifacts = {
        "trial_report": str(trial_report_path),
        "markdown": _string_value(payload.get("markdown_path")),
        "overlay": _string_value(payload.get("overlay_path")),
        "chunks": _string_value(payload.get("chunks_path")),
    }
    source_id = _string_value(payload.get("source_id"))
    trial_decision = _string_value(payload.get("decision"))
    return LocalCorpusCallerHandoff(
        id=LOCAL_CORPUS_CALLER_HANDOFF_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        reason_code=reason_code,
        trial_report_path=trial_report_path,
        source_id=source_id,
        title=_string_value(payload.get("title")),
        recommended_query=_string_value(payload.get("query")),
        registration_status=_string_value(summary.get("formal_registration_status"))
        or "not_registered",
        citation_policy="use_generated_trial_citations_only",
        caller_next_action=caller_next_action,
        artifacts=artifacts,
        summary={
            "status": status,
            "trial_decision": trial_decision,
            "source_id": source_id,
            "retrieved_evidence_count": summary.get("retrieved_evidence_count"),
            "answer_citation_count": summary.get("answer_citation_count"),
            "invalid_citation_count": summary.get("invalid_citation_count"),
            "default_source_catalog_status": summary.get(
                "default_source_catalog_status",
                "unchanged",
            ),
            "runtime_promotion_status": summary.get(
                "runtime_promotion_status",
                "keep_runtime_defaults",
            ),
            "graph_execution_status": summary.get(
                "graph_execution_status",
                "not_executed",
            ),
            **extra_summary,
        },
        recommended_actions=_recommended_actions(status),
        non_goals=_non_goals(),
    )


def _blocked_handoff(
    *,
    trial_report_path: Path,
    reason_code: str,
    error: str,
) -> LocalCorpusCallerHandoff:
    return LocalCorpusCallerHandoff(
        id=LOCAL_CORPUS_CALLER_HANDOFF_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status="blocked",
        reason_code=reason_code,
        trial_report_path=trial_report_path,
        source_id=None,
        title=None,
        recommended_query=None,
        registration_status="not_registered",
        citation_policy="use_generated_trial_citations_only",
        caller_next_action="export_local_business_corpus_trial_first",
        artifacts={
            "trial_report": str(trial_report_path),
            "markdown": None,
            "overlay": None,
            "chunks": None,
        },
        summary={
            "status": "blocked",
            "error": error,
            "default_source_catalog_status": "unchanged",
            "runtime_promotion_status": "keep_runtime_defaults",
            "graph_execution_status": "not_executed",
        },
        recommended_actions=_recommended_actions("blocked"),
        non_goals=_non_goals(),
    )


def _status_from_trial_decision(decision: str | None) -> tuple[str, str, str]:
    if decision == "go":
        return (
            "ready_for_caller_review",
            "trial_go_ready_for_caller_review",
            "review_trial_artifacts_before_formal_binding",
        )
    if decision == "review":
        return (
            "review",
            "trial_needs_review_before_caller_handoff",
            "review_trial_query_markdown_and_evidence_before_integration",
        )
    return (
        "blocked",
        "trial_blocked_before_caller_handoff",
        "fix_blocked_trial_before_caller_review",
    )


def _recommended_actions(status: str) -> list[str]:
    if status == "ready_for_caller_review":
        return [
            "review_trial_artifacts_before_formal_binding",
            "decide_whether_to_formally_register_local_source",
            "keep_provider_default_catalog_unchanged_until_approved",
        ]
    if status == "review":
        return [
            "review_trial_query_markdown_and_evidence",
            "rerun_local_business_corpus_trial_after_adjustment",
            "export_caller_handoff_after_trial_go",
        ]
    return [
        "export_or_fix_local_business_corpus_trial",
        "rerun_local_corpus_caller_handoff",
    ]


def _non_goals() -> list[str]:
    return [
        "does_not_modify_default_source_catalog",
        "does_not_expose_provider_http_source",
        "does_not_create_source_binding",
        "does_not_run_formal_ingestion_job",
        "does_not_persist_index_lifecycle_state",
        "does_not_promote_retrieval_backend",
        "does_not_run_myprivateagent_orchestration",
        "does_not_execute_graphrag",
        "does_not_start_ocr_services",
    ]


def _string_value(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _dict_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _format_value(value: Any) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
