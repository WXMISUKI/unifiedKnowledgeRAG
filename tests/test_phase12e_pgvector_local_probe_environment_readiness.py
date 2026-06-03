import json
from pathlib import Path

from app.services.phase12e_pgvector_local_probe_environment_readiness import (
    build_phase12e_pgvector_local_probe_environment_readiness_report,
    export_phase12e_pgvector_local_probe_environment_readiness_report,
    render_phase12e_pgvector_local_probe_environment_readiness_markdown,
)


def test_build_phase12e_pgvector_local_probe_environment_readiness_is_ready_with_local_pack(
    tmp_path,
):
    _seed_local_environment(tmp_path)

    report = build_phase12e_pgvector_local_probe_environment_readiness_report(
        base_dir=tmp_path
    )

    assert report.id == "phase12e-pgvector-local-probe-environment-readiness-v1"
    assert report.status == "ready"
    assert report.decision == "continue_spike"
    assert report.summary["candidate_backend_id"] == "pgvector"
    assert report.summary["optional_dependency_present"] is True
    assert report.summary["phase12d_report_status"] == "review"
    assert report.summary["handoff_bundle_visible"] is True
    assert report.summary["handoff_refresh_visible"] is True
    assert all(family.status == "ready" for family in report.environment_families)
    assert any(
        artifact.id == "optional_dependency_file" and artifact.status == "ready"
        for artifact in report.supporting_artifacts
    )


def test_export_phase12e_pgvector_local_probe_environment_readiness_writes_outputs(
    tmp_path,
):
    _seed_local_environment(tmp_path)

    report = export_phase12e_pgvector_local_probe_environment_readiness_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["summary"]["candidate_backend_id"] == "pgvector"
    assert "# Phase 12e PGVector Local Probe Environment Readiness" in markdown
    assert (
        render_phase12e_pgvector_local_probe_environment_readiness_markdown(report)
        == markdown
    )


def _seed_local_environment(base_dir: Path) -> None:
    _write_text(
        base_dir / "requirements-pgvector.txt",
        "psycopg[binary]==3.2.1\n",
    )
    _write_text(
        base_dir / "docker-compose.pgvector.example.yml",
        "services:\n  pgvector:\n    image: pgvector/pgvector:pg16\n",
    )
    _write_text(
        base_dir / "docker/pgvector/init.sql",
        "CREATE EXTENSION IF NOT EXISTS vector;\n",
    )
    _write_text(
        base_dir / "docs/operations/pgvector-local-probe-environment/runbook.md",
        "# Runbook\n",
    )
    _write_text(
        base_dir / "docs/operations/pgvector-local-probe-environment/config-reference.md",
        "# Config Reference\n",
    )
    _write_text(
        base_dir / ".env.example",
        "PGVECTOR_DATABASE_URL=postgresql://localhost:5433/unifiedKnowledgeRAG\n"
        "PGVECTOR_SCHEMA=unified_knowledge_rag\n"
        "PGVECTOR_TABLE=knowledge_chunks\n"
        "PGVECTOR_INDEX_NAME=knowledge_chunks_embedding_idx\n"
        "PGVECTOR_VECTOR_SIZE=1024\n",
    )
    _write_json(
        base_dir
        / "docs/operations/pgvector-live-probe-readiness/"
        / "phase12d-pgvector-live-probe-readiness.json",
        {
            "status": "review",
            "decision": "continue_spike",
        },
    )
    _write_json(
        base_dir / "docs/integration/provider-handoff/provider-handoff-bundle.json",
        {
            "evidence_artifacts": [
                {"id": "phase12e_pgvector_local_probe_environment_readiness"}
            ]
        },
    )
    _write_json(
        base_dir / "docs/integration/provider-handoff-refresh/provider-handoff-refresh.json",
        {
            "steps": [
                {"id": "phase12e_pgvector_local_probe_environment_readiness"}
            ]
        },
    )


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_json(path: Path, payload: dict[str, object]) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
