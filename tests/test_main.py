import logging

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from src.config import settings
from src.main import app

client = TestClient(app)

VALID_COCKTAIL = {
    "id": 7,
    "name": "Martini",
    "spirit": "Gin",
    "ingredients": ["Gin", "Vermouth"],
}


def test_legacy_health_endpoint_remains_compatible():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_liveness_endpoint_returns_healthy():
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": app.title,
        "version": app.version,
    }


def test_liveness_endpoint_does_not_check_dynamodb(monkeypatch):
    def fail_if_called() -> bool:
        raise AssertionError("Liveness must not check DynamoDB")

    monkeypatch.setattr(
        "src.main.health_service.is_dynamodb_ready",
        fail_if_called,
    )

    response = client.get("/health/live")

    assert response.status_code == 200


def test_legacy_health_endpoint_does_not_check_dynamodb(monkeypatch):
    def fail_if_called() -> bool:
        raise AssertionError("Legacy health must not check DynamoDB")

    monkeypatch.setattr(
        "src.main.health_service.is_dynamodb_ready",
        fail_if_called,
    )

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_endpoint_returns_200_when_dynamodb_is_ready(monkeypatch):
    monkeypatch.setattr(
        "src.main.health_service.is_dynamodb_ready",
        lambda: True,
    )

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": app.title,
        "version": app.version,
        "dependencies": {
            "dynamodb": {
                "status": "healthy",
            }
        },
    }


def test_readiness_endpoint_returns_503_when_dynamodb_is_unavailable(
    monkeypatch,
):
    monkeypatch.setattr(
        "src.main.health_service.is_dynamodb_ready",
        lambda: False,
    )

    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "unhealthy",
        "service": app.title,
        "version": app.version,
        "dependencies": {
            "dynamodb": {
                "status": "unhealthy",
            }
        },
    }
    assert "detail" not in response.json()


def test_unhealthy_readiness_response_does_not_expose_dependency_details(
    monkeypatch,
):
    monkeypatch.setattr(
        "src.main.health_service.is_dynamodb_ready",
        lambda: False,
    )

    response = client.get("/health/ready")
    response_text = response.text.lower()

    assert response.status_code == 503
    for sensitive_value in (
        "access denied",
        "cocktails",
        "ap-southeast-2",
        "clienterror",
        "traceback",
    ):
        assert sensitive_value not in response_text


def test_successful_health_endpoints_do_not_log_at_info(monkeypatch, caplog):
    monkeypatch.setattr(
        "src.main.health_service.is_dynamodb_ready",
        lambda: True,
    )

    with caplog.at_level(logging.INFO, logger="cocktail_api"):
        responses = [
            client.get("/health"),
            client.get("/health/live"),
            client.get("/health/ready"),
        ]

    assert all(response.status_code == 200 for response in responses)
    assert not [
        record
        for record in caplog.records
        if record.name == "cocktail_api" and record.levelno >= logging.INFO
    ]


def test_openapi_version_matches_current_release():
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["version"] == "0.4.0"


def test_application_metadata_uses_central_settings():
    assert app.title == settings.app_name
    assert app.version == settings.app_version


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


@pytest.mark.parametrize("missing_field", VALID_COCKTAIL)
def test_create_rejects_missing_required_fields(missing_field):
    payload = {
        key: value for key, value in VALID_COCKTAIL.items() if key != missing_field
    }

    response = client.post("/cocktails", json=payload)

    assert response.status_code == 422
    assert isinstance(response.json()["detail"], list)
    assert any(missing_field in error["loc"] for error in response.json()["detail"])


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("id", "not-a-number"),
        ("ingredients", "Gin"),
        ("name", {"unexpected": "mapping"}),
        ("spirit", ["Gin"]),
    ],
)
def test_create_rejects_invalid_field_types(field, invalid_value):
    payload = {**VALID_COCKTAIL, field: invalid_value}

    response = client.post("/cocktails", json=payload)

    assert response.status_code == 422


