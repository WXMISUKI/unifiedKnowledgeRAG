import json
from pathlib import Path

from app.services.phase12c_pgvector_candidate_backend_readiness import (
    build_phase12c_pgvector_candidate_backend_readiness_report,
    export_phase12c_pgvector_candidate_backend_readiness_report,
    render_phase12c_pgvector_candidate_backend_readiness_markdown,
)


def test_build_phase12c_pgvector_candidate_backend_readiness_defaults_to_blocked_without_configuration(
    monkeypatch,
):
    for env_name in [
        "PGVECTOR_DATABASE_URL",
        "PGVECTOR_SCHEMA",
        "PGVECTOR_TABLE",
        "PGVECTOR_INDEX_NAME",
        "PGVECTOR_VECTOR_SIZE",
    ]:
        monkeypatch.delenv(env_name, raising=False)

    report = build_phase12c_pgvector_candidate_backend_readiness_report()

    assert report.id == "phase12c-pgvector-candidate-backend-readiness-v1"
    assert report.status == "blocked"
    assert report.decision == "keep_current_default"
    assert report.summary["strategy_verdict"] == "continue_provider_first_with_candidate_backends"
    assert report.summary["pgvector_database_url_present"] is False
    assert report.summary["candidate_backend_id"] == "pgvector"
    assert any(signal.id == "pgvector_connection_posture" for signal in report.signals)
    assert any(family.id == "pgvector_configuration_gate" for family in report.candidate_families)


def test_build_phase12c_pgvector_candidate_backend_readiness_is_review_when_configured(
    monkeypatch,
):
    monkeypatch.setenv(
        "PGVECTOR_DATABASE_URL",
        "postgresql://user:password@localhost:5432/unifiedKnowledgeRAG",
    )
    monkeypatch.setenv("PGVECTOR_SCHEMA", "public")
    monkeypatch.setenv("PGVECTOR_TABLE", "knowledge_chunks")
    monkeypatch.setenv("PGVECTOR_INDEX_NAME", "knowledge_chunks_embedding_idx")
    monkeypatch.setenv("PGVECTOR_VECTOR_SIZE", "1024")

    report = build_phase12c_pgvector_candidate_backend_readiness_report(
        base_dir=Path(__file__).resolve().parents[1]
    )

    assert report.status == "review"
    assert report.decision == "continue_spike"
    assert report.summary["pgvector_database_url_present"] is True
    assert report.summary["pgvector_schema"] == "public"
    assert report.summary["pgvector_table"] == "knowledge_chunks"
    assert report.summary["pgvector_index_name"] == "knowledge_chunks_embedding_idx"
    assert report.summary["pgvector_vector_size"] == 1024
    assert report.summary["review_signals"] >= 1


def test_export_phase12c_pgvector_candidate_backend_readiness_writes_outputs(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setenv(
        "PGVECTOR_DATABASE_URL",
        "postgresql://user:password@localhost:5432/unifiedKnowledgeRAG",
    )
    monkeypatch.setenv("PGVECTOR_SCHEMA", "public")
    monkeypatch.setenv("PGVECTOR_TABLE", "knowledge_chunks")
    monkeypatch.setenv("PGVECTOR_INDEX_NAME", "knowledge_chunks_embedding_idx")
    monkeypatch.setenv("PGVECTOR_VECTOR_SIZE", "1024")

    report = export_phase12c_pgvector_candidate_backend_readiness_report(
        output_dir=tmp_path / "out",
        base_dir=Path(__file__).resolve().parents[1],
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["summary"]["strategy_verdict"] == "continue_provider_first_with_candidate_backends"
    assert payload["summary"]["candidate_backend_id"] == "pgvector"
    assert "# Phase 12c PGVector Candidate Backend Readiness" in markdown
    assert render_phase12c_pgvector_candidate_backend_readiness_markdown(report) == markdown
