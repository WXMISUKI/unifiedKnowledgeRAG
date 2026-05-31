from app.config import Settings, get_settings
from app.models.contracts import ProviderIntegrationManifest


PROVIDER_ID = "unifiedKnowledgeProvider"
PROVIDER_NAME = "unifiedKnowledgeRAG"
PROVIDER_VERSION = "0.1.0"
MANIFEST_VERSION = "provider-integration-manifest-v1"
CONTRACT_VERSION = "knowledge-provider-contract-v1"
COMPONENT_ROLE = "knowledge_data_plane"
COMPATIBLE_CONTROL_PLANES = ["MyPrivateAgent"]
SUPPORTED_CAPABILITY_IDS = [
    "knowledge.rag.source_documents",
    "knowledge.rag.retrieve",
    "knowledge.rag.answer",
    "knowledge.provider.source_bindings",
    "knowledge.graph.query",
]


def build_provider_integration_manifest(
    settings: Settings | None = None,
) -> ProviderIntegrationManifest:
    settings = settings or get_settings()
    return ProviderIntegrationManifest(
        provider_id=PROVIDER_ID,
        provider_name=PROVIDER_NAME,
        provider_version=PROVIDER_VERSION,
        manifest_version=MANIFEST_VERSION,
        contract_version=CONTRACT_VERSION,
        component_role=COMPONENT_ROLE,
        compatible_control_planes=COMPATIBLE_CONTROL_PLANES,
        description=(
            "External knowledge data-plane provider for MyPrivateAgent. "
            "The provider owns knowledge ingestion, indexing, retrieval, "
            "citation evidence, and GraphRAG contract boundaries."
        ),
        endpoints={
            "live": "/live",
            "ready": "/ready",
            "health": "/health",
            "manifest": "/api/provider/manifest",
            "preflight": "/api/provider/preflight",
            "provider_handoff": "/api/provider/handoff",
            "source_bindings": "/api/provider/source-bindings",
            "capabilities": "/api/capabilities",
            "openapi": "/openapi.json",
            "catalog": "/api/catalog",
            "ingestion_source_preflight_template": (
                "/api/ingestion/sources/{source_id}/preflight"
            ),
            "rag_sources": "/api/rag/sources",
            "rag_source_documents_template": "/api/rag/sources/{source_id}/documents",
            "rag_retrieve": "/api/rag/retrieve",
            "rag_answer": "/api/rag/answer",
            "graph_schemas": "/api/graph/schemas",
            "graph_query": "/api/graph/query",
            "ingestion_jobs": "/api/ingestion/jobs",
            "index_status_template": "/api/indexes/{source_id}/status",
        },
        capability_ids=SUPPORTED_CAPABILITY_IDS,
        evidence={
            "provider_contract_smoke_json": (
                "docs/smoke/provider-contract/provider-contract-smoke.json"
            ),
            "provider_contract_smoke_markdown": (
                "docs/smoke/provider-contract/provider-contract-smoke.md"
            ),
            "production_indexing_decision": (
                "docs/architecture/production_indexing_architecture.md"
            ),
        },
        access={
            "type": "component_api_key",
            "provider_api_key_configured": bool(settings.provider_api_key),
            "public_paths": ["/live", "/ready", "/health"],
            "protected_path_patterns": ["/api/*"],
            "accepted_header_schemes": [
                "Authorization: Bearer <token>",
                "X-Provider-Api-Key: <token>",
            ],
            "secret_values_in_manifest": False,
            "boundary": (
                "Component access control only; user identity, RBAC, approvals, "
                "audit policy, source-to-agent binding, and final answer workflow "
                "belong to the external control plane."
            ),
        },
        boundaries={
            "control_plane_owner": "MyPrivateAgent",
            "provider_owner": "unifiedKnowledgeRAG",
            "rag_status": "implemented",
            "graph_status": "contract_boundary_planned_execution",
            "implementation_internals": (
                "Embedding models, vector stores, queues, rerankers, and graph "
                "stores are provider internals, not MyPrivateAgent binding contracts."
            ),
        },
    )
