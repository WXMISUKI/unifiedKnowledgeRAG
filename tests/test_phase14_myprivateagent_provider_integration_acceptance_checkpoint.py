import json
from pathlib import Path

from app.services.phase14_myprivateagent_provider_integration_acceptance_checkpoint import (
    build_phase14_myprivateagent_provider_integration_acceptance_checkpoint_report,
    export_phase14_myprivateagent_provider_integration_acceptance_checkpoint_report,
    render_phase14_myprivateagent_provider_integration_acceptance_checkpoint_markdown,
)


def test_build_phase14_acceptance_checkpoint_reports_repo_side_trial_ready(tmp_path):
    _seed_phase14_ready_evidence(tmp_path)

    report = build_phase14_myprivateagent_provider_integration_acceptance_checkpoint_report(
        base_dir=tmp_path
    )

    assert report.id == "phase14-myprivateagent-provider-integration-acceptance-checkpoint-v1"
    assert report.status == "ready"
    assert report.acceptance_state == "ready_for_myprivateagent_repo_side_trial"
    assert report.decision == "approve_myprivateagent_repo_side_trial"
    assert report.summary["roadmap_focus"] == "myprivateagent_repo_side_trial"
    assert report.summary["blocker_category"] == "none"
    assert report.summary["phase10_status"] == "ready"
    assert report.summary["phase11_status"] == "ready"
    assert report.summary["phase13_status"] == "ready"
    assert report.summary["handoff_status"] == "ready"
    assert report.summary["ready_signals"] == len(report.signals)
    assert report.summary["open_gate_ids"] == []
    assert all(signal.status == "ready" for signal in report.signals)


def test_build_phase14_acceptance_checkpoint_classifies_missing_handoff_visibility(tmp_path):
    _seed_phase14_ready_evidence(tmp_path, include_handoff=False)

    report = build_phase14_myprivateagent_provider_integration_acceptance_checkpoint_report(
        base_dir=tmp_path
    )

    assert report.status == "ready"
    assert report.acceptance_state == "ready_for_myprivateagent_repo_side_trial"
    assert report.summary["blocker_category"] == "none"
    assert "provider_handoff_bundle" in report.summary["blocked_signal_ids"]
    assert "provider_handoff_refresh" in report.summary["blocked_signal_ids"]
    assert "provider_handoff_bundle" not in report.summary["missing_primitive_signal_ids"]
    assert render_phase14_myprivateagent_provider_integration_acceptance_checkpoint_markdown(
        report
    ).startswith("# Phase 14 MyPrivateAgent Provider Integration Acceptance Checkpoint")


def test_export_phase14_acceptance_checkpoint_writes_outputs(tmp_path):
    _seed_phase14_ready_evidence(tmp_path)

    report = export_phase14_myprivateagent_provider_integration_acceptance_checkpoint_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["acceptance_state"] == "ready_for_myprivateagent_repo_side_trial"
    assert payload["summary"]["blocker_category"] == "none"
    assert "# Phase 14 MyPrivateAgent Provider Integration Acceptance Checkpoint" in markdown


def _seed_phase14_ready_evidence(base_dir: Path, *, include_handoff: bool = True) -> None:
    _write_json(
        base_dir / "docs/smoke/provider-contract/provider-contract-smoke.json",
        {
            "passed": True,
            "summary": {
                "total_checks": 8,
                "failed_checks": 0,
            },
        },
    )
    _write_json(
        base_dir
        / "docs/integration/myprivateagent-local-consumer-verification/"
        / "phase10-myprivateagent-local-consumer-readiness.json",
        {
            "status": "ready",
            "local_consumer_state": "ready_for_local_consumer_probe",
            "summary": {
                "runtime_promotion_status": "keep_runtime_defaults",
                "source_binding_policy_owner": "caller",
            },
        },
    )
    _write_json(
        base_dir
        / "docs/smoke/myprivateagent-local-consumer-verification/"
        / "phase10-myprivateagent-local-consumer-probe.json",
        {
            "status": "ready",
            "summary": {
                "total_checks": 4,
                "passed_checks": 4,
            },
        },
    )
    _write_json(
        base_dir
        / "docs/integration/myprivateagent-local-provider-integration/"
        / "phase11-local-provider-integration-profile.json",
        {
            "status": "ready",
            "integration_state": "ready_for_local_provider_integration",
            "summary": {
                "local_provider_url": "http://127.0.0.1:8020",
                "api_key_mode": "not_configured_local_dev",
            },
        },
    )
    _write_json(
        base_dir
        / "docs/smoke/myprivateagent-local-provider-integration/"
        / "phase11-provider-discovery-smoke.json",
        {
            "status": "ready",
            "summary": {
                "provider_discovery_state": "ready",
                "total_checks": 3,
                "passed_checks": 3,
            },
        },
    )
    _write_json(
        base_dir
        / "docs/smoke/myprivateagent-local-provider-integration/"
        / "phase11-rag-retrieve-consumption-smoke.json",
        {
            "status": "ready",
            "summary": {
                "rag_retrieve_state": "ready",
                "total_checks": 3,
                "passed_checks": 3,
            },
        },
    )
    _write_json(
        base_dir
        / "docs/smoke/myprivateagent-local-provider-integration/"
        / "phase11-source-binding-preview-smoke.json",
        {
            "status": "ready",
            "summary": {
                "source_binding_preview_state": "ready",
                "total_checks": 3,
                "passed_checks": 3,
            },
        },
    )
    _write_json(
        base_dir
        / "docs/operations/provider-roadmap-decision-checkpoint/"
        / "phase13-provider-roadmap-decision-checkpoint.json",
        {
            "status": "ready",
            "checkpoint_state": "ready_for_provider_integration_hardening",
            "decision": "continue_provider_first_with_candidate_backends",
            "summary": {
                "roadmap_focus": "resume_provider_integration_hardening",
                "candidate_backend_posture": "pause_pgvector_until_live_probe_executed",
                "phase12d_status": "ready",
                "phase12f_status": "ready",
            },
        },
    )
    if include_handoff:
        _write_json(
            base_dir / "docs/integration/provider-handoff/provider-handoff-bundle.json",
            {
                "status": "ready",
                "decision": "continue_provider_first_with_candidate_backends",
                "evidence_artifacts": [
                    {"id": "phase14_myprivateagent_provider_integration_acceptance_checkpoint"}
                ],
            },
        )
        _write_json(
            base_dir / "docs/integration/provider-handoff-refresh/provider-handoff-refresh.json",
            {
                "status": "ready",
                "decision": "continue_provider_first_with_candidate_backends",
                "steps": [
                    {"id": "phase14_myprivateagent_provider_integration_acceptance_checkpoint"}
                ],
            },
        )


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
