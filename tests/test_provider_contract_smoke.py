import json

from fastapi.testclient import TestClient

from app.main import create_app
from app.services.provider_contract_smoke import (
    export_provider_contract_smoke_report,
    provider_contract_smoke_report_to_dict,
    render_provider_contract_smoke_markdown,
    run_provider_contract_smoke,
)


def test_provider_contract_smoke_passes_default_contract():
    report = run_provider_contract_smoke(client=TestClient(create_app()))
    payload = provider_contract_smoke_report_to_dict(report)

    assert payload["id"] == "provider-contract-smoke-v1"
    assert payload["passed"] is True
    assert payload["summary"] == {"total": 9, "passed": 9, "failed": 0}
    assert [check["name"] for check in payload["checks"]] == [
        "health_readiness",
        "provider_integration_manifest",
        "provider_preflight",
        "capability_invocation_metadata",
        "graph_schema_discovery",
        "rag_retrieve_contract",
        "rag_answer_contract",
        "rag_insufficient_evidence_pack_contract",
        "graph_planned_boundary",
    ]


def test_provider_contract_smoke_covers_trace_filter_and_citations():
    report = run_provider_contract_smoke(client=TestClient(create_app()))
    checks = {check.name: check for check in report.checks}

    manifest = checks["provider_integration_manifest"]
    assert manifest.details["contract_version"] == "knowledge-provider-contract-v1"
    assert manifest.details["component_role"] == "knowledge_data_plane"
    assert manifest.details["capability_count"] == 5

    preflight = checks["provider_preflight"]
    assert preflight.details["contract_version"] == "knowledge-provider-contract-v1"
    assert preflight.details["bindable"] is True
    assert preflight.details["check_count"] == 6
    assert preflight.details["graph_status"] == "planned"

    graph_schema = checks["graph_schema_discovery"]
    assert graph_schema.details == {
        "graph_count": 1,
        "graph_ids": ["ecommerce_order_graph"],
        "graph_status": "planned",
        "graph_store": "neo4j_planned",
        "entity_type_count": 4,
        "relation_type_count": 3,
    }

    retrieve = checks["rag_retrieve_contract"]
    assert retrieve.details["document_count"] > 0
    assert retrieve.details["citations"]
    assert retrieve.details["retrieval_trace_version"] == "retrieval-trace-v1"
    assert retrieve.details["filter_context_present"] is True

    answer = checks["rag_answer_contract"]
    assert answer.details["answer_status"] == "answered"
    assert answer.details["citation_count"] > 0
    assert answer.details["retrieval_trace_version"] == "retrieval-trace-v1"
    assert answer.details["evidence_pack_version"] == "evidence-pack-v1"
    assert answer.details["evidence_pack_status"] == "answerable"
    assert answer.details["answer_trace_version"] == "answer-trace-v1"
    assert answer.details["final_status"] == "answered"

    insufficient = checks["rag_insufficient_evidence_pack_contract"]
    assert insufficient.details == {
        "retrieval_pack_status": "insufficient_evidence",
        "retrieval_pack_reason": "no_documents",
        "retrieval_allowed_citation_count": 0,
        "retrieval_evidence_count": 0,
        "answer_status": "insufficient_evidence",
        "answer_pack_status": "insufficient_evidence",
        "answer_pack_reason": "no_documents",
        "answer_allowed_citation_count": 0,
        "answer_evidence_count": 0,
    }

    graph = checks["graph_planned_boundary"]
    assert graph.details == {
        "error_code": "GRAPH_NOT_IMPLEMENTED",
        "graph_id": "ecommerce_order_graph",
        "status": "planned",
        "capability_id": "knowledge.graph.query",
    }


def test_provider_contract_smoke_export_writes_json_and_markdown(tmp_path):
    report = export_provider_contract_smoke_report(
        output_dir=tmp_path / "smoke",
        client=TestClient(create_app()),
    )

    assert report.passed is True
    assert report.json_path is not None
    assert report.markdown_path is not None
    payload = json.loads(report.json_path.read_text(encoding="utf-8"))
    markdown = report.markdown_path.read_text(encoding="utf-8")

    assert payload["passed"] is True
    assert payload["json_path"] == str(report.json_path)
    assert payload["markdown_path"] == str(report.markdown_path)
    assert "# Provider Contract Smoke Report" in markdown
    assert "`rag_answer_contract`" in markdown
    assert "`graph_schema_discovery`" in markdown
    assert '"graph_count": 1' in markdown
    assert "`rag_insufficient_evidence_pack_contract`" in markdown
    assert '"retrieval_pack_status": "insufficient_evidence"' in markdown
    assert '"error_code": "GRAPH_NOT_IMPLEMENTED"' in markdown


def test_provider_contract_smoke_markdown_marks_failures():
    report = run_provider_contract_smoke(client=TestClient(create_app()))
    failed_check = report.checks[0].__class__(
        name="forced_failure",
        endpoint="GET /forced",
        passed=False,
        error="forced",
    )
    failed_report = report.__class__(
        id=report.id,
        generated_at=report.generated_at,
        passed=False,
        checks=[failed_check],
        summary={"total": 1, "passed": 0, "failed": 1},
    )

    markdown = render_provider_contract_smoke_markdown(failed_report)

    assert "- Status: `failed`" in markdown
    assert "| `forced_failure` | `GET /forced` | `failed` | `forced` |" in markdown
