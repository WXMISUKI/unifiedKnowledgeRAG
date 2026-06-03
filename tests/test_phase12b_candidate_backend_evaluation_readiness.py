import json

from app.services.phase12b_candidate_backend_evaluation_readiness import (
    build_phase12b_candidate_backend_evaluation_readiness_report,
    export_phase12b_candidate_backend_evaluation_readiness_report,
    render_phase12b_candidate_backend_evaluation_readiness_markdown,
)


def test_build_phase12b_candidate_backend_readiness_defaults_to_blocked_without_inputs(
    tmp_path,
):
    report = build_phase12b_candidate_backend_evaluation_readiness_report(base_dir=tmp_path)

    assert report.id == "phase12b-candidate-backend-evaluation-readiness-v1"
    assert report.status == "blocked"
    assert report.decision == "keep_current_default"
    assert report.summary["strategy_verdict"] == "continue_provider_first_with_candidate_backends"
    assert report.summary["reference_only_candidates"] == [
        "Haystack",
        "RAGFlow",
        "LightRAG",
        "pgvector",
    ]
    assert any(family.status == "reference_only" for family in report.candidate_families)
    assert any(family.status == "blocked" for family in report.candidate_families)


def test_export_phase12b_candidate_backend_readiness_writes_outputs(tmp_path):
    _write_minimal_inputs(tmp_path)

    report = export_phase12b_candidate_backend_evaluation_readiness_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["summary"]["strategy_verdict"] == "continue_provider_first_with_candidate_backends"
    assert "# Phase 12b Candidate Backend Evaluation Readiness" in markdown
    assert render_phase12b_candidate_backend_evaluation_readiness_markdown(report) == markdown


def _write_minimal_inputs(base_dir) -> None:
    for file_path, payload in [
        (
            "docs/integration/myprivateagent-local-rag-integration-hardening/"
            "phase12-local-rag-integration-hardening-profile.json",
            {
                "status": "review",
                "hardening_state": "ready_for_local_rag_hardening_review",
                "summary": {"open_gate_ids": ["provider_handoff_bundle"]},
            },
        ),
        (
            "docs/integration/myprivateagent-local-provider-integration/"
            "phase11-local-provider-integration-profile.json",
            {
                "status": "ready",
                "integration_state": "ready_for_local_provider_integration",
                "summary": {"open_gate_ids": []},
            },
        ),
        (
            "docs/smoke/provider-contract/provider-contract-smoke.json",
            {"passed": True, "summary": {"passed": 4, "total": 4}},
        ),
        (
            "docs/integration/provider-handoff/provider-handoff-bundle.json",
            {"status": "ready", "evidence_artifacts": 12},
        ),
        (
            "docs/smoke/myprivateagent-local-provider-integration/"
            "phase11-source-binding-preview-smoke.json",
            {"status": "ready", "summary": {"passed_checks": 4, "total_checks": 4}},
        ),
        (
            "docs/smoke/myprivateagent-local-provider-integration/"
            "phase11-rag-retrieve-consumption-smoke.json",
            {"status": "ready", "summary": {"passed_checks": 3, "total_checks": 3}},
        ),
        (
            "docs/operations/deployment-readiness/deployment-readiness.json",
            {"status": "review", "runtime_config": {"rag_retrieval_backend": "fixture"}},
        ),
        (
            "docs/operations/reindex-readiness/reindex-readiness.json",
            {"status": "ready", "retrieval_backend": "fixture"},
        ),
        (
            "docs/benchmark/chinese-seed/retrieval-promotion-readiness/"
            "phase3-retrieval-promotion-readiness.json",
            {"status": "review", "summary": {"decision": "keep_runtime_defaults"}},
        ),
        (
            "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/"
            "phase3-candidate-runtime-diagnostics.json",
            {"status": "review", "summary": {"decision": "keep_runtime_defaults"}},
        ),
        (
            "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/"
            "phase3-candidate-latency-resource-diagnostics.json",
            {
                "status": "review",
                "summary": {"avg_latency_ms": 120.5, "decision": "keep_runtime_defaults"},
            },
        ),
        (
            "docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json",
            {"status": "review", "summary": {"artifact_state": "ready"}},
        ),
        (
            "docs/operations/qdrant-vector-store-readiness/"
            "phase6-qdrant-vector-store-readiness.json",
            {"status": "review", "summary": {"decision": "keep_runtime_defaults"}},
        ),
        (
            "docs/operations/private-network-promotion/"
            "phase6-qdrant-bge-private-network-promotion-readiness.json",
            {"status": "review", "summary": {"decision": "keep_runtime_defaults"}},
        ),
        (
            "docs/operations/deployed-field-validation/"
            "phase6-deployed-field-validation-readiness.json",
            {"status": "review", "summary": {"decision": "keep_runtime_defaults"}},
        ),
    ]:
        path = base_dir / file_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload), encoding="utf-8")
