from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app())


def test_health_reports_machine_readable_readiness():
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "unifiedKnowledgeProvider"
    assert body["rag"]["status"] == "ready"
    assert body["graph"]["status"] == "planned"


def test_capabilities_include_rag_and_graph_boundaries():
    response = client.get("/api/capabilities")

    assert response.status_code == 200
    body = response.json()
    capability_ids = {item["id"] for item in body["capabilities"]}
    assert "knowledge.rag.retrieve" in capability_ids
    assert "knowledge.graph.query" in capability_ids


def test_catalog_exposes_knowledge_bases_and_graphs():
    response = client.get("/api/catalog")

    assert response.status_code == 200
    body = response.json()
    assert body["knowledge_bases"][0]["id"] == "refund_policy_docs"
    assert body["knowledge_bases"][0]["status"] == "ready"
    assert body["graphs"][0]["id"] == "ecommerce_order_graph"
    assert body["graphs"][0]["status"] == "planned"


def test_rag_sources_are_available_separately():
    response = client.get("/api/rag/sources")

    assert response.status_code == 200
    body = response.json()
    assert [source["id"] for source in body["knowledge_bases"]] == [
        "refund_policy_docs",
        "logistics_faq",
    ]


def test_rag_retrieve_returns_compact_context_and_citations():
    response = client.post(
        "/api/rag/retrieve",
        json={
            "query": "客户三天未发货能否退款？",
            "knowledge_base_ids": ["refund_policy_docs"],
            "top_k": 2,
            "filters": {
                "agent_id": "ecommerce_support",
                "role": "after_sales_specialist",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert "三天未发货" in body["result"]["answer_context"]
    assert body["result"]["documents"][0]["source_id"] == "refund_policy_docs"
    assert body["result"]["documents"][0]["citation"] == "refund_policy_2026#section-3"


def test_rag_answer_returns_cited_answer_envelope():
    response = client.post(
        "/api/rag/answer",
        json={
            "query": "客户三天未发货能否退款？",
            "knowledge_base_ids": ["refund_policy_docs"],
            "top_k": 2,
            "filters": {
                "agent_id": "ecommerce_support",
                "role": "after_sales_specialist",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["result"]["answer_status"] == "answered"
    assert "三天未发货" in body["result"]["answer"]
    assert body["result"]["citations"]
    document_citations = {
        document["citation"] for document in body["result"]["documents"]
    }
    assert set(body["result"]["citations"]).issubset(document_citations)
    assert body["result"]["metadata"]["composer"] == "deterministic-extractive-v1"


def test_rag_retrieve_empty_result_is_explicit_success():
    response = client.post(
        "/api/rag/retrieve",
        json={
            "query": "完全不存在的月球仓库规则",
            "knowledge_base_ids": ["refund_policy_docs"],
            "top_k": 3,
            "filters": {"agent_id": "ecommerce_support"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body == {
        "ok": True,
        "result": {
            "answer_context": "",
            "documents": [],
        },
        "error": None,
    }


def test_rag_answer_empty_result_is_insufficient_evidence():
    response = client.post(
        "/api/rag/answer",
        json={
            "query": "完全不存在的月球仓库规则",
            "knowledge_base_ids": ["refund_policy_docs"],
            "top_k": 3,
            "filters": {"agent_id": "ecommerce_support"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body == {
        "ok": True,
        "result": {
            "answer_status": "insufficient_evidence",
            "answer": "",
            "citations": [],
            "documents": [],
            "metadata": {
                "composer": "deterministic-extractive-v1",
                "evidence_count": 0,
                "retrieval_backend": "fixture",
            },
        },
        "error": None,
    }


def test_rag_retrieve_unknown_source_returns_structured_error():
    response = client.post(
        "/api/rag/retrieve",
        json={
            "query": "测试",
            "knowledge_base_ids": ["missing_docs"],
            "top_k": 3,
            "filters": {"agent_id": "ecommerce_support"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert body["result"] is None
    assert body["error"]["code"] == "UNKNOWN_KNOWLEDGE_BASE"
    assert "missing_docs" in body["error"]["message"]


def test_rag_answer_unknown_source_returns_structured_error():
    response = client.post(
        "/api/rag/answer",
        json={
            "query": "测试",
            "knowledge_base_ids": ["missing_docs"],
            "top_k": 3,
            "filters": {"agent_id": "ecommerce_support"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert body["result"] is None
    assert body["error"]["code"] == "UNKNOWN_KNOWLEDGE_BASE"
    assert "missing_docs" in body["error"]["message"]


def test_graph_schemas_expose_serializable_metadata():
    response = client.get("/api/graph/schemas")

    assert response.status_code == 200
    body = response.json()
    assert body["graphs"][0]["id"] == "ecommerce_order_graph"
    assert body["graphs"][0]["ontology_version"] == "2026-05"
    assert "Order" in body["graphs"][0]["entity_types"]


def test_graph_query_returns_structured_not_implemented_error():
    response = client.post(
        "/api/graph/query",
        json={
            "graph_id": "ecommerce_order_graph",
            "query": "订单 order-1 的售后关系",
            "entity_ids": ["order-1"],
            "relation_types": ["has_refund", "shipped_by"],
            "filters": {"agent_id": "ecommerce_support"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert body["result"] is None
    assert body["error"]["code"] == "GRAPH_NOT_IMPLEMENTED"
