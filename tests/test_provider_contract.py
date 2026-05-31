from fastapi.testclient import TestClient

from app.main import create_app


client = TestClient(create_app())


def test_liveness_reports_process_without_readiness_side_effects(monkeypatch):
    def fail_if_readiness_runs(*_args, **_kwargs):
        raise AssertionError("liveness must not run readiness checks")

    monkeypatch.setattr(
        "app.services.provider_health.create_document_retriever",
        fail_if_readiness_runs,
    )
    monkeypatch.setattr(
        "app.services.provider_health.answer_composer_readiness",
        fail_if_readiness_runs,
    )
    monkeypatch.setattr(
        "app.services.provider_health.not_ready_sources",
        fail_if_readiness_runs,
    )

    response = client.get("/live")

    assert response.status_code == 200
    assert response.json() == {
        "status": "live",
        "service": "unifiedKnowledgeProvider",
    }


def test_readiness_matches_health_contract():
    health_response = client.get("/health")
    ready_response = client.get("/ready")

    assert health_response.status_code == 200
    assert ready_response.status_code == 200
    assert ready_response.json() == health_response.json()


def test_readiness_returns_503_when_provider_is_degraded(monkeypatch):
    monkeypatch.setenv("RAG_ANSWER_COMPOSER", "hosted")
    scoped_client = TestClient(create_app())

    health_response = scoped_client.get("/health")
    ready_response = scoped_client.get("/ready")

    assert health_response.status_code == 200
    assert health_response.json()["status"] == "degraded"
    assert ready_response.status_code == 503
    assert ready_response.json() == health_response.json()


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
    assert "knowledge.rag.source_documents" in capability_ids
    assert "knowledge.rag.retrieve" in capability_ids
    assert "knowledge.rag.answer" in capability_ids
    assert "knowledge.provider.source_bindings" in capability_ids
    assert "knowledge.graph.query" in capability_ids
    capabilities = {item["id"]: item for item in body["capabilities"]}
    assert capabilities["knowledge.rag.source_documents"]["invocation"] == {
        "protocol": "http",
        "method": "GET",
        "path": "/api/rag/sources/{source_id}/documents",
        "request_schema_ref": None,
        "response_schema_ref": "#/components/schemas/SourceDocumentManifestResponse",
        "example_request": {"source_id": "refund_policy_docs"},
    }
    assert capabilities["knowledge.rag.retrieve"]["invocation"] == {
        "protocol": "http",
        "method": "POST",
        "path": "/api/rag/retrieve",
        "request_schema_ref": "#/components/schemas/RagRetrieveRequest",
        "response_schema_ref": "#/components/schemas/RagRetrieveResponse",
        "example_request": {
            "query": "客户三天未发货能否退款？",
            "knowledge_base_ids": ["refund_policy_docs"],
            "top_k": 2,
            "filters": {
                "agent_id": "myprivateagent_probe",
                "role": "after_sales_specialist",
            },
        },
    }
    assert capabilities["knowledge.rag.retrieve"]["reason"] is None
    assert capabilities["knowledge.rag.answer"]["invocation"] == {
        "protocol": "http",
        "method": "POST",
        "path": "/api/rag/answer",
        "request_schema_ref": "#/components/schemas/RagAnswerRequest",
        "response_schema_ref": "#/components/schemas/RagAnswerResponse",
        "example_request": {
            "query": "客户三天未发货能否退款？",
            "knowledge_base_ids": ["refund_policy_docs"],
            "top_k": 2,
            "filters": {
                "agent_id": "myprivateagent_probe",
                "role": "after_sales_specialist",
            },
        },
    }
    assert capabilities["knowledge.rag.answer"]["status"] == "ready"
    assert capabilities["knowledge.rag.answer"]["reason"] is None
    assert capabilities["knowledge.provider.source_bindings"]["invocation"] == {
        "protocol": "http",
        "method": "GET",
        "path": "/api/provider/source-bindings",
        "request_schema_ref": None,
        "response_schema_ref": (
            "#/components/schemas/ProviderSourceBindingSummaryResponse"
        ),
        "example_request": {"scope": "all_configured_sources"},
    }
    assert (
        "Binding policy"
        in capabilities["knowledge.provider.source_bindings"]["description"]
    )
    assert capabilities["knowledge.graph.query"]["status"] == "planned"
    assert "not implemented" in capabilities["knowledge.graph.query"]["reason"]
    assert capabilities["knowledge.graph.query"]["invocation"]["example_request"] == {
        "graph_id": "ecommerce_order_graph",
        "query": "订单 order-1 的售后关系",
        "entity_ids": ["order-1"],
        "relation_types": ["has_refund"],
        "filters": {"agent_id": "myprivateagent_probe"},
    }


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


