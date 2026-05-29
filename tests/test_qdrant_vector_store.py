from app.config import Settings
from app.models.contracts import IndexStatusResponse
from app.services.qdrant_vector_store import (
    VectorEvidenceChunk,
    build_qdrant_source_index,
    build_qdrant_payload_filter,
    chunk_to_qdrant_point,
    create_qdrant_client,
    ensure_qdrant_collection,
    query_qdrant_documents,
    query_qdrant_documents_for_text,
    markdown_source_to_qdrant_chunks,
    markdown_source_to_section_chunks,
    markdown_source_to_token_window_chunks,
    upsert_qdrant_chunks,
)
from app.services.index_lifecycle import get_index_status
from app.services.index_lifecycle_store import IndexLifecycleStore
from app.services.retrieval_backends import create_document_retriever
from app.services.retrieval_benchmark import qdrant_retrieval_candidate


class FakeQdrantClient:
    def __init__(self, collection_exists=True, hits=None, fail=False):
        self._collection_exists = collection_exists
        self.hits = hits or []
        self.fail = fail
        self.created_collections = []
        self.upserts = []
        self.queries = []

    def collection_exists(self, collection_name):
        if self.fail:
            raise RuntimeError("qdrant unavailable")
        return self._collection_exists

    def create_collection(self, **kwargs):
        self.created_collections.append(kwargs)

    def upsert(self, **kwargs):
        self.upserts.append(kwargs)

    def query_points(self, **kwargs):
        self.queries.append(kwargs)
        return self.hits


def test_qdrant_settings_have_safe_candidate_defaults():
    settings = Settings()

    assert settings.rag_retrieval_backend == "fixture"
    assert settings.qdrant_url == "http://localhost:6333"
    assert settings.qdrant_collection == "knowledge_chunks"
    assert settings.qdrant_vector_name == "text-dense"
    assert settings.qdrant_vector_size == 1024


def test_qdrant_point_mapping_preserves_evidence_metadata():
    settings = Settings(qdrant_vector_name="body-dense")
    chunk = VectorEvidenceChunk(
        point_id="refund_policy_2026:section-3:0",
        source_id="refund_policy_docs",
        document_id="refund_policy_2026",
        chunk_id="section-3:0",
        title="售后退款规则",
        text="客户三天未发货可以申请退款。",
        citation="refund_policy_2026#section-3",
        vector=[0.1, 0.2, 0.3],
        metadata={
            "tenant_id": "tenant-a",
            "document_version": "2026-05-28",
            "acl_tags": ["after_sales"],
            "embedding_model": "undecided",
            "chunking_strategy": "structure-aware-v1",
        },
    )

    point = chunk_to_qdrant_point(chunk, settings)

    assert point["id"] != "refund_policy_2026:section-3:0"
    assert point["payload"]["point_id"] == "refund_policy_2026:section-3:0"
    assert point["vector"] == {"body-dense": [0.1, 0.2, 0.3]}
    assert point["payload"]["tenant_id"] == "tenant-a"
    assert point["payload"]["source_id"] == "refund_policy_docs"
    assert point["payload"]["document_id"] == "refund_policy_2026"
    assert point["payload"]["chunk_id"] == "section-3:0"
    assert point["payload"]["citation"] == "refund_policy_2026#section-3"
    assert point["payload"]["text"] == "客户三天未发货可以申请退款。"
    assert point["payload"]["acl_tags"] == ["after_sales"]
    assert point["payload"]["chunking_strategy"] == "structure-aware-v1"


def test_markdown_source_to_qdrant_chunks_preserves_source_metadata(tmp_path):
    source_path = tmp_path / "refund_policy_docs.md"
    source_path.write_text(
        "# 售后退款规则\n\n客户三天未发货可以申请退款。\n\n退款处理需要保留订单编号。",
        encoding="utf-8",
    )

    chunks = markdown_source_to_qdrant_chunks(
        source_id="refund_policy_docs",
        source_path=source_path,
        content=source_path.read_text(encoding="utf-8"),
    )

    assert [chunk.chunk_id for chunk in chunks] == ["chunk-1", "chunk-2"]
    assert chunks[0].point_id == "refund_policy_2026:chunk-1"
    assert chunks[0].document_id == "refund_policy_2026"
    assert chunks[0].title == "售后退款规则"
    assert chunks[0].citation == "refund_policy_2026#section-3"
    assert chunks[0].text == "客户三天未发货可以申请退款。"
    assert chunks[0].metadata["tenant_id"] == "default"
    assert chunks[0].metadata["chunking_strategy"] == "markdown-paragraph-v1"
    assert chunks[0].metadata["source_path"] == str(source_path)


