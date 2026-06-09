import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.services.local_business_rag_golden_cases import DEFAULT_OUTPUT_DIR


SOURCE_EVALUATION_PACK_ONBOARDING_ID = "source-evaluation-pack-onboarding-v1"
DEFAULT_ONBOARDING_ROOT = DEFAULT_OUTPUT_DIR / "onboarding"
ONBOARDING_JSON_FILENAME = "source-evaluation-pack-onboarding.json"
ONBOARDING_MARKDOWN_FILENAME = "source-evaluation-pack-onboarding.md"


@dataclass(frozen=True)
class SourceEvaluationTemplateArtifact:
    pack_type: str
    path: Path
    template_case_count: int
    notes: str


@dataclass(frozen=True)
class SourceEvaluationPackOnboardingReport:
    id: str
    generated_at: str
    source_id: str
    output_dir: Path
    summary: dict[str, Any]
    generated_templates: list[SourceEvaluationTemplateArtifact]
    recommended_next_steps: list[str]
    non_goals: list[str]
    json_path: Path | None = None
    markdown_path: Path | None = None


def export_source_evaluation_pack_onboarding(
    *,
    source_id: str,
    output_root: Path = DEFAULT_ONBOARDING_ROOT,
) -> SourceEvaluationPackOnboardingReport:
    report = build_source_evaluation_pack_onboarding(source_id=source_id, output_root=output_root)
    output_dir = report.output_dir
    json_path = output_dir / ONBOARDING_JSON_FILENAME
    markdown_path = output_dir / ONBOARDING_MARKDOWN_FILENAME
    exported = SourceEvaluationPackOnboardingReport(
        id=report.id,
        generated_at=report.generated_at,
        source_id=report.source_id,
        output_dir=report.output_dir,
        summary=report.summary,
        generated_templates=report.generated_templates,
        recommended_next_steps=report.recommended_next_steps,
        non_goals=report.non_goals,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(source_evaluation_pack_onboarding_report_to_dict(exported), ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_source_evaluation_pack_onboarding_markdown(exported),
        encoding="utf-8",
    )
    return exported


def build_source_evaluation_pack_onboarding(
    *,
    source_id: str,
    output_root: Path = DEFAULT_ONBOARDING_ROOT,
) -> SourceEvaluationPackOnboardingReport:
    output_dir = output_root / source_id
    output_dir.mkdir(parents=True, exist_ok=True)
    templates = [
        _write_template(
            path=output_dir / "baseline-pack.fixture.template.json",
            payload=_baseline_template(source_id),
            pack_type="baseline_pack",
            notes="Start with answerable and insufficient-evidence golden cases for the new source.",
        ),
        _write_template(
            path=output_dir / "failed-question-pack.fixture.template.json",
            payload=_failed_question_template(source_id),
            pack_type="failed_question_pack",
            notes="Use for difficult, failed, or boundary questions after baseline exists.",
        ),
        _write_template(
            path=output_dir / "confirmation-pack.fixture.template.json",
            payload=_confirmation_template(source_id),
            pack_type="confirmation_pack",
            notes="Use only when a repeated failure candidate needs a narrower confirmation verdict.",
        ),
    ]
    return SourceEvaluationPackOnboardingReport(
        id=SOURCE_EVALUATION_PACK_ONBOARDING_ID,
        generated_at=datetime.now(UTC).isoformat(),
        source_id=source_id,
        output_dir=output_dir,
        summary={
            "template_count": len(templates),
            "pack_types": [template.pack_type for template in templates],
            "output_dir": str(output_dir),
        },
        generated_templates=templates,
        recommended_next_steps=[
            "fill_baseline_template_with_real_answerable_and_insufficient_evidence_cases",
            "export_real_pack_only_after_template_fields_are_replaced_with_real_questions",
            "use_failed_question_pack_after_a_source_has_a_passing_or_reviewable_baseline",
            "use_confirmation_pack_only_for_repeated_failure_candidates",
            "update_source_evaluation_pack_catalog_after_real_pack_artifacts_exist",
        ],
        non_goals=_non_goals(),
    )


def source_evaluation_pack_onboarding_report_to_dict(
    report: SourceEvaluationPackOnboardingReport,
) -> dict[str, Any]:
    payload = asdict(report)
    payload["output_dir"] = str(report.output_dir)
    for template in payload.get("generated_templates", []):
        template["path"] = str(template["path"])
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_source_evaluation_pack_onboarding_markdown(
    report: SourceEvaluationPackOnboardingReport,
) -> str:
    lines = [
        "# Source Evaluation Pack Onboarding",
        "",
        f"- Report: `{report.id}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Source ID: `{report.source_id}`",
        f"- Output Dir: `{report.output_dir}`",
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
            "## Generated Templates",
            "",
            "| Pack Type | Path | Template Cases | Notes |",
            "|---|---|---:|---|",
        ]
    )
    for template in report.generated_templates:
        lines.append(
            f"| `{template.pack_type}` | `{template.path}` | "
            f"`{template.template_case_count}` | `{template.notes}` |"
        )
    lines.extend(["", "## Recommended Next Steps", ""])
    lines.extend(f"- {step}" for step in report.recommended_next_steps)
    lines.extend(["", "## Non-Goals", ""])
    lines.extend(f"- {item}" for item in report.non_goals)
    return "\n".join(lines).rstrip() + "\n"


