import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PHASE25_LIVE_TRIAL_OUTCOME_FEEDBACK_ID = (
    "phase25-myprivateagent-live-trial-outcome-feedback-v1"
)
OUTPUT_JSON_FILENAME = "phase25-myprivateagent-live-trial-outcome-feedback.json"
OUTPUT_MARKDOWN_FILENAME = "phase25-myprivateagent-live-trial-outcome-feedback.md"


@dataclass(frozen=True)
class Phase25TrialOutcomeEvidence:
    trial_outcome_path: str
    input_status: str
    live_trial_status: str
    reason_code: str
    provider_base_url: str
    agent_id: str
    domain: str
    query: str
    provider_retrieve_status: str
    provider_retrieve_reason_code: str
    document_count: int
    evidence_pack_status: str
    citation_policy: str
    allowed_citation_count: int
    missing_critical_fields: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Phase25LiveTrialOutcomeFeedbackReport:
    id: str
    generated_at: str
    status: str
    provider_action: str
    reason_code: str
    recommended_next_actions: list[str]
    summary: dict[str, Any]
    trial_outcome_evidence: Phase25TrialOutcomeEvidence
    notes: list[str] = field(default_factory=list)
    json_path: Path | None = None
    markdown_path: Path | None = None


def build_phase25_live_trial_outcome_feedback_report(
    *,
    trial_outcome_path: Path,
) -> Phase25LiveTrialOutcomeFeedbackReport:
    payload, input_status, input_error = _read_trial_outcome_payload(trial_outcome_path)
    evidence = _build_outcome_evidence(
        trial_outcome_path=trial_outcome_path,
        payload=payload,
        input_status=input_status,
        input_error=input_error,
    )
    status, provider_action, reason_code = _classify_feedback(evidence)

    return Phase25LiveTrialOutcomeFeedbackReport(
        id=PHASE25_LIVE_TRIAL_OUTCOME_FEEDBACK_ID,
        generated_at=datetime.now(UTC).isoformat(),
        status=status,
        provider_action=provider_action,
        reason_code=reason_code,
        recommended_next_actions=_recommended_next_actions(provider_action),
        summary={
            "roadmap_phase": "Phase 25",
            "roadmap_focus": "myprivateagent_live_trial_outcome_feedback_closure",
            "trial_outcome_path": str(trial_outcome_path),
            "input_status": evidence.input_status,
            "live_trial_status": evidence.live_trial_status,
            "provider_retrieve_status": evidence.provider_retrieve_status,
            "document_count": evidence.document_count,
            "evidence_pack_status": evidence.evidence_pack_status,
            "allowed_citation_count": evidence.allowed_citation_count,
            "runtime_promotion_status": "keep_runtime_defaults",
            "retrieval_backend_promotion_status": "not_promoted_by_this_report",
            "graph_execution_status": "planned_boundary_only",
            "source_binding_policy_owner": "caller",
            "trial_execution_owner": "MyPrivateAgent",
        },
        trial_outcome_evidence=evidence,
        notes=[
            "This report is a provider-side feedback closure over an explicit MyPrivateAgent live trial outcome file.",
            "It does not execute MyPrivateAgent, call provider HTTP endpoints, create source-to-agent bindings, or mutate provider runtime defaults.",
            "MyPrivateAgent owns trial execution, final answer policy, source binding policy, and audit behavior.",
            "Provider follow-up should be opened only when this report identifies a provider-owned review or blocked state.",
        ],
    )


