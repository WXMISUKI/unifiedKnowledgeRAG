import json

from app.services.phase6_qdrant_bge_private_network_promotion_readiness import (
    build_phase6_qdrant_bge_private_network_promotion_readiness_report,
    export_phase6_qdrant_bge_private_network_promotion_readiness_report,
)


def test_build_phase6_private_network_promotion_readiness_report_defaults():
    report = build_phase6_qdrant_bge_private_network_promotion_readiness_report()

    assert report.id == "phase6-qdrant-bge-private-network-promotion-readiness-v1"
    assert report.status in {"review", "blocked", "ready"}
    assert report.decision == "keep_runtime_defaults"
    assert report.summary["total_signals"] == 12


def test_export_phase6_private_network_promotion_readiness_report(tmp_path):
    base = tmp_path
    (base / "docs/operations/private-network-promotion").mkdir(parents=True, exist_ok=True)
    (base / "docs/operations/qdrant-vector-store-readiness").mkdir(
        parents=True,
        exist_ok=True,
    )
    (base / "docs/smoke/qdrant-backup-restore").mkdir(parents=True, exist_ok=True)
    (base / "docs/operations/bge-m3-artifact-readiness").mkdir(
        parents=True,
        exist_ok=True,
    )
    (base / "docs/operations/bge-m3-comparison-readiness").mkdir(
        parents=True,
        exist_ok=True,
    )
    (base / "docs/smoke/bge-m3-comparison").mkdir(parents=True, exist_ok=True)
    (base / "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics").mkdir(
        parents=True,
        exist_ok=True,
    )
    (base / "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics").mkdir(
        parents=True,
        exist_ok=True,
    )
    (base / "docs/benchmark/chinese-seed/fp-fn-review").mkdir(parents=True, exist_ok=True)
    (base / "docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration").mkdir(
        parents=True,
        exist_ok=True,
    )
    (base / "docs/operations/deployment-readiness").mkdir(parents=True, exist_ok=True)

    (
        base
        / "docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-review-contract.md"
    ).write_text("# contract\n", encoding="utf-8")

    for file_path in [
        "docs/operations/qdrant-vector-store-readiness/phase6-qdrant-vector-store-readiness.json",
        "docs/smoke/qdrant-backup-restore/phase6-qdrant-backup-restore-smoke.json",
        "docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json",
        "docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-vs-mock-fixture-diagnostics.json",
        "docs/smoke/bge-m3-comparison/phase6-bge-m3-comparison-smoke.json",
        "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/phase3-candidate-runtime-diagnostics.json",
        "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/phase3-candidate-latency-resource-diagnostics.json",
        "docs/benchmark/chinese-seed/fp-fn-review/phase3-fp-fn-review.json",
        "docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration/phase3-hybrid-fusion-threshold-calibration.json",
        "docs/operations/deployment-readiness/deployment-readiness.json",
    ]:
        (base / file_path).write_text(
            json.dumps({"status": "ready", "decision": "keep_runtime_defaults"}),
            encoding="utf-8",
        )

    report = export_phase6_qdrant_bge_private_network_promotion_readiness_report(
        output_dir=base / "out",
        base_dir=base,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))

    assert report.status == "review"
    assert payload["promotion_review_state"] == "review"
    assert "deployed_provider_smoke" in payload["summary"]["open_gate_ids"]