def _write_template(
    *,
    path: Path,
    payload: list[dict[str, Any]],
    pack_type: str,
    notes: str,
) -> SourceEvaluationTemplateArtifact:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return SourceEvaluationTemplateArtifact(
        pack_type=pack_type,
        path=path,
        template_case_count=len(payload),
        notes=notes,
    )


def _baseline_template(source_id: str) -> list[dict[str, Any]]:
    return [
        {
            "id": f"{source_id}-answerable-example",
            "query": "REPLACE_WITH_REAL_ANSWERABLE_QUERY",
            "expected_mode": "answerable",
            "expected_source_id": source_id,
            "expected_citation_prefix": f"{source_id}#",
            "business_question_type": "replace_me",
            "description": "Template placeholder for a real answerable baseline case.",
        },
        {
            "id": f"{source_id}-negative-control-example",
            "query": "REPLACE_WITH_REAL_INSUFFICIENT_EVIDENCE_QUERY",
            "expected_mode": "insufficient_evidence",
            "expected_source_id": None,
            "expected_citation_prefix": None,
            "business_question_type": "negative_control",
            "description": "Template placeholder for a real fail-closed baseline case.",
        },
    ]


def _failed_question_template(source_id: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "case_id": f"{source_id}-failed-question-example",
            "query": "REPLACE_WITH_REAL_FAILED_OR_BOUNDARY_QUERY",
            "expected_mode": "insufficient_evidence",
            "expected_citation_prefix": None,
            "business_question_type": "replace_me",
            "failure_mode": "unclassified",
            "risk_level": "medium",
            "question_origin": "accepted_real_failure_candidate",
            "observed_failure": "replace_with_observed_failure",
            "notes": "Template placeholder for a difficult or failed real question.",
            "description": "Template placeholder for failed-question-pack onboarding.",
        }
    ]


def _confirmation_template(source_id: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "case_id": f"{source_id}-confirmation-negative-example",
            "query": "REPLACE_WITH_REAL_NEGATIVE_VARIANT_QUERY",
            "expected_mode": "insufficient_evidence",
            "expected_citation_prefix": None,
            "business_question_type": "replace_me",
            "failure_mode": "unclassified",
            "risk_level": "high",
            "question_origin": "accepted_real_failure_candidate",
            "observed_failure": "replace_with_repeated_failure_signal",
            "notes": "Template placeholder for a negative or boundary confirmation case.",
            "description": "Template placeholder for confirmation-pack negative variant.",
        },
        {
            "source_id": source_id,
            "case_id": f"{source_id}-confirmation-positive-example",
            "query": "REPLACE_WITH_REAL_POSITIVE_VARIANT_QUERY",
            "expected_mode": "answerable",
            "expected_citation_prefix": f"{source_id}#",
            "business_question_type": "replace_me",
            "failure_mode": "unclassified",
            "risk_level": "medium",
            "question_origin": "real_boundary_question",
            "observed_failure": "replace_with_neighbor_positive_expectation",
            "notes": "Template placeholder for a positive confirmation control.",
            "description": "Template placeholder for confirmation-pack positive variant.",
        },
    ]


def _non_goals() -> list[str]:
    return [
        "does_not_run_retrieve_or_answer_evaluation",
        "does_not_generate_real_business_questions_automatically",
        "does_not_infer_failure_classes_automatically",
        "does_not_change_runtime_retrieval_defaults",
        "does_not_enable_query_rewrite_rerank_hybrid_or_graphrag",
    ]


def _format_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)
