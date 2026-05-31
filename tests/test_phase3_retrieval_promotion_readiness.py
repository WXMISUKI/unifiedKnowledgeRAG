import json
from pathlib import Path

from app.services.phase3_retrieval_promotion_readiness import (
    build_phase3_retrieval_promotion_readiness_report,
    export_phase3_retrieval_promotion_readiness_report,
    render_phase3_retrieval_promotion_readiness_markdown,
)


def test_build_phase3_retrieval_promotion_readiness_report_summarizes_current_evidence():
    report = build_phase3_retrieval_promotion_readiness_report()

    assert report.id == "phase3-retrieval-promotion-readiness-v1"
    assert report.status == "review"
    assert report.decision == "keep_runtime_defaults"
    assert report.gap_matrix_path == (
        "docs/benchmark/chinese-seed/retrieval-promotion-readiness/"
        "phase3-retrieval-promotion-gap-matrix.md"
    )

    gates = {gate.id: gate for gate in report.gates}
    assert gates["qdrant_vector_store"].status in {"candidate", "review"}
    assert any(
        path.endswith("qdrant-bge-m3-smoke.json")
        for path in gates["qdrant_vector_store"].evidence_paths
    )
    assert gates["deployed_smoke"].status == "review"
    assert gates["deployed_smoke"].evidence_present is False
    assert gates["deployed_smoke"].recommended_action == (
        "run_deployed_provider_smoke_after_deployment"
    )

    supporting = {item.id: item for item in report.supporting_evidence}
    assert supporting["phase3_seed_retrieval_baseline"].status == "ready"
    assert supporting["phase3_fp_fn_review"].status == "ready"
    assert "total_cases=29" in supporting["phase3_seed_retrieval_baseline"].summary
    assert "false_positive_count=2" in supporting["phase3_fp_fn_review"].summary


def test_export_phase3_retrieval_promotion_readiness_report_writes_json_and_markdown(
    tmp_path,
):
    report = export_phase3_retrieval_promotion_readiness_report(
        output_dir=tmp_path / "readiness",
    )

    assert report.json_path == (
        tmp_path / "readiness" / "phase3-retrieval-promotion-readiness.json"
    )
    assert report.markdown_path == (
        tmp_path / "readiness" / "phase3-retrieval-promotion-readiness.md"
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["status"] == report.status
    assert payload["decision"] == report.decision
    assert payload["json_path"] == str(report.json_path)
    assert "# Phase 3 Retrieval Promotion Readiness Report" in markdown
    assert "| Gate | Status | Evidence | Open Gap | Next Evidence |" in markdown
    assert render_phase3_retrieval_promotion_readiness_markdown(report) == markdown


def test_phase3_retrieval_promotion_readiness_report_handles_missing_live_smoke(
    tmp_path,
):
    report = build_phase3_retrieval_promotion_readiness_report(
        base_dir=tmp_path,
    )

    gates = {gate.id: gate for gate in report.gates}
    assert report.status == "review"
    assert gates["deployed_smoke"].status == "review"
    assert gates["deployed_smoke"].evidence_present is False
    assert gates["deployed_smoke"].summary == "Optional deployed smoke evidence is missing."
