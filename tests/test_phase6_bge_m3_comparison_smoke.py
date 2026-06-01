import json

from app.services.phase6_bge_m3_comparison_smoke import (
    build_phase6_bge_m3_comparison_smoke_report,
    export_phase6_bge_m3_comparison_smoke_report,
)


def test_build_phase6_bge_m3_comparison_smoke_report():
    report = build_phase6_bge_m3_comparison_smoke_report()

    assert report.id == "phase6-bge-m3-comparison-smoke-v1"
    assert report.status in {"ready", "review"}
    assert report.decision == "keep_runtime_defaults"
    assert report.summary["total_checks"] == 6


def test_export_phase6_bge_m3_comparison_smoke_report(tmp_path):
    (tmp_path / "docs/operations/bge-m3-comparison-readiness").mkdir(
        parents=True,
        exist_ok=True,
    )
    (tmp_path / "docs/operations/bge-m3-artifact-readiness").mkdir(
        parents=True,
        exist_ok=True,
    )
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
        / "docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-quality-latency-comparison-contract.md"
    ).write_text("# contract\n", encoding="utf-8")
    (
        tmp_path
        / "docs/operations/bge-m3-comparison-readiness/phase6-bge-m3-vs-mock-fixture-diagnostics.json"
    ).write_text("{}", encoding="utf-8")
    (
        tmp_path
        / "docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json"
    ).write_text("{}", encoding="utf-8")
    (
        tmp_path
        / "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/phase3-candidate-runtime-diagnostics.json"
    ).write_text("{}", encoding="utf-8")
    (
        tmp_path
        / "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/phase3-candidate-latency-resource-diagnostics.json"
    ).write_text("{}", encoding="utf-8")
    (tmp_path / "docs/operations/deployment-readiness/deployment-readiness.json").write_text(
        "{}",
        encoding="utf-8",
    )

    report = export_phase6_bge_m3_comparison_smoke_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))

    assert report.status == "ready"
    assert payload["summary"]["passed_checks"] == 6
