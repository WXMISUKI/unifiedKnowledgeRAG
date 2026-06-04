import json
from dataclasses import dataclass
from pathlib import Path

from app.services.provider_handoff_refresh import (
    HandoffRefreshStepSpec,
    default_handoff_refresh_steps,
    _phase3_fp_fn_step_status,
    refresh_provider_handoff_evidence,
    render_provider_handoff_refresh_markdown,
)


@dataclass(frozen=True)
class FakeRefreshReport:
    status: str
    json_path: Path
    markdown_path: Path


def test_handoff_refresh_reports_ready_when_all_steps_ready(tmp_path):
    report = refresh_provider_handoff_evidence(
        output_dir=tmp_path / "refresh",
        steps=[
            _step(tmp_path, "integration", "ready"),
            _step(tmp_path, "smoke", "ready"),
        ],
    )

    assert report.status == "ready"
    assert [step["status"] for step in report.steps] == ["ready", "ready"]
    assert report.json_path is not None
    assert report.markdown_path is not None
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")
    assert payload["id"] == "provider-handoff-refresh-v1"
    assert "# Provider Handoff Evidence Refresh" in markdown


def test_handoff_refresh_preserves_review_state(tmp_path):
    report = refresh_provider_handoff_evidence(
        output_dir=tmp_path / "refresh",
        steps=[
            _step(tmp_path, "integration", "ready"),
            _step(tmp_path, "deployment", "review"),
            _step(tmp_path, "handoff", "ready"),
        ],
    )

    assert report.status == "review"
    assert [step["status"] for step in report.steps] == [
        "ready",
        "review",
        "ready",
    ]
    assert any("human review" in note for note in report.operation_notes)


def test_handoff_refresh_blocks_and_skips_after_failure(tmp_path):
    report = refresh_provider_handoff_evidence(
        output_dir=tmp_path / "refresh",
        steps=[
            _step(tmp_path, "integration", "ready"),
            _failing_step("smoke"),
            _step(tmp_path, "deployment", "ready"),
        ],
    )

    assert report.status == "blocked"
    assert [step["status"] for step in report.steps] == [
        "ready",
        "blocked",
        "skipped",
    ]
    assert report.steps[1]["recommended_action"] == "resolve_step_failure"
    assert report.steps[2]["recommended_action"] == "not_run_due_to_previous_failure"


def test_handoff_refresh_blocks_on_blocked_step_status(tmp_path):
    report = refresh_provider_handoff_evidence(
        output_dir=tmp_path / "refresh",
        steps=[
            _step(tmp_path, "integration", "blocked"),
            _step(tmp_path, "smoke", "ready"),
        ],
    )

    assert report.status == "blocked"
    assert [step["status"] for step in report.steps] == ["blocked", "skipped"]
    assert "Refresh stopped" in "\n".join(report.operation_notes)


def test_handoff_refresh_markdown_lists_outputs(tmp_path):
    report = refresh_provider_handoff_evidence(
        output_dir=tmp_path / "refresh",
        steps=[_step(tmp_path, "integration", "ready")],
    )

    markdown = render_provider_handoff_refresh_markdown(report)

    assert "| Step | Category | Status | Output Paths | Recommended Action | Summary |" in markdown
    assert "integration.json" in markdown
    assert "integration.md" in markdown


