import json

from app.services.phase11_rag_retrieve_consumption_smoke import (
    build_phase11_rag_retrieve_consumption_smoke_report,
)


def test_phase11_retrieve_consumption_smoke_ready(tmp_path):
    _write_phase4(tmp_path, status="ready")
    _write_contract_smoke(tmp_path, passed=True)
    _write_phase10_probe(tmp_path, keep_runtime_defaults=True)

    report = build_phase11_rag_retrieve_consumption_smoke_report(base_dir=tmp_path)

    assert report.status == "ready"


def test_phase11_retrieve_consumption_smoke_blocks_runtime_boundary(tmp_path):
    _write_phase4(tmp_path, status="ready")
    _write_contract_smoke(tmp_path, passed=True)
    _write_phase10_probe(tmp_path, keep_runtime_defaults=False)

    report = build_phase11_rag_retrieve_consumption_smoke_report(base_dir=tmp_path)

    assert report.status == "blocked"


def _write_phase4(base_dir, *, status: str) -> None:
    path = (
        base_dir
        / "docs/smoke/evidence-pack-consumption/"
        / "phase4-caller-consumption-smoke.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"status": status}), encoding="utf-8")


def _write_contract_smoke(base_dir, *, passed: bool) -> None:
    path = base_dir / "docs/smoke/provider-contract/provider-contract-smoke.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"passed": passed}), encoding="utf-8")


def _write_phase10_probe(base_dir, *, keep_runtime_defaults: bool) -> None:
    path = (
        base_dir
        / "docs/smoke/myprivateagent-local-consumer-verification/"
        / "phase10-myprivateagent-local-consumer-probe.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "summary": {
                    "runtime_promotion_status": (
                        "keep_runtime_defaults"
                        if keep_runtime_defaults
                        else "promote_runtime_defaults"
                    )
                }
            }
        ),
        encoding="utf-8",
    )
