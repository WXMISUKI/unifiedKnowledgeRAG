import json
from pathlib import Path

from app.services.phase16_myprivateagent_minimal_access_loop import (
    build_phase16_myprivateagent_minimal_access_loop_report,
    export_phase16_myprivateagent_minimal_access_loop_report,
    render_phase16_myprivateagent_minimal_access_loop_markdown,
)


def test_build_phase16_access_loop_reports_ready(tmp_path):
    _seed_phase16_ready_evidence(tmp_path)

    report = build_phase16_myprivateagent_minimal_access_loop_report(base_dir=tmp_path)

    assert report.id == "phase16-myprivateagent-minimal-access-loop-v1"
    assert report.status == "ready"
    assert report.access_loop_state == "ready_for_minimal_access_loop"
    assert report.decision == "begin_myprivateagent_repo_side_trial"
    assert report.summary["roadmap_focus"] == "myprivateagent_minimal_access_loop"
    assert report.summary["blocker_category"] == "none"
    assert report.summary["phase10_status"] == "ready"
    assert report.summary["phase11_status"] == "ready"
    assert report.summary["phase13_status"] == "ready"
    assert report.summary["phase14_status"] == "ready"
    assert report.summary["phase15_status"] == "ready"
    assert report.summary["handoff_status"] == "ready"
    assert report.summary["caller_checklist"] == [
        "begin_myprivateagent_repo_side_trial",
        "capture_trial_outcome_and_refresh_evidence",
    ]
    assert report.caller_checklist == report.summary["caller_checklist"]
    assert report.summary["ready_signals"] == len(report.signals)
    assert report.summary["open_gate_ids"] == []
    assert all(signal.status == "ready" for signal in report.signals)


def test_build_phase16_access_loop_uses_access_focused_handoff_visibility(tmp_path):
    _seed_phase16_ready_evidence(
        tmp_path,
        handoff_overall_status="review",
        handoff_access_status="ready",
    )

    report = build_phase16_myprivateagent_minimal_access_loop_report(base_dir=tmp_path)

    assert report.status == "ready"
    assert report.summary["blocker_category"] == "none"
    assert report.summary["handoff_status"] == "ready"
    assert "provider_handoff_bundle" not in report.summary["blocked_signal_ids"]
    assert "provider_handoff_refresh" not in report.summary["blocked_signal_ids"]


def test_build_phase16_access_loop_classifies_missing_handoff_visibility(tmp_path):
    _seed_phase16_ready_evidence(tmp_path, include_handoff=False)

    report = build_phase16_myprivateagent_minimal_access_loop_report(base_dir=tmp_path)

    assert report.status == "ready"
    assert report.access_loop_state == "ready_for_minimal_access_loop"
    assert report.summary["blocker_category"] == "none"
    assert "provider_handoff_bundle" in report.summary["blocked_signal_ids"]
    assert "provider_handoff_refresh" in report.summary["blocked_signal_ids"]
    assert "provider_handoff_bundle" not in report.summary["missing_primitive_signal_ids"]
    assert render_phase16_myprivateagent_minimal_access_loop_markdown(
        report
    ).startswith("# Phase 16 MyPrivateAgent Minimal Access Loop")


def test_build_phase16_access_loop_classifies_external_environment(tmp_path):
    _seed_phase16_ready_evidence(
        tmp_path,
        phase14_blocker_category="external_environment",
    )

    report = build_phase16_myprivateagent_minimal_access_loop_report(base_dir=tmp_path)

    assert report.status == "ready"
    assert report.access_loop_state == "ready_for_minimal_access_loop"
    assert report.summary["blocker_category"] == "none"
    assert "phase14_myprivateagent_provider_integration_acceptance_checkpoint" in report.summary[
        "review_signal_ids"
    ]
    assert "phase14_myprivateagent_provider_integration_acceptance_checkpoint" in report.summary[
        "open_review_context_signal_ids"
    ]


def test_export_phase16_access_loop_writes_outputs(tmp_path):
    _seed_phase16_ready_evidence(tmp_path)

    report = export_phase16_myprivateagent_minimal_access_loop_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["access_loop_state"] == "ready_for_minimal_access_loop"
    assert payload["summary"]["blocker_category"] == "none"
    assert "# Phase 16 MyPrivateAgent Minimal Access Loop" in markdown


