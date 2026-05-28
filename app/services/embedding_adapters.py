import hashlib
import math
import os
from abc import ABC, abstractmethod
from importlib import import_module

from app.config import Settings


class EmbeddingAdapter(ABC):
    provider_name: str
    model_name: str
    vector_size: int

    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        raise NotImplementedError

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]

    def readiness(self) -> tuple[str, str | None]:
        return "ready", None


class MockEmbeddingAdapter(EmbeddingAdapter):
    provider_name = "mock"

    def __init__(self, settings: Settings):
        self.model_name = settings.embedding_model
        self.vector_size = settings.embedding_vector_size or settings.qdrant_vector_size

    def embed_text(self, text: str) -> list[float]:
        if not text:
            return [0.0] * self.vector_size
        vector = [0.0] * self.vector_size
        for index, byte in enumerate(hashlib.sha256(text.encode("utf-8")).digest()):
            vector[index % self.vector_size] += (byte / 255.0) - 0.5
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [round(value / norm, 6) for value in vector]


class HostedEmbeddingAdapter(EmbeddingAdapter):
    provider_name = "hosted"

    def __init__(self, settings: Settings):
        self.model_name = settings.embedding_model
        self.vector_size = settings.embedding_vector_size or settings.qdrant_vector_size

    def embed_text(self, text: str) -> list[float]:
        raise NotImplementedError("Hosted embedding adapter is not implemented yet.")

    def readiness(self) -> tuple[str, str | None]:
        return "degraded", "Hosted embedding provider is not approved or implemented yet."


class LocalEmbeddingAdapter(EmbeddingAdapter):
    provider_name = "local"

    def __init__(self, settings: Settings):
        self.model_name = settings.embedding_model
        self.vector_size = settings.embedding_vector_size or settings.qdrant_vector_size

    def embed_text(self, text: str) -> list[float]:
        raise NotImplementedError("Local embedding adapter is not implemented yet.")

    def readiness(self) -> tuple[str, str | None]:
        return "degraded", "Local embedding provider is not approved or implemented yet."


class BgeM3LocalEmbeddingAdapter(EmbeddingAdapter):
    provider_name = "bge_m3_local"

    def __init__(self, settings: Settings):
        self.settings = settings
        self.model_name = settings.embedding_model or "BAAI/bge-m3"
        self.vector_size = settings.embedding_vector_size or settings.qdrant_vector_size
        self._model = None

    def embed_text(self, text: str) -> list[float]:
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        output = self._load_model().encode(
            texts,
            batch_size=self.settings.bge_m3_batch_size,
            max_length=self.settings.bge_m3_max_length,
            return_dense=True,
            return_sparse=False,
            return_colbert_vecs=False,
        )
        vectors = output["dense_vecs"]
        normalized_vectors = [_as_float_list(vector) for vector in vectors]
        for vector in normalized_vectors:
            if len(vector) != self.vector_size:
                raise ValueError(
                    f"BGE-M3 vector size mismatch: expected {self.vector_size}, "
                    f"got {len(vector)}"
                )
        return normalized_vectors

    def readiness(self) -> tuple[str, str | None]:
        try:
            self._load_model()
        except Exception as error:
            return "degraded", f"BGE-M3 local embedding model is not ready: {error}"
        return "ready", None

    def _load_model(self):
        if self._model is not None:
            return self._model
        self._configure_huggingface_environment()
        flag_embedding = import_module("FlagEmbedding")
        model_path = (
            str(self.settings.embedding_model_path)
            if self.settings.embedding_model_path is not None
            else self.model_name
        )
        self._model = flag_embedding.BGEM3FlagModel(
            model_path,
            use_fp16=self.settings.bge_m3_use_fp16,
        )
        return self._model

    def _configure_huggingface_environment(self) -> None:
        if self.settings.embedding_hf_endpoint:
            os.environ["HF_ENDPOINT"] = self.settings.embedding_hf_endpoint
        if self.settings.embedding_local_files_only:
            os.environ["HF_HUB_OFFLINE"] = "1"
            os.environ["TRANSFORMERS_OFFLINE"] = "1"


def create_embedding_adapter(settings: Settings) -> EmbeddingAdapter:
    provider = settings.embedding_provider.lower()
    if provider == "mock":
        return MockEmbeddingAdapter(settings)
    if provider == "hosted":
        return HostedEmbeddingAdapter(settings)
    if provider == "local":
        return LocalEmbeddingAdapter(settings)
    if provider in {"bge_m3_local", "bge-m3-local", "bge_m3"}:
        return BgeM3LocalEmbeddingAdapter(settings)
    raise ValueError(f"Unsupported EMBEDDING_PROVIDER: {settings.embedding_provider}")


def _as_float_list(vector) -> list[float]:
    if hasattr(vector, "tolist"):
        vector = vector.tolist()
    return [float(value) for value in vector]