def test_invalid_create_does_not_call_service_or_log_success(
    monkeypatch,
    caplog,
):
    def fail_if_called(cocktail):
        raise AssertionError("Invalid payload must not reach the service")

    monkeypatch.setattr(
        "src.main.cocktail_service.create_cocktail",
        fail_if_called,
    )

    with caplog.at_level(logging.INFO, logger="cocktail_api"):
        response = client.post(
            "/cocktails",
            json={**VALID_COCKTAIL, "id": "not-a-number"},
        )

    assert response.status_code == 422
    assert not any(
        "Cocktail created" in record.getMessage()
        for record in caplog.records
        if record.name == "cocktail_api"
    )


def test_invalid_update_does_not_call_service(monkeypatch):
    def fail_if_called(cocktail_id, cocktail):
        raise AssertionError("Invalid payload must not reach the service")

    monkeypatch.setattr(
        "src.main.cocktail_service.update_cocktail",
        fail_if_called,
    )

    response = client.put(
        "/cocktails/7",
        json={**VALID_COCKTAIL, "ingredients": "Gin"},
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("GET", "/cocktails/not-a-number"),
        ("PUT", "/cocktails/not-a-number"),
        ("DELETE", "/cocktails/not-a-number"),
        ("GET", "/cocktails/html/not-a-number"),
    ],
)
def test_routes_reject_non_integer_cocktail_ids(method, path):
    response = client.request(
        method,
        path,
        json=VALID_COCKTAIL if method == "PUT" else None,
    )

    assert response.status_code == 422


def test_get_missing_cocktail_returns_404(monkeypatch):
    def raise_not_found(cocktail_id):
        raise HTTPException(status_code=404, detail="Cocktail not found")

    monkeypatch.setattr(
        "src.main.cocktail_service.get_cocktail",
        raise_not_found,
    )

    response = client.get("/cocktails/123")

    assert response.status_code == 404
    assert response.json() == {"detail": "Cocktail not found"}


def test_delete_missing_cocktail_returns_404(monkeypatch):
    def raise_not_found(cocktail_id):
        raise HTTPException(status_code=404, detail="Cocktail not found")

    monkeypatch.setattr(
        "src.main.cocktail_service.delete_cocktail",
        raise_not_found,
    )

    response = client.delete("/cocktails/123")

    assert response.status_code == 404
    assert response.json() == {"detail": "Cocktail not found"}


def test_update_missing_cocktail_returns_404(monkeypatch):
    def raise_not_found(cocktail_id, cocktail):
        raise HTTPException(status_code=404, detail="Cocktail not found")

    monkeypatch.setattr(
        "src.main.cocktail_service.update_cocktail",
        raise_not_found,
    )

    response = client.put("/cocktails/123", json=VALID_COCKTAIL)

    assert response.status_code == 404
    assert response.json() == {"detail": "Cocktail not found"}


def test_unhandled_service_failure_returns_500_without_details(monkeypatch):
    def raise_database_failure():
        raise RuntimeError("sensitive database failure")

    monkeypatch.setattr(
        "src.main.cocktail_service.get_all_cocktails",
        raise_database_failure,
    )
    failure_client = TestClient(app, raise_server_exceptions=False)

    response = failure_client.get("/cocktails")

    assert response.status_code == 500
    assert "sensitive database failure" not in response.text


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


def test_cocktail_html_does_not_duplicate_not_found_log(monkeypatch, caplog):
    def raise_not_found(cocktail_id: int):
        raise HTTPException(status_code=404, detail="Cocktail not found")

    monkeypatch.setattr(
        "src.main.cocktail_service.get_cocktail",
        raise_not_found,
    )

    with caplog.at_level(logging.DEBUG, logger="cocktail_api"):
        response = client.get("/cocktails/html/123")

    assert response.status_code == 404
    assert response.json() == {"detail": "Cocktail not found"}
    assert not [record for record in caplog.records if record.name == "cocktail_api"]
