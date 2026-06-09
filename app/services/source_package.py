from app.models.contracts import SourcePackageMetadata
from app.services.approved_local_corpus_source_registration import (
    get_approved_local_source,
)
from app.services.source_catalog import get_knowledge_base


SOURCE_PACKAGES = {
    "refund_policy_docs": {
        "domain": "after_sales_policy",
        "language": "zh-CN",
        "sensitivity": "internal",
        "supported_formats": ["markdown"],
        "default_chunking_strategy": "markdown-paragraph-v1",
        "citation_granularity": "section",
        "allowed_parser_statuses": ["ready"],
        "metadata": {
            "business_use": "refund_policy_support",
            "package_role": "local_enterprise_onboarding_fixture",
        },
    },
    "logistics_faq": {
        "domain": "logistics_support",
        "language": "zh-CN",
        "sensitivity": "internal",
        "supported_formats": ["markdown"],
        "default_chunking_strategy": "markdown-paragraph-v1",
        "citation_granularity": "section",
        "allowed_parser_statuses": ["ready"],
        "metadata": {
            "business_use": "logistics_faq_support",
            "package_role": "local_enterprise_onboarding_fixture",
        },
    },
    "invoice_policy_faq": {
        "domain": "invoice_policy_support",
        "language": "zh-CN",
        "sensitivity": "internal",
        "supported_formats": ["markdown"],
        "default_chunking_strategy": "markdown-paragraph-v1",
        "citation_granularity": "section",
        "allowed_parser_statuses": ["ready"],
        "metadata": {
            "business_use": "invoice_policy_support",
            "package_role": "local_enterprise_onboarding_fixture",
        },
    },
    "source_template_example": {
        "domain": "onboarding_example",
        "language": "zh-CN",
        "sensitivity": "internal",
        "supported_formats": ["markdown"],
        "default_chunking_strategy": "markdown-paragraph-v1",
        "citation_granularity": "section",
        "allowed_parser_statuses": ["ready"],
        "metadata": {
            "business_use": "source_onboarding_example",
            "package_role": "local_enterprise_onboarding_fixture",
        },
    },
}


def get_source_package(source_id: str) -> SourcePackageMetadata | None:
    source = get_knowledge_base(source_id)
    if source is None:
        return None
    approved_source = get_approved_local_source(source_id)
    if approved_source is not None:
        return SourcePackageMetadata(
            source_id=source.id,
            owner=source.owner,
            version=source.version,
            domain=approved_source.domain,
            language=approved_source.language,
            sensitivity=approved_source.sensitivity,
            supported_formats=list(approved_source.supported_formats),
            default_chunking_strategy=approved_source.default_chunking_strategy,
            citation_granularity=approved_source.citation_granularity,
            allowed_parser_statuses=["ready"],
            metadata=dict(approved_source.metadata),
        )
    package = SOURCE_PACKAGES.get(source_id, {})
    return SourcePackageMetadata(
        source_id=source.id,
        owner=source.owner,
        version=source.version,
        domain=package.get("domain", "general"),
        language=package.get("language", "unknown"),
        sensitivity=package.get("sensitivity", "internal"),
        supported_formats=list(package.get("supported_formats", ["markdown"])),
        default_chunking_strategy=package.get(
            "default_chunking_strategy",
            "markdown-paragraph-v1",
        ),
        citation_granularity=package.get("citation_granularity", "section"),
        allowed_parser_statuses=list(package.get("allowed_parser_statuses", ["ready"])),
        metadata=dict(package.get("metadata", {})),
    )
