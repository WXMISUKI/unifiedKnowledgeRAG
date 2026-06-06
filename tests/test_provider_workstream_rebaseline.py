import json

from app.services.provider_workstream_rebaseline import (
    build_provider_workstream_rebaseline_report,
    export_provider_workstream_rebaseline_report,
)


def test_rebaseline_closes_access_readiness_chain():
    report = build_provider_workstream_rebaseline_report()

    access = _workstream(report, "myprivateagent_access_readiness")

    assert report.status == "ready"
    assert report.summary["access_readiness_status"] == "closed"
    assert report.summary["continue_phase26_access_readiness"] is False
    assert access.status == "closed"
    assert "do_not_open_phase26_access_readiness" in access.allowed_next_actions


def test_rebaseline_keeps_retrieval_backend_candidate_only():
    report = build_provider_workstream_rebaseline_report()

    backend = _workstream(report, "retrieval_backend_promotion")

    assert report.summary["retrieval_backend_promotion_status"] == "candidate_only"
    assert backend.status == "candidate_only"
    assert "keep_runtime_defaults_until_promotion_gate_closes" in backend.allowed_next_actions


def test_rebaseline_defers_parser_and_graphrag_without_triggers():
    report = build_provider_workstream_rebaseline_report()

    parser = _workstream(report, "corpus_parser_expansion")
    graph = _workstream(report, "graphrag_execution")

    assert parser.status == "deferred"
    assert graph.status == "deferred"
    assert report.summary["parser_expansion_status"] == "deferred_until_real_corpus_demand"
    assert report.summary["graphrag_execution_status"] == "deferred_until_relationship_heavy_use_case"


def test_rebaseline_exports_json_and_markdown(tmp_path):
    report = export_provider_workstream_rebaseline_report(output_dir=tmp_path / "out")

    assert report.json_path is not None
    assert report.markdown_path is not None
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["decision"] == "close_access_readiness_and_use_triggered_workstreams"
    assert payload["summary"]["access_readiness_status"] == "closed"
    assert "# Provider Workstream Rebaseline" in markdown
    assert "`myprivateagent_access_readiness`" in markdown


def _workstream(report, workstream_id):
    for workstream in report.workstreams:
        if workstream.id == workstream_id:
            return workstream
    raise AssertionError(f"Missing workstream: {workstream_id}")
