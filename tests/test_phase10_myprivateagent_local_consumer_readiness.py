import json

from app.services.phase10_myprivateagent_local_consumer_readiness import (
    build_phase10_myprivateagent_local_consumer_readiness_report,
    export_phase10_myprivateagent_local_consumer_readiness_report,
)


def test_build_phase10_local_consumer_readiness_defaults():
    report = build_phase10_myprivateagent_local_consumer_readiness_report()

    assert report.id == "phase10-myprivateagent-local-consumer-readiness-v1"
    assert report.status in {"ready", "review", "blocked"}
    assert report.local_consumer_state in {
        "ready_for_local_consumer_probe",
        "ready_for_local_consumer_probe_review",
        "blocked",
    }
    assert report.summary["total_signals"] == 8
    assert report.summary["local_provider_url"] == "http://127.0.0.1:8020"
    assert report.summary["source_binding_policy_owner"] == "caller"


def test_export_phase10_local_consumer_readiness_ready(tmp_path):
    _write_contract(tmp_path)
    _write_phase9_readiness(tmp_path, status="ready", local_handoff_ready=True)
    _write_phase9_smoke(tmp_path, status="ready")
    _write_handoff_bundle(tmp_path, status="ready")
    _write_phase4_pack(tmp_path, status="ready")
    _write_phase4_smoke(tmp_path, status="ready")
    _write_provider_contract_smoke(tmp_path, passed=True, graph_planned=True)
    _write_deployed_smoke(tmp_path, status="ready")

    report = export_phase10_myprivateagent_local_consumer_readiness_report(
        output_dir=tmp_path / "out",
        base_dir=tmp_path,
    )
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert report.status == "ready"
    assert report.local_consumer_state == "ready_for_local_consumer_probe"
    assert payload["summary"]["phase4_evidence_pack_ready"] is True
    assert payload["summary"]["graph_boundary_ready"] is True
    assert "# Phase 10 MyPrivateAgent Local Consumer Readiness" in markdown


def test_phase10_local_consumer_readiness_blocks_without_phase9(tmp_path):
    _write_contract(tmp_path)
    _write_phase4_pack(tmp_path, status="ready")
    _write_phase4_smoke(tmp_path, status="ready")
    _write_provider_contract_smoke(tmp_path, passed=True, graph_planned=True)

    report = build_phase10_myprivateagent_local_consumer_readiness_report(
        base_dir=tmp_path
    )

    assert report.status == "blocked"
    assert "phase9_myprivateagent_local_consumption_readiness" in report.summary["open_gate_ids"]
    assert "phase9_myprivateagent_local_consumption_smoke" in report.summary["open_gate_ids"]


def _write_contract(base_dir) -> None:
    path = (
        base_dir
        / "docs/integration/myprivateagent-local-consumer-verification/"
        / "phase10-myprivateagent-local-consumer-verification-contract.md"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# contract\n", encoding="utf-8")


def _write_phase9_readiness(
    base_dir,
    *,
    status: str,
    local_handoff_ready: bool,
) -> None:
    path = (
        base_dir
        / "docs/integration/myprivateagent-local-consumption/"
        / "phase9-myprivateagent-local-consumption-readiness.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": status,
                "local_consumption_state": "ready_for_local_consumption",
                "summary": {
                    "local_handoff_ready": local_handoff_ready,
                    "runtime_promotion_ready": False,
                },
            }
        ),
        encoding="utf-8",
    )


def _write_phase9_smoke(base_dir, *, status: str) -> None:
    path = (
        base_dir
        / "docs/smoke/myprivateagent-local-consumption/"
        / "phase9-myprivateagent-local-consumption-smoke.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {"status": status, "summary": {"passed_checks": 7, "total_checks": 7}}
        ),
        encoding="utf-8",
    )


def _write_handoff_bundle(base_dir, *, status: str) -> None:
    path = base_dir / "docs/integration/provider-handoff/provider-handoff-bundle.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"status": status, "evidence_artifacts": [{"id": "phase9"}]}),
        encoding="utf-8",
    )


def _write_phase4_pack(base_dir, *, status: str) -> None:
    path = (
        base_dir
        / "docs/benchmark/chinese-seed/evidence-pack-readiness/"
        / "phase4-evidence-pack-readiness.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"status": status, "decision": "keep_caller_ownership"}),
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
        json.dumps({"status": status, "summary": {"passed_checks": 3, "total_checks": 3}}),
        encoding="utf-8",
    )


def _write_provider_contract_smoke(
    base_dir,
    *,
    passed: bool,
    graph_planned: bool,
) -> None:
    path = base_dir / "docs/smoke/provider-contract/provider-contract-smoke.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "passed": passed,
                "summary": {"passed": 9 if passed else 8, "total": 9},
                "checks": [
                    {
                        "name": "graph_planned_boundary",
                        "passed": graph_planned,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def _write_deployed_smoke(base_dir, *, status: str) -> None:
    path = (
        base_dir
        / "docs/integration/deployed-provider-smoke/deployed-provider-smoke.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "status": status,
                "base_url": "http://127.0.0.1:8020",
                "operation_notes": [
                    "No provider API credentials were supplied; this is only expected for local development."
                ],
            }
        ),
        encoding="utf-8",
    )
