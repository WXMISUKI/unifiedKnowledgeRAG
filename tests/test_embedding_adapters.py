from app.config import Settings
from app.services.embedding_adapters import (
    HostedEmbeddingAdapter,
    LocalEmbeddingAdapter,
    MockEmbeddingAdapter,
    create_embedding_adapter,
)
from app.services.qdrant_vector_store import VectorEvidenceChunk, embed_qdrant_chunks


def test_mock_embedding_is_deterministic_and_uses_configured_size():
    settings = Settings(embedding_vector_size=8)
    adapter = MockEmbeddingAdapter(settings)

    first = adapter.embed_text("客户三天未发货可以申请退款。")
    second = adapter.embed_text("客户三天未发货可以申请退款。")
    different = adapter.embed_text("物流轨迹超过二十四小时未更新。")

    assert adapter.provider_name == "mock"
    assert adapter.model_name == "mock-hash-v1"
    assert adapter.vector_size == 8
    assert first == second
    assert first != different
    assert len(first) == 8
    assert adapter.embed_text("") == [0.0] * 8


def test_embedding_factory_selects_mock_by_default():
    adapter = create_embedding_adapter(Settings(qdrant_vector_size=6))

    assert isinstance(adapter, MockEmbeddingAdapter)
    assert adapter.vector_size == 6
    assert adapter.readiness() == ("ready", None)


def test_embedding_factory_rejects_unknown_provider():
    try:
        create_embedding_adapter(Settings(embedding_provider="unknown"))
    except ValueError as error:
        assert "Unsupported EMBEDDING_PROVIDER" in str(error)
    else:
        raise AssertionError("Expected unknown embedding provider to be rejected")


def test_hosted_embedding_placeholder_fails_closed():
    adapter = create_embedding_adapter(
        Settings(embedding_provider="hosted", embedding_model="hosted-candidate")
    )

    assert isinstance(adapter, HostedEmbeddingAdapter)
    assert adapter.readiness()[0] == "degraded"
    try:
        adapter.embed_text("test")
    except NotImplementedError as error:
        assert "Hosted embedding adapter is not implemented yet" in str(error)
    else:
        raise AssertionError("Expected hosted embedding adapter to fail closed")


def test_local_embedding_placeholder_fails_closed():
    adapter = create_embedding_adapter(
        Settings(embedding_provider="local", embedding_model="local-candidate")
    )

    assert isinstance(adapter, LocalEmbeddingAdapter)
    assert adapter.readiness()[0] == "degraded"
    try:
        adapter.embed_text("test")
    except NotImplementedError as error:
        assert "Local embedding adapter is not implemented yet" in str(error)
    else:
        raise AssertionError("Expected local embedding adapter to fail closed")


def test_embed_qdrant_chunks_preserves_payload_metadata():
    adapter = MockEmbeddingAdapter(Settings(embedding_vector_size=4))
    chunk = VectorEvidenceChunk(
        point_id="refund_policy_2026:section-3:0",
        source_id="refund_policy_docs",
        document_id="refund_policy_2026",
        chunk_id="section-3:0",
        title="售后退款规则",
        text="客户三天未发货可以申请退款。",
        citation="refund_policy_2026#section-3",
        vector=[],
        metadata={"tenant_id": "tenant-a", "acl_tags": ["after_sales"]},
    )

    embedded = embed_qdrant_chunks([chunk], adapter)[0]

    assert embedded.point_id == chunk.point_id
    assert embedded.source_id == chunk.source_id
    assert embedded.document_id == chunk.document_id
    assert embedded.chunk_id == chunk.chunk_id
    assert embedded.title == chunk.title
    assert embedded.text == chunk.text
    assert embedded.citation == chunk.citation
    assert len(embedded.vector) == 4
    assert embedded.metadata["tenant_id"] == "tenant-a"
    assert embedded.metadata["acl_tags"] == ["after_sales"]
    assert embedded.metadata["embedding_provider"] == "mock"
    assert embedded.metadata["embedding_model"] == "mock-hash-v1"
