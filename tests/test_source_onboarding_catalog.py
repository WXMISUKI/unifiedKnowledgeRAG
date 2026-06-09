import json

from app.services.source_onboarding_catalog import (
    build_source_onboarding_catalog,
    export_source_onboarding_catalog,
)


def test_source_onboarding_catalog_summarizes_ready_and_template_only_sources(tmp_path):
    onboarding_root = tmp_path / "onboarding"
    _write_onboarding_source(
        onboarding_root / "template_demo",
        source_id="template_demo",
        include_real_baseline=False,
        validation_decision=None,
    )
    _write_onboarding_source(
        onboarding_root / "ready_demo",
        source_id="ready_demo",
        include_real_baseline=True,
        validation_decision="go",
    )

    report = build_source_onboarding_catalog(
        onboarding_root=onboarding_root,
        output_dir=tmp_path,
    )

    assert report.summary["source_count"] == 2
    assert report.summary["ready_source_count"] == 1
    assert report.summary["template_only_source_count"] == 1
    ready_entry = next(entry for entry in report.entries if entry.source_id == "ready_demo")
    assert ready_entry.onboarding_status == "ready"
    assert ready_entry.validation_decision == "go"
    template_entry = next(
        entry for entry in report.entries if entry.source_id == "template_demo"
    )
    assert template_entry.onboarding_status == "template_only"
    assert template_entry.recommended_next_step == "fill_real_baseline_fixture"


def test_source_onboarding_catalog_marks_review_when_validation_is_review(tmp_path):
    onboarding_root = tmp_path / "onboarding"
    _write_onboarding_source(
        onboarding_root / "review_demo",
        source_id="review_demo",
        include_real_baseline=True,
        validation_decision="review",
    )

    report = export_source_onboarding_catalog(
        onboarding_root=onboarding_root,
        output_dir=tmp_path,
    )

    assert report.decision == "review"
    assert report.summary["review_source_count"] == 1
    assert report.json_path.exists()
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    assert payload["summary"]["review_source_count"] == 1
    entry = payload["entries"][0]
    assert entry["onboarding_status"] == "review"
    assert entry["recommended_next_step"] == "review_validation_findings_before_strategy_changes"


def _write_onboarding_source(
    path,
    *,
    source_id: str,
    include_real_baseline: bool,
    validation_decision: str | None,
):
    path.mkdir(parents=True, exist_ok=True)
    (path / "baseline-pack.fixture.template.json").write_text("[]\n", encoding="utf-8")
    (path / "failed-question-pack.fixture.template.json").write_text("[]\n", encoding="utf-8")
    (path / "confirmation-pack.fixture.template.json").write_text("[]\n", encoding="utf-8")
    (path / "source-evaluation-pack-onboarding.json").write_text(
        json.dumps(
            {
                "id": "source-evaluation-pack-onboarding-v1",
                "source_id": source_id,
                "summary": {"template_count": 3},
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    if include_real_baseline:
        (path / "baseline-pack.fixture.json").write_text("[]\n", encoding="utf-8")
    if validation_decision is not None:
        (path / f"{source_id}-validation.json").write_text(
            json.dumps(
                {
                    "id": "local-business-rag-golden-cases-v1",
                    "source_id": source_id,
                    "decision": validation_decision,
                    "reason_code": f"{validation_decision}_reason",
                    "summary": {"case_count": 3},
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
