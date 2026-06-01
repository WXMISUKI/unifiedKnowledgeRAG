import json

from app.services.phase8_live_url_smoke_consistency_check import (
    build_phase8_live_url_smoke_consistency_check_report,
    export_phase8_live_url_smoke_consistency_check_report,
    render_phase8_live_url_smoke_consistency_check_markdown,
)


def test_build_phase8_live_url_smoke_consistency_check_report_ready(tmp_path):
    _write_readiness_report(
        tmp_path,
        status="review",
        live_validation_state="await_live_url_validation",
        decision="keep_runtime_defaults_until_live_url_validation",
        deployed_smoke_present=False,
        deployed_smoke_status="review",
        live_url_present=False,
        open_gate_ids=["deployed_provider_smoke"],
    )
    _write_handoff_bundle(
        tmp_path,
        status="review",
        row_status="review",
        live_validation_state="await_live_url_validation",
        decision="keep_runtime_defaults_until_live_url_validation",
        deployed_smoke_present=False,
        deployed_smoke_status="review",
        live_url_present=False,
        open_gate_count=1,
    )

    report = build_phase8_live_url_smoke_consistency_check_report(base_dir=tmp_path)

    assert report.id == "phase8-live-url-smoke-consistency-check-v1"
    assert report.status == "ready"
    assert report.summary["total_checks"] == 10
    assert report.summary["passed_checks"] == 10
    assert report.summary["failed_checks"] == 0
    assert report.summary["readiness_status"] == "review"
    assert report.summary["bundle_status"] == "review"
    assert report.summary["bundle_row_status"] == "review"


def test_export_phase8_live_url_smoke_consistency_check_report_writes_outputs(tmp_path):
    _write_readiness_report(
        tmp_path,
        status="ready",
        live_validation_state="ready_for_live_url_validation",
        decision="confirm_live_url_validation_evidence",
        deployed_smoke_present=True,
        deployed_smoke_status="ready",
        live_url_present=True,
        open_gate_ids=[],
    )
    _write_handoff_bundle(
        tmp_path,
        status="ready",
        row_status="ready",
        live_validation_state="ready_for_live_url_validation",
        decision="confirm_live_url_validation_evidence",
        deployed_smoke_present=True,
        deployed_smoke_status="ready",
        live_url_present=True,
        open_gate_count=0,
    )

    report = export_phase8_live_url_smoke_consistency_check_report(
        output_dir=tmp_path / "summary",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert report.status == "ready"
    assert payload["id"] == report.id
    assert payload["status"] == report.status
    assert "# Phase 8 Live URL Smoke Consistency Check" in markdown
    assert "| Check | Required | Status | Summary | Recommended Action |" in markdown
    assert render_phase8_live_url_smoke_consistency_check_markdown(report) == markdown


def test_phase8_live_url_smoke_consistency_check_blocks_on_mismatch(tmp_path):
    _write_readiness_report(
        tmp_path,
        status="review",
        live_validation_state="await_live_url_validation",
        decision="keep_runtime_defaults_until_live_url_validation",
        deployed_smoke_present=False,
        deployed_smoke_status="review",
        live_url_present=False,
        open_gate_ids=["deployed_provider_smoke"],
    )
    _write_handoff_bundle(
        tmp_path,
        status="review",
        row_status="ready",
        live_validation_state="ready_for_live_url_validation",
        decision="confirm_live_url_validation_evidence",
        deployed_smoke_present=True,
        deployed_smoke_status="ready",
        live_url_present=True,
        open_gate_count=0,
    )

    report = build_phase8_live_url_smoke_consistency_check_report(base_dir=tmp_path)

    assert report.status == "blocked"
    assert any(check.status == "blocked" for check in report.checks)
    assert "status_alignment" in {check.id for check in report.checks}


def _write_readiness_report(
    base_dir,
    *,
    status: str,
    live_validation_state: str,
    decision: str,
    deployed_smoke_present: bool,
    deployed_smoke_status: str,
    live_url_present: bool,
    open_gate_ids: list[str],
) -> None:
    path = (
        base_dir
        / "docs/operations/live-url-validation/"
        / "phase8-live-url-validation-readiness.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": status,
                "live_validation_state": live_validation_state,
                "decision": decision,
                "summary": {
                    "total_signals": 4,
                    "required_signals": 3,
                    "ready_signals": 3 if status == "ready" else 1,
                    "review_signals": 1 if status != "ready" else 0,
                    "blocked_signals": 0,
                    "deployed_smoke_present": deployed_smoke_present,
                    "deployed_smoke_status": deployed_smoke_status,
                    "live_url_present": live_url_present,
                    "open_gate_ids": open_gate_ids,
                },
                "signals": [],
                "notes": [],
            }
        ),
        encoding="utf-8",
    )


def _write_handoff_bundle(
    base_dir,
    *,
    status: str,
    row_status: str,
    live_validation_state: str,
    decision: str,
    deployed_smoke_present: bool,
    deployed_smoke_status: str,
    live_url_present: bool,
    open_gate_count: int,
) -> None:
    path = base_dir / "docs/integration/provider-handoff/provider-handoff-bundle.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": status,
                "evidence_artifacts": [
                    {
                        "id": "phase8_live_url_validation_readiness",
                        "status": row_status,
                        "summary": (
                            f"status={row_status}; live_validation_state={live_validation_state}; "
                            f"decision={decision}; deployed_smoke_present={deployed_smoke_present}; "
                            f"deployed_smoke_status={deployed_smoke_status}; live_url_present={live_url_present}; "
                            f"open_gate_count={open_gate_count}"
                        ),
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
