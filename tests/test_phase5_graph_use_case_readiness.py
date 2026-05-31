import json
from pathlib import Path

import app.services.phase5_graph_use_case_readiness as phase5_graph_use_case_readiness
from app.services.phase5_graph_use_case_readiness import (
    build_phase5_graph_use_case_readiness_report,
    export_phase5_graph_use_case_readiness_report,
    render_phase5_graph_use_case_readiness_markdown,
)


def test_build_phase5_graph_use_case_readiness_report_summarizes_current_evidence():
    report = build_phase5_graph_use_case_readiness_report()

    assert report.id == "phase5-graph-use-case-readiness-v1"
    assert report.status == "ready"
    assert report.decision == "keep_graph_query_planned"
    assert Path(report.contract_path).as_posix().endswith(
        "docs/benchmark/chinese-seed/graph-use-case-readiness/"
        "phase5-graph-use-case-readiness-contract.md"
    )
    assert report.preflight_path == "/api/provider/preflight"
    assert Path(report.smoke_report_path).as_posix().endswith(
        "docs/smoke/provider-contract/provider-contract-smoke.json"
    )

    summary = report.summary
    assert summary["total_artifacts"] == 3
    assert summary["ready_artifacts"] == 3
    assert summary["review_artifacts"] == 0
    assert summary["blocked_artifacts"] == 0
    assert summary["required_artifacts"] == 3
    assert summary["required_ready_artifacts"] == 3
    assert summary["graph_schema_count"] >= 1
    assert summary["graph_query_status"] == "planned"
    assert summary["graph_query_planned"] is True
    assert summary["preflight_graph_boundary_ready"] is True
    assert summary["smoke_checks_passed"] is True
    assert summary["smoke_graph_check_passed"] is True

    artifacts = {artifact.id: artifact for artifact in report.supporting_evidence}
    assert artifacts["graph_use_case_contract_doc"].status == "ready"
    assert artifacts["provider_preflight_graph_boundary"].status == "ready"
    assert artifacts["provider_preflight_graph_boundary"].summary.startswith(
        "graph_schema_count="
    )
    assert artifacts["provider_contract_smoke"].status == "ready"
    assert "graph_check_status=passed" in artifacts["provider_contract_smoke"].summary


def test_export_phase5_graph_use_case_readiness_report_writes_json_and_markdown(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        phase5_graph_use_case_readiness,
        "build_provider_preflight_response",
        _fake_preflight_response,
    )

    contract_dir = (
        tmp_path
        / "docs/benchmark/chinese-seed/graph-use-case-readiness"
    )
    contract_dir.mkdir(parents=True, exist_ok=True)
    (contract_dir / "phase5-graph-use-case-readiness-contract.md").write_text(
        "# graph contract\n",
        encoding="utf-8",
    )

    smoke_dir = tmp_path / "docs/smoke/provider-contract"
    smoke_dir.mkdir(parents=True, exist_ok=True)
    smoke_dir.joinpath("provider-contract-smoke.json").write_text(
        json.dumps(
            {
                "passed": True,
                "summary": {"total": 1, "passed": 1, "failed": 0},
                "checks": [
                    {
                        "name": "graph_planned_boundary",
                        "passed": True,
                        "details": {
                            "graph_id": "ecommerce_order_graph",
                            "status": "planned",
                            "error_code": "GRAPH_NOT_IMPLEMENTED",
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    report = export_phase5_graph_use_case_readiness_report(
        output_dir=tmp_path / "readiness",
        base_dir=tmp_path,
    )

    assert report.json_path == (
        tmp_path / "readiness" / "phase5-graph-use-case-readiness.json"
    )
    assert report.markdown_path == (
        tmp_path / "readiness" / "phase5-graph-use-case-readiness.md"
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["status"] == report.status
    assert payload["decision"] == report.decision
    assert payload["json_path"] == str(report.json_path)
    assert "# Phase 5 Graph Use-Case Readiness Report" in markdown
    assert "| Evidence | Category | Status | Summary |" in markdown
    assert render_phase5_graph_use_case_readiness_markdown(report) == markdown


def test_phase5_graph_use_case_readiness_report_blocks_when_contract_is_missing(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        phase5_graph_use_case_readiness,
        "build_provider_preflight_response",
        _fake_preflight_response,
    )
    smoke_dir = tmp_path / "docs/smoke/provider-contract"
    smoke_dir.mkdir(parents=True, exist_ok=True)
    smoke_dir.joinpath("provider-contract-smoke.json").write_text(
        json.dumps(
            {
                "passed": True,
                "summary": {"total": 1, "passed": 1, "failed": 0},
                "checks": [
                    {
                        "name": "graph_planned_boundary",
                        "passed": True,
                        "details": {"status": "planned"},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    report = build_phase5_graph_use_case_readiness_report(base_dir=tmp_path)

    artifacts = {artifact.id: artifact for artifact in report.supporting_evidence}
    assert report.status == "blocked"
    assert artifacts["graph_use_case_contract_doc"].status == "blocked"
    assert artifacts["provider_preflight_graph_boundary"].status == "ready"
    assert artifacts["provider_contract_smoke"].status == "ready"


def test_phase5_graph_use_case_readiness_report_blocks_when_smoke_is_missing(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        phase5_graph_use_case_readiness,
        "build_provider_preflight_response",
        _fake_preflight_response,
    )
    contract_dir = (
        tmp_path
        / "docs/benchmark/chinese-seed/graph-use-case-readiness"
    )
    contract_dir.mkdir(parents=True, exist_ok=True)
    (contract_dir / "phase5-graph-use-case-readiness-contract.md").write_text(
        "# graph contract\n",
        encoding="utf-8",
    )

    report = build_phase5_graph_use_case_readiness_report(base_dir=tmp_path)

    artifacts = {artifact.id: artifact for artifact in report.supporting_evidence}
    assert report.status == "blocked"
    assert artifacts["graph_use_case_contract_doc"].status == "ready"
    assert artifacts["provider_preflight_graph_boundary"].status == "ready"
    assert artifacts["provider_contract_smoke"].status == "blocked"
    assert artifacts["provider_contract_smoke"].present is False


def _fake_preflight_response():
    class FakeCheck:
        def __init__(self):
            self.name = "graph_boundary"
            self.passed = True
            self.details = {
                "capability_id": "knowledge.graph.query",
                "capability_status": "planned",
                "execution_status": "planned",
                "graph_schema_count": 1,
                "graph_ids": ["ecommerce_order_graph"],
                "graph_statuses": {"ecommerce_order_graph": "planned"},
                "graph_stores": {"ecommerce_order_graph": "neo4j_planned"},
            }

    class FakePreflightResponse:
        def __init__(self):
            self.checks = [FakeCheck()]

    return FakePreflightResponse()