def test_markdown_source_to_qdrant_chunks_uses_known_business_citations(tmp_path):
    source_path = tmp_path / "logistics_faq.md"
    source_path.write_text(
        "# 物流常见问题\n\n"
        "物流轨迹超过二十四小时未更新时，应先联系承运商确认揽收和中转状态。\n\n"
        "同城即时配送超过两小时未送达时，客服应优先核实骑手位置和收件人联系方式。\n\n"
        "承运商确认包裹丢失后，客服应创建物流异常工单，并同步售后团队评估补发或退款。\n\n"
        "工作流缩写 LST-BATCH-OPS 是批量物流异常升级代号；样例订单 ORD-ZS-2026-0007 用于演示承运商网点滞留后的拦截和升级凭据。\n\n"
        "用户要求修改收货地址时，如果订单已经出库，应先联系承运商拦截。\n\n"
        "批量物流异常处理中，如果同一承运商在一个小时内出现五单以上轨迹停滞。",
        encoding="utf-8",
    )

    chunks = markdown_source_to_qdrant_chunks(
        source_id="logistics_faq",
        source_path=source_path,
        content=source_path.read_text(encoding="utf-8"),
    )

    assert [chunk.citation for chunk in chunks] == [
        "logistics_faq_2026#delay",
        "logistics_faq_2026#same-city-timeout",
        "logistics_faq_2026#lost-package",
        "logistics_faq_2026#exact-logistics-id",
        "logistics_faq_2026#address-intercept",
        "logistics_faq_2026#batch-exception",
    ]


def test_markdown_source_to_qdrant_chunks_uses_exact_term_refund_citation(tmp_path):
    source_path = tmp_path / "refund_policy_docs.md"
    source_path.write_text(
        "# 售后退款规则\n\n"
        "客户三天未发货可以申请退款，售后专员应核验订单状态和发货记录后处理。\n\n"
        "退款处理需要保留订单编号、付款记录、售后沟通记录和处理人信息。\n\n"
        "政策编号 RFD-2026-003 适用于三天未发货退款复核；售后专员需填写表单 AF-REFUND-02，并关联原订单编号和付款凭证。",
        encoding="utf-8",
    )

    chunks = markdown_source_to_qdrant_chunks(
        source_id="refund_policy_docs",
        source_path=source_path,
        content=source_path.read_text(encoding="utf-8"),
    )

    assert chunks[2].citation == "refund_policy_2026#exact-refund-code"


def test_markdown_source_to_qdrant_chunks_falls_back_for_unmapped_paragraphs(tmp_path):
    source_path = tmp_path / "unknown_docs.md"
    source_path.write_text(
        "# 未知文档\n\n第一段。\n\n第二段。",
        encoding="utf-8",
    )

    chunks = markdown_source_to_qdrant_chunks(
        source_id="unknown_docs",
        source_path=source_path,
        content=source_path.read_text(encoding="utf-8"),
    )

    assert [chunk.citation for chunk in chunks] == [
        "unknown_docs#chunk-1",
        "unknown_docs#chunk-2",
    ]


def test_markdown_source_to_section_chunks_groups_heading_content(tmp_path):
    source_path = tmp_path / "refund_policy_docs.md"
    source_path.write_text(
        "# 售后退款规则\n\n"
        "客户三天未发货可以申请退款。\n\n"
        "退款处理需要保留订单编号。\n\n"
        "## 退款申诉复核\n\n"
        "退款申诉复核场景中，应提交二线审核。",
        encoding="utf-8",
    )

    chunks = markdown_source_to_section_chunks(
        source_id="refund_policy_docs",
        source_path=source_path,
        content=source_path.read_text(encoding="utf-8"),
    )

    assert [chunk.chunk_id for chunk in chunks] == ["section-1", "section-2"]
    assert chunks[0].citation == "refund_policy_2026#section-candidate"
    assert chunks[1].citation == "refund_policy_2026#section-2"
    assert chunks[0].title == "售后退款规则"
    assert chunks[1].title == "退款申诉复核"
    assert chunks[0].metadata["chunking_strategy"] == "markdown-section-v1"
    assert "客户三天未发货" in chunks[0].text
    assert "二线审核" in chunks[1].text


