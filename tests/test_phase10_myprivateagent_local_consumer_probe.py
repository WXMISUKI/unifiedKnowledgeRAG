import json

from app.services.phase10_myprivateagent_local_consumer_probe import (
    build_phase10_myprivateagent_local_consumer_probe_report,
    export_phase10_myprivateagent_local_consumer_probe_report,
    render_phase10_myprivateagent_local_consumer_probe_markdown,
)


def test_build_phase10_local_consumer_probe_ready(tmp_path):
    _write_readiness(tmp_path, runtime_promotion_ready=False)
    _write_contract(tmp_path, include_required_tokens=True)
    _write_handoff_bundle(tmp_path, include_phase10=True)
    _write_provider_contract_smoke(tmp_path, graph_planned=True)
    _write_phase4_smoke(tmp_path, status="ready")

    report = build_phase10_myprivateagent_local_consumer_probe_report(
        base_dir=tmp_path
    )

    assert report.status == "ready"
    assert report.summary["total_checks"] == 7
    assert report.summary["failed_checks"] == 0
    assert report.summary["api_key_mode"] == "not_configured_local_dev"


def test_export_phase10_local_consumer_probe_writes_outputs(tmp_path):
    _write_readiness(tmp_path, runtime_promotion_ready=False)
    _write_contract(tmp_path, include_required_tokens=True)
    _write_handoff_bundle(tmp_path, include_phase10=True)
    _write_provider_contract_smoke(tmp_path, graph_planned=True)
    _write_phase4_smoke(tmp_path, status="review")

    report = export_phase10_myprivateagent_local_consumer_probe_report(
        output_dir=tmp_path / "probe",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert report.status == "ready"
    assert payload["id"] == report.id
    assert "# Phase 10 MyPrivateAgent Local Consumer Probe" in markdown
    assert render_phase10_myprivateagent_local_consumer_probe_markdown(report) == markdown


def test_phase10_local_consumer_probe_blocks_when_handoff_lacks_phase10(tmp_path):
    _write_readiness(tmp_path, runtime_promotion_ready=False)
    _write_contract(tmp_path, include_required_tokens=True)
    _write_handoff_bundle(tmp_path, include_phase10=False)
    _write_provider_contract_smoke(tmp_path, graph_planned=True)
    _write_phase4_smoke(tmp_path, status="ready")

    report = build_phase10_myprivateagent_local_consumer_probe_report(
        base_dir=tmp_path
    )

    assert report.status == "blocked"
    assert any(
        check.id == "handoff_phase10_presence" and check.status == "blocked"
        for check in report.checks
    )


def test_phase10_local_consumer_probe_blocks_on_runtime_promotion_boundary_break(
    tmp_path,
):
    _write_readiness(tmp_path, runtime_promotion_ready=True)
    _write_contract(tmp_path, include_required_tokens=True)
    _write_handoff_bundle(tmp_path, include_phase10=True)
    _write_provider_contract_smoke(tmp_path, graph_planned=True)
    _write_phase4_smoke(tmp_path, status="ready")

    report = build_phase10_myprivateagent_local_consumer_probe_report(
        base_dir=tmp_path
    )

    assert report.status == "blocked"
    assert any(
        check.id == "runtime_promotion_boundary" and check.status == "blocked"
        for check in report.checks
    )


def _write_readiness(base_dir, *, runtime_promotion_ready: bool) -> None:
    path = (
        base_dir
        / "docs/integration/myprivateagent-local-consumer-verification/"
        / "phase10-myprivateagent-local-consumer-readiness.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": "review",
                "local_consumer_state": "ready_for_local_consumer_probe_review",
                "summary": {
                    "local_provider_url": "http://127.0.0.1:8020",
                    "api_key_mode": "not_configured_local_dev",
                    "graph_boundary_ready": True,
                    "runtime_promotion_ready": runtime_promotion_ready,
                    "runtime_promotion_status": (
                        "promote_runtime_defaults"
                        if runtime_promotion_ready
                        else "keep_runtime_defaults"
                    ),
                },
            }
        ),
        encoding="utf-8",
    )


def _write_contract(base_dir, *, include_required_tokens: bool) -> None:
    path = (
        base_dir
        / "docs/integration/myprivateagent-local-consumer-verification/"
        / "phase10-myprivateagent-local-consumer-verification-contract.md"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "# Contract\n"
    if include_required_tokens:
        text += (
            "http://127.0.0.1:8020\n"
            "PROVIDER_API_KEY\n"
            "GET /api/provider/manifest\n"
            "GET /api/provider/preflight\n"
            "GET /api/provider/source-bindings\n"
            "GET /api/provider/handoff\n"
            "source-to-agent binding\n"
            "GraphRAG\n"
        )
    path.write_text(text, encoding="utf-8")


def _write_handoff_bundle(base_dir, *, include_phase10: bool) -> None:
    path = base_dir / "docs/integration/provider-handoff/provider-handoff-bundle.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    evidence_artifacts = []
    if include_phase10:
        evidence_artifacts = [
            {"id": "phase10_myprivateagent_local_consumer_readiness"},
            {"id": "phase10_myprivateagent_local_consumer_probe"},
        ]
    path.write_text(
        json.dumps({"status": "review", "evidence_artifacts": evidence_artifacts}),
        encoding="utf-8",
    )


def _write_provider_contract_smoke(base_dir, *, graph_planned: bool) -> None:
    path = base_dir / "docs/smoke/provider-contract/provider-contract-smoke.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "checks": [
                    {
                        "name": "graph_planned_boundary",
                        "passed": graph_planned,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def _write_phase4_smoke(base_dir, *, status: str) -> None:
    path = (
        base_dir
        / "docs/smoke/evidence-pack-consumption/"
        / "phase4-caller-consumption-smoke.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"status": status}), encoding="utf-8")
