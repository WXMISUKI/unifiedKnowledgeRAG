from fastapi.testclient import TestClient

from app.main import create_app


def test_api_routes_remain_open_when_provider_api_key_is_unset(monkeypatch):
    monkeypatch.delenv("PROVIDER_API_KEY", raising=False)
    client = TestClient(create_app())

    response = client.get("/api/provider/manifest")

    assert response.status_code == 200
    assert response.json()["provider_id"] == "unifiedKnowledgeProvider"


def test_api_route_rejects_missing_provider_api_key(monkeypatch):
    monkeypatch.setenv("PROVIDER_API_KEY", "secret-token")
    client = TestClient(create_app())

    response = client.get("/api/provider/manifest")

    assert response.status_code == 401
    assert response.json() == {
        "ok": False,
        "error": {
            "code": "PROVIDER_API_KEY_REQUIRED",
            "message": "A valid provider API key is required for this endpoint.",
        },
    }


def test_api_route_rejects_invalid_provider_api_key(monkeypatch):
    monkeypatch.setenv("PROVIDER_API_KEY", "secret-token")
    client = TestClient(create_app())

    response = client.get(
        "/api/provider/manifest",
        headers={"Authorization": "Bearer wrong-token"},
    )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "PROVIDER_API_KEY_REQUIRED"


def test_api_route_accepts_bearer_provider_api_key(monkeypatch):
    monkeypatch.setenv("PROVIDER_API_KEY", "secret-token")
    client = TestClient(create_app())

    response = client.get(
        "/api/provider/manifest",
        headers={"Authorization": "Bearer secret-token"},
    )

    assert response.status_code == 200
    assert response.json()["provider_id"] == "unifiedKnowledgeProvider"


def test_api_route_accepts_provider_api_key_header(monkeypatch):
    monkeypatch.setenv("PROVIDER_API_KEY", "secret-token")
    client = TestClient(create_app())

    response = client.get(
        "/api/provider/manifest",
        headers={"X-Provider-Api-Key": "secret-token"},
    )

    assert response.status_code == 200
    assert response.json()["provider_id"] == "unifiedKnowledgeProvider"


def test_health_remains_public_when_provider_api_key_is_set(monkeypatch):
    monkeypatch.setenv("PROVIDER_API_KEY", "secret-token")
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "unifiedKnowledgeProvider"
