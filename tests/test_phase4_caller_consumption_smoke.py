import json
from pathlib import Path

from app.services.phase4_caller_consumption_smoke import (
    run_phase4_caller_consumption_smoke,
    export_phase4_caller_consumption_smoke_report,
    render_phase4_caller_consumption_smoke_markdown,
)


def test_run_phase4_caller_consumption_smoke_summarizes_current_evidence():
    report = run_phase4_caller_consumption_smoke()

    assert report.id == "phase4-caller-consumption-smoke-v1"
    assert report.status == "ready"
    assert Path(report.contract_path).as_posix().endswith(
        "docs/benchmark/chinese-seed/evidence-pack-consumption-contract/"
        "phase4-evidence-pack-consumption-contract.md"
    )

    summary = report.summary
    assert summary["total"] == 3
    assert summary["passed"] == 3
    assert summary["failed"] == 0
    assert summary["answerable_checks"] == 1
    assert summary["insufficient_checks"] == 1
    assert summary["contract_doc_present"] == 1

    checks = {check.name: check for check in report.checks}
    assert checks["caller_allowlist_rule"].passed is True
    assert checks["caller_allowlist_rule"].details["allowed_citations"] == [
        "refund_policy_2026#section-3",
        "logistics_2026#section-2",
    ]
    assert checks["caller_fail_closed_rule"].passed is True
    assert checks["caller_fail_closed_rule"].details["status"] == "insufficient_evidence"
    assert checks["caller_contract_artifact"].passed is True


def test_export_phase4_caller_consumption_smoke_report_writes_json_and_markdown(
    tmp_path,
):
    report = export_phase4_caller_consumption_smoke_report(
        output_dir=tmp_path / "smoke",
    )

    assert report.json_path == (
        tmp_path / "smoke" / "phase4-caller-consumption-smoke.json"
    )
    assert report.markdown_path == (
        tmp_path / "smoke" / "phase4-caller-consumption-smoke.md"
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["status"] == report.status
    assert payload["json_path"] == str(report.json_path)
    assert "# Phase 4 Caller Consumption Smoke Report" in markdown
    assert "| Check | Scenario | Status | Details |" in markdown
    assert render_phase4_caller_consumption_smoke_markdown(report) == markdown


def test_phase4_caller_consumption_smoke_blocks_when_contract_doc_missing(
    tmp_path,
):
    report = run_phase4_caller_consumption_smoke(base_dir=tmp_path)

    checks = {check.name: check for check in report.checks}
    assert report.status == "blocked"
    assert checks["caller_allowlist_rule"].passed is True
    assert checks["caller_fail_closed_rule"].passed is True
    assert checks["caller_contract_artifact"].passed is False
    assert checks["caller_contract_artifact"].error == (
        "caller-consumption contract doc is missing"
    )
