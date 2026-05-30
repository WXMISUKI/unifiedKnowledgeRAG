import json

from app.config import Settings
from app.services.deployment_readiness import (
    build_deployment_readiness_report,
    export_deployment_readiness_report,
    render_deployment_readiness_markdown,
)


def test_deployment_readiness_report_summarizes_default_provider():
    report = build_deployment_readiness_report()

    assert report.id == "deployment-readiness-v1"
    assert report.status == "review"
    assert report.provider["provider_id"] == "unifiedKnowledgeProvider"
    assert report.health["status"] == "ok"
    assert report.preflight["bindable"] is True
    assert report.contract_smoke["passed"] is True
    assert report.contract_smoke["summary"]["failed"] == 0
    assert report.runtime_config["rag_retrieval_backend"] == "fixture"
    assert report.runtime_config["embedding_provider"] == "mock"
    assert report.model_artifacts["status"] == "not_configured"
    assert any("mock" in note for note in report.operation_notes)


def test_deployment_readiness_redacts_qdrant_api_key():
    settings = Settings(qdrant_api_key="secret-token")

    report = build_deployment_readiness_report(settings=settings)
    payload = json.dumps(report.runtime_config, ensure_ascii=False)
    markdown = render_deployment_readiness_markdown(report)

    assert report.runtime_config["qdrant_api_key_configured"] is True
    assert "secret-token" not in payload
    assert "secret-token" not in markdown


def test_deployment_readiness_reports_model_artifact_status(tmp_path):
    model_dir = tmp_path / "bge-m3"
    model_dir.mkdir()
    (model_dir / "model-manifest.json").write_text("{}", encoding="utf-8")
    settings = Settings(
        embedding_provider="bge_m3_local",
        embedding_model="BAAI/bge-m3",
        embedding_model_path=model_dir,
    )

    report = build_deployment_readiness_report(settings=settings)

    assert report.model_artifacts == {
        "status": "ready",
        "model_path": str(model_dir),
        "path_exists": True,
        "manifest_exists": True,
    }


def test_export_deployment_readiness_writes_json_and_markdown(tmp_path):
    report = export_deployment_readiness_report(output_dir=tmp_path / "readiness")

    assert report.json_path is not None
    assert report.markdown_path is not None
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == "deployment-readiness-v1"
    assert payload["status"] == report.status
    assert payload["json_path"] == str(report.json_path)
    assert "# Deployment Readiness Report" in markdown
    assert "| Contract Smoke |" in markdown
