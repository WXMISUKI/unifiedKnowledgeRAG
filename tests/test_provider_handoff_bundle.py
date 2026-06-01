import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app
from app.services.provider_handoff_bundle import (
    HandoffEvidenceSpec,
    build_provider_handoff_bundle_report,
    export_provider_handoff_bundle_report,
    render_provider_handoff_bundle_markdown,
)


def test_provider_handoff_bundle_summarizes_default_evidence():
    report = build_provider_handoff_bundle_report()

    assert report.id == "provider-handoff-bundle-v1"
    assert report.status == "review"
    assert report.provider["provider_id"] == "unifiedKnowledgeProvider"
    assert report.provider["contract_version"] == "knowledge-provider-contract-v1"
    artifacts = {artifact["id"]: artifact for artifact in report.evidence_artifacts}
    assert artifacts["provider_integration_probe"]["status"] == "ready"
    assert artifacts["provider_contract_smoke"]["status"] == "ready"
    assert artifacts["deployment_readiness"]["status"] == "review"
    assert artifacts["reindex_readiness"]["status"] == "ready"
    assert artifacts["source_binding_summary"]["status"] == "ready"
    assert artifacts["source_binding_summary"]["summary"] == (
        "status=ready; bindable_sources=2/2; source_statuses=ready:2; "
        "recommended_actions=bind_source_from_control_plane:2"
    )
    assert artifacts["phase3_seed_retrieval_baseline"]["present"] is True
    assert artifacts["phase3_seed_retrieval_baseline"]["required"] is False
    assert artifacts["phase3_seed_retrieval_baseline"]["status"] == "ready"
    assert "total_cases=32" in artifacts["phase3_seed_retrieval_baseline"]["summary"]
    assert artifacts["phase3_fp_fn_review"]["present"] is True
    assert artifacts["phase3_fp_fn_review"]["required"] is False
    assert artifacts["phase3_fp_fn_review"]["status"] == "ready"
    assert "false_positive_count=3" in artifacts["phase3_fp_fn_review"]["summary"]
    assert artifacts["phase3_retrieval_promotion_readiness"]["present"] is True
    assert artifacts["phase3_retrieval_promotion_readiness"]["required"] is False
    assert artifacts["phase3_retrieval_promotion_readiness"]["status"] == "review"
    assert "decision=keep_runtime_defaults" in artifacts[
        "phase3_retrieval_promotion_readiness"
    ]["summary"]
    assert artifacts["phase3_candidate_runtime_diagnostics"]["present"] is True
    assert artifacts["phase3_candidate_runtime_diagnostics"]["required"] is False
    assert artifacts["phase3_candidate_runtime_diagnostics"]["status"] == "review"
    assert "decision=keep_runtime_defaults" in artifacts[
        "phase3_candidate_runtime_diagnostics"
    ]["summary"]
    assert artifacts["phase3_candidate_latency_resource_diagnostics"]["present"] is True
    assert artifacts["phase3_candidate_latency_resource_diagnostics"]["required"] is False
    assert artifacts["phase3_candidate_latency_resource_diagnostics"]["status"] == "review"
    assert "decision=keep_runtime_defaults" in artifacts[
        "phase3_candidate_latency_resource_diagnostics"
    ]["summary"]
    assert "avg_latency_ms=" in artifacts[
        "phase3_candidate_latency_resource_diagnostics"
    ]["summary"]
    assert artifacts["phase3_hybrid_cross_case_fp_fn_smoke"]["present"] is True
    assert artifacts["phase3_hybrid_cross_case_fp_fn_smoke"]["required"] is False
    assert artifacts["phase3_hybrid_cross_case_fp_fn_smoke"]["status"] == "ready"
    assert "false_positive_count=3" in artifacts[
        "phase3_hybrid_cross_case_fp_fn_smoke"
    ]["summary"]
    assert artifacts["phase3_aggregation_relation_negative_control_smoke"]["present"] is True
    assert artifacts["phase3_aggregation_relation_negative_control_smoke"]["required"] is False
    assert artifacts["phase3_aggregation_relation_negative_control_smoke"]["status"] == "ready"
    assert "relation_unsupported_count=1" in artifacts[
        "phase3_aggregation_relation_negative_control_smoke"
    ]["summary"]
    assert artifacts["phase4_evidence_pack_readiness"]["present"] is True
    assert artifacts["phase4_evidence_pack_readiness"]["required"] is False
    assert artifacts["phase4_evidence_pack_readiness"]["status"] == "ready"
    assert "decision=keep_caller_ownership" in artifacts[
        "phase4_evidence_pack_readiness"
    ]["summary"]
    assert artifacts["phase4_caller_consumption_smoke"]["present"] is True
    assert artifacts["phase4_caller_consumption_smoke"]["required"] is False
    assert artifacts["phase4_caller_consumption_smoke"]["status"] == "ready"
    assert "passed_checks=3/3" in artifacts[
        "phase4_caller_consumption_smoke"
    ]["summary"]
    assert artifacts["phase5_graph_use_case_readiness"]["present"] is True
    assert artifacts["phase5_graph_use_case_readiness"]["required"] is False
    assert artifacts["phase5_graph_use_case_readiness"]["status"] == "ready"
    assert "decision=keep_graph_query_planned" in artifacts[
        "phase5_graph_use_case_readiness"
    ]["summary"]
    assert artifacts["phase5_graph_boundary_smoke_summary"]["present"] is True
    assert artifacts["phase5_graph_boundary_smoke_summary"]["required"] is False
    assert artifacts["phase5_graph_boundary_smoke_summary"]["status"] == "ready"
    assert "graph_checks_passed=2" in artifacts[
        "phase5_graph_boundary_smoke_summary"
    ]["summary"]
    assert artifacts["deployed_provider_smoke"]["present"] is False
    assert artifacts["deployed_provider_smoke"]["required"] is False
    assert artifacts["deployed_provider_smoke"]["status"] == "review"
    assert artifacts["deployed_provider_smoke"]["recommended_action"] == (
        "run_deployed_provider_smoke_after_deployment"
    )
    assert any("read-only" in note for note in report.operation_notes)
    assert any(
        "Deployed provider smoke evidence is optional" in note
        for note in report.operation_notes
    )


