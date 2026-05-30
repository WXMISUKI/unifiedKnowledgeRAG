from app.config import Settings, get_settings
from app.models.contracts import (
    ProviderError,
    SourceDocumentManifest,
    SourceDocumentManifestResponse,
    SourceDocumentManifestResult,
)
from app.services.index_lifecycle import get_index_status
from app.services.source_catalog import get_knowledge_base


SOURCE_DOCUMENT_MANIFESTS = {
    "refund_policy_docs": [
        SourceDocumentManifest(
            document_id="refund_policy_2026",
            title="售后退款规则",
            source_path="app/data/sources/refund_policy_docs.md",
            format="markdown",
            version="2026-05-28",
            chunking_strategy="markdown-paragraph-v1",
            citation_anchors=[
                "refund_policy_2026#section-3",
                "refund_policy_2026#section-5",
                "refund_policy_2026#exact-refund-code",
                "refund_policy_2026#exception",
                "refund_policy_2026#high-value-review",
                "refund_policy_2026#address-change",
                "refund_policy_2026#appeal-review",
            ],
            metadata={
                "language": "zh-CN",
                "document_role": "local_contract_fixture",
            },
        )
    ],
    "logistics_faq": [
        SourceDocumentManifest(
            document_id="logistics_faq_2026",
            title="物流常见问题",
            source_path="app/data/sources/logistics_faq.md",
            format="markdown",
            version="2026-05-28",
            chunking_strategy="markdown-paragraph-v1",
            citation_anchors=[
                "logistics_faq_2026#delay",
                "logistics_faq_2026#same-city-timeout",
                "logistics_faq_2026#lost-package",
                "logistics_faq_2026#exact-logistics-id",
                "logistics_faq_2026#address-intercept",
                "logistics_faq_2026#batch-exception",
            ],
            metadata={
                "language": "zh-CN",
                "document_role": "local_contract_fixture",
            },
        )
    ],
}


def get_source_document_manifest(
    source_id: str,
    settings: Settings | None = None,
) -> SourceDocumentManifestResponse:
    settings = settings or get_settings()
    source = get_knowledge_base(source_id)
    if source is None:
        return SourceDocumentManifestResponse(
            ok=False,
            error=ProviderError(
                code="UNKNOWN_KNOWLEDGE_BASE",
                message=f"Unknown knowledge base id: {source_id}",
                details={
                    "requested_source_id": source_id,
                    "unknown_source_ids": [source_id],
                },
            ),
        )

    index_status = get_index_status(source_id, settings)
    return SourceDocumentManifestResponse(
        ok=True,
        result=SourceDocumentManifestResult(
            source_id=source.id,
            status=source.status,
            owner=source.owner,
            version=source.version,
            retrieval_backend=settings.rag_retrieval_backend.lower(),
            index_status=index_status.status,
            index_reason=index_status.reason,
            indexed_at=index_status.indexed_at,
            latest_index_job_id=index_status.latest_job_id,
            documents=SOURCE_DOCUMENT_MANIFESTS.get(source_id, []),
        ),
    )
