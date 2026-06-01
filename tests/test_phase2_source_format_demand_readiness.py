import json

from app.services.phase2_source_format_demand_readiness import (
    build_phase2_source_format_demand_readiness_report,
    export_phase2_source_format_demand_readiness_report,
    render_phase2_source_format_demand_readiness_markdown,
)


def test_build_phase2_source_format_demand_readiness_report_summarizes_current_evidence():
    report = build_phase2_source_format_demand_readiness_report()

    assert report.id == "phase2-source-format-demand-readiness-v1"
    assert report.status == "ready"
    assert report.decision == "keep_markdown_baseline"
    assert report.baseline_parser == "markdown"

    summary = report.summary
    assert summary["total_sources"] == 2
    assert summary["bindable_sources"] == 2
    assert summary["markdown_only_sources"] == 2
    assert summary["non_markdown_sources"] == 0
    assert summary["parser_ready_documents"] == 2
    assert summary["unsupported_documents"] == 0
    assert summary["source_binding_ready"] is True
    assert summary["format_expansion_demand_signal"] is False
    assert summary["open_gate_count"] == 0
    assert summary["supported_format_counts"] == {"markdown": 2}
    assert summary["parser_status_counts"] == {"ready": 2}

    artifacts = {artifact.id: artifact for artifact in report.supporting_evidence}
    assert artifacts["phase2_parser_expansion_demand_contract"].status == "ready"
    assert artifacts["source_binding_summary"].status == "ready"


def test_export_phase2_source_format_demand_readiness_report_writes_json_and_markdown(
    tmp_path,
):
    contract_path = (
        tmp_path
        / "docs/operations/source-format-demand/phase2-parser-expansion-demand-contract.md"
    )
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    contract_path.write_text("# contract\n", encoding="utf-8")

    source_binding_path = (
        tmp_path / "docs/integration/source-bindings/provider-source-bindings.json"
    )
    source_binding_path.parent.mkdir(parents=True, exist_ok=True)
    source_binding_path.write_text(
        json.dumps(
            {
                "status": "ready",
                "total_source_count": 1,
                "bindable_source_count": 1,
                "sources": [
                    {
                        "supported_formats": ["markdown"],
                        "parser_ready_document_count": 2,
                        "unsupported_document_count": 0,
                        "parser_statuses": ["ready"],
                        "bindable": True,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    report = export_phase2_source_format_demand_readiness_report(
        output_dir=tmp_path / "output",
        base_dir=tmp_path,
    )

    assert report.json_path == (
        tmp_path / "output" / "phase2-source-format-demand-readiness.json"
    )
    assert report.markdown_path == (
        tmp_path / "output" / "phase2-source-format-demand-readiness.md"
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["status"] == report.status
    assert payload["decision"] == report.decision
    assert payload["json_path"] == str(report.json_path)
    assert "# Phase 2 Source Format Demand Readiness" in markdown
    assert "| Evidence | Category | Status | Summary |" in markdown
    assert render_phase2_source_format_demand_readiness_markdown(report) == markdown


def test_phase2_source_format_demand_readiness_report_blocks_when_source_binding_missing(
    tmp_path,
):
    contract_path = (
        tmp_path
        / "docs/operations/source-format-demand/phase2-parser-expansion-demand-contract.md"
    )
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    contract_path.write_text("# contract\n", encoding="utf-8")

    report = build_phase2_source_format_demand_readiness_report(base_dir=tmp_path)
    artifacts = {artifact.id: artifact for artifact in report.supporting_evidence}

    assert report.status == "blocked"
    assert artifacts["phase2_parser_expansion_demand_contract"].status == "ready"
    assert artifacts["source_binding_summary"].status == "blocked"


def test_phase2_source_format_demand_readiness_report_marks_demand_signal_review(
    tmp_path,
):
    contract_path = (
        tmp_path
        / "docs/operations/source-format-demand/phase2-parser-expansion-demand-contract.md"
    )
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    contract_path.write_text("# contract\n", encoding="utf-8")

    source_binding_path = (
        tmp_path / "docs/integration/source-bindings/provider-source-bindings.json"
    )
    source_binding_path.parent.mkdir(parents=True, exist_ok=True)
    source_binding_path.write_text(
        json.dumps(
            {
                "status": "ready",
                "sources": [
                    {
                        "supported_formats": ["markdown", "pdf"],
                        "parser_ready_document_count": 1,
                        "unsupported_document_count": 2,
                        "parser_statuses": ["ready", "unsupported"],
                        "bindable": False,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    report = build_phase2_source_format_demand_readiness_report(base_dir=tmp_path)

    assert report.status == "review"
    assert report.summary["format_expansion_demand_signal"] is True
    assert report.summary["open_gate_count"] == 4
    assert report.open_gate_ids == [
        "customer_like_format_benchmark",
        "parser_false_positive_false_negative_review",
        "parser_latency_resource_review",
        "parser_deployment_ownership_review",
    ]
