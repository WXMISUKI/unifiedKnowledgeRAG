import json

from app.services.phase6_bge_m3_vs_mock_fixture_diagnostics import (
    build_phase6_bge_m3_vs_mock_fixture_diagnostics_report,
    export_phase6_bge_m3_vs_mock_fixture_diagnostics_report,
    render_phase6_bge_m3_vs_mock_fixture_diagnostics_markdown,
)


def test_build_phase6_bge_m3_vs_mock_fixture_diagnostics_report():
    report = build_phase6_bge_m3_vs_mock_fixture_diagnostics_report()

    assert report.id == "phase6-bge-m3-vs-mock-fixture-diagnostics-v1"
    assert report.status in {"review", "blocked", "ready"}
    assert report.decision == "keep_runtime_defaults"
    assert report.summary["total_signals"] == 7


def test_export_phase6_bge_m3_vs_mock_fixture_diagnostics_report(tmp_path):
    base = tmp_path
    (base / "docs/benchmark/chinese-seed/retrieval-candidates").mkdir(
        parents=True,
        exist_ok=True,
    )
    (base / "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics").mkdir(
        parents=True,
        exist_ok=True,
    )
    (base / "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics").mkdir(
        parents=True,
        exist_ok=True,
    )
    (base / "docs/operations/bge-m3-artifact-readiness").mkdir(parents=True, exist_ok=True)
    (base / "docs/operations/deployment-readiness").mkdir(parents=True, exist_ok=True)

    baseline = {
        "report": {
            "summary": {
                "total_cases": 2,
                "hit_rate": 0.5,
                "citation_match_rate": 0.5,
                "empty_handling_rate": 0.5,
            },
            "cases": [
                {"id": "a", "latency_ms": 100.0},
                {"id": "b", "latency_ms": 200.0},
            ],
        }
    }
    candidate = {
        "report": {
            "summary": {
                "total_cases": 2,
                "hit_rate": 0.6,
                "citation_match_rate": 0.6,
                "empty_handling_rate": 0.6,
            },
            "cases": [
                {"id": "c", "latency_ms": 120.0},
                {"id": "d", "latency_ms": 220.0},
            ],
        }
    }
    (base / "docs/benchmark/chinese-seed/retrieval-candidates/fixture-chinese-seed-baseline.json").write_text(
        json.dumps(baseline),
        encoding="utf-8",
    )
    (base / "docs/benchmark/chinese-seed/retrieval-candidates/qdrant-bge-m3-smoke.json").write_text(
        json.dumps(candidate),
        encoding="utf-8",
    )
    (base / "docs/benchmark/chinese-seed/retrieval-latency-resource-diagnostics/phase3-candidate-latency-resource-diagnostics.json").write_text(
        json.dumps({"status": "review"}),
        encoding="utf-8",
    )
    (base / "docs/benchmark/chinese-seed/retrieval-runtime-diagnostics/phase3-candidate-runtime-diagnostics.json").write_text(
        json.dumps({"status": "review"}),
        encoding="utf-8",
    )
    (base / "docs/operations/bge-m3-artifact-readiness/phase6-bge-m3-artifact-readiness.json").write_text(
        json.dumps({"status": "ready"}),
        encoding="utf-8",
    )
    (base / "docs/operations/deployment-readiness/deployment-readiness.json").write_text(
        json.dumps({"status": "review"}),
        encoding="utf-8",
    )

    report = export_phase6_bge_m3_vs_mock_fixture_diagnostics_report(
        output_dir=base / "out",
        base_dir=base,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["quality_delta"]["hit_rate_delta"] == 0.1
    assert "# Phase 6 BGE-M3 vs Mock/Fixture Diagnostics" in markdown
    assert render_phase6_bge_m3_vs_mock_fixture_diagnostics_markdown(report) == markdown