def test_markdown_source_to_token_window_chunks_overlap_and_metadata(tmp_path):
    source_path = tmp_path / "refund_policy_docs.md"
    source_path.write_text(
        "# 售后退款规则\n\n"
        "客户三天未发货可以申请退款，并且客服需要保留订单编号和沟通记录。",
        encoding="utf-8",
    )

    chunks = markdown_source_to_token_window_chunks(
        source_id="refund_policy_docs",
        source_path=source_path,
        content=source_path.read_text(encoding="utf-8"),
        max_tokens=12,
        overlap_tokens=4,
        min_tokens=4,
    )

    assert [chunk.chunk_id for chunk in chunks] == [
        "token-window-1",
        "token-window-2",
        "token-window-3",
        "token-window-4",
    ]
    assert chunks[0].point_id == "refund_policy_2026:token-window-1"
    assert chunks[0].citation == "refund_policy_2026#token-window-candidate-1"
    assert chunks[1].citation == "refund_policy_2026#token-window-2"
    assert chunks[0].metadata["chunking_strategy"] == "token-window-v1"
    assert chunks[0].metadata["token_window_max_tokens"] == 12
    assert chunks[0].metadata["token_window_overlap_tokens"] == 4
    assert chunks[0].metadata["token_window_min_tokens"] == 4
    assert chunks[0].text[-4:] == chunks[1].text[:4]


def test_markdown_source_to_token_window_chunks_rejects_invalid_settings(tmp_path):
    source_path = tmp_path / "unknown_docs.md"
    source_path.write_text("# 未知文档\n\n第一段。", encoding="utf-8")

    for kwargs, expected_message in [
        ({"max_tokens": 0}, "max_tokens"),
        ({"overlap_tokens": -1}, "overlap_tokens"),
        ({"max_tokens": 4, "overlap_tokens": 4}, "overlap_tokens"),
        ({"max_tokens": 4, "overlap_tokens": 1, "min_tokens": 5}, "min_tokens"),
    ]:
        try:
            markdown_source_to_token_window_chunks(
                source_id="unknown_docs",
                source_path=source_path,
                content=source_path.read_text(encoding="utf-8"),
                **kwargs,
            )
        except ValueError as error:
            assert expected_message in str(error)
        else:
            raise AssertionError("Expected invalid token-window settings to fail")


def test_qdrant_payload_filter_includes_tenant_sources_and_acl():
    payload_filter = build_qdrant_payload_filter(
        source_ids=["refund_policy_docs", "logistics_faq"],
        tenant_id="tenant-a",
        document_ids=["refund_policy_2026"],
        acl_tags=["after_sales"],
    )

    assert payload_filter == {
        "must": [
            {"key": "tenant_id", "match": {"value": "tenant-a"}},
            {
                "key": "source_id",
                "match": {"any": ["refund_policy_docs", "logistics_faq"]},
            },
            {"key": "document_id", "match": {"any": ["refund_policy_2026"]}},
            {"key": "acl_tags", "match": {"any": ["after_sales"]}},
        ]
    }


def test_qdrant_candidate_metadata_leaves_embedding_undecided():
    candidate = qdrant_retrieval_candidate(
        Settings(
            qdrant_collection="enterprise_chunks",
            qdrant_vector_name="text-dense",
        )
    )

    assert candidate.id == "qdrant-candidate"
    assert candidate.backend == "qdrant"
    assert candidate.metadata == {
        "vector_store": "qdrant",
        "collection": "enterprise_chunks",
        "vector_name": "text-dense",
        "embedding": "undecided",
        "reranker": "undecided",
        "deployment_path": "local-public-test-or-private-network",
    }


