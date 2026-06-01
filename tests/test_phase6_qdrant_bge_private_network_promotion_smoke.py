import json

from app.services.phase6_qdrant_bge_private_network_promotion_smoke import (
    build_phase6_qdrant_bge_private_network_promotion_smoke_report,
    export_phase6_qdrant_bge_private_network_promotion_smoke_report,
)


def test_build_phase6_private_network_promotion_smoke_report():
    report = build_phase6_qdrant_bge_private_network_promotion_smoke_report()

    assert report.id == "phase6-qdrant-bge-private-network-promotion-smoke-v1"
    assert report.status in {"ready", "review"}
    assert report.decision == "keep_runtime_defaults"
    assert report.summary["total_checks"] == 10


def test_export_phase6_private_network_promotion_smoke_report(tmp_path):
    (tmp_path / "docs/operations/private-network-promotion").mkdir(
        parents=True,
        exist_ok=True,
    )
    (tmp_path / "docs/operations/qdrant-vector-store-readiness").mkdir(
        parents=True,
        exist_ok=True,
    )
    (tmp_path / "docs/smoke/qdrant-backup-restore").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs/operations/bge-m3-artifact-readiness").mkdir(
        parents=True,
        exist_ok=True,
    )
    (tmp_path / "docs/operations/bge-m3-comparison-readiness").mkdir(
        parents=True,
        exist_ok=True,
    )
    (tmp_path / "docs/smoke/bge-m3-comparison").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics").mkdir(
        parents=True,
        exist_ok=True,
    )
    (tmp_path / "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics").mkdir(
        parents=True,
        exist_ok=True,
    )
    (tmp_path / "docs/operations/deployment-readiness").mkdir(parents=True, exist_ok=True)

    (
        tmp_path
        / "docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-review-contract.md"
    ).write_text("# contract\n", encoding="utf-8")

    for file_path in [
        "docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-readiness.json",
        "docs/operations/qdrant-vector-store-readiness/phase6-qdrant-vector-store-readiness.json",
        "docs/smoke/qdrant-backup-restore/phase6-qdrant-backup-restore-smoke.json",
        "docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json",
        "docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-vs-mock-fixture-diagnostics.json",
        "docs/smoke/bge-m3-comparison/phase6-bge-m3-comparison-smoke.json",
        "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/phase3-candidate-runtime-diagnostics.json",
        "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/phase3-candidate-latency-resource-diagnostics.json",
        "docs/operations/deployment-readiness/deployment-readiness.json",
    ]:
        (tmp_path / file_path).write_text("{}", encoding="utf-8")

    report = export_phase6_qdrant_bge_private_network_promotion_smoke_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))

    assert report.status == "ready"
    assert payload["summary"]["passed_checks"] == 10
