import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.services.local_business_rag_golden_cases import DEFAULT_OUTPUT_DIR
from app.services.source_evaluation_pack_onboarding import (
    DEFAULT_ONBOARDING_ROOT,
    ONBOARDING_JSON_FILENAME,
)


SOURCE_ONBOARDING_CATALOG_ID = "source-onboarding-catalog-v1"
SOURCE_ONBOARDING_CATALOG_JSON_FILENAME = "source-onboarding-catalog.json"
SOURCE_ONBOARDING_CATALOG_MARKDOWN_FILENAME = "source-onboarding-catalog.md"


@dataclass(frozen=True)
class SourceOnboardingCatalogEntry:
    source_id: str
    onboarding_dir: Path
    template_count: int
    has_baseline_template: bool
    has_failed_question_template: bool
    has_confirmation_template: bool
    has_real_baseline_fixture: bool
    has_validation_report: bool
    validation_report_path: Path | None
    validation_decision: str | None
    validation_reason_code: str | None
    onboarding_status: str
    recommended_next_step: str
    notes: str


@dataclass(frozen=True)
class SourceOnboardingCatalogReport:
    id: str
    generated_at: str
    decision: str
    reason_code: str
    onboarding_root: Path
    summary: dict[str, Any]
    entries: list[SourceOnboardingCatalogEntry]
    recommended_actions: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


