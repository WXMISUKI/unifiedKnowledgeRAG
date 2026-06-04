import json
from pathlib import Path

from app.services.phase12f_pgvector_local_live_probe_execution_readiness import (
    build_phase12f_pgvector_local_live_probe_execution_readiness_report,
    export_phase12f_pgvector_local_live_probe_execution_readiness_report,
    render_phase12f_pgvector_local_live_probe_execution_readiness_markdown,
)


def test_build_phase12f_pgvector_local_live_probe_execution_readiness_is_review_with_blocked_probe(
    tmp_path,
):
    _seed_local_execution_evidence(tmp_path)

    report = build_phase12f_pgvector_local_live_probe_execution_readiness_report(
        base_dir=tmp_path
    )

    assert report.id == "phase12f-pgvector-local-live-probe-execution-readiness-v1"
    assert report.status == "review"
    assert report.decision == "continue_spike"
    assert report.summary["candidate_backend_id"] == "pgvector"
    assert report.summary["phase12e_environment_status"] == "ready"
    assert report.summary["phase12d_live_probe_status"] == "blocked"
    assert report.summary["execution_ready"] is True
    assert report.summary["rerun_required"] is True
    assert any(family.status == "ready" for family in report.execution_families)
    assert any(
        artifact.id == "phase12d_live_probe_readiness_report" and artifact.status == "ready"
        for artifact in report.supporting_artifacts
    )


def test_export_phase12f_pgvector_local_live_probe_execution_readiness_writes_outputs(
    tmp_path,
):
    _seed_local_execution_evidence(tmp_path)

    report = export_phase12f_pgvector_local_live_probe_execution_readiness_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["summary"]["phase12d_live_probe_status"] == "blocked"
    assert "# Phase 12f PGVector Local Live Probe Execution Readiness" in markdown
    assert (
        render_phase12f_pgvector_local_live_probe_execution_readiness_markdown(report)
        == markdown
    )


def _seed_local_execution_evidence(base_dir: Path) -> None:
    _write_text(
        base_dir / "docs/operations/pgvector-local-live-probe-execution/runbook.md",
        "# Runbook\n",
    )
    _write_json(
        base_dir
        / "docs/operations/pgvector-local-probe-environment/"
        / "phase12e-pgvector-local-probe-environment-readiness.json",
        {
            "status": "ready",
            "decision": "continue_spike",
        },
    )
    _write_json(
        base_dir
        / "docs/operations/pgvector-live-probe-readiness/"
        / "phase12d-pgvector-live-probe-readiness.json",
        {
            "status": "blocked",
            "decision": "keep_current_default",
            "summary": {
                "pgvector_connection_status": "blocked",
            },
        },
    )
    _write_json(
        base_dir / "docs/integration/provider-handoff/provider-handoff-bundle.json",
        {
            "evidence_artifacts": [
                {
                    "id": "phase12f_pgvector_local_live_probe_execution_readiness",
                }
            ]
        },
    )
    _write_json(
        base_dir / "docs/integration/provider-handoff-refresh/provider-handoff-refresh.json",
        {
            "steps": [
                {
                    "id": "phase12f_pgvector_local_live_probe_execution_readiness",
                }
            ]
        },
    )


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_json(path: Path, payload: dict[str, object]) -> None:
    _write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