def test_default_handoff_refresh_runs_source_binding_before_bundle():
    steps = default_handoff_refresh_steps()
    step_ids = [step.id for step in steps]

    assert "source_binding_summary" in step_ids
    assert "phase2_source_format_demand_readiness" in step_ids
    assert "phase2_unsupported_format_negative_control_smoke" in step_ids
    assert "phase6_bge_m3_artifact_readiness" in step_ids
    assert "phase6_bge_m3_vs_mock_fixture_diagnostics" in step_ids
    assert "phase6_bge_m3_comparison_smoke" in step_ids
    assert "phase6_qdrant_vector_store_readiness" in step_ids
    assert "phase6_qdrant_backup_restore_smoke" in step_ids
    assert "phase6_qdrant_bge_private_network_promotion_readiness" in step_ids
    assert "phase6_qdrant_bge_private_network_promotion_smoke" in step_ids
    assert "phase6_deployed_field_validation_readiness" in step_ids
    assert "phase6_deployed_handoff_consistency_smoke" in step_ids
    assert "phase3_fp_fn_review" in step_ids
    assert "phase3_candidate_runtime_diagnostics" in step_ids
    assert "phase3_candidate_latency_resource_diagnostics" in step_ids
    assert "phase3_hybrid_fusion_threshold_calibration" in step_ids
    assert "phase3_hybrid_cross_case_fp_fn_smoke" in step_ids
    assert "phase3_aggregation_relation_negative_control_smoke" in step_ids
    assert "phase3_hybrid_runtime_promotion_decision_readiness" in step_ids
    assert "phase3_hybrid_runtime_promotion_decision_smoke" in step_ids
    assert "phase4_evidence_pack_readiness" in step_ids
    assert "phase4_caller_consumption_smoke" in step_ids
    assert "phase5_graph_use_case_readiness" in step_ids
    assert "phase5_graph_boundary_smoke_summary" in step_ids
    assert "phase7_provider_release_readiness" in step_ids
    assert "phase7_cross_phase_handoff_consistency_smoke" in step_ids
    assert "phase8_live_url_validation_readiness" in step_ids
    assert "phase9_myprivateagent_local_consumption_readiness" in step_ids
    assert "phase9_myprivateagent_local_consumption_smoke" in step_ids
    assert "phase10_myprivateagent_local_consumer_readiness" in step_ids
    assert "phase11_local_provider_integration_profile" in step_ids
    assert "phase10_myprivateagent_local_consumer_probe" in step_ids
    assert "phase11_provider_discovery_smoke" in step_ids
    assert "phase11_rag_retrieve_consumption_smoke" in step_ids
    assert "phase11_source_binding_preview_smoke" in step_ids
    assert "phase14_myprivateagent_provider_integration_acceptance_checkpoint" in step_ids
    assert "phase15_myprivateagent_repo_side_trial_dispatch_package" in step_ids
    assert "phase12b_candidate_backend_evaluation_readiness" in step_ids
    assert "phase12c_pgvector_candidate_backend_readiness" in step_ids
    assert "phase12d_pgvector_live_probe_readiness" in step_ids
    assert "phase12e_pgvector_local_probe_environment_readiness" in step_ids
    assert "phase12f_pgvector_local_live_probe_execution_readiness" in step_ids
    assert "phase13_provider_roadmap_decision_checkpoint" in step_ids
    assert "phase8_live_url_smoke_consistency_check" in step_ids
    assert step_ids.index("source_binding_summary") < step_ids.index(
        "phase3_fp_fn_review"
    )
    assert step_ids.index("reindex_readiness") < step_ids.index(
        "phase6_bge_m3_artifact_readiness"
    )
    assert step_ids.index("phase6_bge_m3_artifact_readiness") < step_ids.index(
        "phase6_bge_m3_vs_mock_fixture_diagnostics"
    )
    assert step_ids.index("phase6_bge_m3_vs_mock_fixture_diagnostics") < step_ids.index(
        "phase6_bge_m3_comparison_smoke"
    )
    assert step_ids.index("phase6_bge_m3_comparison_smoke") < step_ids.index(
        "phase6_qdrant_vector_store_readiness"
    )
    assert step_ids.index("phase6_qdrant_vector_store_readiness") < step_ids.index(
        "phase6_qdrant_backup_restore_smoke"
    )
    assert step_ids.index("phase6_qdrant_backup_restore_smoke") < step_ids.index(
        "phase6_qdrant_bge_private_network_promotion_readiness"
    )
    assert step_ids.index("phase6_qdrant_bge_private_network_promotion_readiness") < step_ids.index(
        "phase6_qdrant_bge_private_network_promotion_smoke"
    )
    assert step_ids.index("phase6_qdrant_bge_private_network_promotion_smoke") < step_ids.index(
        "source_binding_summary"
    )
    assert step_ids.index("source_binding_summary") < step_ids.index(
        "phase2_source_format_demand_readiness"
    )
    assert step_ids.index("phase2_source_format_demand_readiness") < step_ids.index(
        "phase2_unsupported_format_negative_control_smoke"
    )
    assert step_ids.index("phase2_unsupported_format_negative_control_smoke") < step_ids.index(
        "phase6_deployed_field_validation_readiness"
    )
    assert step_ids.index("phase6_deployed_field_validation_readiness") < step_ids.index(
        "phase3_fp_fn_review"
    )
    assert step_ids.index("phase3_fp_fn_review") < step_ids.index(
        "phase3_retrieval_promotion_readiness"
    )
    assert step_ids.index("phase3_retrieval_promotion_readiness") < step_ids.index(
        "phase3_candidate_runtime_diagnostics"
    )
    assert step_ids.index("phase3_candidate_runtime_diagnostics") < step_ids.index(
        "phase3_candidate_latency_resource_diagnostics"
    )
    assert step_ids.index(
        "phase3_candidate_latency_resource_diagnostics"
    ) < step_ids.index(
        "phase3_hybrid_fusion_threshold_calibration"
    )
    assert step_ids.index(
        "phase3_hybrid_fusion_threshold_calibration"
    ) < step_ids.index(
        "phase3_hybrid_cross_case_fp_fn_smoke"
    )
    assert step_ids.index("phase3_hybrid_cross_case_fp_fn_smoke") < step_ids.index(
        "phase3_aggregation_relation_negative_control_smoke"
    )
    assert step_ids.index(
        "phase3_aggregation_relation_negative_control_smoke"
    ) < step_ids.index(
        "phase3_hybrid_runtime_promotion_decision_readiness"
    )
    assert step_ids.index(
        "phase3_hybrid_runtime_promotion_decision_readiness"
    ) < step_ids.index(
        "phase3_hybrid_runtime_promotion_decision_smoke"
    )
    assert step_ids.index(
        "phase3_hybrid_runtime_promotion_decision_smoke"
    ) < step_ids.index(
        "phase4_evidence_pack_readiness"
    )
    assert step_ids.index("phase4_evidence_pack_readiness") < step_ids.index(
        "phase4_caller_consumption_smoke"
    )
    assert step_ids.index("phase4_caller_consumption_smoke") < step_ids.index(
        "phase5_graph_use_case_readiness"
    )
    assert step_ids.index("phase5_graph_use_case_readiness") < step_ids.index(
        "phase5_graph_boundary_smoke_summary"
    )
    assert step_ids.index("phase5_graph_boundary_smoke_summary") < step_ids.index(
        "phase7_provider_release_readiness"
    )
    assert step_ids.index("phase7_provider_release_readiness") < step_ids.index(
        "phase7_cross_phase_handoff_consistency_smoke"
    )
    assert step_ids.index("phase7_cross_phase_handoff_consistency_smoke") < step_ids.index(
        "phase8_live_url_validation_readiness"
    )
    assert step_ids.index("phase8_live_url_validation_readiness") < step_ids.index(
        "phase9_myprivateagent_local_consumption_readiness"
    )
    assert step_ids.index("phase9_myprivateagent_local_consumption_readiness") < step_ids.index(
        "phase9_myprivateagent_local_consumption_smoke"
    )
    assert step_ids.index("phase9_myprivateagent_local_consumption_smoke") < step_ids.index(
        "phase10_myprivateagent_local_consumer_readiness"
    )
    assert step_ids.index("phase10_myprivateagent_local_consumer_readiness") < step_ids.index(
        "phase11_local_provider_integration_profile"
    )
    assert step_ids.index("phase11_local_provider_integration_profile") < step_ids.index(
        "phase12b_candidate_backend_evaluation_readiness"
    )
    assert step_ids.index("phase12b_candidate_backend_evaluation_readiness") < step_ids.index(
        "phase12c_pgvector_candidate_backend_readiness"
    )
    assert step_ids.index("phase12c_pgvector_candidate_backend_readiness") < step_ids.index(
        "phase12d_pgvector_live_probe_readiness"
    )
    assert step_ids.index("phase12d_pgvector_live_probe_readiness") < step_ids.index(
        "phase12e_pgvector_local_probe_environment_readiness"
    )
    assert step_ids.index("phase12e_pgvector_local_probe_environment_readiness") < step_ids.index(
        "phase12f_pgvector_local_live_probe_execution_readiness"
    )
    assert step_ids.index("phase12f_pgvector_local_live_probe_execution_readiness") < step_ids.index(
        "phase13_provider_roadmap_decision_checkpoint"
    )
    assert step_ids.index("phase11_provider_discovery_smoke") < step_ids.index(
        "phase10_myprivateagent_local_consumer_probe"
    )
    assert step_ids.index("phase10_myprivateagent_local_consumer_probe") < step_ids.index(
        "phase11_rag_retrieve_consumption_smoke"
    )
    assert step_ids.index("phase11_rag_retrieve_consumption_smoke") < step_ids.index(
        "phase11_source_binding_preview_smoke"
    )
    assert step_ids.index("phase11_source_binding_preview_smoke") < step_ids.index(
        "phase14_myprivateagent_provider_integration_acceptance_checkpoint"
    )
    assert step_ids.index(
        "phase14_myprivateagent_provider_integration_acceptance_checkpoint"
    ) < step_ids.index("phase15_myprivateagent_repo_side_trial_dispatch_package")
    assert step_ids.index(
        "phase15_myprivateagent_repo_side_trial_dispatch_package"
    ) < step_ids.index("provider_handoff_bundle")
    assert step_ids.index("phase13_provider_roadmap_decision_checkpoint") < step_ids.index(
        "provider_handoff_bundle"
    )
    assert step_ids.index("provider_handoff_bundle") < step_ids.index(
        "phase6_deployed_handoff_consistency_smoke"
    )
    assert step_ids.index(
        "phase12b_candidate_backend_evaluation_readiness"
    ) < step_ids.index("phase12c_pgvector_candidate_backend_readiness")
    assert step_ids.index("phase10_myprivateagent_local_consumer_probe") < step_ids.index(
        "phase6_deployed_handoff_consistency_smoke"
    )
    assert step_ids.index("phase6_deployed_handoff_consistency_smoke") < step_ids.index(
        "phase8_live_url_smoke_consistency_check"
    )


