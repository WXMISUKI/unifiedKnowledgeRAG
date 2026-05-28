import os
from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    rag_retrieval_backend: str = Field(default="fixture")
    rag_index_dir: Path = Field(default=Path("app/data/indexes/llamaindex"))
    rag_source_dir: Path = Field(default=Path("app/data/sources"))
    rag_score_threshold: float = Field(default=0.01, ge=0.0, le=1.0)
    qdrant_url: str = Field(default="http://localhost:6333")
    qdrant_api_key: str | None = Field(default=None)
    qdrant_collection: str = Field(default="knowledge_chunks")
    qdrant_vector_name: str = Field(default="text-dense")
    qdrant_vector_size: int = Field(default=1024, ge=1)
    embedding_provider: str = Field(default="mock")
    embedding_model: str = Field(default="mock-hash-v1")
    embedding_vector_size: int | None = Field(default=None, ge=1)


def get_settings() -> Settings:
    return Settings(
        rag_retrieval_backend=os.getenv("RAG_RETRIEVAL_BACKEND", "fixture"),
        rag_index_dir=Path(os.getenv("RAG_INDEX_DIR", "app/data/indexes/llamaindex")),
        rag_source_dir=Path(os.getenv("RAG_SOURCE_DIR", "app/data/sources")),
        rag_score_threshold=float(os.getenv("RAG_SCORE_THRESHOLD", "0.01")),
        qdrant_url=os.getenv("QDRANT_URL", "http://localhost:6333"),
        qdrant_api_key=os.getenv("QDRANT_API_KEY"),
        qdrant_collection=os.getenv("QDRANT_COLLECTION", "knowledge_chunks"),
        qdrant_vector_name=os.getenv("QDRANT_VECTOR_NAME", "text-dense"),
        qdrant_vector_size=int(os.getenv("QDRANT_VECTOR_SIZE", "1024")),
        embedding_provider=os.getenv("EMBEDDING_PROVIDER", "mock"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "mock-hash-v1"),
        embedding_vector_size=(
            int(os.getenv("EMBEDDING_VECTOR_SIZE"))
            if os.getenv("EMBEDDING_VECTOR_SIZE")
            else None
        ),
    )
