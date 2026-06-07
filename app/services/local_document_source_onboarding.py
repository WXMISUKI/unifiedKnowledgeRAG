import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from app.services.approved_local_corpus_acceptance_smoke import (
    DEFAULT_TOP_K,
    export_approved_local_corpus_acceptance_smoke,
)
from app.services.approved_local_corpus_source_registration import (
    register_approved_local_corpus_source,
)
from app.services.local_business_corpus_trial import (
    DEFAULT_MARKDOWN_PATH,
    DEFAULT_QUERY,
    DEFAULT_SOURCE_ID,
    DEFAULT_TITLE,
    export_local_business_corpus_trial_report,
)
from app.services.local_corpus_caller_handoff import (
    export_local_corpus_caller_handoff,
)


LOCAL_DOCUMENT_SOURCE_ONBOARDING_ID = "local-document-source-onboarding-loop-v1"
DEFAULT_OUTPUT_DIR = Path("docs/local-run/document-source-onboarding")
OUTPUT_JSON_FILENAME = "local-document-source-onboarding.json"
OUTPUT_MARKDOWN_FILENAME = "local-document-source-onboarding.md"


@dataclass(frozen=True)
class OnboardingStep:
    id: str
    status: str
    reason_code: str
    artifacts: dict[str, str | None]
    summary: dict[str, Any]


@dataclass(frozen=True)
class LocalDocumentSourceOnboardingReport:
    id: str
    generated_at: str
    decision: str
    reason_code: str
    source_id: str
    title: str
    markdown_path: Path
    query: str
    top_k: int
    steps: list[OnboardingStep]
    summary: dict[str, Any]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path_out: Path | None = None


