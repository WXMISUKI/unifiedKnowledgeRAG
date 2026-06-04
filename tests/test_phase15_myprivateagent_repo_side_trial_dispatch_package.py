import json
from pathlib import Path

from app.services.phase15_myprivateagent_repo_side_trial_dispatch_package import (
    build_phase15_myprivateagent_repo_side_trial_dispatch_package_report,
    export_phase15_myprivateagent_repo_side_trial_dispatch_package_report,
    render_phase15_myprivateagent_repo_side_trial_dispatch_package_markdown,
)


def test_build_phase15_dispatch_package_reports_repo_side_trial_ready(tmp_path):
    _seed_phase15_ready_evidence(tmp_path)

    report = build_phase15_myprivateagent_repo_side_trial_dispatch_package_report(
        base_dir=tmp_path
    )

    assert report.id == "phase15-myprivateagent-repo-side-trial-dispatch-package-v1"
    assert report.status == "ready"
    assert report.dispatch_state == "ready_for_repo_side_trial_dispatch"
    assert report.decision == "dispatch_myprivateagent_repo_side_trial"
    assert report.summary["roadmap_focus"] == "myprivateagent_repo_side_trial_dispatch"
    assert report.summary["blocker_category"] == "none"
    assert report.summary["phase10_status"] == "ready"
    assert report.summary["phase11_status"] == "ready"
    assert report.summary["phase13_status"] == "ready"
    assert report.summary["phase14_status"] == "ready"
    assert report.summary["handoff_status"] == "ready"
    assert report.summary["caller_checklist"] == [
        "dispatch_myprivateagent_repo_side_trial",
        "capture_trial_outcome_and_refresh_evidence",
    ]
    assert report.caller_checklist == report.summary["caller_checklist"]
    assert report.summary["ready_signals"] == len(report.signals)
    assert report.summary["open_gate_ids"] == []
    assert all(signal.status == "ready" for signal in report.signals)


def test_build_phase15_dispatch_package_classifies_missing_provider_evidence(tmp_path):
    _seed_phase15_ready_evidence(tmp_path, include_phase10_readiness=False)

    report = build_phase15_myprivateagent_repo_side_trial_dispatch_package_report(
        base_dir=tmp_path
    )

    assert report.status == "blocked"
    assert report.dispatch_state == "blocked_for_repo_side_trial_dispatch"
    assert report.summary["blocker_category"] == "provider_evidence"
    assert "phase10_myprivateagent_local_consumer_readiness" in report.summary[
        "blocked_signal_ids"
    ]


def test_build_phase15_dispatch_package_classifies_missing_handoff_visibility(tmp_path):
    _seed_phase15_ready_evidence(tmp_path, include_handoff=False)

    report = build_phase15_myprivateagent_repo_side_trial_dispatch_package_report(
        base_dir=tmp_path
    )

    assert report.status == "blocked"
    assert report.dispatch_state == "blocked_for_repo_side_trial_dispatch"
    assert report.summary["blocker_category"] == "handoff_visibility"
    assert "provider_handoff_bundle" in report.summary["blocked_signal_ids"]
    assert "provider_handoff_refresh" in report.summary["blocked_signal_ids"]
    assert render_phase15_myprivateagent_repo_side_trial_dispatch_package_markdown(
        report
    ).startswith("# Phase 15 MyPrivateAgent Repo-Side Trial Dispatch Package")


def test_build_phase15_dispatch_package_classifies_external_environment(tmp_path):
    _seed_phase15_ready_evidence(
        tmp_path,
        phase14_blocker_category="external_environment",
    )

    report = build_phase15_myprivateagent_repo_side_trial_dispatch_package_report(
        base_dir=tmp_path
    )

    assert report.status == "review"
    assert report.dispatch_state == "review_for_repo_side_trial_dispatch"
    assert report.summary["blocker_category"] == "external_environment"
    assert "phase14_myprivateagent_provider_integration_acceptance_checkpoint" in report.summary[
        "review_signal_ids"
    ]
    assert "phase14_myprivateagent_provider_integration_acceptance_checkpoint" in report.summary[
        "open_gate_ids"
    ]


def test_export_phase15_dispatch_package_writes_outputs(tmp_path):
    _seed_phase15_ready_evidence(tmp_path)

    report = export_phase15_myprivateagent_repo_side_trial_dispatch_package_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["dispatch_state"] == "ready_for_repo_side_trial_dispatch"
    assert payload["summary"]["blocker_category"] == "none"
    assert "# Phase 15 MyPrivateAgent Repo-Side Trial Dispatch Package" in markdown


def _seed_phase15_ready_evidence(
    base_dir: Path,
    *,
    include_phase10_readiness: bool = True,
    include_handoff: bool = True,
    phase14_blocker_category: str = "none",
) -> None:
    if include_phase10_readiness:
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
    if include_handoff:
        _write_json(
            base_dir / "docs/integration/provider-handoff/provider-handoff-bundle.json",
            {
                "status": "ready",
                "decision": "continue_provider_first_with_candidate_backends",
                "evidence_artifacts": [
                    {"id": "phase15_myprivateagent_repo_side_trial_dispatch_package"}
                ],
            },
        )
        _write_json(
            base_dir / "docs/integration/provider-handoff-refresh/provider-handoff-refresh.json",
            {
                "status": "ready",
                "decision": "continue_provider_first_with_candidate_backends",
                "steps": [
                    {"id": "phase15_myprivateagent_repo_side_trial_dispatch_package"}
                ],
            },
        )


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