def phase25_live_trial_outcome_feedback_report_to_dict(
    report: Phase25LiveTrialOutcomeFeedbackReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_phase25_live_trial_outcome_feedback_markdown(
    report: Phase25LiveTrialOutcomeFeedbackReport,
) -> str:
    evidence = report.trial_outcome_evidence
    lines = [
        "# Phase 25 MyPrivateAgent Live Trial Outcome Feedback",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{report.status}`",
        f"- Provider Action: `{report.provider_action}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
    ]
    for key, value in report.summary.items():
        lines.append(f"| `{key}` | `{_format_value(value)}` |")
    lines.extend(["", "## Trial Outcome Evidence", ""])
    lines.extend(
        [
            "| Field | Value |",
            "|---|---|",
            f"| `trial_outcome_path` | `{evidence.trial_outcome_path}` |",
            f"| `input_status` | `{evidence.input_status}` |",
            f"| `live_trial_status` | `{evidence.live_trial_status}` |",
            f"| `reason_code` | `{evidence.reason_code}` |",
            f"| `provider_base_url` | `{evidence.provider_base_url}` |",
            f"| `agent_id` | `{evidence.agent_id}` |",
            f"| `domain` | `{evidence.domain}` |",
            f"| `provider_retrieve_status` | `{evidence.provider_retrieve_status}` |",
            f"| `provider_retrieve_reason_code` | `{evidence.provider_retrieve_reason_code}` |",
            f"| `document_count` | `{evidence.document_count}` |",
            f"| `evidence_pack_status` | `{evidence.evidence_pack_status}` |",
            f"| `citation_policy` | `{evidence.citation_policy}` |",
            f"| `allowed_citation_count` | `{evidence.allowed_citation_count}` |",
            f"| `missing_critical_fields` | `{_format_value(evidence.missing_critical_fields)}` |",
            f"| `blockers` | `{_format_value(evidence.blockers)}` |",
            f"| `warnings` | `{_format_value(evidence.warnings)}` |",
        ]
    )
    lines.extend(["", "## Recommended Next Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_next_actions)
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in report.notes)
    return "\n".join(lines).rstrip() + "\n"


def export_phase25_live_trial_outcome_feedback_report(
    *,
    trial_outcome_path: Path,
    output_dir: Path = Path(
        "docs/integration/myprivateagent-live-trial-outcome-feedback"
    ),
) -> Phase25LiveTrialOutcomeFeedbackReport:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_phase25_live_trial_outcome_feedback_report(
        trial_outcome_path=trial_outcome_path,
    )
    json_path = output_dir / OUTPUT_JSON_FILENAME
    markdown_path = output_dir / OUTPUT_MARKDOWN_FILENAME
    exported = Phase25LiveTrialOutcomeFeedbackReport(
        id=report.id,
        generated_at=report.generated_at,
        status=report.status,
        provider_action=report.provider_action,
        reason_code=report.reason_code,
        recommended_next_actions=report.recommended_next_actions,
        summary=report.summary,
        trial_outcome_evidence=report.trial_outcome_evidence,
        notes=report.notes,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            phase25_live_trial_outcome_feedback_report_to_dict(exported),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_phase25_live_trial_outcome_feedback_markdown(exported),
        encoding="utf-8",
    )
    return exported


def _read_trial_outcome_payload(path: Path) -> tuple[dict[str, Any], str, str]:
    if not path.exists():
        return {}, "missing", "trial_outcome_file_missing"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}, "invalid", "trial_outcome_json_invalid"
    if not isinstance(payload, dict):
        return {}, "invalid", "trial_outcome_json_not_object"
    return payload, "ready", ""


def _build_outcome_evidence(
    *,
    trial_outcome_path: Path,
    payload: dict[str, Any],
    input_status: str,
    input_error: str,
) -> Phase25TrialOutcomeEvidence:
    payload = _feedback_payload(payload)
    provider_retrieve = _dict_value(payload.get("provider_retrieve"))
    evidence_pack = _dict_value(provider_retrieve.get("evidence_pack"))
    allowed_citations = provider_retrieve.get("allowed_citations")
    if not isinstance(allowed_citations, list):
        allowed_citations = evidence_pack.get("allowed_citations")
    allowed_citations = allowed_citations if isinstance(allowed_citations, list) else []

    blockers = _string_list(payload.get("blockers")) + _string_list(
        provider_retrieve.get("blockers")
    )
    warnings = _string_list(payload.get("warnings")) + _string_list(
        provider_retrieve.get("warnings")
    )
    missing_critical_fields = _detect_missing_critical_fields(
        payload=payload,
        provider_retrieve=provider_retrieve,
    )
    if input_error:
        blockers = [input_error, *blockers]
    if missing_critical_fields:
        warnings = [*warnings, *[f"missing:{field}" for field in missing_critical_fields]]

    return Phase25TrialOutcomeEvidence(
        trial_outcome_path=str(trial_outcome_path),
        input_status=input_status,
        live_trial_status=_string_value(payload.get("live_trial_status")),
        reason_code=_string_value(payload.get("reason_code")),
        provider_base_url=_string_value(payload.get("provider_base_url")),
        agent_id=_string_value(payload.get("agent_id")),
        domain=_string_value(payload.get("domain")),
        query=_string_value(payload.get("query")),
        provider_retrieve_status=_string_value(provider_retrieve.get("status")),
        provider_retrieve_reason_code=_string_value(provider_retrieve.get("reason_code")),
        document_count=_int_value(provider_retrieve.get("document_count")),
        evidence_pack_status=_string_value(
            provider_retrieve.get("evidence_pack_status")
            or evidence_pack.get("status")
        ),
        citation_policy=_string_value(
            provider_retrieve.get("citation_policy")
            or evidence_pack.get("citation_policy")
        ),
        allowed_citation_count=len(allowed_citations),
        missing_critical_fields=missing_critical_fields,
        blockers=blockers,
        warnings=warnings,
    )


def _classify_feedback(
    evidence: Phase25TrialOutcomeEvidence,
) -> tuple[str, str, str]:
    if evidence.input_status != "ready":
        return "blocked", "provider_blocked", "invalid_trial_outcome_input"
    if evidence.missing_critical_fields:
        return "review", "provider_review_required", "incomplete_trial_outcome_input"

    retrieve_status = evidence.provider_retrieve_status
    live_status = evidence.live_trial_status
    if retrieve_status in {"blocked", "failed", "error"}:
        return "blocked", "provider_blocked", "provider_retrieve_failed"
    if live_status == "blocked" and evidence.blockers:
        return "blocked", "provider_blocked", "live_trial_blocked_with_provider_blockers"
    if live_status == "go" and retrieve_status == "ready":
        return "ready", "no_provider_action_required", "caller_live_trial_passed"
    if live_status in {"review", "blocked"}:
        return "review", "provider_review_required", "caller_live_trial_needs_review"
    if evidence.evidence_pack_status in {"insufficient_evidence", "no_documents"}:
        return "review", "provider_review_required", "insufficient_evidence_review"
    return "review", "provider_review_required", "trial_outcome_unclassified"


def _detect_missing_critical_fields(
    *,
    payload: dict[str, Any],
    provider_retrieve: dict[str, Any],
) -> list[str]:
    missing: list[str] = []
    required_top_level = [
        "live_trial_status",
        "reason_code",
        "provider_base_url",
        "agent_id",
        "query",
        "provider_retrieve",
    ]
    for field_name in required_top_level:
        value = payload.get(field_name)
        if field_name == "provider_retrieve":
            if not isinstance(value, dict):
                missing.append(field_name)
        elif not isinstance(value, str) or not value.strip():
            missing.append(field_name)

    required_retrieve_fields = [
        "status",
        "reason_code",
        "document_count",
        "evidence_pack_status",
        "citation_policy",
        "allowed_citations",
    ]
    for field_name in required_retrieve_fields:
        value = provider_retrieve.get(field_name)
        if field_name == "document_count":
            if not isinstance(value, int):
                missing.append(f"provider_retrieve.{field_name}")
        elif field_name == "allowed_citations":
            if not isinstance(value, list):
                missing.append(f"provider_retrieve.{field_name}")
        elif not isinstance(value, str) or not value.strip():
            missing.append(f"provider_retrieve.{field_name}")

    return missing


def _recommended_next_actions(provider_action: str) -> list[str]:
    if provider_action == "no_provider_action_required":
        return [
            "close_provider_access_readiness_loop",
            "keep_runtime_defaults_unchanged",
            "only_open_provider_fix_if_future_trial_exposes_a_concrete_provider_bug",
        ]
    if provider_action == "provider_review_required":
        return [
            "review_trial_evidence_pack_and_citation_allowlist",
            "classify_whether_issue_is_provider_corpus_or_caller_policy",
            "open_focused_provider_change_only_if_provider_owned_gap_is_confirmed",
        ]
    return [
        "open_focused_provider_fix_for_live_trial_blocker",
        "rerun_provider_contract_smoke_after_fix",
        "ask_myprivateagent_to_rerun_live_trial_after_provider_fix",
    ]


def _dict_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _feedback_payload(payload: dict[str, Any]) -> dict[str, Any]:
    nested_payload = payload.get("provider_feedback_input")
    return nested_payload if isinstance(nested_payload, dict) else payload


def _string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _int_value(value: Any) -> int:
    return value if isinstance(value, int) else 0


def _format_value(value: Any) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)
