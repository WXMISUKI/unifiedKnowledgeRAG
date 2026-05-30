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
