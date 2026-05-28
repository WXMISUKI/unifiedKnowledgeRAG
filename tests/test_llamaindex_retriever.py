from app.config import Settings
from app.services.llamaindex_retriever import LlamaIndexLocalRetriever


def test_llamaindex_retriever_preserves_provider_citations(tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n客户三天未发货可以申请退款，售后专员应核验订单状态和发货记录后处理。",
        encoding="utf-8",
    )

    settings = Settings(
        rag_retrieval_backend="llamaindex",
        rag_source_dir=source_dir,
        rag_index_dir=tmp_path / "index",
        rag_score_threshold=0.0,
    )

    retriever = LlamaIndexLocalRetriever(settings)
    retriever.build_index(["refund_policy_docs"], latest_job_id="test_job")
    unknown_sources, documents = retriever.retrieve(
        query="三天未发货退款",
        knowledge_base_ids=["refund_policy_docs"],
        top_k=1,
    )

    assert unknown_sources == []
    assert len(documents) == 1
    assert documents[0].source_id == "refund_policy_docs"
    assert documents[0].document_id == "refund_policy_2026"
    assert documents[0].title == "售后退款规则"
    assert documents[0].citation == "refund_policy_2026#section-3"
    assert "三天未发货" in documents[0].snippet
    assert isinstance(documents[0].score, float)


def test_llamaindex_retriever_reports_unknown_source(tmp_path):
    settings = Settings(
        rag_retrieval_backend="llamaindex",
        rag_source_dir=tmp_path / "sources",
        rag_index_dir=tmp_path / "index",
    )

    retriever = LlamaIndexLocalRetriever(settings)
    unknown_sources, documents = retriever.retrieve(
        query="测试",
        knowledge_base_ids=["missing_docs"],
        top_k=1,
    )

    assert unknown_sources == ["missing_docs"]
    assert documents == []
