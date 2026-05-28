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
    embedding_model_path: Path | None = Field(default=None)
    embedding_vector_size: int | None = Field(default=None, ge=1)
    embedding_hf_endpoint: str | None = Field(default=None)
    embedding_local_files_only: bool = Field(default=False)
    bge_m3_use_fp16: bool = Field(default=True)
    bge_m3_batch_size: int = Field(default=12, ge=1)
    bge_m3_max_length: int = Field(default=8192, ge=1)


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
        embedding_model_path=(
            Path(os.getenv("EMBEDDING_MODEL_PATH"))
            if os.getenv("EMBEDDING_MODEL_PATH")
            else None
        ),
        embedding_vector_size=(
            int(os.getenv("EMBEDDING_VECTOR_SIZE"))
            if os.getenv("EMBEDDING_VECTOR_SIZE")
            else None
        ),
        embedding_hf_endpoint=os.getenv("EMBEDDING_HF_ENDPOINT"),
        embedding_local_files_only=(
            os.getenv("EMBEDDING_LOCAL_FILES_ONLY", "false").lower()
            in {"1", "true", "yes", "on"}
        ),
        bge_m3_use_fp16=(
            os.getenv("BGE_M3_USE_FP16", "true").lower()
            in {"1", "true", "yes", "on"}
        ),
        bge_m3_batch_size=int(os.getenv("BGE_M3_BATCH_SIZE", "12")),
        bge_m3_max_length=int(os.getenv("BGE_M3_MAX_LENGTH", "8192")),
    )
