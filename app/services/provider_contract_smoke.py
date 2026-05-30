import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ProviderContractSmokeCheck:
    name: str
    passed: bool
    endpoint: str
    details: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass(frozen=True)
class ProviderContractSmokeReport:
    id: str
    generated_at: str
    passed: bool
    checks: list[ProviderContractSmokeCheck]
    summary: dict[str, int]
    json_path: Path | None = None
    markdown_path: Path | None = None


def run_provider_contract_smoke(client: Any | None = None) -> ProviderContractSmokeReport:
    if client is None:
        from fastapi.testclient import TestClient

        from app.main import create_app

        client = TestClient(create_app())

    checks = [
        _run_check("health_readiness", "GET /health", lambda: _check_health(client)),
        _run_check(
            "provider_integration_manifest",
            "GET /api/provider/manifest",
            lambda: _check_manifest(client),
        ),
        _run_check(
            "capability_invocation_metadata",
            "GET /api/capabilities",
            lambda: _check_capabilities(client),
        ),
        _run_check(
            "rag_retrieve_contract",
            "POST /api/rag/retrieve",
            lambda: _check_retrieve(client),
        ),
        _run_check(
            "rag_answer_contract",
            "POST /api/rag/answer",
            lambda: _check_answer(client),
        ),
        _run_check(
            "graph_planned_boundary",
            "POST /api/graph/query",
            lambda: _check_graph_boundary(client),
        ),
    ]
    passed_count = sum(1 for check in checks if check.passed)
    summary = {
        "total": len(checks),
        "passed": passed_count,
        "failed": len(checks) - passed_count,
    }
    return ProviderContractSmokeReport(
        id="provider-contract-smoke-v1",
        generated_at=datetime.now(UTC).isoformat(),
        passed=summary["failed"] == 0,
        checks=checks,
        summary=summary,
    )


def provider_contract_smoke_report_to_dict(
    report: ProviderContractSmokeReport,
) -> dict[str, Any]:
    payload = asdict(report)
    if report.json_path is not None:
        payload["json_path"] = str(report.json_path)
    if report.markdown_path is not None:
        payload["markdown_path"] = str(report.markdown_path)
    return payload


def render_provider_contract_smoke_markdown(
    report: ProviderContractSmokeReport,
) -> str:
    status = "passed" if report.passed else "failed"
    lines = [
        "# Provider Contract Smoke Report",
        "",
        f"- Report: `{report.id}`",
        f"- Status: `{status}`",
        f"- Generated At: `{report.generated_at}`",
        f"- Checks: `{report.summary['passed']}/{report.summary['total']}` passed",
        "",
        "| Check | Endpoint | Status | Details |",
        "|---|---|---|---|",
    ]
    for check in report.checks:
        check_status = "passed" if check.passed else "failed"
        details = _compact_markdown_details(check)
        lines.append(
            f"| `{check.name}` | `{check.endpoint}` | `{check_status}` | {details} |"
        )
    lines.append("")
    return "\n".join(lines)