def export_source_onboarding_catalog(
    *,
    onboarding_root: Path = DEFAULT_ONBOARDING_ROOT,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> SourceOnboardingCatalogReport:
    report = build_source_onboarding_catalog(
        onboarding_root=onboarding_root,
        output_dir=output_dir,
    )
    json_path = output_dir / SOURCE_ONBOARDING_CATALOG_JSON_FILENAME
    markdown_path = output_dir / SOURCE_ONBOARDING_CATALOG_MARKDOWN_FILENAME
    exported = SourceOnboardingCatalogReport(
        id=report.id,
        generated_at=report.generated_at,
        decision=report.decision,
        reason_code=report.reason_code,
        onboarding_root=report.onboarding_root,
        summary=report.summary,
        entries=report.entries,
        recommended_actions=report.recommended_actions,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(source_onboarding_catalog_report_to_dict(exported), ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_source_onboarding_catalog_markdown(exported),
        encoding="utf-8",
    )
    return exported


def build_source_onboarding_catalog(
    *,
    onboarding_root: Path = DEFAULT_ONBOARDING_ROOT,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> SourceOnboardingCatalogReport:
    entries = [
        _build_entry(source_dir)
        for source_dir in sorted(
            (path for path in onboarding_root.iterdir() if path.is_dir()),
            key=lambda path: path.name,
        )
    ] if onboarding_root.exists() else []
    decision = _catalog_decision(entries)
    return SourceOnboardingCatalogReport(
        id=SOURCE_ONBOARDING_CATALOG_ID,
        generated_at=datetime.now(UTC).isoformat(),
        decision=decision,
        reason_code=_catalog_reason(decision),
        onboarding_root=onboarding_root,
        summary=_catalog_summary(entries, onboarding_root, output_dir),
        entries=entries,
        recommended_actions=_recommended_actions(decision, entries),
        non_goals=_non_goals(),
    )


def source_onboarding_catalog_report_to_dict(
    report: SourceOnboardingCatalogReport,
) -> dict[str, Any]:
    payload = asdict(report)
    payload["onboarding_root"] = str(report.onboarding_root)
    for entry in payload.get("entries", []):
        entry["onboarding_dir"] = str(entry["onboarding_dir"])
        if entry.get("validation_report_path") is not None:
            entry["validation_report_path"] = str(entry["validation_report_path"])
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_source_onboarding_catalog_markdown(
    report: SourceOnboardingCatalogReport,
) -> str:
    lines = [
        "# Source Onboarding Catalog",
        "",
        f"- Report: `{report.id}`",
        f"- Decision: `{report.decision}`",
        f"- Reason: `{report.reason_code}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Onboarding Root: `{report.onboarding_root}`",
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
            "## Sources",
            "",
            "| Source ID | Status | Templates | Baseline Fixture | Validation | Validation Decision | Next Step |",
            "|---|---|---:|---|---|---|---|",
        ]
    )
    for entry in report.entries:
        lines.append(
            f"| `{entry.source_id}` | `{entry.onboarding_status}` | `{entry.template_count}` | "
            f"`{entry.has_real_baseline_fixture}` | `{entry.has_validation_report}` | "
            f"`{entry.validation_decision or 'n/a'}` | `{entry.recommended_next_step}` |"
        )
    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {action}" for action in report.recommended_actions)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in report.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def _build_entry(source_dir: Path) -> SourceOnboardingCatalogEntry:
    onboarding_json_path = source_dir / ONBOARDING_JSON_FILENAME
    onboarding_payload = _load_json(onboarding_json_path)
    template_count = int((onboarding_payload.get("summary") or {}).get("template_count") or 0)
    baseline_template_path = source_dir / "baseline-pack.fixture.template.json"
    failed_question_template_path = source_dir / "failed-question-pack.fixture.template.json"
    confirmation_template_path = source_dir / "confirmation-pack.fixture.template.json"
    real_baseline_fixture_path = source_dir / "baseline-pack.fixture.json"
    validation_report_path = _find_validation_report(source_dir)
    validation_payload = _load_json(validation_report_path) if validation_report_path else {}
    validation_decision = _string_or_none(validation_payload.get("decision"))
    validation_reason_code = _string_or_none(validation_payload.get("reason_code"))
    onboarding_status = _entry_status(
        has_onboarding=onboarding_json_path.exists(),
        has_templates=all(
            path.exists()
            for path in (
                baseline_template_path,
                failed_question_template_path,
                confirmation_template_path,
            )
        ),
        has_real_baseline_fixture=real_baseline_fixture_path.exists(),
        validation_decision=validation_decision,
    )
    return SourceOnboardingCatalogEntry(
        source_id=source_dir.name,
        onboarding_dir=source_dir,
        template_count=template_count,
        has_baseline_template=baseline_template_path.exists(),
        has_failed_question_template=failed_question_template_path.exists(),
        has_confirmation_template=confirmation_template_path.exists(),
        has_real_baseline_fixture=real_baseline_fixture_path.exists(),
        has_validation_report=validation_report_path is not None,
        validation_report_path=validation_report_path,
        validation_decision=validation_decision,
        validation_reason_code=validation_reason_code,
        onboarding_status=onboarding_status,
        recommended_next_step=_recommended_next_step(
            onboarding_status=onboarding_status,
            validation_decision=validation_decision,
        ),
        notes=_notes(
            onboarding_status=onboarding_status,
            validation_decision=validation_decision,
        ),
    )


def _find_validation_report(source_dir: Path) -> Path | None:
    candidates = [
        path
        for path in source_dir.glob("*.json")
        if path.name not in {
            ONBOARDING_JSON_FILENAME,
            "baseline-pack.fixture.json",
            "baseline-pack.fixture.template.json",
            "failed-question-pack.fixture.template.json",
            "confirmation-pack.fixture.template.json",
        }
    ]
    if not candidates:
        return None
    return sorted(candidates, key=lambda path: path.name)[0]


def _entry_status(
    *,
    has_onboarding: bool,
    has_templates: bool,
    has_real_baseline_fixture: bool,
    validation_decision: str | None,
) -> str:
    if not has_onboarding:
        return "missing"
    if validation_decision == "go":
        return "ready"
    if validation_decision in {"review", "blocked"}:
        return "review"
    if has_templates and has_real_baseline_fixture:
        return "baseline_ready"
    if has_templates:
        return "template_only"
    return "missing"


def _recommended_next_step(
    *,
    onboarding_status: str,
    validation_decision: str | None,
) -> str:
    if onboarding_status == "ready":
        return "consider_catalog_bridge_or_add_next_distinct_source"
    if onboarding_status == "review":
        if validation_decision == "blocked":
            return "restore_missing_or_blocked_validation_artifacts"
        return "review_validation_findings_before_strategy_changes"
    if onboarding_status == "baseline_ready":
        return "run_real_baseline_validation_export"
    if onboarding_status == "template_only":
        return "fill_real_baseline_fixture"
    return "rebuild_onboarding_templates"


def _notes(
    *,
    onboarding_status: str,
    validation_decision: str | None,
) -> str:
    if onboarding_status == "ready":
        return "Onboarding templates and real validation evidence are both present."
    if onboarding_status == "review":
        return f"Validation report exists with decision `{validation_decision or 'unknown'}`."
    if onboarding_status == "baseline_ready":
        return "Real baseline fixture exists but validation report is still missing."
    if onboarding_status == "template_only":
        return "Only template scaffolding exists; no real baseline validation yet."
    return "Expected onboarding artifacts are missing."


def _catalog_decision(entries: list[SourceOnboardingCatalogEntry]) -> str:
    if not entries:
        return "review"
    if any(entry.onboarding_status == "missing" for entry in entries):
        return "review"
    if any(entry.onboarding_status == "review" for entry in entries):
        return "review"
    return "go"


def _catalog_reason(decision: str) -> str:
    if decision == "go":
        return "source_onboarding_catalog_ready"
    return "source_onboarding_catalog_needs_review"


def _catalog_summary(
    entries: list[SourceOnboardingCatalogEntry],
    onboarding_root: Path,
    output_dir: Path,
) -> dict[str, Any]:
    return {
        "source_count": len(entries),
        "ready_source_count": sum(1 for entry in entries if entry.onboarding_status == "ready"),
        "template_only_source_count": sum(
            1 for entry in entries if entry.onboarding_status == "template_only"
        ),
        "baseline_ready_source_count": sum(
            1 for entry in entries if entry.onboarding_status == "baseline_ready"
        ),
        "review_source_count": sum(1 for entry in entries if entry.onboarding_status == "review"),
        "missing_source_count": sum(1 for entry in entries if entry.onboarding_status == "missing"),
        "ready_source_ids": [
            entry.source_id for entry in entries if entry.onboarding_status == "ready"
        ],
        "template_only_source_ids": [
            entry.source_id for entry in entries if entry.onboarding_status == "template_only"
        ],
        "onboarding_root": str(onboarding_root),
        "output_dir": str(output_dir),
        "runtime_promotion_status": "keep_runtime_defaults",
        "source_registration_status": "not_created",
        "aggregate_baseline_expansion_status": "not_expanded",
    }


def _recommended_actions(
    decision: str,
    entries: list[SourceOnboardingCatalogEntry],
) -> list[str]:
    actions: list[str] = []
    if any(entry.onboarding_status == "template_only" for entry in entries):
        actions.append("fill_real_baseline_fixtures_for_template_only_sources")
    if any(entry.onboarding_status == "baseline_ready" for entry in entries):
        actions.append("run_validation_export_for_baseline_ready_sources")
    if any(entry.onboarding_status == "review" for entry in entries):
        actions.append("review_validation_findings_before_strategy_changes")
    if decision == "go":
        actions.append("consider_evidence_only_bridge_into_source_evaluation_pack_catalog")
    if not actions:
        actions.append("rebuild_or_refresh_onboarding_artifacts")
    return actions


def _non_goals() -> list[str]:
    return [
        "does_not_register_sources_into_provider_runtime",
        "does_not_expand_main_aggregate_baseline_automatically",
        "does_not_rerun_retrieval_or_answer_evaluations",
        "does_not_change_runtime_retrieval_defaults",
        "does_not_enable_query_rewrite_rerank_hybrid_or_graphrag",
    ]


def _load_json(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _format_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
