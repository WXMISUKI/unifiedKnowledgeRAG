import json

from app.services.phase9_myprivateagent_local_consumption_smoke import (
    build_phase9_myprivateagent_local_consumption_smoke_report,
    export_phase9_myprivateagent_local_consumption_smoke_report,
    render_phase9_myprivateagent_local_consumption_smoke_markdown,
)


def test_build_phase9_local_consumption_smoke_ready(tmp_path):
    _write_readiness(tmp_path, runtime_promotion_ready=False)
    _write_contract(tmp_path, include_required_tokens=True)
    _write_integration_probe(tmp_path, compatible=True)
    _write_provider_contract_smoke(tmp_path, graph_planned_passed=True)
    _write_source_binding_summary(tmp_path, status="ready")
    _write_phase4_smoke(tmp_path, status="ready")

    report = build_phase9_myprivateagent_local_consumption_smoke_report(
        base_dir=tmp_path
    )

    assert report.status == "ready"
    assert report.summary["total_checks"] == 7
    assert report.summary["failed_checks"] == 0


def test_export_phase9_local_consumption_smoke_writes_outputs(tmp_path):
    _write_readiness(tmp_path, runtime_promotion_ready=False)
    _write_contract(tmp_path, include_required_tokens=True)
    _write_integration_probe(tmp_path, compatible=True)
    _write_provider_contract_smoke(tmp_path, graph_planned_passed=True)
    _write_source_binding_summary(tmp_path, status="review")
    _write_phase4_smoke(tmp_path, status="review")

    report = export_phase9_myprivateagent_local_consumption_smoke_report(
        output_dir=tmp_path / "summary",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert report.status == "ready"
    assert payload["id"] == report.id
    assert "# Phase 9 MyPrivateAgent Local Consumption Smoke" in markdown
    assert render_phase9_myprivateagent_local_consumption_smoke_markdown(report) == markdown


def test_phase9_local_consumption_smoke_blocks_on_runtime_boundary_break(tmp_path):
    _write_readiness(tmp_path, runtime_promotion_ready=True)
    _write_contract(tmp_path, include_required_tokens=True)
    _write_integration_probe(tmp_path, compatible=True)
    _write_provider_contract_smoke(tmp_path, graph_planned_passed=True)
    _write_source_binding_summary(tmp_path, status="ready")
    _write_phase4_smoke(tmp_path, status="ready")

    report = build_phase9_myprivateagent_local_consumption_smoke_report(
        base_dir=tmp_path
    )

    assert report.status == "blocked"
    assert any(check.id == "runtime_promotion_boundary" and check.status == "blocked" for check in report.checks)


def _write_readiness(base_dir, *, runtime_promotion_ready: bool) -> None:
    path = (
        base_dir
        / "docs/integration/myprivateagent-local-consumption/"
        / "phase9-myprivateagent-local-consumption-readiness.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": "review",
                "local_consumption_state": "review",
                "decision": "keep_local_consumption_review",
                "summary": {
                    "local_handoff_ready": True,
                    "runtime_promotion_ready": runtime_promotion_ready,
                },
            }
        ),
        encoding="utf-8",
    )


def _write_contract(base_dir, *, include_required_tokens: bool) -> None:
    path = (
        base_dir
        / "docs/integration/myprivateagent-local-consumption/"
        / "phase9-myprivateagent-local-consumption-contract.md"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "Phase 9 Contract\n"
    if include_required_tokens:
        text += (
            "http://127.0.0.1:8020\nPROVIDER_API_KEY\nMyPrivateAgent\n"
            "source-to-agent binding\n"
        )
    path.write_text(text, encoding="utf-8")


def _write_integration_probe(base_dir, *, compatible: bool) -> None:
    path = base_dir / "docs/integration/provider-binding/provider-integration-probe.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "checks": [
                    {
                        "name": "manifest_identity",
                        "details": {
                            "compatible_control_planes": (
                                ["MyPrivateAgent"] if compatible else ["Other"]
                            )
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def _write_provider_contract_smoke(base_dir, *, graph_planned_passed: bool) -> None:
    path = base_dir / "docs/smoke/provider-contract/provider-contract-smoke.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "checks": [
                    {
                        "name": "graph_planned_boundary",
                        "passed": graph_planned_passed,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def _write_source_binding_summary(base_dir, *, status: str) -> None:
    path = base_dir / "docs/integration/source-bindings/provider-source-bindings.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": status,
                "bindable_source_count": 2,
                "total_source_count": 2,
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
    path.write_text(
        json.dumps({"status": status}),
        encoding="utf-8",
    )
