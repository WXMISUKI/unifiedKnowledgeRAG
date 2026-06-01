import json

from app.services.phase3_hybrid_fusion_threshold_calibration import (
    build_phase3_hybrid_fusion_threshold_calibration_report,
    export_phase3_hybrid_fusion_threshold_calibration_report,
    render_phase3_hybrid_fusion_threshold_calibration_markdown,
)


def test_build_phase3_hybrid_fusion_threshold_calibration_report_summarizes_current_evidence():
    report = build_phase3_hybrid_fusion_threshold_calibration_report()

    assert report.id == "phase3-hybrid-fusion-threshold-calibration-v1"
    assert report.status == "review"
    assert report.decision == "keep_runtime_defaults"
    assert report.summary["total_signals"] == 6
    assert report.summary["ready_signals"] == 3
    assert report.summary["review_signals"] == 3
    assert report.calibration["fusion_mode"] == "rrf"
    assert report.calibration["score_filter_mode"] == "disabled-for-rrf-fusion-score"
    assert report.calibration["selected_dense_threshold"] == 0.7
    assert report.calibration["runtime_threshold"] == 0.01
    assert report.calibration["threshold_delta"] == 0.69
    assert report.calibration["hybrid_exact_term_hit_rate"] == 1.0
    assert report.calibration["hybrid_empty_stress_empty_handling_rate"] == 0.0
    assert "runtime_threshold_alignment" in report.summary["open_signal_ids"]


def test_export_phase3_hybrid_fusion_threshold_calibration_report_writes_artifacts(tmp_path):
    report = export_phase3_hybrid_fusion_threshold_calibration_report(
        output_dir=tmp_path / "hybrid-calibration",
    )

    assert report.json_path == (
        tmp_path
        / "hybrid-calibration"
        / "phase3-hybrid-fusion-threshold-calibration.json"
    )
    assert report.markdown_path == (
        tmp_path
        / "hybrid-calibration"
        / "phase3-hybrid-fusion-threshold-calibration.md"
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["status"] == report.status
    assert payload["decision"] == report.decision
    assert "# Phase 3 Hybrid Fusion Threshold Calibration" in markdown
    assert "| Signal | Status | Summary | Recommended Action |" in markdown
    assert render_phase3_hybrid_fusion_threshold_calibration_markdown(report) == markdown
