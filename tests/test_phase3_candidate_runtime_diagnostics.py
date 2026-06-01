import json
from pathlib import Path

from app.services.phase3_candidate_runtime_diagnostics import (
    build_phase3_candidate_runtime_diagnostics_report,
    export_phase3_candidate_runtime_diagnostics_report,
    render_phase3_candidate_runtime_diagnostics_markdown,
)


def test_build_phase3_candidate_runtime_diagnostics_report_summarizes_defaults():
    report = build_phase3_candidate_runtime_diagnostics_report()

    assert report.id == "phase3-candidate-runtime-diagnostics-v1"
    assert report.status == "review"
    assert report.decision == "keep_runtime_defaults"
    assert report.summary["total_checks"] == 6
    assert report.summary["ready_checks"] >= 0
    assert report.summary["review_checks"] >= 1
    assert report.summary["blocked_checks"] == 0
    assert "candidate_embedding_provider" in report.summary["open_prerequisite_ids"]
    assert report.runtime_config["embedding_provider"] == "mock"


def test_export_phase3_candidate_runtime_diagnostics_report_writes_artifacts(tmp_path):
    readiness_dir = (
        tmp_path
        / "docs/benchmark/chinese-seed/retrieval-promotion-readiness"
    )
    readiness_dir.mkdir(parents=True, exist_ok=True)
    readiness_dir.joinpath("phase3-retrieval-promotion-readiness.json").write_text(
        json.dumps(
            {
                "status": "review",
                "decision": "keep_runtime_defaults",
                "summary": {"open_gates": 7},
            }
        ),
        encoding="utf-8",
    )

    report = export_phase3_candidate_runtime_diagnostics_report(
        output_dir=tmp_path / "diagnostics",
        base_dir=tmp_path,
    )

    assert report.json_path == (
        tmp_path / "diagnostics" / "phase3-candidate-runtime-diagnostics.json"
    )
    assert report.markdown_path == (
        tmp_path / "diagnostics" / "phase3-candidate-runtime-diagnostics.md"
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")
    assert payload["id"] == report.id
    assert payload["status"] == report.status
    assert payload["decision"] == report.decision
    assert payload["json_path"] == str(report.json_path)
    assert "# Phase 3 Candidate Runtime Diagnostics" in markdown
    assert "| Prerequisite | Status | Summary | Recommended Action |" in markdown
    assert render_phase3_candidate_runtime_diagnostics_markdown(report) == markdown


def test_runtime_diagnostics_marks_missing_readiness_as_review(tmp_path):
    report = build_phase3_candidate_runtime_diagnostics_report(base_dir=tmp_path)

    prereq = {item.id: item for item in report.prerequisites}
    assert report.status == "review"
    assert prereq["phase3_readiness_export"].status == "review"
    assert prereq["phase3_readiness_export"].recommended_action == (
        "regenerate_phase3_retrieval_promotion_readiness"
    )