def test_phase3_fp_fn_step_status_uses_counts():
    @dataclass(frozen=True)
    class FakeFpFn:
        false_positive_count: int
        false_negative_count: int

    assert _phase3_fp_fn_step_status(FakeFpFn(0, 0)) == "ready"
    assert _phase3_fp_fn_step_status(FakeFpFn(1, 0)) == "review"
    assert _phase3_fp_fn_step_status(FakeFpFn(0, 1)) == "review"


def _step(tmp_path: Path, step_id: str, status: str) -> HandoffRefreshStepSpec:
    def exporter(output_dir: Path) -> FakeRefreshReport:
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / f"{step_id}.json"
        markdown_path = output_dir / f"{step_id}.md"
        json_path.write_text("{}", encoding="utf-8")
        markdown_path.write_text("# report\n", encoding="utf-8")
        return FakeRefreshReport(
            status=status,
            json_path=json_path,
            markdown_path=markdown_path,
        )

    return HandoffRefreshStepSpec(
        id=step_id,
        category="test",
        output_dir=tmp_path / step_id,
        exporter=exporter,
        status_reader=lambda report: report.status,
    )


def _failing_step(step_id: str) -> HandoffRefreshStepSpec:
    def exporter(output_dir: Path) -> FakeRefreshReport:
        raise RuntimeError("boom")

    return HandoffRefreshStepSpec(
        id=step_id,
        category="test",
        output_dir=Path(step_id),
        exporter=exporter,
        status_reader=lambda report: report.status,
    )
