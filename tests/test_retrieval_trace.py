from app.models.contracts import EvidenceDocument
from app.services.retrieval_trace import build_retrieval_trace


def test_retrieval_trace_summarizes_documents_and_scores():
    documents = [
        EvidenceDocument(
            source_id="refund_policy_docs",
            document_id="refund_policy_2026",
            title="售后退款规则",
            snippet="客户三天未发货可以退款。",
            score=0.8,
            citation="refund_policy_2026#section-3",
        ),
        EvidenceDocument(
            source_id="refund_policy_docs",
            document_id="refund_policy_2026",
            title="退款凭证规则",
            snippet="退款需要保留凭证。",
            score=0.4,
            citation="refund_policy_2026#section-5",
        ),
    ]

    trace = build_retrieval_trace(
        backend="fixture",
        requested_source_ids=["refund_policy_docs"],
        top_k=2,
        documents=documents,
        filter_context={"backend": "fixture", "enforced": False},
    )

    assert trace["trace_id"].startswith("retrieval-trace-")
    assert trace["version"] == "retrieval-trace-v1"
    assert trace["backend"] == "fixture"
    assert trace["requested_source_ids"] == ["refund_policy_docs"]
    assert trace["top_k"] == 2
    assert trace["document_count"] == 2
    assert trace["citations"] == [
        "refund_policy_2026#section-3",
        "refund_policy_2026#section-5",
    ]
    assert trace["score_summary"] == {
        "max_score": 0.8,
        "min_score": 0.4,
    }


def test_retrieval_trace_handles_empty_documents():
    trace = build_retrieval_trace(
        backend="fixture",
        requested_source_ids=["refund_policy_docs"],
        top_k=3,
        documents=[],
        filter_context={"backend": "fixture", "enforced": False},
    )

    assert trace["document_count"] == 0
    assert trace["citations"] == []
    assert trace["score_summary"] == {
        "max_score": None,
        "min_score": None,
    }