def test_qdrant_retriever_is_opt_in_and_reports_not_ready_sources(monkeypatch):
    monkeypatch.setattr(
        "app.services.qdrant_vector_store.create_qdrant_client",
        lambda settings: FakeQdrantClient(),
    )
    monkeypatch.setattr(
        "app.services.qdrant_vector_store.ensure_qdrant_collection",
        lambda client, settings: ("ready", None),
    )
    monkeypatch.setattr(
        "app.services.qdrant_vector_store.query_qdrant_documents_for_text",
        lambda **kwargs: [],
    )
    retriever = create_document_retriever(Settings(rag_retrieval_backend="qdrant"))

    backend_status, reason = retriever.readiness()
    unknown_sources, documents = retriever.retrieve(
        query="客户三天未发货能否退款？",
        knowledge_base_ids=["refund_policy_docs"],
        top_k=3,
    )

    assert retriever.backend_name == "qdrant"
    assert backend_status == "ready"
    assert reason is None
    assert unknown_sources == []
    assert documents == []
    assert retriever.not_ready_sources(["refund_policy_docs"]) == ["refund_policy_docs"]


def test_qdrant_retriever_reads_persisted_source_readiness(tmp_path):
    settings = Settings(
        rag_retrieval_backend="qdrant",
        rag_index_dir=tmp_path / "index",
    )
    IndexLifecycleStore(settings).write_source_status(IndexStatusResponse(
        source_id="refund_policy_docs",
        status="ready",
        backend="qdrant",
        indexed_at="2026-05-28T00:00:00+00:00",
        latest_job_id="idx_ready",
    ))

    retriever = create_document_retriever(settings)

    assert retriever.not_ready_sources(["refund_policy_docs"]) == []
    assert retriever.not_ready_sources(["refund_policy_docs", "logistics_faq"]) == [
        "logistics_faq"
    ]


def test_create_qdrant_client_supports_local_memory_mode():
    client = create_qdrant_client(Settings(qdrant_url=":memory:"))

    assert client is not None


def test_ensure_qdrant_collection_reports_existing_collection_ready():
    client = FakeQdrantClient(collection_exists=True)

    status, reason = ensure_qdrant_collection(client, Settings())

    assert status == "ready"
    assert reason is None
    assert client.created_collections == []


def test_ensure_qdrant_collection_creates_missing_collection():
    client = FakeQdrantClient(collection_exists=False)
    settings = Settings(qdrant_collection="enterprise_chunks")

    status, reason = ensure_qdrant_collection(client, settings)

    assert status == "ready"
    assert reason is None
    assert client.created_collections[0]["collection_name"] == "enterprise_chunks"
    assert "text-dense" in client.created_collections[0]["vectors_config"]


def test_ensure_qdrant_collection_reports_degraded_on_failure():
    status, reason = ensure_qdrant_collection(FakeQdrantClient(fail=True), Settings())

    assert status == "degraded"
    assert "qdrant unavailable" in reason


def test_upsert_qdrant_chunks_writes_existing_payload_contract():
    client = FakeQdrantClient()
    settings = Settings(qdrant_collection="enterprise_chunks")
    chunk = VectorEvidenceChunk(
        point_id="refund_policy_2026:section-3:0",
        source_id="refund_policy_docs",
        document_id="refund_policy_2026",
        chunk_id="section-3:0",
        title="售后退款规则",
        text="客户三天未发货可以申请退款。",
        citation="refund_policy_2026#section-3",
        vector=[0.1, 0.2, 0.3],
        metadata={"tenant_id": "tenant-a", "acl_tags": ["after_sales"]},
    )

    count = upsert_qdrant_chunks(client, [chunk], settings)

    assert count == 1
    assert client.upserts[0]["collection_name"] == "enterprise_chunks"
    assert client.upserts[0]["wait"] is True
    point = client.upserts[0]["points"][0]
    assert point.payload["tenant_id"] == "tenant-a"
    assert point.payload["citation"] == "refund_policy_2026#section-3"
    assert point.vector == {"text-dense": [0.1, 0.2, 0.3]}


