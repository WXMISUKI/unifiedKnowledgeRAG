from app.services.request_filter_context import normalize_request_filter_context


def test_request_filter_context_normalizes_supported_and_extra_filters():
    context = normalize_request_filter_context({
        "tenant_id": " tenant-a ",
        "document_ids": ["refund_policy_2026", "", 123],
        "acl_tags": "after_sales",
        "agent_id": "ecommerce_support",
        "role": "after_sales_specialist",
        "channel": "web",
    })

    assert context.tenant_id == "tenant-a"
    assert context.document_ids == ["refund_policy_2026"]
    assert context.acl_tags == ["after_sales"]
    assert context.agent_id == "ecommerce_support"
    assert context.role == "after_sales_specialist"
    assert context.extra_filters == {"channel": "web"}
    assert context.metadata(backend="fixture", enforced=False) == {
        "tenant_id": "tenant-a",
        "document_ids": ["refund_policy_2026"],
        "acl_tags": ["after_sales"],
        "agent_id": "ecommerce_support",
        "role": "after_sales_specialist",
        "extra_filters": {"channel": "web"},
        "backend": "fixture",
        "enforced": False,
    }
