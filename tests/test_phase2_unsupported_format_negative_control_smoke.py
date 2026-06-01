import json

from app.services.phase2_unsupported_format_negative_control_smoke import (
    build_phase2_unsupported_format_negative_control_smoke_report,
    export_phase2_unsupported_format_negative_control_smoke_report,
    render_phase2_unsupported_format_negative_control_smoke_markdown,
)


def test_build_phase2_unsupported_format_negative_control_smoke_report_from_current_evidence():
    report = build_phase2_unsupported_format_negative_control_smoke_report()

    assert report.id == "phase2-unsupported-format-negative-control-smoke-v1"
    assert report.status == "ready"
    assert report.decision == "keep_markdown_baseline"
    assert report.summary["total_checks"] == 5
    assert report.summary["passed_checks"] == 5
    assert report.summary["failed_checks"] == 0
    assert report.summary["unsupported_documents"] == 0
    assert report.summary["non_markdown_sources"] == 0
    assert report.summary["format_expansion_demand_signal"] is False


def test_export_phase2_unsupported_format_negative_control_smoke_report_writes_files(
    tmp_path,
):
    readiness_path = (
        tmp_path / "docs/operations/source-format-demand/phase2-source-format-demand-readiness.json"
    )
    readiness_path.parent.mkdir(parents=True, exist_ok=True)
    readiness_path.write_text(
        json.dumps(
            {
                "status": "ready",
                "decision": "keep_markdown_baseline",
                "summary": {
                    "parser_ready_documents": 3,
                    "unsupported_documents": 0,
                    "non_markdown_sources": 0,
                    "format_expansion_demand_signal": False,
                },
            }
        ),
        encoding="utf-8",
    )

    report = export_phase2_unsupported_format_negative_control_smoke_report(
        output_dir=tmp_path / "output",
        base_dir=tmp_path,
    )

    assert report.json_path == (
        tmp_path / "output" / "phase2-unsupported-format-negative-control-smoke.json"
    )
    assert report.markdown_path == (
        tmp_path / "output" / "phase2-unsupported-format-negative-control-smoke.md"
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")
    assert payload["id"] == report.id
    assert payload["status"] == report.status
    assert payload["json_path"] == str(report.json_path)
    assert "# Phase 2 Unsupported Format Negative-Control Smoke" in markdown
    assert "| Check | Passed | Details |" in markdown
    assert (
        render_phase2_unsupported_format_negative_control_smoke_markdown(report)
        == markdown
    )


def test_phase2_unsupported_format_negative_control_smoke_blocks_when_readiness_missing(
    tmp_path,
):
    report = build_phase2_unsupported_format_negative_control_smoke_report(
        base_dir=tmp_path
    )
    assert report.status == "blocked"
    assert report.summary["failed_checks"] == 1
    assert report.checks[0].name == "phase2_source_format_demand_readiness_present"
    assert report.checks[0].passed is False


def test_phase2_unsupported_format_negative_control_smoke_reviews_when_negative_control_fails(
    tmp_path,
):
    readiness_path = (
        tmp_path / "docs/operations/source-format-demand/phase2-source-format-demand-readiness.json"
    )
    readiness_path.parent.mkdir(parents=True, exist_ok=True)
    readiness_path.write_text(
        json.dumps(
            {
                "status": "review",
                "decision": "keep_markdown_baseline",
                "summary": {
                    "parser_ready_documents": 1,
                    "unsupported_documents": 2,
                    "non_markdown_sources": 1,
                    "format_expansion_demand_signal": True,
                },
            }
        ),
        encoding="utf-8",
    )

    report = build_phase2_unsupported_format_negative_control_smoke_report(
        base_dir=tmp_path
    )
    assert report.status == "review"
    assert report.summary["unsupported_documents"] == 2
    assert report.summary["non_markdown_sources"] == 1
    assert report.summary["format_expansion_demand_signal"] is True
    assert report.summary["failed_checks"] == 3
