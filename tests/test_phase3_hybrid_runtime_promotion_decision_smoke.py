import json

from app.services.phase3_hybrid_runtime_promotion_decision_smoke import (
    build_phase3_hybrid_runtime_promotion_decision_smoke_report,
    export_phase3_hybrid_runtime_promotion_decision_smoke_report,
)


def test_build_phase3_hybrid_runtime_promotion_decision_smoke_report():
    report = build_phase3_hybrid_runtime_promotion_decision_smoke_report()

    assert report.id == "phase3-hybrid-runtime-promotion-decision-smoke-v1"
    assert report.status in {"ready", "review"}
    assert report.decision == "keep_runtime_defaults"
    assert report.summary["total_checks"] == 16


def test_export_phase3_hybrid_runtime_promotion_decision_smoke_report(tmp_path):
    (tmp_path / "docs/benchmark/chinese-seed/hybrid-runtime-promotion").mkdir(
        parents=True,
        exist_ok=True,
    )
    (
        tmp_path
        / "docs/benchmark/chinese-seed/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-contract.md"
    ).write_text("# contract\n", encoding="utf-8")

    for file_path in [
        "docs/benchmark/chinese-seed/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-readiness.json",
        "docs/benchmark/chinese-seed/retrieval-promotion-readiness/phase3-retrieval-promotion-readiness.json",
        "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/phase3-candidate-runtime-diagnostics.json",
        "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/phase3-candidate-latency-resource-diagnostics.json",
        "docs/benchmark/chinese-seed/hybrid-fusion-threshold-calibration/phase3-hybrid-fusion-threshold-calibration.json",
        "docs/smoke/hybrid-cross-case-fp-fn/phase3-hybrid-cross-case-fp-fn-smoke.json",
        "docs/smoke/aggregation-relation-negative-control/phase3-aggregation-relation-negative-control-smoke.json",
        "docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json",
        "docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-vs-mock-fixture-diagnostics.json",
        "docs/smoke/bge-m3-comparison/phase6-bge-m3-comparison-smoke.json",
        "docs/operations/qdrant-vector-store-readiness/phase6-qdrant-vector-store-readiness.json",
        "docs/smoke/qdrant-backup-restore/phase6-qdrant-backup-restore-smoke.json",
        "docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-readiness.json",
        "docs/smoke/private-network-promotion/phase6-qdrant-bge-private-network-promotion-smoke.json",
    ]:
        path = tmp_path / file_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "status": "ready",
                    "decision": "keep_runtime_defaults",
                    "review_state": "review",
                    "summary": {"open_gate_ids": ["deployed_provider_smoke"]},
                }
            ),
            encoding="utf-8",
        )

    report = export_phase3_hybrid_runtime_promotion_decision_smoke_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))

    assert report.status == "ready"
    assert payload["summary"]["passed_checks"] == 16
