from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_health_endpoint_returns_ok(monkeypatch):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_favicon_is_served_at_conventional_browser_url():
    response = client.get("/favicon.ico")

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/svg+xml"
    assert "Cocktail glass" in response.text


def test_cocktails_endpoint_uses_service(monkeypatch):
    monkeypatch.setattr(
        "src.main.cocktail_service.get_all_cocktails",
        lambda: [{"id": 1, "name": "Margarita", "spirit": "Tequila"}],
    )

    response = client.get("/cocktails")

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Margarita", "spirit": "Tequila"}]
