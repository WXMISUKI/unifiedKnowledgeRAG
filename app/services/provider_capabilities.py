from app.config import Settings, get_settings
from app.models.contracts import CapabilitiesResponse, Capability, CapabilityInvocation
from app.services.rag_answer_orchestrator import answer_composer_readiness


def build_capabilities_response(
    settings: Settings | None = None,
) -> CapabilitiesResponse:
    settings = settings or get_settings()
    answer_status, answer_reason, _answer_backend, _answer_model = (
        answer_composer_readiness(settings)
    )
    graph_reason = "Graph query execution is not implemented in this slice."
    return CapabilitiesResponse(
        capabilities=[
            Capability(
                id="knowledge.rag.source_documents",
                status="ready",
                description=(
                    "Inspect provider-owned source document manifests, citation "
                    "anchors, chunking metadata, and index readiness."
                ),
                invocation=CapabilityInvocation(
                    method="GET",
                    path="/api/rag/sources/{source_id}/documents",
                    response_schema_ref=(
                        "#/components/schemas/SourceDocumentManifestResponse"
                    ),
                    example_request={"source_id": "refund_policy_docs"},
                ),
            ),
            Capability(
                id="knowledge.rag.retrieve",
                status="ready",
                description="Retrieve compact document evidence with stable citations.",
                invocation=CapabilityInvocation(
                    method="POST",
                    path="/api/rag/retrieve",
                    request_schema_ref="#/components/schemas/RagRetrieveRequest",
                    response_schema_ref="#/components/schemas/RagRetrieveResponse",
                    example_request=_rag_example_request(),
                ),
            ),
            Capability(
                id="knowledge.rag.answer",
                status=answer_status,
                description=(
                    "Compose cited document RAG answers with evidence gating and "
                    "configurable composer boundaries."
                ),
                reason=answer_reason,
                invocation=CapabilityInvocation(
                    method="POST",
                    path="/api/rag/answer",
                    request_schema_ref="#/components/schemas/RagAnswerRequest",
                    response_schema_ref="#/components/schemas/RagAnswerResponse",
                    example_request=_rag_example_request(),
                ),
            ),
            Capability(
                id="knowledge.graph.query",
                status="planned",
                description="Graph query contract boundary; execution is deferred.",
                reason=graph_reason,
                invocation=CapabilityInvocation(
                    method="POST",
                    path="/api/graph/query",
                    request_schema_ref="#/components/schemas/GraphQueryRequest",
                    response_schema_ref="#/components/schemas/GraphQueryResponse",
                    example_request={
                        "graph_id": "ecommerce_order_graph",
                        "query": "订单 order-1 的售后关系",
                        "entity_ids": ["order-1"],
                        "relation_types": ["has_refund"],
                        "filters": {"agent_id": "myprivateagent_probe"},
                    },
                ),
            ),
        ]
    )


def _rag_example_request() -> dict[str, object]:
    return {
        "query": "客户三天未发货能否退款？",
        "knowledge_base_ids": ["refund_policy_docs"],
        "top_k": 2,
        "filters": {
            "agent_id": "myprivateagent_probe",
            "role": "after_sales_specialist",
        },
    }
