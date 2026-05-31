from app.models.contracts import EvidenceDocument
from app.services.evidence_pack import build_evidence_pack


def _document(citation: str = "refund_policy_2026#section-3") -> EvidenceDocument:
    return EvidenceDocument(
        source_id="refund_policy_docs",
        document_id="refund_policy_2026",
        title="售后退款规则",
        snippet="客户三天未发货可以申请退款。",
        score=0.91,
        citation=citation,
        metadata={
            "source_path": "app/data/sources/refund_policy_docs.md",
            "chunk_id": "section-3",
            "chunking_strategy": "fixture-evidence-v1",
            "citation_anchor": citation,
        },
    )


def test_evidence_pack_marks_answerable_documents():
    document = _document()

    pack = build_evidence_pack(
        query="客户三天未发货能否退款？",
        requested_source_ids=["refund_policy_docs"],
        retrieval_backend="fixture",
        documents=[document],
        filter_context={"backend": "fixture", "enforced": False},
    )

    assert pack["pack_id"].startswith("evidence-pack-")
    assert pack["version"] == "evidence-pack-v1"
    assert pack["status"] == "answerable"
    assert pack["reason"] == "documents_returned"
    assert pack["citation_policy"] == "use_only_returned_citations"
    assert pack["allowed_citations"] == [document.citation]
    assert pack["evidence_count"] == 1
    assert pack["score_summary"] == {"max_score": 0.91, "min_score": 0.91}
    assert pack["evidence"][0]["citation"] == document.citation
    assert pack["evidence"][0]["snippet"] == document.snippet
    assert pack["evidence"][0]["provenance"] == {
        "source_path": "app/data/sources/refund_policy_docs.md",
        "chunk_id": "section-3",
        "chunking_strategy": "fixture-evidence-v1",
        "citation_anchor": "refund_policy_2026#section-3",
    }


def test_evidence_pack_marks_empty_retrieval_as_insufficient():
    pack = build_evidence_pack(
        query="完全不存在的月球仓库规则",
        requested_source_ids=["refund_policy_docs"],
        retrieval_backend="fixture",
        documents=[],
        filter_context={"backend": "fixture", "enforced": False},
    )

    assert pack["status"] == "insufficient_evidence"
    assert pack["reason"] == "no_documents"
    assert pack["allowed_citations"] == []
    assert pack["evidence_count"] == 0
    assert pack["score_summary"] == {"max_score": None, "min_score": None}
    assert pack["evidence"] == []
