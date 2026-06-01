import json

from app.services.phase7_cross_phase_handoff_consistency_smoke import (
    build_phase7_cross_phase_handoff_consistency_smoke_report,
    export_phase7_cross_phase_handoff_consistency_smoke_report,
    render_phase7_cross_phase_handoff_consistency_smoke_markdown,
)


def test_build_phase7_cross_phase_handoff_consistency_smoke_report_defaults():
    report = build_phase7_cross_phase_handoff_consistency_smoke_report()

    assert report.id == "phase7-cross-phase-handoff-consistency-smoke-v1"
    assert report.status in {"ready", "review", "blocked"}
    assert report.summary["total_checks"] >= 1


def test_export_phase7_cross_phase_handoff_consistency_smoke_report(tmp_path):
    readiness = (
        tmp_path
        / "docs/operations/provider-release-readiness/phase7-provider-release-readiness.json"
    )
    readiness.parent.mkdir(parents=True, exist_ok=True)
    readiness.write_text(
        json.dumps(
            {
                "release_state": "ready_for_local_handoff",
                "decision": "keep_runtime_defaults",
                "summary": {
                    "ready_for_local_provider_handoff": True,
                    "ready_for_runtime_default_promotion": False,
                },
            }
        ),
        encoding="utf-8",
    )

    phase2_record = (
        tmp_path
        / "docs/operations/source-format-demand/phase2-parser-expansion-decision-record.md"
    )
    phase2_record.parent.mkdir(parents=True, exist_ok=True)
    phase2_record.write_text("keep_markdown_baseline\n", encoding="utf-8")

    phase3_record = (
        tmp_path
        / "docs/benchmark/chinese-seed/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-record.md"
    )
    phase3_record.parent.mkdir(parents=True, exist_ok=True)
    phase3_record.write_text("keep_runtime_defaults\n", encoding="utf-8")

    phase4_smoke = (
        tmp_path
        / "docs/smoke/evidence-pack-consumption/phase4-caller-consumption-smoke.json"
    )
    phase4_smoke.parent.mkdir(parents=True, exist_ok=True)
    phase4_smoke.write_text(json.dumps({"status": "ready"}), encoding="utf-8")

    phase5_smoke = (
        tmp_path / "docs/smoke/graph-boundary-summary/phase5-graph-boundary-smoke-summary.json"
    )
    phase5_smoke.parent.mkdir(parents=True, exist_ok=True)
    phase5_smoke.write_text(
        json.dumps({"status": "ready", "summary": {"graph_query_planned": True}}),
        encoding="utf-8",
    )

    phase6_field = (
        tmp_path
        / "docs/operations/deployed-field-validation/phase6-deployed-field-validation-readiness.json"
    )
    phase6_field.parent.mkdir(parents=True, exist_ok=True)
    phase6_field.write_text(
        json.dumps({"status": "review", "field_validation_state": "await_live_url"}),
        encoding="utf-8",
    )

    report = export_phase7_cross_phase_handoff_consistency_smoke_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert report.status == "ready"
    assert payload["summary"]["failed_checks"] == 0
    assert "# Phase 7 Cross-Phase Handoff Consistency Smoke" in markdown
    assert render_phase7_cross_phase_handoff_consistency_smoke_markdown(report) == markdown


def test_phase7_cross_phase_handoff_consistency_smoke_blocks_when_readiness_missing(
    tmp_path,
):
    report = build_phase7_cross_phase_handoff_consistency_smoke_report(base_dir=tmp_path)
    assert report.status == "blocked"
    assert report.checks[0].name == "phase7_provider_release_readiness_present"
    assert report.checks[0].passed is False
