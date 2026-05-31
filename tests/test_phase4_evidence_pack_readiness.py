import json
from pathlib import Path

from app.services.phase4_evidence_pack_readiness import (
    build_phase4_evidence_pack_readiness_report,
    export_phase4_evidence_pack_readiness_report,
    render_phase4_evidence_pack_readiness_markdown,
)


def test_build_phase4_evidence_pack_readiness_report_summarizes_current_evidence():
    report = build_phase4_evidence_pack_readiness_report()

    assert report.id == "phase4-evidence-pack-readiness-v1"
    assert report.status == "ready"
    assert report.decision == "keep_caller_ownership"
    assert Path(report.contract_path).as_posix().endswith(
        "docs/benchmark/chinese-seed/evidence-pack-consumption-contract/"
        "phase4-evidence-pack-consumption-contract.md"
    )
    assert Path(report.smoke_report_path).as_posix().endswith(
        "docs/smoke/provider-contract/provider-contract-smoke.json"
    )

    summary = report.summary
    assert summary["total_artifacts"] == 5
    assert summary["ready_artifacts"] == 5
    assert summary["review_artifacts"] == 0
    assert summary["blocked_artifacts"] == 0
    assert summary["required_artifacts"] == 2
    assert summary["required_ready_artifacts"] == 2
    assert summary["smoke_passed"] is True
    assert summary["evidence_pack_checks_passed"] is True

    artifacts = {artifact.id: artifact for artifact in report.supporting_evidence}
    assert artifacts["evidence_pack_contract_doc"].status == "ready"
    assert artifacts["provider_contract_smoke"].status == "ready"
    assert artifacts["provider_contract_smoke"].summary.startswith("passed=True;")
    assert artifacts["test-provider-contract"].status == "ready"
    assert artifacts["test-provider-contract-smoke"].status == "ready"


def test_export_phase4_evidence_pack_readiness_report_writes_json_and_markdown(
    tmp_path,
):
    report = export_phase4_evidence_pack_readiness_report(
        output_dir=tmp_path / "readiness",
    )

    assert report.json_path == (
        tmp_path / "readiness" / "phase4-evidence-pack-readiness.json"
    )
    assert report.markdown_path == (
        tmp_path / "readiness" / "phase4-evidence-pack-readiness.md"
    )

    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["id"] == report.id
    assert payload["status"] == report.status
    assert payload["decision"] == report.decision
    assert payload["json_path"] == str(report.json_path)
    assert "# Phase 4 Evidence Pack Readiness Report" in markdown
    assert "| Evidence | Category | Status | Summary |" in markdown
    assert render_phase4_evidence_pack_readiness_markdown(report) == markdown


def test_phase4_evidence_pack_readiness_report_blocks_when_smoke_is_missing(tmp_path):
    contract_doc = (
        tmp_path
        / "docs/benchmark/chinese-seed/evidence-pack-consumption-contract"
        / "phase4-evidence-pack-consumption-contract.md"
    )
    contract_doc.parent.mkdir(parents=True, exist_ok=True)
    contract_doc.write_text("# contract\n", encoding="utf-8")

    report = build_phase4_evidence_pack_readiness_report(base_dir=tmp_path)

    artifacts = {artifact.id: artifact for artifact in report.supporting_evidence}
    assert report.status == "blocked"
    assert artifacts["evidence_pack_contract_doc"].status == "ready"
    assert artifacts["provider_contract_smoke"].status == "blocked"
    assert artifacts["provider_contract_smoke"].present is False
    assert artifacts["test-provider-contract"].status == "review"
    assert artifacts["test-provider-contract-smoke"].status == "review"
