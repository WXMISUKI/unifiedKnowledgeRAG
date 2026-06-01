import json

from app.services.phase6_deployed_handoff_consistency_smoke import (
    build_phase6_deployed_handoff_consistency_smoke_report,
    export_phase6_deployed_handoff_consistency_smoke_report,
    render_phase6_deployed_handoff_consistency_smoke_markdown,
)


def test_build_phase6_deployed_handoff_consistency_smoke_report_summarizes_alignment(
    tmp_path,
):
    _write_readiness_report(
        tmp_path,
        status="review",
        field_validation_state="await_live_url",
        decision="keep_local_review_until_deployed_smoke",
        live_url_present=False,
        open_gate_ids=["deployed_provider_smoke"],
    )
    _write_handoff_bundle(
        tmp_path,
        status="review",
        row_status="review",
        field_validation_state="await_live_url",
        decision="keep_local_review_until_deployed_smoke",
        live_url_present=False,
        open_gate_count=1,
    )

    report = build_phase6_deployed_handoff_consistency_smoke_report(base_dir=tmp_path)

    assert report.id == "phase6-deployed-handoff-consistency-smoke-v1"
    assert report.status == "ready"
    assert report.decision == "keep_runtime_defaults"
    assert report.summary["total_checks"] == 8
    assert report.summary["passed_checks"] == 8
    assert report.summary["failed_checks"] == 0
    assert report.summary["readiness_status"] == "review"
    assert report.summary["bundle_status"] == "review"
    assert report.summary["bundle_row_status"] == "review"
    assert report.summary["field_validation_state"] == "await_live_url"
    assert report.summary["live_url_present"] is False
    assert report.summary["open_gate_count"] == 1


def test_export_phase6_deployed_handoff_consistency_smoke_report_writes_outputs(
    tmp_path,
):
    _write_readiness_report(
        tmp_path,
        status="ready",
        field_validation_state="ready_for_live_validation",
        decision="confirm_deployed_field_validation",
        live_url_present=True,
        open_gate_ids=[],
    )
    _write_handoff_bundle(
        tmp_path,
        status="ready",
        row_status="ready",
        field_validation_state="ready_for_live_validation",
        decision="confirm_deployed_field_validation",
        live_url_present=True,
        open_gate_count=0,
    )

    report = export_phase6_deployed_handoff_consistency_smoke_report(
        output_dir=tmp_path / "summary",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert report.status == "ready"
    assert payload["id"] == report.id
    assert payload["status"] == report.status
    assert "# Phase 6 Deployed Handoff Consistency Smoke" in markdown
    assert "| Check | Required | Status | Summary | Recommended Action |" in markdown
    assert render_phase6_deployed_handoff_consistency_smoke_markdown(report) == markdown


def test_deployed_handoff_consistency_smoke_blocks_on_bundle_mismatch(tmp_path):
    _write_readiness_report(
        tmp_path,
        status="review",
        field_validation_state="await_live_url",
        decision="keep_local_review_until_deployed_smoke",
        live_url_present=False,
        open_gate_ids=["deployed_provider_smoke"],
    )
    _write_handoff_bundle(
        tmp_path,
        status="review",
        row_status="ready",
        field_validation_state="ready_for_live_validation",
        decision="confirm_deployed_field_validation",
        live_url_present=True,
        open_gate_count=0,
    )

    report = build_phase6_deployed_handoff_consistency_smoke_report(base_dir=tmp_path)

    assert report.status == "blocked"
    assert any(check.status == "blocked" for check in report.checks)
    assert "status_alignment" in {check.id for check in report.checks}


def _write_readiness_report(
    base_dir,
    *,
    status: str,
    field_validation_state: str,
    decision: str,
    live_url_present: bool,
    open_gate_ids: list[str],
) -> None:
    path = (
        base_dir
        / "docs/operations/deployed-field-validation/"
        / "phase6-deployed-field-validation-readiness.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": status,
                "field_validation_state": field_validation_state,
                "decision": decision,
                "summary": {
                    "total_signals": 4,
                    "required_signals": 3,
                    "ready_signals": 3 if status == "ready" else 1,
                    "review_signals": 1 if status != "ready" else 0,
                    "blocked_signals": 0,
                    "open_gate_ids": open_gate_ids,
                    "live_url_present": live_url_present,
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
    field_validation_state: str,
    decision: str,
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
                        "id": "phase6_deployed_field_validation_readiness",
                        "status": row_status,
                        "summary": (
                            f"status={row_status}; field_validation_state={field_validation_state}; "
                            f"decision={decision}; live_url_present={live_url_present}; "
                            f"open_gate_count={open_gate_count}"
                        ),
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
