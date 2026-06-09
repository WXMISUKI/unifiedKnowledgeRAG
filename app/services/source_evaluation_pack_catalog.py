import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.services.local_business_rag_golden_cases import DEFAULT_OUTPUT_DIR


SOURCE_EVALUATION_PACK_CATALOG_ID = "source-evaluation-pack-catalog-v1"
CATALOG_OUTPUT_JSON_FILENAME = "source-evaluation-pack-catalog.json"
CATALOG_OUTPUT_MARKDOWN_FILENAME = "source-evaluation-pack-catalog.md"


@dataclass(frozen=True)
class SourceEvaluationPackEntry:
    pack_id: str
    pack_type: str
    source_scope: str
    artifact_json_path: Path
    artifact_markdown_path: Path
    decision: str
    reason_code: str
    case_count: int
    recommended_next_gate: str
    available: bool
    notes: str


@dataclass(frozen=True)
class SourceEvaluationPackCatalogReport:
    id: str
    generated_at: str
    decision: str
    reason_code: str
    summary: dict[str, Any]
    packs: list[SourceEvaluationPackEntry]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


def export_source_evaluation_pack_catalog(
    *,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> SourceEvaluationPackCatalogReport:
    report = build_source_evaluation_pack_catalog(output_dir=output_dir)
    json_path = output_dir / CATALOG_OUTPUT_JSON_FILENAME
    markdown_path = output_dir / CATALOG_OUTPUT_MARKDOWN_FILENAME
    exported = SourceEvaluationPackCatalogReport(
        id=report.id,
        generated_at=report.generated_at,
        decision=report.decision,
        reason_code=report.reason_code,
        summary=report.summary,
        packs=report.packs,
        recommended_actions=report.recommended_actions,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(source_evaluation_pack_catalog_report_to_dict(exported), ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_source_evaluation_pack_catalog_markdown(exported),
        encoding="utf-8",
    )
    return exported


def build_source_evaluation_pack_catalog(
    *,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> SourceEvaluationPackCatalogReport:
    pack_specs = [
        {
            "pack_id": "local-business-rag-golden-cases-v1",
            "pack_type": "baseline_pack",
            "source_scope": "single_source",
            "artifact_json_path": output_dir / "local-business-rag-golden-cases.json",
            "artifact_markdown_path": output_dir / "local-business-rag-golden-cases.md",
            "default_next_gate": "expand_real_sources_or_failed_packs",
            "notes": "Single-source baseline gate for an approved local business corpus.",
        },
        {
            "pack_id": "real-business-corpus-golden-cases-v1",
            "pack_type": "baseline_pack",
            "source_scope": "multi_source",
            "artifact_json_path": output_dir / "real-business-corpus-golden-cases.json",
            "artifact_markdown_path": output_dir / "real-business-corpus-golden-cases.md",
            "default_next_gate": "expand_real_sources_or_failed_packs",
            "notes": "Aggregate breadth gate across approved real business sources.",
        },
        {
            "pack_id": "real-failed-question-pack-baseline-v1",
            "pack_type": "failed_question_pack",
            "source_scope": "multi_source",
            "artifact_json_path": output_dir / "real-failed-question-pack.json",
            "artifact_markdown_path": output_dir / "real-failed-question-pack.md",
            "default_next_gate": "confirm_failure_class_before_strategy_changes",
            "notes": "Difficulty and boundary-question pack for accepted failure signals.",
        },
        {
            "pack_id": "refund-organization-negative-control-confirmation-v1",
            "pack_type": "confirmation_pack",
            "source_scope": "single_source_confirmation",
            "artifact_json_path": output_dir
            / "refund-organization-negative-control-confirmation.json",
            "artifact_markdown_path": output_dir
            / "refund-organization-negative-control-confirmation.md",
            "default_next_gate": "review_confirmed_failure_class_scope_before_strategy_changes",
            "notes": "Confirmation pack that turns a review candidate into a narrower verdict.",
        },
    ]

    packs = [_load_pack_entry(spec) for spec in pack_specs]
    decision = _catalog_decision(packs)
    return SourceEvaluationPackCatalogReport(
        id=SOURCE_EVALUATION_PACK_CATALOG_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision=decision,
        reason_code=_catalog_reason(decision),
        summary=_catalog_summary(packs),
        packs=packs,
        recommended_actions=_catalog_recommended_actions(decision, packs),
        non_goals=_non_goals(),
    )


def source_evaluation_pack_catalog_report_to_dict(
    report: SourceEvaluationPackCatalogReport,
) -> dict[str, Any]:
    payload = asdict(report)
    for pack in payload.get("packs", []):
        if "artifact_json_path" in pack:
            pack["artifact_json_path"] = str(pack["artifact_json_path"])
        if "artifact_markdown_path" in pack:
            pack["artifact_markdown_path"] = str(pack["artifact_markdown_path"])
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_source_evaluation_pack_catalog_markdown(
    report: SourceEvaluationPackCatalogReport,
) -> str:
    lines = [
        "# Source Evaluation Pack Catalog",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
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
    lines.extend(
        [
            "",
            "## Packs",
            "",
            "| Pack ID | Type | Scope | Decision | Cases | Next Gate | Available |",
            "|---|---|---|---|---:|---|---|",
        ]
    )
    for pack in report.packs:
        lines.append(
            f"| `{pack.pack_id}` | `{pack.pack_type}` | `{pack.source_scope}` | "
            f"`{pack.decision}` | `{pack.case_count}` | `{pack.recommended_next_gate}` | "
            f"`{pack.available}` |"
        )
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in report.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def _load_pack_entry(spec: dict[str, Any]) -> SourceEvaluationPackEntry:
    artifact_json_path = Path(spec["artifact_json_path"])
    artifact_markdown_path = Path(spec["artifact_markdown_path"])
    if not artifact_json_path.exists():
        return SourceEvaluationPackEntry(
            pack_id=str(spec["pack_id"]),
            pack_type=str(spec["pack_type"]),
            source_scope=str(spec["source_scope"]),
            artifact_json_path=artifact_json_path,
            artifact_markdown_path=artifact_markdown_path,
            decision="missing",
            reason_code="artifact_missing",
            case_count=0,
            recommended_next_gate="refresh_missing_evaluation_artifact",
            available=False,
            notes=str(spec["notes"]),
        )

    payload = json.loads(artifact_json_path.read_text(encoding="utf-8"))
    summary = payload.get("summary", {})
    case_count = int(
        summary.get("case_count")
        or summary.get("variant_count")
        or 0
    )
    recommended_next_gate = _pack_recommended_next_gate(
        pack_type=str(spec["pack_type"]),
        decision=str(payload.get("decision") or "review"),
        payload=payload,
        default_next_gate=str(spec["default_next_gate"]),
    )
    return SourceEvaluationPackEntry(
        pack_id=str(payload.get("id") or spec["pack_id"]),
        pack_type=str(spec["pack_type"]),
        source_scope=str(spec["source_scope"]),
        artifact_json_path=artifact_json_path,
        artifact_markdown_path=artifact_markdown_path,
        decision=str(payload.get("decision") or "review"),
        reason_code=str(payload.get("reason_code") or "evaluation_artifact_review"),
        case_count=case_count,
        recommended_next_gate=recommended_next_gate,
        available=True,
        notes=str(spec["notes"]),
    )


def _pack_recommended_next_gate(
    *,
    pack_type: str,
    decision: str,
    payload: dict[str, Any],
    default_next_gate: str,
) -> str:
    summary = payload.get("summary", {})
    if isinstance(summary, dict) and summary.get("recommended_next_gate"):
        return str(summary["recommended_next_gate"])
    if pack_type == "confirmation_pack":
        return str(summary.get("recommended_next_gate") or default_next_gate)
    if decision == "go":
        return "expand_real_sources_or_failed_packs"
    return default_next_gate


def _catalog_decision(packs: list[SourceEvaluationPackEntry]) -> str:
    if any(not pack.available for pack in packs):
        return "review"
    if any(pack.decision == "blocked" for pack in packs):
        return "blocked"
    if any(pack.decision == "review" for pack in packs):
        return "review"
    return "go"


def _catalog_reason(decision: str) -> str:
    if decision == "go":
        return "source_evaluation_pack_catalog_ready"
    if decision == "blocked":
        return "source_evaluation_pack_catalog_blocked"
    return "source_evaluation_pack_catalog_needs_review"


def _catalog_summary(packs: list[SourceEvaluationPackEntry]) -> dict[str, Any]:
    return {
        "pack_count": len(packs),
        "available_pack_count": sum(1 for pack in packs if pack.available),
        "missing_pack_count": sum(1 for pack in packs if not pack.available),
        "baseline_pack_count": sum(1 for pack in packs if pack.pack_type == "baseline_pack"),
        "failed_question_pack_count": sum(
            1 for pack in packs if pack.pack_type == "failed_question_pack"
        ),
        "confirmation_pack_count": sum(
            1 for pack in packs if pack.pack_type == "confirmation_pack"
        ),
        "review_pack_ids": [pack.pack_id for pack in packs if pack.decision == "review"],
        "missing_pack_ids": [pack.pack_id for pack in packs if not pack.available],
    }


def _catalog_recommended_actions(
    decision: str,
    packs: list[SourceEvaluationPackEntry],
) -> list[str]:
    actions: list[str] = []
    if any(not pack.available for pack in packs):
        actions.append("refresh_missing_evaluation_artifacts_before_strategy_changes")
    review_packs = [pack for pack in packs if pack.decision == "review"]
    if any(pack.pack_type == "failed_question_pack" for pack in review_packs):
        actions.append("confirm_failure_class_before_strategy_changes")
    if any(pack.pack_type == "confirmation_pack" for pack in review_packs):
        actions.append("review_confirmed_failure_class_scope_before_strategy_changes")
    if decision == "go":
        actions.append("expand_real_sources_or_failed_packs")
    if not actions:
        actions.append("keep_runtime_defaults_and_reuse_existing_evaluation_packs")
    return actions


def _non_goals() -> list[str]:
    return [
        "does_not_rerun_underlying_retrieval_evaluations",
        "does_not_change_runtime_retrieval_defaults",
        "does_not_enable_query_rewrite_rerank_or_hybrid",
        "does_not_create_source_to_agent_binding",
        "does_not_execute_graphrag",
    ]


def _format_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