def test_build_qdrant_source_index_embeds_upserts_and_marks_ready(tmp_path):
    source_dir = tmp_path / "sources"
    source_dir.mkdir()
    (source_dir / "refund_policy_docs.md").write_text(
        "# 售后退款规则\n\n客户三天未发货可以申请退款。\n\n退款处理需要保留订单编号。",
        encoding="utf-8",
    )
    settings = Settings(
        rag_retrieval_backend="qdrant",
        rag_source_dir=source_dir,
        rag_index_dir=tmp_path / "index",
        embedding_vector_size=3,
    )
    client = FakeQdrantClient(collection_exists=False)

    count = build_qdrant_source_index(
        "refund_policy_docs",
        settings,
        latest_job_id="idx_qdrant_test",
        client=client,
    )

    assert count == 2
    assert client.created_collections
    assert len(client.upserts[0]["points"]) == 2
    first_point = client.upserts[0]["points"][0]
    assert first_point.payload["source_id"] == "refund_policy_docs"
    assert first_point.payload["document_id"] == "refund_policy_2026"
    assert first_point.payload["citation"] == "refund_policy_2026#section-3"
    assert first_point.payload["embedding_provider"] == "mock"
    assert first_point.payload["embedding_model"] == "mock-hash-v1"
    assert first_point.payload["chunking_strategy"] == "markdown-paragraph-v1"
    assert len(first_point.vector["text-dense"]) == 3

    status = get_index_status("refund_policy_docs", settings)
    assert status.status == "ready"
    assert status.backend == "qdrant"
    assert status.latest_job_id == "idx_qdrant_test"


def test_query_qdrant_documents_maps_valid_hits_and_skips_malformed_hits():
    client = FakeQdrantClient(
        hits=[
            {
                "score": 0.91,
                "payload": {
                    "source_id": "refund_policy_docs",
                    "document_id": "refund_policy_2026",
                    "title": "售后退款规则",
                    "text": "客户三天未发货可以申请退款。",
                    "citation": "refund_policy_2026#section-3",
                },
            },
            {"score": 0.5, "payload": {"source_id": "refund_policy_docs"}},
        ]
    )

    documents = query_qdrant_documents(
        client,
        query_vector=[0.1, 0.2, 0.3],
        source_ids=["refund_policy_docs"],
        settings=Settings(qdrant_collection="enterprise_chunks"),
        top_k=3,
        tenant_id="tenant-a",
        acl_tags=["after_sales"],
    )

    assert len(documents) == 1
    assert documents[0].source_id == "refund_policy_docs"
    assert documents[0].document_id == "refund_policy_2026"
    assert documents[0].snippet == "客户三天未发货可以申请退款。"
    assert documents[0].score == 0.91
    assert documents[0].citation == "refund_policy_2026#section-3"
    assert client.queries[0]["collection_name"] == "enterprise_chunks"
    assert client.queries[0]["query"] == [0.1, 0.2, 0.3]
    assert client.queries[0]["using"] == "text-dense"
    assert client.queries[0]["limit"] == 3
    assert client.queries[0]["query_filter"].model_dump(exclude_none=True) == {
        "must": [
            {"key": "tenant_id", "match": {"value": "tenant-a"}},
            {"key": "source_id", "match": {"any": ["refund_policy_docs"]}},
            {"key": "acl_tags", "match": {"any": ["after_sales"]}},
        ]
    }


def test_query_qdrant_documents_filters_hits_below_score_threshold():
    client = FakeQdrantClient(
        hits=[
            {
                "score": 0.42,
                "payload": {
                    "source_id": "refund_policy_docs",
                    "document_id": "refund_policy_2026",
                    "title": "售后退款规则",
                    "text": "低置信命中。",
                    "citation": "refund_policy_2026#chunk-low",
                },
            },
            {
                "score": 0.88,
                "payload": {
                    "source_id": "refund_policy_docs",
                    "document_id": "refund_policy_2026",
                    "title": "售后退款规则",
                    "text": "高置信命中。",
                    "citation": "refund_policy_2026#chunk-high",
                },
            },
        ]
    )

    documents = query_qdrant_documents(
        client,
        query_vector=[0.1, 0.2, 0.3],
        source_ids=["refund_policy_docs"],
        settings=Settings(rag_score_threshold=0.5),
        top_k=3,
    )

    assert [document.citation for document in documents] == [
        "refund_policy_2026#chunk-high"
    ]


