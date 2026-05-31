from app.models.contracts import SourcePackageMetadata
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
}


def get_source_package(source_id: str) -> SourcePackageMetadata | None:
    source = get_knowledge_base(source_id)
    if source is None:
        return None
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
