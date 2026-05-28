import hashlib
import math
from abc import ABC, abstractmethod

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


def create_embedding_adapter(settings: Settings) -> EmbeddingAdapter:
    provider = settings.embedding_provider.lower()
    if provider == "mock":
        return MockEmbeddingAdapter(settings)
    if provider == "hosted":
        return HostedEmbeddingAdapter(settings)
    if provider == "local":
        return LocalEmbeddingAdapter(settings)
    raise ValueError(f"Unsupported EMBEDDING_PROVIDER: {settings.embedding_provider}")
