from app.services import document_retriever


def test_fixture_retriever_filters_weak_negative_control_overlap():
    unknown_sources, documents = document_retriever.retrieve(
        query="退款政策里的员工名单有哪些？",
        knowledge_base_ids=["refund_policy_docs"],
        top_k=3,
    )

    assert unknown_sources == []
    assert documents == []


def test_fixture_retriever_keeps_exact_term_refund_policy_lookup():
    unknown_sources, documents = document_retriever.retrieve(
        query="RFD-2026-003 对应哪类退款复核？",
        knowledge_base_ids=["refund_policy_docs"],
        top_k=3,
    )

    assert unknown_sources == []
    assert documents
    assert documents[0].citation == "refund_policy_2026#exact-refund-code"
