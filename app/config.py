import os
from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    rag_retrieval_backend: str = Field(default="fixture")
    rag_index_dir: Path = Field(default=Path("app/data/indexes/llamaindex"))
    rag_source_dir: Path = Field(default=Path("app/data/sources"))
    rag_score_threshold: float = Field(default=0.01, ge=0.0, le=1.0)


def get_settings() -> Settings:
    return Settings(
        rag_retrieval_backend=os.getenv("RAG_RETRIEVAL_BACKEND", "fixture"),
        rag_index_dir=Path(os.getenv("RAG_INDEX_DIR", "app/data/indexes/llamaindex")),
        rag_source_dir=Path(os.getenv("RAG_SOURCE_DIR", "app/data/sources")),
        rag_score_threshold=float(os.getenv("RAG_SCORE_THRESHOLD", "0.01")),
    )
