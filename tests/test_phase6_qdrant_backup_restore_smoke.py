import json

from app.services.phase6_qdrant_backup_restore_smoke import (
    build_phase6_qdrant_backup_restore_smoke_report,
    export_phase6_qdrant_backup_restore_smoke_report,
)


def test_build_phase6_qdrant_backup_restore_smoke_report():
    report = build_phase6_qdrant_backup_restore_smoke_report()

    assert report.id == "phase6-qdrant-backup-restore-smoke-v1"
    assert report.status in {"ready", "review"}
    assert report.decision == "keep_runtime_defaults"
    assert report.summary["total_checks"] == 4


def test_export_phase6_qdrant_backup_restore_smoke_report(tmp_path):
    (tmp_path / "docs/operations/deployment-readiness").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs/operations/reindex-readiness").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs/operations/qdrant-vector-store-readiness").mkdir(
        parents=True,
        exist_ok=True,
    )
    (tmp_path / "docs/operations/qdrant-vector-store-readiness/phase6-qdrant-deployment-backup-recovery-contract.md").write_text(
        "# contract\n",
        encoding="utf-8",
    )
    (tmp_path / "docs/operations/qdrant-vector-store-readiness/phase6-qdrant-vector-store-readiness.json").write_text(
        "{}",
        encoding="utf-8",
    )
    (tmp_path / "docs/operations/deployment-readiness/deployment-readiness.json").write_text(
        "{}",
        encoding="utf-8",
    )
    (tmp_path / "docs/operations/reindex-readiness/reindex-readiness.json").write_text(
        "{}",
        encoding="utf-8",
    )

    report = export_phase6_qdrant_backup_restore_smoke_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))

    assert report.status == "ready"
    assert payload["summary"]["passed_checks"] == 4
