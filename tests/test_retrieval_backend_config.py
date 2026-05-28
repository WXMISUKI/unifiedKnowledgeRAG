from app.config import Settings
from app.services.retrieval_backends import FixtureDocumentRetriever, LlamaIndexDocumentRetriever, create_document_retriever


def test_fixture_backend_is_selected_from_settings():
    settings = Settings(rag_retrieval_backend="fixture")

    retriever = create_document_retriever(settings)

    assert isinstance(retriever, FixtureDocumentRetriever)
    assert retriever.backend_name == "fixture"


def test_llamaindex_backend_is_selected_from_settings(tmp_path):
    settings = Settings(
        rag_retrieval_backend="llamaindex",
        rag_index_dir=tmp_path / "index",
        rag_source_dir=tmp_path / "sources",
    )

    retriever = create_document_retriever(settings)

    assert isinstance(retriever, LlamaIndexDocumentRetriever)
    assert retriever.backend_name == "llamaindex"
