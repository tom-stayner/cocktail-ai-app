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


def test_html_collection_routes_use_service(monkeypatch):
    cocktails = [
        {
            "id": 1,
            "name": "Margarita",
            "spirit": "Tequila",
            "ingredients": ["Tequila", "Lime juice"],
        }
    ]
    monkeypatch.setattr(
        "src.main.cocktail_service.get_all_cocktails",
        lambda: cocktails,
    )

    home_response = client.get("/")
    library_response = client.get("/cocktails/html")

    assert home_response.status_code == 200
    assert library_response.status_code == 200
    assert "Margarita" in home_response.text
    assert "Tequila" in library_response.text


def test_cocktail_html_uses_service(monkeypatch):
    monkeypatch.setattr(
        "src.main.cocktail_service.get_cocktail",
        lambda cocktail_id: {
            "id": cocktail_id,
            "name": "Margarita",
            "spirit": "Tequila",
            "ingredients": ["Tequila", "Lime juice"],
        },
    )

    response = client.get("/cocktails/html/1")

    assert response.status_code == 200
    assert "Margarita" in response.text
    assert "Lime juice" in response.text
