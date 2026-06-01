import json
from pathlib import Path

from app.services.phase3_aggregation_relation_negative_control_smoke import (
    build_phase3_aggregation_relation_negative_control_smoke_report,
    export_phase3_aggregation_relation_negative_control_smoke_report,
    render_phase3_aggregation_relation_negative_control_smoke_markdown,
)


def test_build_phase3_aggregation_relation_negative_control_smoke_report_summarizes_current_evidence():
    report = build_phase3_aggregation_relation_negative_control_smoke_report()

    assert report.id == "phase3-aggregation-relation-negative-control-smoke-v1"
    assert report.status == "ready"
    assert report.decision == "keep_runtime_defaults"
    assert report.summary["total_checks"] == 4
    assert report.summary["passed_checks"] == 4
    assert report.summary["failed_checks"] == 0
    assert report.summary["open_check_ids"] == []

    checks = {check.id: check for check in report.checks}
    assert checks["aggregation_positive_control"].status == "ready"
    assert checks["aggregation_negative_control"].status == "ready"
    assert checks["relation_aware_labeling"].status == "ready"
    assert checks["relation_aware_summary"].status == "ready"
    assert "relation_unsupported_count=1" in checks["relation_aware_summary"].summary


def test_export_phase3_aggregation_relation_negative_control_smoke_report_writes_artifacts(
    tmp_path,
):
    candidate_dir = (
        tmp_path / "docs/benchmark/chinese-seed/multi-chunk-aggregation-candidates"
    )
    negative_dir = (
        tmp_path / "docs/benchmark/chinese-seed/multi-chunk-aggregation-negative-controls"
    )
    relation_dir = (
        tmp_path / "docs/benchmark/chinese-seed/relation-aware-aggregation-grading"
    )
    candidate_dir.mkdir(parents=True, exist_ok=True)
    negative_dir.mkdir(parents=True, exist_ok=True)
    relation_dir.mkdir(parents=True, exist_ok=True)

    candidate_dir.joinpath("qdrant-bge-m3-hybrid-multi-chunk-aggregation.json").write_text(
        json.dumps(
            {
                "report": {
                    "summary": {
                        "backend": "qdrant-hybrid:source-document-identifier-coverage-v1",
                        "total_cases": 1,
                        "hit_rate": 1.0,
                        "citation_match_rate": 1.0,
                        "empty_handling_rate": 0.0,
                    },
                    "cases": [
                        {
                            "id": "split-chunk-refund-policy-and-form",
                            "hit_at_k": True,
                            "citation_match": True,
                        }
                    ],
                }
            }
        ),
        encoding="utf-8",
    )
    negative_dir.joinpath("qdrant-bge-m3-hybrid-multi-chunk-aggregation.json").write_text(
        json.dumps(
            {
                "report": {
                    "summary": {
                        "backend": "qdrant-hybrid:source-document-identifier-coverage-v1",
                        "total_cases": 1,
                        "hit_rate": 0.0,
                        "citation_match_rate": 0.0,
                        "empty_handling_rate": 0.0,
                    },
                    "cases": [
                        {
                            "id": "multi-chunk-empty-unsupported-form-policy-link",
                            "hit_at_k": False,
                            "citation_match": False,
                            "empty_query_handling": False,
                        }
                    ],
                }
            }
        ),
        encoding="utf-8",
    )
    relation_dir.joinpath("relation-aware-aggregation-grading.json").write_text(
        json.dumps(
            {
                "total_cases": 1,
                "answer_bearing_rate": 1.0,
                "related_insufficient_count": 0,
                "relation_unsupported_count": 1,
                "missing_evidence_count": 0,
                "unexpected_evidence_count": 0,
                "expected_empty_pass_rate": 1.0,
                "results": [
                    {
                        "candidate": {
                            "id": "relation-aware-aggregation-grader-v1",
                        },
                        "cases": [
                            {
                                "case_id": "multi-chunk-empty-unsupported-form-policy-link",
                                "grading_label": "relation_unsupported",
                                "grading_reason": (
                                    "Returned evidence contains identifiers but does not prove the requested relationship."
                                ),
                            }
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    report = export_phase3_aggregation_relation_negative_control_smoke_report(
        output_dir=tmp_path / "smoke",
        base_dir=tmp_path,
    )

    assert report.json_path == (
        tmp_path / "smoke" / "phase3-aggregation-relation-negative-control-smoke.json"
    )
    assert report.markdown_path == (
        tmp_path / "smoke" / "phase3-aggregation-relation-negative-control-smoke.md"
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["status"] == report.status
    assert payload["decision"] == report.decision
    assert "# Phase 3 Aggregation Relation Negative-Control Smoke Report" in markdown
    assert "| Check | Status | Summary | Recommended Action |" in markdown
    assert render_phase3_aggregation_relation_negative_control_smoke_markdown(report) == markdown


def test_aggregation_relation_negative_control_smoke_marks_missing_sources_as_blocked(tmp_path):
    report = build_phase3_aggregation_relation_negative_control_smoke_report(
        base_dir=tmp_path,
    )

    assert report.status == "blocked"
    checks = {check.id: check for check in report.checks}
    assert checks["aggregation_positive_control"].status == "blocked"
    assert checks["aggregation_negative_control"].status == "blocked"
    assert checks["relation_aware_labeling"].status == "blocked"
    assert checks["relation_aware_summary"].status == "blocked"