def test_provider_handoff_bundle_blocks_missing_evidence(tmp_path):
    specs = [
        HandoffEvidenceSpec(
            id="provider_contract_smoke",
            category="contract",
            path="missing-smoke.json",
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "blocked"
    artifact = report.evidence_artifacts[0]
    assert artifact["present"] is False
    assert artifact["required"] is True
    assert artifact["status"] == "missing"
    assert artifact["recommended_action"] == "regenerate_provider_contract_smoke"


def test_provider_handoff_bundle_blocks_failed_smoke(tmp_path):
    smoke_path = tmp_path / "smoke.json"
    smoke_path.write_text(
        json.dumps(
            {
                "passed": False,
                "summary": {
                    "total": 8,
                    "passed": 7,
                    "failed": 1,
                },
            }
        ),
        encoding="utf-8",
    )
    specs = [
        HandoffEvidenceSpec(
            id="provider_contract_smoke",
            category="contract",
            path="smoke.json",
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "blocked"
    artifact = report.evidence_artifacts[0]
    assert artifact["present"] is True
    assert artifact["required"] is True
    assert artifact["status"] == "blocked"
    assert artifact["recommended_action"] == "resolve_failed_evidence"


def test_provider_handoff_bundle_preserves_review_status(tmp_path):
    readiness_path = tmp_path / "deployment-readiness.json"
    readiness_path.write_text(
        json.dumps({"status": "review"}),
        encoding="utf-8",
    )
    specs = [
        HandoffEvidenceSpec(
            id="deployment_readiness",
            category="operations",
            path="deployment-readiness.json",
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "review"
    artifact = report.evidence_artifacts[0]
    assert artifact["status"] == "review"
    assert artifact["recommended_action"] == "review_evidence_notes"


def test_export_provider_handoff_bundle_writes_json_and_markdown(tmp_path):
    output_dir = tmp_path / "handoff"
    report = export_provider_handoff_bundle_report(output_dir=output_dir)

    assert report.json_path is not None
    assert report.markdown_path is not None
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == "provider-handoff-bundle-v1"
    assert payload["status"] == report.status
    assert payload["json_path"] == str(report.json_path)
    assert "# Provider Handoff Bundle" in markdown
    assert "| Artifact | Category | Present | Status | Summary | Recommended Action |" in markdown
    assert "provider_contract_smoke" in render_provider_handoff_bundle_markdown(report)


def test_provider_handoff_endpoint_returns_current_bundle():
    client = TestClient(create_app())

    response = client.get("/api/provider/handoff")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "provider-handoff-bundle-v1"
    assert body["status"] == "review"
    assert body["provider"]["provider_id"] == "unifiedKnowledgeProvider"
    artifacts = {artifact["id"]: artifact for artifact in body["evidence_artifacts"]}
    assert artifacts["provider_integration_probe"]["status"] == "ready"
    assert artifacts["provider_contract_smoke"]["status"] == "ready"
    assert artifacts["deployment_readiness"]["status"] == "review"
    assert artifacts["reindex_readiness"]["status"] == "ready"
    assert artifacts["source_binding_summary"]["status"] == "ready"
    assert artifacts["phase3_seed_retrieval_baseline"]["status"] == "ready"
    assert artifacts["phase3_fp_fn_review"]["status"] == "ready"
    assert artifacts["phase3_retrieval_promotion_readiness"]["status"] == "review"
    assert artifacts["phase3_candidate_runtime_diagnostics"]["status"] == "review"
    assert artifacts["phase3_candidate_latency_resource_diagnostics"]["status"] == "review"
    assert artifacts["phase3_hybrid_cross_case_fp_fn_smoke"]["status"] == "ready"
    assert artifacts["phase3_aggregation_relation_negative_control_smoke"]["status"] == "ready"
    assert artifacts["phase4_evidence_pack_readiness"]["status"] == "ready"
    assert artifacts["phase4_caller_consumption_smoke"]["status"] == "ready"
    assert artifacts["phase5_graph_use_case_readiness"]["status"] == "ready"
    assert artifacts["phase5_graph_boundary_smoke_summary"]["status"] == "ready"
    assert artifacts["deployed_provider_smoke"]["status"] == "review"
    assert artifacts["deployed_provider_smoke"]["recommended_action"] == (
        "run_deployed_provider_smoke_after_deployment"
    )
    assert body["json_path"] is None
    assert body["markdown_path"] is None


def test_provider_handoff_endpoint_is_side_effect_free(monkeypatch):
    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("handoff endpoint must only read handoff evidence")

    monkeypatch.setattr(
        "app.services.provider_handoff_refresh.refresh_provider_handoff_evidence",
        fail_if_called,
    )
    monkeypatch.setattr(
        "app.services.retrieval_backends.FixtureDocumentRetriever.retrieve",
        fail_if_called,
    )
    monkeypatch.setattr("app.routers.graph.query_graph", fail_if_called)

    client = TestClient(create_app())
    response = client.get("/api/provider/handoff")

    assert response.status_code == 200
    assert response.json()["id"] == "provider-handoff-bundle-v1"


def test_provider_handoff_bundle_summarizes_ready_deployed_smoke(tmp_path):
    smoke_path = tmp_path / "deployed-smoke.json"
    smoke_path.write_text(
        json.dumps(
            {
                "status": "ready",
                "base_url": "https://provider.example.com",
                "handoff": {"status": "ready"},
            }
        ),
        encoding="utf-8",
    )
    specs = [
        HandoffEvidenceSpec(
            id="deployed_provider_smoke",
            category="deployed-integration",
            path=Path("deployed-smoke.json"),
            required=False,
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "ready"
    artifact = report.evidence_artifacts[0]
    assert artifact["present"] is True
    assert artifact["required"] is False
    assert artifact["status"] == "ready"
    assert artifact["summary"] == (
        "status=ready; base_url=https://provider.example.com; handoff_status=ready"
    )
    assert artifact["recommended_action"] == "no_action_required"


def test_provider_handoff_bundle_blocks_blocked_deployed_smoke(tmp_path):
    smoke_path = tmp_path / "deployed-smoke.json"
    smoke_path.write_text(
        json.dumps(
            {
                "status": "blocked",
                "base_url": "https://provider.example.com",
                "handoff": {"status": "blocked"},
            }
        ),
        encoding="utf-8",
    )
    specs = [
        HandoffEvidenceSpec(
            id="deployed_provider_smoke",
            category="deployed-integration",
            path=Path("deployed-smoke.json"),
            required=False,
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "blocked"
    artifact = report.evidence_artifacts[0]
    assert artifact["present"] is True
    assert artifact["required"] is False
    assert artifact["status"] == "blocked"
    assert artifact["recommended_action"] == "resolve_failed_evidence"


def test_provider_handoff_bundle_blocks_missing_source_binding_evidence(tmp_path):
    specs = [
        HandoffEvidenceSpec(
            id="source_binding_summary",
            category="source-binding",
            path=Path("missing-source-bindings.json"),
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "blocked"
    artifact = report.evidence_artifacts[0]
    assert artifact["present"] is False
    assert artifact["required"] is True
    assert artifact["status"] == "missing"
    assert artifact["recommended_action"] == "regenerate_source_binding_summary"


def test_provider_handoff_bundle_summarizes_source_binding_evidence(tmp_path):
    source_binding_path = tmp_path / "source-bindings.json"
    source_binding_path.write_text(
        json.dumps(
            {
                "status": "ready",
                "sources": [
                    {"source_id": "refund_policy_docs", "bindable": True},
                    {"source_id": "logistics_faq", "bindable": True},
                ],
            }
        ),
        encoding="utf-8",
    )
    specs = [
        HandoffEvidenceSpec(
            id="source_binding_summary",
            category="source-binding",
            path=Path("source-bindings.json"),
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "ready"
    artifact = report.evidence_artifacts[0]
    assert artifact["status"] == "ready"
    assert artifact["summary"] == (
        "status=ready; bindable_sources=2/2; source_statuses=none; "
        "recommended_actions=none"
    )


def test_provider_handoff_bundle_prefers_source_binding_aggregate_counts(tmp_path):
    source_binding_path = tmp_path / "source-bindings.json"
    source_binding_path.write_text(
        json.dumps(
            {
                "status": "ready",
                "total_source_count": 3,
                "bindable_source_count": 2,
                "status_counts": {"ready": 2, "review": 1},
                "recommended_action_counts": {
                    "bind_source_from_control_plane": 2,
                    "review_source_fingerprint_before_binding": 1,
                },
                "sources": [
                    {
                        "source_id": "stale_row",
                        "status": "blocked",
                        "bindable": False,
                        "recommended_action": "run_ingestion_job_before_binding",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    specs = [
        HandoffEvidenceSpec(
            id="source_binding_summary",
            category="source-binding",
            path=Path("source-bindings.json"),
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    artifact = report.evidence_artifacts[0]
    assert artifact["summary"] == (
        "status=ready; bindable_sources=2/3; "
        "source_statuses=ready:2, review:1; "
        "recommended_actions=bind_source_from_control_plane:2, "
        "review_source_fingerprint_before_binding:1"
    )


def test_provider_handoff_bundle_summarizes_source_binding_actions(tmp_path):
    source_binding_path = tmp_path / "source-bindings.json"
    source_binding_path.write_text(
        json.dumps(
            {
                "status": "blocked",
                "sources": [
                    {
                        "source_id": "ready_docs",
                        "status": "ready",
                        "bindable": True,
                        "recommended_action": "bind_source_from_control_plane",
                    },
                    {
                        "source_id": "review_docs",
                        "status": "review",
                        "bindable": False,
                        "recommended_action": (
                            "review_source_fingerprint_before_binding"
                        ),
                    },
                    {
                        "source_id": "blocked_docs",
                        "status": "blocked",
                        "bindable": False,
                        "recommended_action": "run_ingestion_job_before_binding",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    specs = [
        HandoffEvidenceSpec(
            id="source_binding_summary",
            category="source-binding",
            path=Path("source-bindings.json"),
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "blocked"
    artifact = report.evidence_artifacts[0]
    assert artifact["status"] == "blocked"
    assert artifact["summary"] == (
        "status=blocked; bindable_sources=1/3; "
        "source_statuses=blocked:1, ready:1, review:1; "
        "recommended_actions=bind_source_from_control_plane:1, "
        "review_source_fingerprint_before_binding:1, "
        "run_ingestion_job_before_binding:1"
    )


def test_provider_handoff_bundle_keeps_missing_phase3_evidence_reviewable(tmp_path):
    specs = [
        HandoffEvidenceSpec(
            id="phase3_seed_retrieval_baseline",
            category="retrieval-evidence",
            path=Path("missing-phase3-baseline.json"),
            required=False,
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "review"
    artifact = report.evidence_artifacts[0]
    assert artifact["present"] is False
    assert artifact["required"] is False
    assert artifact["status"] == "review"
    assert artifact["recommended_action"] == (
        "regenerate_phase3_seed_retrieval_baseline"
    )


def test_provider_handoff_bundle_keeps_missing_phase3_fp_fn_evidence_reviewable(tmp_path):
    specs = [
        HandoffEvidenceSpec(
            id="phase3_fp_fn_review",
            category="retrieval-evidence",
            path=Path("missing-phase3-fp-fn-review.json"),
            required=False,
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "review"
    artifact = report.evidence_artifacts[0]
    assert artifact["present"] is False
    assert artifact["required"] is False
    assert artifact["status"] == "review"
    assert artifact["recommended_action"] == (
        "regenerate_phase3_fp_fn_review"
    )


def test_provider_handoff_bundle_keeps_missing_phase3_readiness_evidence_reviewable(
    tmp_path,
):
    specs = [
        HandoffEvidenceSpec(
            id="phase3_retrieval_promotion_readiness",
            category="retrieval-evidence",
            path=Path("missing-phase3-readiness.json"),
            required=False,
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "review"
    artifact = report.evidence_artifacts[0]
    assert artifact["present"] is False
    assert artifact["required"] is False
    assert artifact["status"] == "review"
    assert artifact["recommended_action"] == (
        "regenerate_phase3_retrieval_promotion_readiness"
    )


def test_provider_handoff_bundle_keeps_missing_phase3_runtime_diagnostics_reviewable(
    tmp_path,
):
    specs = [
        HandoffEvidenceSpec(
            id="phase3_candidate_runtime_diagnostics",
            category="retrieval-evidence",
            path=Path("missing-phase3-runtime-diagnostics.json"),
            required=False,
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "review"
    artifact = report.evidence_artifacts[0]
    assert artifact["present"] is False
    assert artifact["required"] is False
    assert artifact["status"] == "review"
    assert artifact["recommended_action"] == (
        "regenerate_phase3_candidate_runtime_diagnostics"
    )


def test_provider_handoff_bundle_keeps_missing_phase3_latency_resource_diagnostics_reviewable(
    tmp_path,
):
    specs = [
        HandoffEvidenceSpec(
            id="phase3_candidate_latency_resource_diagnostics",
            category="retrieval-evidence",
            path=Path("missing-phase3-latency-resource-diagnostics.json"),
            required=False,
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "review"
    artifact = report.evidence_artifacts[0]
    assert artifact["present"] is False
    assert artifact["required"] is False
    assert artifact["status"] == "review"
    assert artifact["recommended_action"] == (
        "regenerate_phase3_candidate_latency_resource_diagnostics"
    )


def test_provider_handoff_bundle_keeps_missing_phase3_aggregation_relation_negative_control_smoke_reviewable(
    tmp_path,
):
    specs = [
        HandoffEvidenceSpec(
            id="phase3_aggregation_relation_negative_control_smoke",
            category="retrieval-evidence",
            path=Path("missing-phase3-aggregation-relation-negative-control-smoke.json"),
            required=False,
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "review"
    artifact = report.evidence_artifacts[0]
    assert artifact["present"] is False
    assert artifact["required"] is False
    assert artifact["status"] == "review"
    assert artifact["recommended_action"] == (
        "regenerate_phase3_aggregation_relation_negative_control_smoke"
    )


def test_provider_handoff_bundle_keeps_missing_phase3_hybrid_smoke_reviewable(
    tmp_path,
):
    specs = [
        HandoffEvidenceSpec(
            id="phase3_hybrid_cross_case_fp_fn_smoke",
            category="retrieval-evidence",
            path=Path("missing-phase3-hybrid-cross-case-fp-fn-smoke.json"),
            required=False,
        )
    ]

    report = build_provider_handoff_bundle_report(
        base_dir=tmp_path,
        evidence_specs=specs,
    )

    assert report.status == "review"
    artifact = report.evidence_artifacts[0]
    assert artifact["present"] is False
    assert artifact["required"] is False
    assert artifact["status"] == "review"
    assert artifact["recommended_action"] == (
        "regenerate_phase3_hybrid_cross_case_fp_fn_smoke"
    )