def test_provider_manifest_is_available_for_control_plane_preflight():
    response = client.get("/api/provider/manifest")

    assert response.status_code == 200
    body = response.json()
    assert body["provider_id"] == "unifiedKnowledgeProvider"
    assert body["component_role"] == "knowledge_data_plane"
    assert body["contract_version"] == "knowledge-provider-contract-v1"
    assert body["compatible_control_planes"] == ["MyPrivateAgent"]
    assert body["endpoints"]["capabilities"] == "/api/capabilities"
    assert body["endpoints"]["openapi"] == "/openapi.json"
    assert body["endpoints"]["rag_source_documents_template"] == (
        "/api/rag/sources/{source_id}/documents"
    )
    assert body["capability_ids"] == [
        "knowledge.rag.source_documents",
        "knowledge.rag.retrieve",
        "knowledge.rag.answer",
        "knowledge.provider.source_bindings",
        "knowledge.graph.query",
    ]


def test_provider_preflight_is_available_for_control_plane_binding():
    response = client.get("/api/provider/preflight")

    assert response.status_code == 200
    body = response.json()
    assert body["provider_id"] == "unifiedKnowledgeProvider"
    assert body["contract_version"] == "knowledge-provider-contract-v1"
    assert body["requested_contract_version"] == "knowledge-provider-contract-v1"
    assert body["bindable"] is True
    checks = {check["name"]: check for check in body["checks"]}
    assert checks["required_capabilities"]["details"]["missing_capability_ids"] == []
    assert checks["schema_references"]["details"][
        "missing_schema_ref_capability_ids"
    ] == []


def test_provider_preflight_rejects_incompatible_binding_requirements():
    response = client.get(
        "/api/provider/preflight",
        params=[
            ("required_contract_version", "knowledge-provider-contract-v2"),
            ("required_capability_ids", "knowledge.rag.retrieve"),
            ("required_capability_ids", "knowledge.graph.traverse"),
        ],
    )

    assert response.status_code == 200
    body = response.json()
    checks = {check["name"]: check for check in body["checks"]}
    assert body["bindable"] is False
    assert checks["contract_version"]["passed"] is False
    assert checks["required_capabilities"]["passed"] is False
    assert checks["required_capabilities"]["details"]["missing_capability_ids"] == [
        "knowledge.graph.traverse"
    ]


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


def test_rag_source_document_manifest_exposes_source_documents():
    response = client.get("/api/rag/sources/refund_policy_docs/documents")

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["error"] is None
    assert body["result"]["source_id"] == "refund_policy_docs"
    assert body["result"]["retrieval_backend"] == "fixture"
    assert body["result"]["index_status"] == "ready"
    assert body["result"]["documents"] == [
        {
            "document_id": "refund_policy_2026",
            "title": "售后退款规则",
            "source_path": "app/data/sources/refund_policy_docs.md",
            "format": "markdown",
            "version": "2026-05-28",
            "chunking_strategy": "markdown-paragraph-v1",
            "citation_anchors": [
                "refund_policy_2026#section-3",
                "refund_policy_2026#section-5",
                "refund_policy_2026#exact-refund-code",
                "refund_policy_2026#exception",
                "refund_policy_2026#high-value-review",
                "refund_policy_2026#address-change",
                "refund_policy_2026#appeal-review",
            ],
            "source_file_status": "present",
            "content_sha256": (
                "959c49adc2bcc512f33e62d751fc3f19c5993f1f19fc7ad99183ebdc96be6f6a"
            ),
            "expected_content_sha256": (
                "959c49adc2bcc512f33e62d751fc3f19c5993f1f19fc7ad99183ebdc96be6f6a"
            ),
            "content_byte_size": 1124,
            "drift_status": "in_sync",
            "metadata": {
                "language": "zh-CN",
                "document_role": "local_contract_fixture",
            },
        }
    ]


def test_rag_source_document_manifest_unknown_source_returns_structured_error():
    response = client.get("/api/rag/sources/missing_docs/documents")

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is False
    assert body["result"] is None
    assert body["error"] == {
        "code": "UNKNOWN_KNOWLEDGE_BASE",
        "message": "Unknown knowledge base id: missing_docs",
        "details": {
            "requested_source_id": "missing_docs",
            "unknown_source_ids": ["missing_docs"],
        },
    }