def export_local_document_source_onboarding_report(
    *,
    markdown_path: Path = DEFAULT_MARKDOWN_PATH,
    source_id: str = DEFAULT_SOURCE_ID,
    title: str = DEFAULT_TITLE,
    query: str = DEFAULT_QUERY,
    top_k: int = DEFAULT_TOP_K,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    business_trial_exporter: Callable[..., Any] = export_local_business_corpus_trial_report,
    handoff_exporter: Callable[..., Any] = export_local_corpus_caller_handoff,
    registration_exporter: Callable[..., Any] = register_approved_local_corpus_source,
    acceptance_exporter: Callable[..., Any] = export_approved_local_corpus_acceptance_smoke,
) -> LocalDocumentSourceOnboardingReport:
    report = run_local_document_source_onboarding(
        markdown_path=markdown_path,
        source_id=source_id,
        title=title,
        query=query,
        top_k=top_k,
        output_dir=output_dir,
        business_trial_exporter=business_trial_exporter,
        handoff_exporter=handoff_exporter,
        registration_exporter=registration_exporter,
        acceptance_exporter=acceptance_exporter,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path_out = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = LocalDocumentSourceOnboardingReport(
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
        json.dumps(
            local_document_source_onboarding_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path_out.write_text(
        render_local_document_source_onboarding_markdown(exported),
        encoding="utf-8",
    )
    return exported


def run_local_document_source_onboarding(
    *,
    markdown_path: Path = DEFAULT_MARKDOWN_PATH,
    source_id: str = DEFAULT_SOURCE_ID,
    title: str = DEFAULT_TITLE,
    query: str = DEFAULT_QUERY,
    top_k: int = DEFAULT_TOP_K,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    business_trial_exporter: Callable[..., Any] = export_local_business_corpus_trial_report,
    handoff_exporter: Callable[..., Any] = export_local_corpus_caller_handoff,
    registration_exporter: Callable[..., Any] = register_approved_local_corpus_source,
    acceptance_exporter: Callable[..., Any] = export_approved_local_corpus_acceptance_smoke,
) -> LocalDocumentSourceOnboardingReport:
    output_dir.mkdir(parents=True, exist_ok=True)
    steps: list[OnboardingStep] = []

    trial = business_trial_exporter(
        markdown_path=markdown_path,
        output_dir=output_dir / "business-corpus-trial",
        source_id=source_id,
        title=title,
        query=query,
        top_k=top_k,
    )
    steps.append(_business_trial_step(trial))
    if trial.decision != "go":
        decision = "review" if trial.decision == "review" else "blocked"
        return _report(
            decision=decision,
            reason_code=f"business_corpus_trial_{decision}",
            source_id=source_id,
            title=title,
            markdown_path=Path(markdown_path),
            query=query,
            top_k=top_k,
            steps=steps,
        )

    handoff = handoff_exporter(
        trial_report_path=trial.json_path,
        output_dir=output_dir / "corpus-caller-handoff",
    )
    steps.append(_handoff_step(handoff))
    if handoff.status != "ready_for_caller_review":
        decision = "review" if handoff.status == "review" else "blocked"
        return _report(
            decision=decision,
            reason_code=f"caller_handoff_{decision}",
            source_id=source_id,
            title=title,
            markdown_path=Path(markdown_path),
            query=query,
            top_k=top_k,
            steps=steps,
        )

    registration = registration_exporter(
        handoff_path=handoff.json_path,
        output_dir=output_dir / "approved-local-source-registration",
    )
    steps.append(_registration_step(registration))
    if registration.status != "registered":
        return _report(
            decision="blocked",
            reason_code="approved_source_registration_blocked",
            source_id=source_id,
            title=title,
            markdown_path=Path(markdown_path),
            query=query,
            top_k=top_k,
            steps=steps,
        )

    acceptance = acceptance_exporter(
        source_id=source_id,
        top_k=top_k,
        output_dir=output_dir / "approved-local-corpus-acceptance",
    )
    steps.append(_acceptance_step(acceptance))
    if acceptance.decision != "go":
        decision = "review" if acceptance.decision == "review" else "blocked"
        return _report(
            decision=decision,
            reason_code=f"acceptance_smoke_{decision}",
            source_id=source_id,
            title=title,
            markdown_path=Path(markdown_path),
            query=query,
            top_k=top_k,
            steps=steps,
        )

    return _report(
        decision="go",
        reason_code="local_document_source_onboarded",
        source_id=source_id,
        title=title,
        markdown_path=Path(markdown_path),
        query=query,
        top_k=top_k,
        steps=steps,
    )


def local_document_source_onboarding_report_to_dict(
    report: LocalDocumentSourceOnboardingReport,
) -> dict[str, Any]:
    payload = asdict(report)
    for key in ["markdown_path", "json_path", "markdown_path_out"]:
        if payload[key] is not None:
            payload[key] = str(payload[key])
    return payload


def render_local_document_source_onboarding_markdown(
    report: LocalDocumentSourceOnboardingReport,
) -> str:
    lines = [
        "# Local Document Source Onboarding",
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
    source_id: str,
    title: str,
    markdown_path: Path,
    query: str,
    top_k: int,
    steps: list[OnboardingStep],
) -> LocalDocumentSourceOnboardingReport:
    return LocalDocumentSourceOnboardingReport(
        id=LOCAL_DOCUMENT_SOURCE_ONBOARDING_ID,
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
            "ready_step_count": sum(1 for step in steps if step.status in {"go", "ready_for_caller_review", "registered"}),
            "review_step_count": sum(1 for step in steps if step.status == "review"),
            "blocked_step_count": sum(1 for step in steps if step.status == "blocked"),
            "final_decision": decision,
            "source_binding_status": "not_created",
            "runtime_promotion_status": "keep_runtime_defaults",
            "graph_execution_status": "not_executed",
        },
        recommended_actions=_recommended_actions(decision),
        non_goals=_non_goals(),
    )


def _business_trial_step(trial: Any) -> OnboardingStep:
    return OnboardingStep(
        id="business_corpus_trial",
        status=str(trial.decision),
        reason_code=str(trial.reason_code),
        artifacts={
            "json": _path_string(getattr(trial, "json_path", None)),
            "markdown": _path_string(getattr(trial, "report_markdown_path", None)),
            "overlay": _path_string(getattr(trial, "overlay_path", None)),
            "chunks": _path_string(getattr(trial, "chunks_path", None)),
        },
        summary=dict(getattr(trial, "summary", {}) or {}),
    )


def _handoff_step(handoff: Any) -> OnboardingStep:
    return OnboardingStep(
        id="caller_handoff",
        status=str(handoff.status),
        reason_code=str(handoff.reason_code),
        artifacts={
            "json": _path_string(getattr(handoff, "json_path", None)),
            "markdown": _path_string(getattr(handoff, "markdown_path", None)),
        },
        summary=dict(getattr(handoff, "summary", {}) or {}),
    )


def _registration_step(registration: Any) -> OnboardingStep:
    return OnboardingStep(
        id="approved_source_registration",
        status=str(registration.status),
        reason_code=str(registration.reason_code),
        artifacts={
            "json": _path_string(getattr(registration, "json_path", None)),
            "markdown": _path_string(getattr(registration, "markdown_path", None)),
            "materialized_source": _path_string(getattr(registration, "materialized_source_path", None)),
        },
        summary=dict(getattr(registration, "summary", {}) or {}),
    )


def _acceptance_step(acceptance: Any) -> OnboardingStep:
    return OnboardingStep(
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
            "use_registered_source_for_myprivateagent_explicit_trial",
            "declare_source_id_in_domain_agent_manifest_when_needed",
            "keep_source_to_agent_binding_in_caller_control_plane",
        ]
    if decision == "review":
        return [
            "review_markdown_content_query_or_acceptance_cases",
            "rerun_local_document_source_onboarding_after_adjustment",
        ]
    return [
        "inspect_blocking_step_reason_code",
        "fix_markdown_handoff_registration_or_acceptance_issue",
        "rerun_local_document_source_onboarding",
    ]


def _non_goals() -> list[str]:
    return [
        "does_not_parse_raw_pdf_as_supported_ingestion",
        "does_not_start_ocr_services",
        "does_not_create_source_to_agent_binding",
        "does_not_call_myprivateagent",
        "does_not_create_formal_ingestion_job",
        "does_not_promote_retrieval_backend",
        "does_not_call_vector_databases",
        "does_not_mutate_chat_runtime",
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
