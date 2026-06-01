import json
from pathlib import Path

from app.services.phase3_candidate_latency_resource_diagnostics import (
    build_phase3_candidate_latency_resource_diagnostics_report,
    export_phase3_candidate_latency_resource_diagnostics_report,
    render_phase3_candidate_latency_resource_diagnostics_markdown,
)


def test_build_phase3_candidate_latency_resource_diagnostics_report_summarizes_current_evidence():
    report = build_phase3_candidate_latency_resource_diagnostics_report()

    assert report.id == "phase3-candidate-latency-resource-diagnostics-v1"
    assert report.status == "review"
    assert report.decision == "keep_runtime_defaults"
    assert report.summary["total_signals"] == 6
    assert report.summary["ready_signals"] == 1
    assert report.summary["review_signals"] == 5
    assert report.summary["blocked_signals"] == 0
    assert "deployment_readiness_snapshot" in report.summary["open_signal_ids"]
    assert "deployed_smoke_evidence" in report.summary["open_signal_ids"]
    assert report.latency_profile["backend"] == "fixture"
    assert report.latency_profile["total_cases"] == 32
    assert report.latency_profile["empty_case_count"] == 12
    assert report.latency_profile["average_latency_ms"] > 0.0
    assert report.resource_posture["deployment_readiness_status"] == "review"
    assert report.resource_posture["runtime_diagnostics_status"] == "review"
    assert report.resource_posture["model_artifacts_status"] == "not_configured"


def test_export_phase3_candidate_latency_resource_diagnostics_report_writes_artifacts(
    tmp_path,
):
    baseline_dir = tmp_path / "docs/benchmark/chinese-seed/retrieval-candidates"
    readiness_dir = tmp_path / "docs/operations/deployment-readiness"
    runtime_dir = (
        tmp_path / "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics"
    )
    baseline_dir.mkdir(parents=True, exist_ok=True)
    readiness_dir.mkdir(parents=True, exist_ok=True)
    runtime_dir.mkdir(parents=True, exist_ok=True)

    baseline_dir.joinpath("fixture-chinese-seed-baseline.json").write_text(
        json.dumps(
            {
                "report": {
                    "summary": {
                        "backend": "fixture",
                        "total_cases": 3,
                        "hit_rate": 1.0,
                        "citation_match_rate": 1.0,
                        "empty_handling_rate": 0.3333,
                    },
                    "cases": [
                        {
                            "id": "case-a",
                            "expect_empty": False,
                            "latency_ms": 10.0,
                        },
                        {
                            "id": "case-b",
                            "expect_empty": False,
                            "latency_ms": 20.0,
                        },
                        {
                            "id": "case-c",
                            "expect_empty": True,
                            "latency_ms": 30.0,
                        },
                    ],
                }
            }
        ),
        encoding="utf-8",
    )
    readiness_dir.joinpath("deployment-readiness.json").write_text(
        json.dumps(
            {
                "status": "review",
                "health": {"status": "ok"},
                "preflight": {"bindable": True},
                "runtime_config": {
                    "rag_retrieval_backend": "fixture",
                    "embedding_provider": "mock",
                    "embedding_model": "mock-hash-v1",
                    "embedding_model_path": None,
                    "provider_api_key_configured": False,
                    "qdrant_api_key_configured": False,
                    "qdrant_url": "http://localhost:6333",
                    "qdrant_collection": "knowledge_chunks",
                },
                "model_artifacts": {
                    "status": "not_configured",
                    "model_path": None,
                    "path_exists": False,
                    "manifest_exists": False,
                },
            }
        ),
        encoding="utf-8",
    )
    runtime_dir.joinpath("phase3-candidate-runtime-diagnostics.json").write_text(
        json.dumps(
            {
                "status": "review",
                "decision": "keep_runtime_defaults",
                "summary": {
                    "total_checks": 6,
                    "ready_checks": 0,
                    "review_checks": 6,
                    "blocked_checks": 0,
                    "open_prerequisite_ids": [
                        "candidate_retrieval_backend",
                        "candidate_embedding_provider",
                    ],
                },
            }
        ),
        encoding="utf-8",
    )

    report = export_phase3_candidate_latency_resource_diagnostics_report(
        output_dir=tmp_path / "latency-resource",
        base_dir=tmp_path,
    )

    assert report.json_path == (
        tmp_path / "latency-resource" / "phase3-candidate-latency-resource-diagnostics.json"
    )
    assert report.markdown_path == (
        tmp_path / "latency-resource" / "phase3-candidate-latency-resource-diagnostics.md"
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["status"] == report.status
    assert payload["decision"] == report.decision
    assert payload["latency_profile"]["average_latency_ms"] == 20.0
    assert payload["latency_profile"]["median_latency_ms"] == 20.0
    assert payload["latency_profile"]["p95_latency_ms"] == 30.0
    assert payload["resource_posture"]["deployment_readiness_status"] == "review"
    assert payload["resource_posture"]["runtime_diagnostics_status"] == "review"
    assert "# Phase 3 Candidate Latency/Resource Diagnostics" in markdown
    assert "| Signal | Status | Summary | Recommended Action |" in markdown
    assert render_phase3_candidate_latency_resource_diagnostics_markdown(report) == markdown


def test_latency_resource_diagnostics_marks_missing_benchmark_as_review(tmp_path):
    report = build_phase3_candidate_latency_resource_diagnostics_report(
        base_dir=tmp_path,
    )

    signals = {item.id: item for item in report.signals}
    assert report.status == "review"
    assert signals["benchmark_latency_profile"].status == "review"
    assert signals["benchmark_latency_profile"].recommended_action == (
        "regenerate_chinese_seed_evidence_bundle"
    )
