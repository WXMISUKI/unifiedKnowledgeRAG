import json

from app.services.source_evaluation_pack_onboarding import (
    build_source_evaluation_pack_onboarding,
    export_source_evaluation_pack_onboarding,
)


def test_source_evaluation_pack_onboarding_writes_templates(tmp_path):
    report = export_source_evaluation_pack_onboarding(
        source_id="sample_source",
        output_root=tmp_path / "onboarding",
    )

    assert report.source_id == "sample_source"
    assert report.summary["template_count"] == 3
    assert report.json_path.exists()
    assert report.markdown_path.exists()
    for template in report.generated_templates:
        assert template.path.exists()

    baseline_payload = json.loads(
        (tmp_path / "onboarding" / "sample_source" / "baseline-pack.fixture.template.json").read_text(
            encoding="utf-8"
        )
    )
    assert baseline_payload[0]["expected_source_id"] == "sample_source"
    assert baseline_payload[1]["expected_mode"] == "insufficient_evidence"


def test_source_evaluation_pack_onboarding_exposes_conservative_next_steps(tmp_path):
    report = build_source_evaluation_pack_onboarding(
        source_id="template_demo",
        output_root=tmp_path / "onboarding",
    )

    assert len(report.generated_templates) == 3
    assert "fill_baseline_template_with_real_answerable_and_insufficient_evidence_cases" in report.recommended_next_steps
    assert "does_not_run_retrieve_or_answer_evaluation" in report.non_goals
    confirmation_template = next(
        template for template in report.generated_templates if template.pack_type == "confirmation_pack"
    )
    assert confirmation_template.template_case_count == 2