def test_query_qdrant_documents_returns_empty_when_all_hits_below_threshold():
    client = FakeQdrantClient(
        hits=[
            {
                "score": 0.3,
                "payload": {
                    "source_id": "refund_policy_docs",
                    "document_id": "refund_policy_2026",
                    "title": "售后退款规则",
                    "text": "低置信命中。",
                    "citation": "refund_policy_2026#chunk-low",
                },
            }
        ]
    )

    documents = query_qdrant_documents(
        client,
        query_vector=[0.1, 0.2, 0.3],
        source_ids=["refund_policy_docs"],
        settings=Settings(rag_score_threshold=0.5),
        top_k=3,
    )

    assert documents == []


def test_query_qdrant_documents_for_text_embeds_query_before_vector_search():
    from app.services.embedding_adapters import MockEmbeddingAdapter

    client = FakeQdrantClient(
        hits=[
            {
                "score": 0.8,
                "payload": {
                    "source_id": "refund_policy_docs",
                    "document_id": "refund_policy_2026",
                    "title": "售后退款规则",
                    "text": "客户三天未发货可以申请退款。",
                    "citation": "refund_policy_2026#section-3",
                },
            }
        ]
    )
    settings = Settings(embedding_vector_size=3)
    adapter = MockEmbeddingAdapter(settings)

    documents = query_qdrant_documents_for_text(
        client=client,
        query="客户三天未发货能否退款？",
        source_ids=["refund_policy_docs"],
        settings=settings,
        embedding_adapter=adapter,
        top_k=1,
        tenant_id="tenant-a",
    )

    assert len(documents) == 1
    assert client.queries[0]["query"] == adapter.embed_text("客户三天未发货能否退款？")
    assert client.queries[0]["query_filter"].model_dump(exclude_none=True) == {
        "must": [
            {"key": "tenant_id", "match": {"value": "tenant-a"}},
            {"key": "source_id", "match": {"any": ["refund_policy_docs"]}},
        ]
    }


def test_qdrant_retriever_uses_text_query_orchestration(monkeypatch):
    from app.models.contracts import EvidenceDocument

    captured = {}

    def fake_query(**kwargs):
        captured.update(kwargs)
        return [
            EvidenceDocument(
                source_id="refund_policy_docs",
                document_id="refund_policy_2026",
                title="售后退款规则",
                snippet="客户三天未发货可以申请退款。",
                score=0.88,
                citation="refund_policy_2026#section-3",
            )
        ]

    monkeypatch.setattr(
        "app.services.qdrant_vector_store.create_qdrant_client",
        lambda settings: FakeQdrantClient(),
    )
    monkeypatch.setattr(
        "app.services.qdrant_vector_store.query_qdrant_documents_for_text",
        fake_query,
    )

    retriever = create_document_retriever(
        Settings(rag_retrieval_backend="qdrant", embedding_vector_size=3)
    )
    unknown_sources, documents = retriever.retrieve(
        query="客户三天未发货能否退款？",
        knowledge_base_ids=["refund_policy_docs"],
        top_k=2,
    )

    assert unknown_sources == []
    assert documents[0].citation == "refund_policy_2026#section-3"
    assert captured["query"] == "客户三天未发货能否退款？"
    assert captured["source_ids"] == ["refund_policy_docs"]
    assert captured["top_k"] == 2
    assert captured["embedding_adapter"].provider_name == "mock"


def test_qdrant_retriever_readiness_degrades_when_embedding_not_ready(monkeypatch):
    monkeypatch.setattr(
        "app.services.qdrant_vector_store.create_qdrant_client",
        lambda settings: FakeQdrantClient(),
    )
    monkeypatch.setattr(
        "app.services.qdrant_vector_store.ensure_qdrant_collection",
        lambda client, settings: ("ready", None),
    )

    retriever = create_document_retriever(
        Settings(rag_retrieval_backend="qdrant", embedding_provider="hosted")
    )

    status, reason = retriever.readiness()

    assert status == "degraded"
    assert "Embedding adapter not ready" in reason
