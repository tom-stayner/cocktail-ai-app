import base64
from dataclasses import replace
import json
from typing import Any

from src.config import settings
from src.lambda_handler import handler


def api_gateway_event(
    path: str,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    route_key = f"{method} {path}"
    event = {
        "version": "2.0",
        "routeKey": route_key,
        "rawPath": path,
        "rawQueryString": "",
        "headers": {
            "host": "example.execute-api.ap-southeast-2.amazonaws.com",
            "user-agent": "pytest",
        },
        "requestContext": {
            "http": {
                "method": method,
                "path": path,
                "protocol": "HTTP/1.1",
                "sourceIp": "127.0.0.1",
                "userAgent": "pytest",
            },
            "routeKey": route_key,
            "stage": "$default",
        },
        "isBase64Encoded": False,
    }

    if payload is not None:
        event["headers"]["content-type"] = "application/json"
        event["body"] = json.dumps(payload)

    return event


def response_body(response: dict[str, Any]) -> bytes:
    body = response["body"]

    if response.get("isBase64Encoded", False):
        return base64.b64decode(body)

    return body.encode()


def test_health_endpoint_through_lambda_handler():
    response = handler(api_gateway_event("/health"), {})

    assert response["statusCode"] == 200
    assert response["isBase64Encoded"] is False
    assert json.loads(response_body(response)) == {"status": "ok"}


def test_static_stylesheet_through_lambda_handler():
    response = handler(api_gateway_event("/static/main.css"), {})
    body = response_body(response).decode()

    assert response["statusCode"] == 200
    assert "text/css" in response["headers"]["content-type"]
    assert body
    assert ".card" in body


def test_favicon_through_lambda_handler():
    response = handler(api_gateway_event("/favicon.ico"), {})
    body = response_body(response)

    assert response["statusCode"] == 200
    assert "image/svg+xml" in response["headers"]["content-type"]
    assert body


def test_disabled_mutation_is_blocked_through_lambda_handler(monkeypatch):
    monkeypatch.setattr(
        "src.main.settings",
        replace(settings, allow_mutations=False),
    )

    def fail_if_called(cocktail):
        raise AssertionError("Disabled mutation must not reach the service")

    monkeypatch.setattr(
        "src.main.cocktail_service.create_cocktail",
        fail_if_called,
    )
    payload = {
        "id": 7,
        "name": "Martini",
        "spirit": "Gin",
        "ingredients": ["Gin", "Vermouth"],
    }

    response = handler(api_gateway_event("/cocktails", "POST", payload), {})

    assert response["statusCode"] == 403
    assert response["isBase64Encoded"] is False
    assert json.loads(response_body(response)) == {
        "detail": "Cocktail mutations are disabled"
    }
