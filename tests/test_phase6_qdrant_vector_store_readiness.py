import json

from app.services.phase6_qdrant_vector_store_readiness import (
    build_phase6_qdrant_vector_store_readiness_report,
    export_phase6_qdrant_vector_store_readiness_report,
    render_phase6_qdrant_vector_store_readiness_markdown,
)


def test_build_phase6_qdrant_vector_store_readiness_report_defaults_to_review():
    report = build_phase6_qdrant_vector_store_readiness_report()

    assert report.id == "phase6-qdrant-vector-store-readiness-v1"
    assert report.status == "review"
    assert report.decision == "keep_runtime_defaults"
    assert report.summary["total_signals"] == 6
    assert report.summary["review_signals"] >= 1
    assert "deployment_uses_qdrant_backend" in report.open_signal_ids


def test_export_phase6_qdrant_vector_store_readiness_report_writes_outputs(tmp_path):
    ops_dir = tmp_path / "docs" / "operations"
    deployment_dir = ops_dir / "deployment-readiness"
    reindex_dir = ops_dir / "reindex-readiness"
    qdrant_dir = ops_dir / "qdrant-vector-store-readiness"
    deployment_dir.mkdir(parents=True, exist_ok=True)
    reindex_dir.mkdir(parents=True, exist_ok=True)
    qdrant_dir.mkdir(parents=True, exist_ok=True)

    deployment_dir.joinpath("deployment-readiness.json").write_text(
        json.dumps(
            {
                "status": "ready",
                "runtime_config": {
                    "rag_retrieval_backend": "qdrant",
                    "embedding_provider": "bge_m3_local",
                    "qdrant_url": "http://127.0.0.1:6333",
                    "qdrant_collection": "knowledge_chunks",
                },
            }
        ),
        encoding="utf-8",
    )
    reindex_dir.joinpath("reindex-readiness.json").write_text(
        json.dumps({"status": "ready", "retrieval_backend": "qdrant", "sources": []}),
        encoding="utf-8",
    )
    qdrant_dir.joinpath("phase6-qdrant-deployment-backup-recovery-contract.md").write_text(
        "# contract\n",
        encoding="utf-8",
    )
    (tmp_path / "docs/benchmark/chinese-seed/retrieval-candidates").mkdir(
        parents=True,
        exist_ok=True,
    )
    (tmp_path / "docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-smoke.json").write_text(
        json.dumps(
            {
                "report": {
                    "summary": {
                        "total_cases": 10,
                        "hit_rate": 0.9,
                        "citation_match_rate": 0.9,
                        "empty_handling_rate": 0.9,
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    report = export_phase6_qdrant_vector_store_readiness_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert report.status == "ready"
    assert payload["summary"]["ready_signals"] == payload["summary"]["total_signals"]
    assert "# Phase 6 Qdrant Vector Store Readiness" in markdown
    assert render_phase6_qdrant_vector_store_readiness_markdown(report) == markdown