def export_provider_contract_smoke_report(
    output_dir: Path = Path("docs/smoke/provider-contract"),
    *,
    client: Any | None = None,
) -> ProviderContractSmokeReport:
    report = run_provider_contract_smoke(client=client)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "provider-contract-smoke.json"
    markdown_path = output_dir / "provider-contract-smoke.md"
    exported_report = ProviderContractSmokeReport(
        id=report.id,
        generated_at=report.generated_at,
        passed=report.passed,
        checks=report.checks,
        summary=report.summary,
        json_path=json_path,
        markdown_path=markdown_path,
    )
    json_path.write_text(
        json.dumps(
            provider_contract_smoke_report_to_dict(exported_report),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(
        render_provider_contract_smoke_markdown(exported_report),
        encoding="utf-8",
    )
    return exported_report


def _run_check(name: str, endpoint: str, check_fn: Any) -> ProviderContractSmokeCheck:
    try:
        details = check_fn()
    except AssertionError as error:
        return ProviderContractSmokeCheck(
            name=name,
            passed=False,
            endpoint=endpoint,
            error=str(error) or error.__class__.__name__,
        )
    except Exception as error:
        return ProviderContractSmokeCheck(
            name=name,
            passed=False,
            endpoint=endpoint,
            error=f"{error.__class__.__name__}: {error}",
        )
    return ProviderContractSmokeCheck(
        name=name,
        passed=True,
        endpoint=endpoint,
        details=details,
    )


def _check_health(client: Any) -> dict[str, Any]:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["rag"]["status"] == "ready"
    assert body["answer"]["status"] == "ready"
    assert body["graph"]["status"] == "planned"
    return {
        "service": body["service"],
        "rag_status": body["rag"]["status"],
        "answer_status": body["answer"]["status"],
        "graph_status": body["graph"]["status"],
    }


def _check_manifest(client: Any) -> dict[str, Any]:
    response = client.get("/api/provider/manifest")
    assert response.status_code == 200
    body = response.json()
    assert body["provider_id"] == "unifiedKnowledgeProvider"
    assert body["manifest_version"] == "provider-integration-manifest-v1"
    assert body["contract_version"] == "knowledge-provider-contract-v1"
    assert body["component_role"] == "knowledge_data_plane"
    assert "MyPrivateAgent" in body["compatible_control_planes"]
    assert body["endpoints"]["health"] == "/health"
    assert body["endpoints"]["capabilities"] == "/api/capabilities"
    assert body["endpoints"]["openapi"] == "/openapi.json"
    assert body["endpoints"]["rag_retrieve"] == "/api/rag/retrieve"
    assert body["endpoints"]["rag_answer"] == "/api/rag/answer"
    assert body["endpoints"]["graph_query"] == "/api/graph/query"
    assert "knowledge.rag.retrieve" in body["capability_ids"]
    assert "knowledge.rag.answer" in body["capability_ids"]
    assert "knowledge.graph.query" in body["capability_ids"]
    assert body["evidence"]["provider_contract_smoke_json"].endswith(
        "provider-contract-smoke.json"
    )
    return {
        "provider_id": body["provider_id"],
        "manifest_version": body["manifest_version"],
        "contract_version": body["contract_version"],
        "component_role": body["component_role"],
        "capability_count": len(body["capability_ids"]),
    }


def _check_capabilities(client: Any) -> dict[str, Any]:
    response = client.get("/api/capabilities")
    assert response.status_code == 200
    capabilities = {item["id"]: item for item in response.json()["capabilities"]}
    expected_paths = {
        "knowledge.rag.retrieve": "/api/rag/retrieve",
        "knowledge.rag.answer": "/api/rag/answer",
        "knowledge.graph.query": "/api/graph/query",
    }
    for capability_id, path in expected_paths.items():
        capability = capabilities[capability_id]
        assert capability["invocation"]["method"] == "POST"
        assert capability["invocation"]["path"] == path
        assert capability["invocation"]["request_schema_ref"]
        assert capability["invocation"]["response_schema_ref"]
    return {
        "capability_ids": sorted(expected_paths),
        "invocation_paths": expected_paths,
        "graph_status": capabilities["knowledge.graph.query"]["status"],
    }


def _check_retrieve(client: Any) -> dict[str, Any]:
    response = client.post(
        "/api/rag/retrieve",
        json=_rag_smoke_payload(),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    result = body["result"]
    assert result["documents"]
    metadata = result["metadata"]
    filter_context = metadata["request_filter_context"]
    retrieval_trace = metadata["retrieval_trace"]
    assert retrieval_trace["version"] == "retrieval-trace-v1"
    assert retrieval_trace["document_count"] == len(result["documents"])
    assert retrieval_trace["citations"]
    assert retrieval_trace["filter_context"] == filter_context
    return {
        "document_count": len(result["documents"]),
        "citations": retrieval_trace["citations"],
        "retrieval_trace_version": retrieval_trace["version"],
        "filter_context_present": bool(filter_context),
    }


def _check_answer(client: Any) -> dict[str, Any]:
    response = client.post(
        "/api/rag/answer",
        json=_rag_smoke_payload(),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    result = body["result"]
    assert result["answer_status"] == "answered"
    assert result["answer"]
    assert result["citations"]
    metadata = result["metadata"]
    assert metadata["retrieval_trace"]["version"] == "retrieval-trace-v1"
    assert metadata["answer_trace"]["version"] == "answer-trace-v1"
    assert metadata["answer_trace"]["final_status"] == "answered"
    assert metadata["request_filter_context"]
    return {
        "answer_status": result["answer_status"],
        "citation_count": len(result["citations"]),
        "retrieval_trace_version": metadata["retrieval_trace"]["version"],
        "answer_trace_version": metadata["answer_trace"]["version"],
        "final_status": metadata["answer_trace"]["final_status"],
    }


def _check_graph_boundary(client: Any) -> dict[str, Any]:
    response = client.post(
        "/api/graph/query",
        json={
            "graph_id": "ecommerce_order_graph",
            "query": "订单 order-1 的售后关系",
            "entity_ids": ["order-1"],
            "relation_types": ["has_refund"],
            "filters": {"agent_id": "provider_contract_smoke"},
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert body["error"]["code"] == "GRAPH_NOT_IMPLEMENTED"
    details = body["error"]["details"]
    assert details["graph_id"] == "ecommerce_order_graph"
    assert details["status"] == "planned"
    assert details["capability_id"] == "knowledge.graph.query"
    return {
        "error_code": body["error"]["code"],
        "graph_id": details["graph_id"],
        "status": details["status"],
        "capability_id": details["capability_id"],
    }


def _rag_smoke_payload() -> dict[str, Any]:
    return {
        "query": "客户三天未发货能否退款？",
        "knowledge_base_ids": ["refund_policy_docs"],
        "top_k": 2,
        "filters": {
            "agent_id": "provider_contract_smoke",
            "role": "integration_probe",
        },
    }


def _compact_markdown_details(check: ProviderContractSmokeCheck) -> str:
    if not check.passed:
        return f"`{check.error}`"
    compact = {
        key: value
        for key, value in check.details.items()
        if key.endswith("_status")
        or key.endswith("_version")
        or key in {
            "document_count",
            "citation_count",
            "error_code",
            "contract_version",
            "component_role",
            "capability_count",
        }
    }
    return f"`{json.dumps(compact, ensure_ascii=False)}`"
