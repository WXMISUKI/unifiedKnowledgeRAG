import json
from pathlib import Path

from app.services.phase13_provider_roadmap_decision_checkpoint import (
    build_phase13_provider_roadmap_decision_checkpoint_report,
    export_phase13_provider_roadmap_decision_checkpoint_report,
    render_phase13_provider_roadmap_decision_checkpoint_markdown,
)


def test_build_phase13_provider_roadmap_decision_checkpoint_prefers_provider_hardening(tmp_path):
    _seed_phase13_evidence(tmp_path)

    report = build_phase13_provider_roadmap_decision_checkpoint_report(base_dir=tmp_path)

    assert report.id == "phase13-provider-roadmap-decision-checkpoint-v1"
    assert report.status == "review"
    assert report.decision == "resume_provider_integration_hardening"
    assert report.summary["roadmap_focus"] == "resume_provider_integration_hardening"
    assert report.summary["candidate_backend_posture"] == "pause_pgvector_until_live_probe_executed"
    assert report.summary["phase12d_status"] == "blocked"
    assert report.summary["phase12f_status"] == "review"
    assert "refresh_provider_integration_handoff_evidence" in report.summary["next_step_tasks"]
    assert any(family.status == "review" for family in report.decision_families)
    assert any(
        artifact.id == "phase12f_pgvector_local_live_probe_execution_readiness"
        and artifact.status == "review"
        for artifact in report.supporting_artifacts
    )


def test_export_phase13_provider_roadmap_decision_checkpoint_writes_outputs(tmp_path):
    _seed_phase13_evidence(tmp_path)

    report = export_phase13_provider_roadmap_decision_checkpoint_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["summary"]["candidate_backend_posture"] == "pause_pgvector_until_live_probe_executed"
    assert "# Phase 13 Provider Roadmap Decision Checkpoint" in markdown
    assert (
        render_phase13_provider_roadmap_decision_checkpoint_markdown(report)
        == markdown
    )


def _seed_phase13_evidence(base_dir: Path) -> None:
    _write_json(
        base_dir
        / "docs/operations/candidate-backend-evaluation-readiness/"
        / "phase12b-candidate-backend-evaluation-readiness.json",
        {
            "status": "review",
            "decision": "continue_spike",
            "summary": {
                "strategy_verdict": "continue_provider_first_with_candidate_backends",
                "review_ready_family_ids": ["local_provider_integration_gate"],
                "reference_only_family_ids": ["reference_only_candidates"],
                "open_gate_ids": ["phase12b_open_gate"],
            },
        },
    )
    _write_json(
        base_dir
        / "docs/operations/pgvector-candidate-backend-readiness/"
        / "phase12c-pgvector-candidate-backend-readiness.json",
        {
            "status": "blocked",
            "evaluation_state": "pgvector_candidate_configuration_blocked",
            "decision": "keep_current_default",
            "summary": {
                "strategy_verdict": "continue_provider_first_with_candidate_backends",
                "pgvector_database_url_present": False,
                "review_ready_family_ids": ["provider_integration_gate"],
                "ready_family_ids": [],
                "blocked_family_ids": ["pgvector_configuration_gate"],
                "open_gate_ids": ["phase12c_open_gate"],
            },
        },
    )
    _write_json(
        base_dir
        / "docs/operations/pgvector-live-probe-readiness/"
        / "phase12d-pgvector-live-probe-readiness.json",
        {
            "status": "blocked",
            "evaluation_state": "pgvector_probe_configuration_blocked",
            "decision": "keep_current_default",
            "summary": {
                "strategy_verdict": "continue_provider_first_with_candidate_backends",
                "pgvector_database_url_present": False,
                "pgvector_driver_available": False,
                "review_ready_family_ids": [],
                "ready_family_ids": ["candidate_evidence_bridge_gate"],
                "blocked_family_ids": ["pgvector_probe_gate", "pgvector_runtime_gate"],
                "open_gate_ids": ["phase12d_open_gate"],
            },
        },
    )
    _write_json(
        base_dir
        / "docs/operations/pgvector-local-probe-environment/"
        / "phase12e-pgvector-local-probe-environment-readiness.json",
        {
            "status": "ready",
            "decision": "continue_spike",
            "summary": {
                "strategy_verdict": "continue_provider_first_with_candidate_backends",
                "phase12d_report_status": "blocked",
                "optional_dependency_present": True,
                "ready_family_ids": ["pgvector_local_environment_pack", "pgvector_probe_bridge"],
                "review_ready_family_ids": [],
                "blocked_family_ids": [],
                "open_gate_ids": [],
            },
        },
    )
    _write_json(
        base_dir
        / "docs/operations/pgvector-local-live-probe-execution/"
        / "phase12f-pgvector-local-live-probe-execution-readiness.json",
        {
            "status": "review",
            "execution_state": "ready_for_local_live_probe_rerun",
            "decision": "continue_spike",
            "summary": {
                "strategy_verdict": "continue_provider_first_with_candidate_backends",
                "phase12e_environment_status": "ready",
                "phase12d_live_probe_status": "blocked",
                "rerun_required": True,
                "ready_family_ids": ["pgvector_local_execution_pack", "pgvector_handoff_bridge"],
                "review_ready_family_ids": [],
                "blocked_family_ids": [],
                "open_gate_ids": ["phase12f_open_gate"],
            },
        },
    )
    _write_json(
        base_dir / "docs/integration/provider-handoff/provider-handoff-bundle.json",
        {
            "status": "review",
            "decision": "review_evidence_notes",
            "evidence_artifacts": [
                {"id": "phase13_provider_roadmap_decision_checkpoint"},
            ],
        },
    )
    _write_json(
        base_dir / "docs/integration/provider-handoff-refresh/provider-handoff-refresh.json",
        {
            "status": "review",
            "decision": "review_evidence_notes",
            "steps": [
                {"id": "phase13_provider_roadmap_decision_checkpoint"},
            ],
        },
    )


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
