import json
from pathlib import Path

from app.config import Settings
from app.services.phase6_bge_m3_artifact_readiness import (
    build_phase6_bge_m3_artifact_readiness_report,
    export_phase6_bge_m3_artifact_readiness_report,
    render_phase6_bge_m3_artifact_readiness_markdown,
)


def test_build_phase6_bge_m3_artifact_readiness_report_summarizes_current_evidence():
    report = build_phase6_bge_m3_artifact_readiness_report()

    assert report.id == "phase6-bge-m3-artifact-readiness-v1"
    assert report.status == "review"
    assert report.decision == "keep_runtime_defaults"
    assert report.summary["total_signals"] == 6
    assert report.summary["review_signals"] >= 1
    assert "model_path_and_manifest_presence" in report.summary["open_signal_ids"]
    assert report.artifact["deployment_readiness_status"] in {"review", "ready", "missing"}


def test_export_phase6_bge_m3_artifact_readiness_report_writes_artifacts(tmp_path):
    model_dir = tmp_path / "models" / "bge-m3"
    model_dir.mkdir(parents=True, exist_ok=True)
    for file_name in (
        "config.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "sentencepiece.bpe.model",
        "model.safetensors",
    ):
        (model_dir / file_name).write_text("fixture", encoding="utf-8")

    manifest = {
        "repo_id": "BAAI/bge-m3",
        "source": "huggingface",
        "local_files_only": True,
        "validation": {
            "required_files": [
                "config.json",
                "tokenizer.json",
                "tokenizer_config.json",
                "sentencepiece.bpe.model",
            ],
            "weight_files": ["model.safetensors"],
            "file_count": 5,
            "checksums": {
                "config.json": "a" * 64,
                "tokenizer.json": "b" * 64,
                "tokenizer_config.json": "c" * 64,
                "sentencepiece.bpe.model": "d" * 64,
                "model.safetensors": "e" * 64,
            },
            "checksum_algorithm": "sha256",
        },
    }
    (model_dir / "model-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    deployment_dir = tmp_path / "docs" / "operations" / "deployment-readiness"
    deployment_dir.mkdir(parents=True, exist_ok=True)
    deployment_dir.joinpath("deployment-readiness.json").write_text(
        json.dumps(
            {
                "status": "review",
                "runtime_config": {
                    "embedding_provider": "bge_m3_local",
                    "embedding_model": "BAAI/bge-m3",
                    "embedding_local_files_only": True,
                },
                "model_artifacts": {
                    "model_path": str(model_dir),
                    "status": "ready",
                    "path_exists": True,
                    "manifest_exists": True,
                },
            }
        ),
        encoding="utf-8",
    )
    settings = Settings(
        embedding_provider="bge_m3_local",
        embedding_model="BAAI/bge-m3",
        embedding_model_path=model_dir,
        embedding_local_files_only=True,
    )

    report = export_phase6_bge_m3_artifact_readiness_report(
        output_dir=tmp_path / "ops-readiness",
        base_dir=tmp_path,
        settings=settings,
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert report.status == "ready"
    assert payload["artifact"]["checksum_coverage_count"] == 5
    assert payload["artifact"]["checksum_target_count"] == 5
    assert payload["artifact"]["checksum_algorithm"] == "sha256"
    assert "# Phase 6 BGE-M3 Artifact Readiness" in markdown
    assert render_phase6_bge_m3_artifact_readiness_markdown(report) == markdown
