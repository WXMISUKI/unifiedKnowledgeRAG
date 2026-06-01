import json

from app.services.phase7_provider_release_readiness import (
    build_phase7_provider_release_readiness_report,
    export_phase7_provider_release_readiness_report,
    render_phase7_provider_release_readiness_markdown,
)


def test_build_phase7_provider_release_readiness_report_defaults():
    report = build_phase7_provider_release_readiness_report()

    assert report.id == "phase7-provider-release-readiness-v1"
    assert report.status in {"review", "blocked", "ready"}
    assert report.release_state in {
        "blocked",
        "review",
        "ready_for_local_handoff",
        "ready_for_runtime_promotion",
    }
    assert report.decision in {
        "fix_required_handoff_gates",
        "review_handoff_signals",
        "keep_runtime_defaults",
        "allow_runtime_default_promotion_review",
    }
    assert report.summary["total_signals"] >= 10


def test_export_phase7_provider_release_readiness_report(tmp_path):
    contract_doc = (
        tmp_path
        / "docs/operations/provider-release-readiness/phase7-provider-handoff-acceptance-contract.md"
    )
    contract_doc.parent.mkdir(parents=True, exist_ok=True)
    contract_doc.write_text("# contract\n", encoding="utf-8")

    probe_path = tmp_path / "docs/integration/provider-binding/provider-integration-probe.json"
    probe_path.parent.mkdir(parents=True, exist_ok=True)
    probe_path.write_text(json.dumps({"bindable": True}), encoding="utf-8")

    smoke_path = tmp_path / "docs/smoke/provider-contract/provider-contract-smoke.json"
    smoke_path.parent.mkdir(parents=True, exist_ok=True)
    smoke_path.write_text(
        json.dumps({"passed": True, "summary": {"passed": 9, "total": 9}}),
        encoding="utf-8",
    )

    source_binding_path = (
        tmp_path / "docs/integration/source-bindings/provider-source-bindings.json"
    )
    source_binding_path.parent.mkdir(parents=True, exist_ok=True)
    source_binding_path.write_text(
        json.dumps({"status": "ready", "total_source_count": 2, "bindable_source_count": 2}),
        encoding="utf-8",
    )

    # Promotion-facing optional evidence intentionally stays review to preserve defaults.
    optional_paths = [
        "docs/benchmark/chinese-seed/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-readiness.json",
        "docs/smoke/hybrid-runtime-promotion/phase3-hybrid-runtime-promotion-decision-smoke.json",
        "docs/operations/private-network-promotion/phase6-qdrant-bge-private-network-promotion-readiness.json",
        "docs/operations/deployed-field-validation/phase6-deployed-field-validation-readiness.json",
    ]
    for rel in optional_paths:
        file_path = tmp_path / rel
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps({"status": "review"}), encoding="utf-8")

    report = export_phase7_provider_release_readiness_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert report.status == "review"
    assert report.release_state == "ready_for_local_handoff"
    assert report.decision == "keep_runtime_defaults"
    assert payload["summary"]["ready_for_local_provider_handoff"] is True
    assert payload["summary"]["ready_for_runtime_default_promotion"] is False
    assert "# Phase 7 Provider Release Readiness" in markdown
    assert render_phase7_provider_release_readiness_markdown(report) == markdown


def test_phase7_provider_release_readiness_blocks_when_required_missing(tmp_path):
    report = build_phase7_provider_release_readiness_report(base_dir=tmp_path)
    assert report.status == "blocked"
    assert report.summary["ready_for_local_provider_handoff"] is False
    assert report.decision == "fix_required_handoff_gates"