def test_rag_source_document_manifest_does_not_construct_retriever(monkeypatch):
    def fail_if_retriever_is_constructed(settings):
        raise AssertionError("manifest endpoint must not construct a retriever")

    monkeypatch.setattr(
        "app.services.retrieval_backends.create_document_retriever",
        fail_if_retriever_is_constructed,
    )

    response = client.get("/api/rag/sources/logistics_faq/documents")

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["result"]["source_id"] == "logistics_faq"
    assert body["result"]["documents"][0]["citation_anchors"][0] == (
        "logistics_faq_2026#delay"
    )


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
    filter_context = body["result"]["metadata"]["request_filter_context"]
    assert filter_context == {
        "tenant_id": None,
        "document_ids": [],
        "acl_tags": [],
        "agent_id": "ecommerce_support",
        "role": "after_sales_specialist",
        "extra_filters": {},
        "backend": "fixture",
        "enforced": False,
    }
    retrieval_trace = body["result"]["metadata"]["retrieval_trace"]
    assert retrieval_trace["version"] == "retrieval-trace-v1"
    assert retrieval_trace["backend"] == "fixture"
    assert retrieval_trace["requested_source_ids"] == ["refund_policy_docs"]
    assert retrieval_trace["top_k"] == 2
    assert retrieval_trace["document_count"] == len(body["result"]["documents"])
    assert retrieval_trace["citations"][0] == "refund_policy_2026#section-3"
    assert retrieval_trace["filter_context"] == filter_context
    evidence_pack = body["result"]["metadata"]["evidence_pack"]
    assert evidence_pack["version"] == "evidence-pack-v1"
    assert evidence_pack["status"] == "answerable"
    assert evidence_pack["reason"] == "documents_returned"
    assert evidence_pack["retrieval_backend"] == "fixture"
    assert evidence_pack["requested_source_ids"] == ["refund_policy_docs"]
    assert evidence_pack["citation_policy"] == "use_only_returned_citations"
    assert evidence_pack["allowed_citations"] == [
        document["citation"] for document in body["result"]["documents"]
    ]
    assert evidence_pack["evidence_count"] == len(body["result"]["documents"])
    assert evidence_pack["filter_context"] == filter_context
    assert "metadata" not in body["result"]["documents"][0]
    assert evidence_pack["evidence"][0]["provenance"] == {
        "source_path": "app/data/sources/refund_policy_docs.md",
        "chunk_id": "section-3",
        "chunking_strategy": "fixture-evidence-v1",
        "citation_anchor": "refund_policy_2026#section-3",
    }


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
    assert body["result"]["metadata"]["request_filter_context"] == {
        "tenant_id": None,
        "document_ids": [],
        "acl_tags": [],
        "agent_id": "ecommerce_support",
        "role": "after_sales_specialist",
        "extra_filters": {},
        "backend": "fixture",
        "enforced": False,
    }
    retrieval_trace = body["result"]["metadata"]["retrieval_trace"]
    assert retrieval_trace["version"] == "retrieval-trace-v1"
    assert retrieval_trace["backend"] == "fixture"
    assert retrieval_trace["requested_source_ids"] == ["refund_policy_docs"]
    assert retrieval_trace["document_count"] == len(body["result"]["documents"])
    evidence_pack = body["result"]["metadata"]["evidence_pack"]
    assert evidence_pack["version"] == "evidence-pack-v1"
    assert evidence_pack["status"] == "answerable"
    assert set(body["result"]["citations"]).issubset(
        set(evidence_pack["allowed_citations"])
    )
    assert evidence_pack["evidence_count"] == len(body["result"]["documents"])
    assert evidence_pack["evidence"][0]["provenance"] == {
        "source_path": "app/data/sources/refund_policy_docs.md",
        "chunk_id": "section-3",
        "chunking_strategy": "fixture-evidence-v1",
        "citation_anchor": "refund_policy_2026#section-3",
    }
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
    output_parser = body["result"]["metadata"]["output_parser"]
    assert output_parser == {
        "parser": "bracketed-citation-output-parser-v1",
        "citation_count": len(body["result"]["citations"]),
    }
    output_validation = body["result"]["metadata"]["output_validation"]
    assert output_validation == {
        "validator": "cited-answer-output-validator-v1",
        "passed": True,
        "reason": "passed",
        "citation_count": len(body["result"]["citations"]),
        "allowed_citation_count": len(prompt_package["allowed_citations"]),
    }
    answer_trace = body["result"]["metadata"]["answer_trace"]
    assert answer_trace["version"] == "answer-trace-v1"
    assert answer_trace["final_status"] == "answered"
    assert [stage["name"] for stage in answer_trace["stages"]] == [
        "retrieval",
        "evidence_gate",
        "composer",
        "output_parser",
        "output_validator",
        "final_decision",
    ]
    assert answer_trace["stages"][0]["document_count"] == len(body["result"]["documents"])
    assert answer_trace["stages"][-1]["reason"] == "validated_answer"


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
    assert body["error"]["details"] == {
        "configured_composer": "hosted",
        "configured_model": "deterministic-extractive-v1",
        "supported_composers": ["deterministic", "hosted", "local"],
    }


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
    assert body["error"]["details"] == {
        "configured_composer": "mystery",
        "configured_model": "deterministic-extractive-v1",
        "supported_composers": ["deterministic", "hosted", "local"],
    }


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
    assert "output_parser" not in body["result"]["metadata"]
    assert "output_validation" not in body["result"]["metadata"]
    answer_trace = body["result"]["metadata"]["answer_trace"]
    assert [stage["name"] for stage in answer_trace["stages"]] == [
        "retrieval",
        "evidence_gate",
        "composer",
        "final_decision",
    ]
    assert answer_trace["final_status"] == "insufficient_evidence"
    assert answer_trace["stages"][1]["status"] == "failed"
    assert answer_trace["stages"][-1]["reason"] == "evidence_gate_failed"
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
    assert "output_parser" not in body["result"]["metadata"]
    assert "output_validation" not in body["result"]["metadata"]
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
            "metadata": {
                "request_filter_context": {
                    "tenant_id": None,
                    "document_ids": [],
                    "acl_tags": [],
                    "agent_id": "ecommerce_support",
                    "role": None,
                    "extra_filters": {},
                    "backend": "fixture",
                    "enforced": False,
                },
                "retrieval_trace": body["result"]["metadata"]["retrieval_trace"],
                "evidence_pack": body["result"]["metadata"]["evidence_pack"],
            },
        },
        "error": None,
    }
    assert body["result"]["metadata"]["retrieval_trace"]["document_count"] == 0
    assert body["result"]["metadata"]["retrieval_trace"]["citations"] == []
    evidence_pack = body["result"]["metadata"]["evidence_pack"]
    assert evidence_pack["status"] == "insufficient_evidence"
    assert evidence_pack["reason"] == "no_documents"
    assert evidence_pack["allowed_citations"] == []


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
                "request_filter_context": {
                    "tenant_id": None,
                    "document_ids": [],
                    "acl_tags": [],
                    "agent_id": "ecommerce_support",
                    "role": None,
                    "extra_filters": {},
                    "backend": "fixture",
                    "enforced": False,
                },
                "retrieval_trace": body["result"]["metadata"]["retrieval_trace"],
                "evidence_pack": body["result"]["metadata"]["evidence_pack"],
                "answer_trace": body["result"]["metadata"]["answer_trace"],
            },
        },
        "error": None,
    }
    assert "prompt_package" not in body["result"]["metadata"]
    assert "prompt_render" not in body["result"]["metadata"]
    assert "output_parser" not in body["result"]["metadata"]
    assert "output_validation" not in body["result"]["metadata"]
    assert body["result"]["metadata"]["answer_trace"]["final_status"] == "insufficient_evidence"
    assert body["result"]["metadata"]["retrieval_trace"]["document_count"] == 0
    evidence_pack = body["result"]["metadata"]["evidence_pack"]
    assert evidence_pack["status"] == "insufficient_evidence"
    assert evidence_pack["reason"] == "no_documents"


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
    assert body["error"]["details"] == {
        "requested_source_ids": ["missing_docs"],
        "unknown_source_ids": ["missing_docs"],
    }


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
    assert body["error"]["details"] == {
        "requested_source_ids": ["missing_docs"],
        "unknown_source_ids": ["missing_docs"],
    }


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
    assert body["error"]["details"] == {
        "graph_id": "ecommerce_order_graph",
        "status": "planned",
        "capability_id": "knowledge.graph.query",
    }
