import json

from app.services.phase3_hybrid_cross_case_fp_fn_smoke import (
    export_phase3_hybrid_cross_case_fp_fn_smoke_report,
    render_phase3_hybrid_cross_case_smoke_markdown,
    run_phase3_hybrid_cross_case_fp_fn_smoke,
)


def test_run_phase3_hybrid_cross_case_fp_fn_smoke_summarizes_current_evidence():
    report = run_phase3_hybrid_cross_case_fp_fn_smoke()

    assert report.id == "phase3-hybrid-cross-case-fp-fn-smoke-v1"
    assert report.status == "ready"
    assert report.summary["total"] == 4
    assert report.summary["passed"] == 4
    assert report.summary["failed"] == 0
    assert report.summary["false_positive_count"] == 2
    assert report.summary["false_negative_count"] == 0

    checks = {check.name: check for check in report.checks}
    assert checks["baseline_cross_case_coverage"].passed is True
    assert checks["false_positive_alignment"].passed is True
    assert checks["positive_control_and_fn_guard"].passed is True
    assert checks["evaluation_protocol_artifact"].passed is True


def test_export_phase3_hybrid_cross_case_fp_fn_smoke_report_writes_artifacts(tmp_path):
    baseline_dir = (
        tmp_path / "docs/benchmark/chinese-seed/retrieval-candidates"
    )
    fpfn_dir = tmp_path / "docs/benchmark/chinese-seed/fp-fn-review"
    protocol_dir = (
        tmp_path / "docs/benchmark/chinese-seed/retrieval-candidate-evaluation-protocol"
    )
    baseline_dir.mkdir(parents=True, exist_ok=True)
    fpfn_dir.mkdir(parents=True, exist_ok=True)
    protocol_dir.mkdir(parents=True, exist_ok=True)

    baseline_dir.joinpath("fixture-chinese-seed-baseline.json").write_text(
        json.dumps(
            {
                "report": {
                    "summary": {"total_cases": 4},
                    "cases": [
                        {
                            "id": "empty-refund-high-value-auto-compensation",
                            "hit_at_k": False,
                            "citation_match": False,
                        },
                        {
                            "id": "empty-refund-high-value-auto-compensation-customer-like-2",
                            "hit_at_k": False,
                            "citation_match": False,
                        },
                        {
                            "id": "logistics-exact-id-customer-like",
                            "hit_at_k": True,
                            "citation_match": True,
                        },
                        {
                            "id": "refund-high-value-review-customer-like-audit-trace-2",
                            "hit_at_k": True,
                            "citation_match": True,
                        },
                    ],
                }
            }
        ),
        encoding="utf-8",
    )
    fpfn_dir.joinpath("phase3-fp-fn-review.json").write_text(
        json.dumps(
            {
                "false_positive_count": 2,
                "false_negative_count": 0,
                "false_positive_cases": [
                    {"id": "empty-refund-high-value-auto-compensation"},
                    {"id": "empty-refund-high-value-auto-compensation-customer-like-2"},
                ],
            }
        ),
        encoding="utf-8",
    )
    protocol_dir.joinpath("phase3-retrieval-candidate-evaluation-protocol.md").write_text(
        "# protocol\n",
        encoding="utf-8",
    )

    report = export_phase3_hybrid_cross_case_fp_fn_smoke_report(
        output_dir=tmp_path / "smoke",
        base_dir=tmp_path,
    )

    assert report.json_path == (
        tmp_path / "smoke" / "phase3-hybrid-cross-case-fp-fn-smoke.json"
    )
    assert report.markdown_path == (
        tmp_path / "smoke" / "phase3-hybrid-cross-case-fp-fn-smoke.md"
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")
    assert payload["id"] == report.id
    assert payload["status"] == report.status
    assert payload["json_path"] == str(report.json_path)
    assert "# Phase 3 Hybrid Cross-Case FP/FN Smoke Report" in markdown
    assert "| Check | Scenario | Status | Details |" in markdown
    assert render_phase3_hybrid_cross_case_smoke_markdown(report) == markdown


def test_phase3_hybrid_cross_case_smoke_blocks_when_protocol_missing(tmp_path):
    baseline_dir = (
        tmp_path / "docs/benchmark/chinese-seed/retrieval-candidates"
    )
    fpfn_dir = tmp_path / "docs/benchmark/chinese-seed/fp-fn-review"
    baseline_dir.mkdir(parents=True, exist_ok=True)
    fpfn_dir.mkdir(parents=True, exist_ok=True)
    baseline_dir.joinpath("fixture-chinese-seed-baseline.json").write_text(
        json.dumps(
            {
                "report": {
                    "summary": {"total_cases": 4},
                    "cases": [
                        {
                            "id": "empty-refund-high-value-auto-compensation",
                            "hit_at_k": False,
                            "citation_match": False,
                        },
                        {
                            "id": "empty-refund-high-value-auto-compensation-customer-like-2",
                            "hit_at_k": False,
                            "citation_match": False,
                        },
                        {
                            "id": "logistics-exact-id-customer-like",
                            "hit_at_k": True,
                            "citation_match": True,
                        },
                        {
                            "id": "refund-high-value-review-customer-like-audit-trace-2",
                            "hit_at_k": True,
                            "citation_match": True,
                        },
                    ],
                }
            }
        ),
        encoding="utf-8",
    )
    fpfn_dir.joinpath("phase3-fp-fn-review.json").write_text(
        json.dumps(
            {
                "false_positive_count": 2,
                "false_negative_count": 0,
                "false_positive_cases": [
                    {"id": "empty-refund-high-value-auto-compensation"},
                    {"id": "empty-refund-high-value-auto-compensation-customer-like-2"},
                ],
            }
        ),
        encoding="utf-8",
    )

    report = run_phase3_hybrid_cross_case_fp_fn_smoke(base_dir=tmp_path)

    assert report.status == "blocked"
    checks = {check.name: check for check in report.checks}
    assert checks["evaluation_protocol_artifact"].passed is False
