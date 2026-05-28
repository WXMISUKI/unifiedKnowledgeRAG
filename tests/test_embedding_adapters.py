import os
from types import SimpleNamespace

from app.config import Settings
from app.services.embedding_adapters import (
    BgeM3LocalEmbeddingAdapter,
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


def test_embedding_factory_selects_bge_m3_local_adapter():
    adapter = create_embedding_adapter(
        Settings(
            embedding_provider="bge_m3_local",
            embedding_model="BAAI/bge-m3",
            embedding_vector_size=1024,
        )
    )

    assert isinstance(adapter, BgeM3LocalEmbeddingAdapter)
    assert adapter.provider_name == "bge_m3_local"
    assert adapter.model_name == "BAAI/bge-m3"
    assert adapter.vector_size == 1024


def test_bge_m3_local_adapter_lazy_loads_and_embeds(monkeypatch):
    created = []

    class FakeBgeM3Model:
        def __init__(self, model_path, use_fp16):
            created.append((model_path, use_fp16))

        def encode(self, texts, batch_size, max_length, **kwargs):
            assert texts == ["客户三天未发货可以申请退款。", "物流轨迹超过二十四小时未更新。"]
            assert batch_size == 2
            assert max_length == 128
            assert kwargs == {
                "return_dense": True,
                "return_sparse": False,
                "return_colbert_vecs": False,
            }
            return {"dense_vecs": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]}

    monkeypatch.setattr(
        "app.services.embedding_adapters.import_module",
        lambda name: SimpleNamespace(BGEM3FlagModel=FakeBgeM3Model),
    )

    adapter = BgeM3LocalEmbeddingAdapter(
        Settings(
            embedding_provider="bge_m3_local",
            embedding_model="BAAI/bge-m3",
            embedding_vector_size=3,
            bge_m3_use_fp16=False,
            bge_m3_batch_size=2,
            bge_m3_max_length=128,
        )
    )

    vectors = adapter.embed_batch([
        "客户三天未发货可以申请退款。",
        "物流轨迹超过二十四小时未更新。",
    ])

    assert created == [("BAAI/bge-m3", False)]
    assert vectors == [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    assert adapter.readiness() == ("ready", None)
    assert len(created) == 1


def test_bge_m3_local_adapter_uses_local_path_and_mirror_settings(monkeypatch, tmp_path):
    created = []
    model_dir = tmp_path / "bge-m3"
    model_dir.mkdir()

    class FakeBgeM3Model:
        def __init__(self, model_path, use_fp16):
            created.append((model_path, use_fp16))

        def encode(self, texts, **kwargs):
            return {"dense_vecs": [[0.1, 0.2, 0.3] for _ in texts]}

    monkeypatch.delenv("HF_ENDPOINT", raising=False)
    monkeypatch.delenv("HF_HUB_OFFLINE", raising=False)
    monkeypatch.delenv("TRANSFORMERS_OFFLINE", raising=False)
    monkeypatch.setattr(
        "app.services.embedding_adapters.import_module",
        lambda name: SimpleNamespace(BGEM3FlagModel=FakeBgeM3Model),
    )

    adapter = BgeM3LocalEmbeddingAdapter(
        Settings(
            embedding_provider="bge_m3_local",
            embedding_model_path=model_dir,
            embedding_vector_size=3,
            embedding_hf_endpoint="https://hf-mirror.com",
            embedding_local_files_only=True,
        )
    )

    assert adapter.embed_text("测试") == [0.1, 0.2, 0.3]
    assert created == [(str(model_dir), True)]
    assert os.environ["HF_ENDPOINT"] == "https://hf-mirror.com"
    assert os.environ["HF_HUB_OFFLINE"] == "1"
    assert os.environ["TRANSFORMERS_OFFLINE"] == "1"


def test_bge_m3_local_adapter_reports_degraded_when_dependency_missing(monkeypatch):
    def missing_module(name):
        raise ModuleNotFoundError("No module named FlagEmbedding")

    monkeypatch.setattr(
        "app.services.embedding_adapters.import_module",
        missing_module,
    )

    adapter = BgeM3LocalEmbeddingAdapter(
        Settings(embedding_provider="bge_m3_local", embedding_vector_size=1024)
    )

    status, reason = adapter.readiness()

    assert status == "degraded"
    assert "BGE-M3 local embedding model is not ready" in reason
    assert "FlagEmbedding" in reason


def test_bge_m3_local_adapter_rejects_unexpected_vector_size(monkeypatch):
    class FakeBgeM3Model:
        def __init__(self, model_path, use_fp16):
            pass

        def encode(self, texts, **kwargs):
            return {"dense_vecs": [[0.1, 0.2]]}

    monkeypatch.setattr(
        "app.services.embedding_adapters.import_module",
        lambda name: SimpleNamespace(BGEM3FlagModel=FakeBgeM3Model),
    )

    adapter = BgeM3LocalEmbeddingAdapter(
        Settings(embedding_provider="bge_m3_local", embedding_vector_size=3)
    )

    try:
        adapter.embed_text("测试")
    except ValueError as error:
        assert "BGE-M3 vector size mismatch" in str(error)
    else:
        raise AssertionError("Expected BGE-M3 vector size mismatch to be rejected")


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


def test_embed_qdrant_chunks_preserves_bge_m3_metadata(monkeypatch):
    class FakeBgeM3Model:
        def __init__(self, model_path, use_fp16):
            pass

        def encode(self, texts, **kwargs):
            return {"dense_vecs": [[0.1, 0.2, 0.3] for _ in texts]}

    monkeypatch.setattr(
        "app.services.embedding_adapters.import_module",
        lambda name: SimpleNamespace(BGEM3FlagModel=FakeBgeM3Model),
    )
    adapter = BgeM3LocalEmbeddingAdapter(
        Settings(
            embedding_provider="bge_m3_local",
            embedding_model="BAAI/bge-m3",
            embedding_vector_size=3,
        )
    )
    chunk = VectorEvidenceChunk(
        point_id="refund_policy_2026:section-3:0",
        source_id="refund_policy_docs",
        document_id="refund_policy_2026",
        chunk_id="section-3:0",
        title="售后退款规则",
        text="客户三天未发货可以申请退款。",
        citation="refund_policy_2026#section-3",
        vector=[],
        metadata={"tenant_id": "tenant-a"},
    )

    embedded = embed_qdrant_chunks([chunk], adapter)[0]

    assert embedded.vector == [0.1, 0.2, 0.3]
    assert embedded.metadata["embedding_provider"] == "bge_m3_local"
    assert embedded.metadata["embedding_model"] == "BAAI/bge-m3"
