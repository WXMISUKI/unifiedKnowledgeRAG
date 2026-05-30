from dataclasses import dataclass, field
from typing import Any


SUPPORTED_FILTER_KEYS = {
    "tenant_id",
    "document_ids",
    "acl_tags",
    "agent_id",
    "role",
}


@dataclass(frozen=True)
class RequestFilterContext:
    tenant_id: str | None = None
    document_ids: list[str] = field(default_factory=list)
    acl_tags: list[str] = field(default_factory=list)
    agent_id: str | None = None
    role: str | None = None
    extra_filters: dict[str, Any] = field(default_factory=dict)

    def metadata(self, backend: str, enforced: bool) -> dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "document_ids": self.document_ids,
            "acl_tags": self.acl_tags,
            "agent_id": self.agent_id,
            "role": self.role,
            "extra_filters": self.extra_filters,
            "backend": backend,
            "enforced": enforced,
        }


def normalize_request_filter_context(
    filters: dict[str, Any] | None,
) -> RequestFilterContext:
    filters = filters or {}
    return RequestFilterContext(
        tenant_id=_string_or_none(filters.get("tenant_id")),
        document_ids=_string_list(filters.get("document_ids")),
        acl_tags=_string_list(filters.get("acl_tags")),
        agent_id=_string_or_none(filters.get("agent_id")),
        role=_string_or_none(filters.get("role")),
        extra_filters={
            key: value
            for key, value in filters.items()
            if key not in SUPPORTED_FILTER_KEYS
        },
    )


def _string_or_none(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if not isinstance(value, list):
        return []
    return [
        item.strip()
        for item in value
        if isinstance(item, str) and item.strip()
    ]