def _seed_phase16_ready_evidence(
    base_dir: Path,
    *,
    include_handoff: bool = True,
    phase14_blocker_category: str = "none",
    handoff_overall_status: str = "ready",
    handoff_access_status: str = "ready",
) -> None:
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
    _write_json(
        base_dir
        / "docs/integration/myprivateagent-provider-integration-acceptance/"
        / "phase14-myprivateagent-provider-integration-acceptance-checkpoint.json",
        {
            "status": "ready" if phase14_blocker_category == "none" else "review",
            "acceptance_state": "ready_for_myprivateagent_repo_side_trial"
            if phase14_blocker_category == "none"
            else "review_for_myprivateagent_repo_side_trial",
            "decision": "approve_myprivateagent_repo_side_trial"
            if phase14_blocker_category == "none"
            else "refresh_provider_integration_evidence",
            "summary": {
                "roadmap_focus": "myprivateagent_repo_side_trial",
                "blocker_category": phase14_blocker_category,
                "phase10_status": "ready",
                "phase11_status": "ready",
                "phase13_status": "ready",
                "handoff_status": "ready",
            },
        },
    )
    _write_json(
        base_dir
        / "docs/integration/myprivateagent-repo-side-trial-dispatch/"
        / "phase15-myprivateagent-repo-side-trial-dispatch-package.json",
        {
            "status": "ready" if phase14_blocker_category == "none" else "review",
            "dispatch_state": "ready_for_repo_side_trial_dispatch"
            if phase14_blocker_category == "none"
            else "review_for_repo_side_trial_dispatch",
            "decision": "dispatch_myprivateagent_repo_side_trial"
            if phase14_blocker_category == "none"
            else "refresh_provider_dispatch_evidence",
            "summary": {
                "roadmap_focus": "myprivateagent_repo_side_trial_dispatch",
                "blocker_category": "none"
                if phase14_blocker_category == "none"
                else "external_environment",
                "phase10_status": "ready",
                "phase11_status": "ready",
                "phase13_status": "ready",
                "phase14_status": "ready"
                if phase14_blocker_category == "none"
                else "review",
                "handoff_status": "ready",
                "caller_checklist": [
                    "dispatch_myprivateagent_repo_side_trial",
                    "capture_trial_outcome_and_refresh_evidence",
                ],
            },
        },
    )
    if include_handoff:
        _write_json(
            base_dir / "docs/integration/provider-handoff/provider-handoff-bundle.json",
            {
                "status": handoff_overall_status,
                "decision": "continue_provider_first_with_candidate_backends",
                "access_focused_visibility": {
                    "status": handoff_access_status,
                    "tracked_artifact_ids": [
                        "phase10_myprivateagent_local_consumer_readiness",
                        "phase10_myprivateagent_local_consumer_probe",
                        "phase11_local_provider_integration_profile",
                        "phase11_provider_discovery_smoke",
                        "phase11_rag_retrieve_consumption_smoke",
                        "phase11_source_binding_preview_smoke",
                        "phase13_provider_roadmap_decision_checkpoint",
                        "phase14_myprivateagent_provider_integration_acceptance_checkpoint",
                        "phase15_myprivateagent_repo_side_trial_dispatch_package",
                    ],
                    "open_gate_ids": []
                    if handoff_access_status == "ready"
                    else [
                        "phase10_myprivateagent_local_consumer_readiness",
                    ],
                },
                "evidence_artifacts": [
                    {"id": "phase15_myprivateagent_repo_side_trial_dispatch_package"}
                ],
            },
        )
        _write_json(
            base_dir / "docs/integration/provider-handoff-refresh/provider-handoff-refresh.json",
            {
                "status": handoff_overall_status,
                "decision": "continue_provider_first_with_candidate_backends",
                "access_focused_visibility": {
                    "status": handoff_access_status,
                    "tracked_step_ids": [
                        "phase10_myprivateagent_local_consumer_readiness",
                        "phase10_myprivateagent_local_consumer_probe",
                        "phase11_local_provider_integration_profile",
                        "phase11_provider_discovery_smoke",
                        "phase11_rag_retrieve_consumption_smoke",
                        "phase11_source_binding_preview_smoke",
                        "phase13_provider_roadmap_decision_checkpoint",
                        "phase14_myprivateagent_provider_integration_acceptance_checkpoint",
                        "phase15_myprivateagent_repo_side_trial_dispatch_package",
                        "provider_handoff_bundle",
                    ],
                    "open_gate_ids": []
                    if handoff_access_status == "ready"
                    else [
                        "phase10_myprivateagent_local_consumer_readiness",
                    ],
                },
                "steps": [
                    {"id": "phase15_myprivateagent_repo_side_trial_dispatch_package"}
                ],
            },
        )


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
