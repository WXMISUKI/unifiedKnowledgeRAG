import json
from pathlib import Path

from app.services.phase5_graph_boundary_smoke_summary import (
    build_phase5_graph_boundary_smoke_summary_report,
    export_phase5_graph_boundary_smoke_summary_report,
    render_phase5_graph_boundary_smoke_summary_markdown,
)


def test_build_phase5_graph_boundary_smoke_summary_report_summarizes_current_evidence():
    report = build_phase5_graph_boundary_smoke_summary_report()

    assert report.id == "phase5-graph-boundary-smoke-summary-v1"
    assert report.status == "ready"
    assert report.decision == "keep_graph_query_planned"
    assert Path(report.source_smoke_path).as_posix().endswith(
        "docs/smoke/provider-contract/provider-contract-smoke.json"
    )

    summary = report.summary
    assert summary["total_artifacts"] == 3
    assert summary["ready_artifacts"] == 3
    assert summary["review_artifacts"] == 0
    assert summary["blocked_artifacts"] == 0
    assert summary["required_artifacts"] == 3
    assert summary["required_ready_artifacts"] == 3
    assert summary["source_smoke_passed"] is True
    assert summary["smoke_checks_passed"] is True
    assert summary["graph_checks_passed"] == 2
    assert summary["graph_schema_count"] == 1
    assert summary["graph_query_status"] == "planned"
    assert summary["graph_query_planned"] is True
    assert summary["graph_error_code"] == "GRAPH_NOT_IMPLEMENTED"

    artifacts = {artifact.id: artifact for artifact in report.supporting_evidence}
    assert artifacts["provider_contract_smoke_source"].status == "ready"
    assert artifacts["graph_schema_discovery_summary"].status == "ready"
    assert "graph_count=1" in artifacts["graph_schema_discovery_summary"].summary
    assert artifacts["graph_planned_boundary_summary"].status == "ready"
    assert "graph_id=ecommerce_order_graph" in artifacts[
        "graph_planned_boundary_summary"
    ].summary


def test_export_phase5_graph_boundary_smoke_summary_report_writes_json_and_markdown(
    tmp_path,
):
    smoke_dir = tmp_path / "docs/smoke/provider-contract"
    smoke_dir.mkdir(parents=True, exist_ok=True)
    smoke_dir.joinpath("provider-contract-smoke.json").write_text(
        json.dumps(
            {
                "passed": True,
                "summary": {"total": 9, "passed": 9, "failed": 0},
                "checks": [
                    {
                        "name": "graph_schema_discovery",
                        "passed": True,
                        "details": {
                            "graph_count": 1,
                            "graph_ids": ["ecommerce_order_graph"],
                            "graph_status": "planned",
                            "graph_store": "neo4j_planned",
                            "entity_type_count": 4,
                            "relation_type_count": 3,
                        },
                    },
                    {
                        "name": "graph_planned_boundary",
                        "passed": True,
                        "details": {
                            "error_code": "GRAPH_NOT_IMPLEMENTED",
                            "graph_id": "ecommerce_order_graph",
                            "status": "planned",
                            "capability_id": "knowledge.graph.query",
                        },
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    report = export_phase5_graph_boundary_smoke_summary_report(
        output_dir=tmp_path / "summary",
        base_dir=tmp_path,
    )

    assert report.json_path == (
        tmp_path / "summary" / "phase5-graph-boundary-smoke-summary.json"
    )
    assert report.markdown_path == (
        tmp_path / "summary" / "phase5-graph-boundary-smoke-summary.md"
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["status"] == report.status
    assert payload["decision"] == report.decision
    assert payload["json_path"] == str(report.json_path)
    assert "# Phase 5 Graph Boundary Smoke Summary" in markdown
    assert "| Evidence | Category | Status | Summary |" in markdown
    assert render_phase5_graph_boundary_smoke_summary_markdown(report) == markdown


def test_phase5_graph_boundary_smoke_summary_report_blocks_when_source_smoke_missing(
    tmp_path,
):
    report = build_phase5_graph_boundary_smoke_summary_report(base_dir=tmp_path)

    artifacts = {artifact.id: artifact for artifact in report.supporting_evidence}
    assert report.status == "blocked"
    assert artifacts["provider_contract_smoke_source"].status == "blocked"
    assert artifacts["graph_schema_discovery_summary"].status == "blocked"
    assert artifacts["graph_planned_boundary_summary"].status == "blocked"
