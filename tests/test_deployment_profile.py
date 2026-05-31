from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_dockerfile_starts_provider_on_expected_port():
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")

    assert "FROM python:3.11-slim" in dockerfile
    assert "EXPOSE 8020" in dockerfile
    assert '"uvicorn", "app.main:app"' in dockerfile
    assert "--port\", \"8020" in dockerfile


def test_dockerignore_excludes_runtime_state_and_generated_evidence():
    dockerignore = (ROOT / ".dockerignore").read_text(encoding="utf-8")

    assert "models/" in dockerignore
    assert "app/data/indexes/" in dockerignore
    assert "docs/benchmark/" in dockerignore
    assert "docs/integration/" in dockerignore
    assert "tests/" in dockerignore


def test_compose_profile_mounts_runtime_state_and_uses_readiness_probe():
    compose = (ROOT / "docker-compose.example.yml").read_text(encoding="utf-8")

    assert "8020:8020" in compose
    assert "./app/data/sources:/app/app/data/sources:ro" in compose
    assert "./app/data/indexes:/app/app/data/indexes" in compose
    assert "./models:/models:ro" in compose
    assert "http://127.0.0.1:8020/ready" in compose
    assert "qdrant:" not in compose


def test_env_example_uses_safe_defaults_and_placeholder_secrets():
    env_example = (ROOT / ".env.example").read_text(encoding="utf-8")

    assert "PROVIDER_API_KEY=replace-with-random-token" in env_example
    assert "RAG_RETRIEVAL_BACKEND=fixture" in env_example
    assert "EMBEDDING_PROVIDER=mock" in env_example
    assert "RAG_ANSWER_COMPOSER=deterministic" in env_example
    assert "QDRANT_API_KEY=replace-with-qdrant-token" in env_example
