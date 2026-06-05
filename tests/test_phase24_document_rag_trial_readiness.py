import json

from app.services.phase24_document_rag_trial_readiness import (
    PHASE11_PROVIDER_DISCOVERY_SMOKE_PATH,
    PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_PATH,
    PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_PATH,
    PHASE16_ACCESS_LOOP_PATH,
    PHASE10_PROBE_PATH,
    PROVIDER_CONTRACT_SMOKE_PATH,
    build_phase24_document_rag_trial_readiness_report,
    export_phase24_document_rag_trial_readiness_report,
)


def test_phase24_readiness_go_when_primitive_signals_are_ready(tmp_path):
    _write_json(tmp_path / PROVIDER_CONTRACT_SMOKE_PATH, {"passed": True, "summary": {"total": 9, "failed": 0}})
    _write_json(tmp_path / PHASE10_PROBE_PATH, {"status": "ready", "summary": {"passed_checks": 5, "total_checks": 5}})
    _write_json(tmp_path / PHASE11_PROVIDER_DISCOVERY_SMOKE_PATH, {"status": "ready"})
    _write_json(tmp_path / PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_PATH, {"status": "ready"})
    _write_json(tmp_path / PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_PATH, {"status": "ready"})
    _write_json(tmp_path / PHASE16_ACCESS_LOOP_PATH, {"status": "review", "decision": "begin_myprivateagent_repo_side_trial"})

    report = build_phase24_document_rag_trial_readiness_report(base_dir=tmp_path)

    assert report.status == "ready"
    assert report.decision == "go"
    assert report.summary["blocked_primitive_signal_ids"] == []
    assert report.summary["open_review_context_signal_ids"] == [
        "phase10_myprivateagent_local_consumer_readiness",
        "phase11_local_provider_integration_profile",
        "phase14_myprivateagent_provider_integration_acceptance_checkpoint",
        "phase15_myprivateagent_repo_side_trial_dispatch_package",
        "phase16_myprivateagent_minimal_access_loop",
        "provider_handoff_bundle",
        "provider_handoff_refresh",
    ]
    assert "begin_myprivateagent_repo_side_document_rag_trial" in report.caller_next_actions


def test_phase24_readiness_blocks_when_required_primitive_is_missing(tmp_path):
    _write_json(tmp_path / PROVIDER_CONTRACT_SMOKE_PATH, {"passed": True, "summary": {"total": 9, "failed": 0}})

    report = build_phase24_document_rag_trial_readiness_report(base_dir=tmp_path)

    assert report.status == "blocked"
    assert report.decision == "blocked"
    assert "phase10_myprivateagent_local_consumer_probe" in report.summary["blocked_primitive_signal_ids"]
    assert report.primitive_signals[1].summary == "status=missing"


def test_phase24_readiness_exports_json_and_markdown(tmp_path):
    _write_json(tmp_path / PROVIDER_CONTRACT_SMOKE_PATH, {"passed": True, "summary": {"total": 9, "failed": 0}})
    _write_json(tmp_path / PHASE10_PROBE_PATH, {"status": "ready"})
    _write_json(tmp_path / PHASE11_PROVIDER_DISCOVERY_SMOKE_PATH, {"status": "ready"})
    _write_json(tmp_path / PHASE11_RAG_RETRIEVE_CONSUMPTION_SMOKE_PATH, {"status": "ready"})
    _write_json(tmp_path / PHASE11_SOURCE_BINDING_PREVIEW_SMOKE_PATH, {"status": "ready"})

    report = export_phase24_document_rag_trial_readiness_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )

    assert report.json_path is not None
    assert report.markdown_path is not None
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["status"] == "ready"
    assert payload["decision"] == "go"
    assert "# Phase 24 Document RAG Trial Readiness" in markdown
    assert "`provider_contract_smoke`" in markdown


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
