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
    assert body["answer"]["status"] == "ready"
    assert body["answer"]["backend"] == "deterministic"
    assert body["answer"]["backend_status"] == "ready"
    assert body["graph"]["status"] == "planned"


def test_health_reports_degraded_answer_composer(monkeypatch):
    monkeypatch.setenv("RAG_ANSWER_COMPOSER", "hosted")
    scoped_client = TestClient(create_app())

    response = scoped_client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "degraded"
    assert body["rag"]["status"] == "ready"
    assert body["answer"]["status"] == "degraded"
    assert body["answer"]["backend"] == "hosted"
    assert body["answer"]["backend_status"] == "degraded"
    assert "not implemented" in body["answer"]["reason"]


def test_capabilities_include_rag_and_graph_boundaries():
    response = client.get("/api/capabilities")

    assert response.status_code == 200
    body = response.json()
    capability_ids = {item["id"] for item in body["capabilities"]}
    assert "knowledge.rag.retrieve" in capability_ids
    assert "knowledge.rag.answer" in capability_ids
    assert "knowledge.graph.query" in capability_ids
    capabilities = {item["id"]: item for item in body["capabilities"]}
    assert capabilities["knowledge.rag.retrieve"]["invocation"] == {
        "protocol": "http",
        "method": "POST",
        "path": "/api/rag/retrieve",
        "request_schema_ref": "#/components/schemas/RagRetrieveRequest",
        "response_schema_ref": "#/components/schemas/RagRetrieveResponse",
    }
    assert capabilities["knowledge.rag.retrieve"]["reason"] is None
    assert capabilities["knowledge.rag.answer"]["invocation"] == {
        "protocol": "http",
        "method": "POST",
        "path": "/api/rag/answer",
        "request_schema_ref": "#/components/schemas/RagAnswerRequest",
        "response_schema_ref": "#/components/schemas/RagAnswerResponse",
    }
    assert capabilities["knowledge.rag.answer"]["status"] == "ready"
    assert capabilities["knowledge.rag.answer"]["reason"] is None
    assert capabilities["knowledge.graph.query"]["status"] == "planned"
    assert "not implemented" in capabilities["knowledge.graph.query"]["reason"]


def test_capabilities_report_degraded_answer_composer(monkeypatch):
    monkeypatch.setenv("RAG_ANSWER_COMPOSER", "local")
    scoped_client = TestClient(create_app())

    response = scoped_client.get("/api/capabilities")

    assert response.status_code == 200
    capabilities = {
        item["id"]: item for item in response.json()["capabilities"]
    }
    assert capabilities["knowledge.rag.retrieve"]["status"] == "ready"
    assert capabilities["knowledge.rag.answer"]["status"] == "degraded"
    assert "not implemented" in capabilities["knowledge.rag.answer"]["reason"]


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
    assert body["result"]["metadata"]["composer_provider"] == "deterministic"
    assert body["result"]["metadata"]["composer_model"] == "deterministic-extractive-v1"
    assert body["result"]["metadata"]["evidence_gate"]["passed"] is True
    prompt_package = body["result"]["metadata"]["prompt_package"]
    assert prompt_package["id"] == "cited-answer-prompt-v1"
    assert prompt_package["citation_policy"] == "use_only_allowed_citations"
    assert prompt_package["allowed_citations"] == body["result"]["citations"]
    assert prompt_package["evidence_count"] == len(body["result"]["citations"])
    prompt_render = body["result"]["metadata"]["prompt_render"]
    assert prompt_render == {
        "renderer": "cited-chat-messages-v1",
        "prompt_package_id": "cited-answer-prompt-v1",
        "message_count": 2,
        "citation_policy": "use_only_allowed_citations",
    }


def test_rag_answer_hosted_composer_fails_closed(monkeypatch):
    monkeypatch.setenv("RAG_ANSWER_COMPOSER", "hosted")
    scoped_client = TestClient(create_app())

    response = scoped_client.post(
        "/api/rag/answer",
        json={
            "query": "客户三天未发货能否退款？",
            "knowledge_base_ids": ["refund_policy_docs"],
            "top_k": 2,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert body["result"] is None
    assert body["error"]["code"] == "ANSWER_COMPOSER_NOT_IMPLEMENTED"
    assert "hosted" in body["error"]["message"]


def test_rag_answer_unknown_composer_returns_structured_error(monkeypatch):
    monkeypatch.setenv("RAG_ANSWER_COMPOSER", "mystery")
    scoped_client = TestClient(create_app())

    response = scoped_client.post(
        "/api/rag/answer",
        json={
            "query": "客户三天未发货能否退款？",
            "knowledge_base_ids": ["refund_policy_docs"],
            "top_k": 2,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert body["result"] is None
    assert body["error"]["code"] == "UNSUPPORTED_ANSWER_COMPOSER"
    assert "mystery" in body["error"]["message"]


def test_rag_answer_low_score_gate_returns_insufficient_evidence(monkeypatch):
    monkeypatch.setenv("RAG_ANSWER_MIN_EVIDENCE_SCORE", "0.7")
    scoped_client = TestClient(create_app())

    response = scoped_client.post(
        "/api/rag/answer",
        json={
            "query": "客户三天未发货能否退款？",
            "knowledge_base_ids": ["refund_policy_docs"],
            "top_k": 2,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["result"]["answer_status"] == "insufficient_evidence"
    assert body["result"]["answer"] == ""
    assert body["result"]["citations"] == []
    assert body["result"]["documents"]
    assert "prompt_package" not in body["result"]["metadata"]
    assert "prompt_render" not in body["result"]["metadata"]
    gate = body["result"]["metadata"]["evidence_gate"]
    assert gate["passed"] is False
    assert gate["reason"] == "top_score_below_minimum"
    assert gate["min_top_score"] == 0.7


def test_rag_answer_min_count_gate_returns_insufficient_evidence(monkeypatch):
    monkeypatch.setenv("RAG_ANSWER_MIN_EVIDENCE_COUNT", "3")
    scoped_client = TestClient(create_app())

    response = scoped_client.post(
        "/api/rag/answer",
        json={
            "query": "客户三天未发货能否退款？",
            "knowledge_base_ids": ["refund_policy_docs"],
            "top_k": 2,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["result"]["answer_status"] == "insufficient_evidence"
    assert body["result"]["answer"] == ""
    assert body["result"]["citations"] == []
    assert len(body["result"]["documents"]) == 2
    assert "prompt_package" not in body["result"]["metadata"]
    assert "prompt_render" not in body["result"]["metadata"]
    gate = body["result"]["metadata"]["evidence_gate"]
    assert gate["passed"] is False
    assert gate["reason"] == "evidence_count_below_minimum"
    assert gate["min_evidence_count"] == 3


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
                    "composer_provider": "deterministic",
                    "composer_model": "deterministic-extractive-v1",
                    "evidence_count": 0,
                    "evidence_gate": {
                    "passed": False,
                    "reason": "no_documents",
                    "min_evidence_count": 1,
                    "min_top_score": 0.0,
                    "top_score": None,
                },
                "retrieval_backend": "fixture",
            },
        },
        "error": None,
    }
    assert "prompt_package" not in body["result"]["metadata"]
    assert "prompt_render" not in body["result"]["metadata"]


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
