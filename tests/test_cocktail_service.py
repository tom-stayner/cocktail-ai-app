import logging
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError
from fastapi import HTTPException

from src.models import Cocktail
from src.services import cocktail_service


def application_records(caplog):
    return [record for record in caplog.records if record.name == "cocktail_api"]


def test_collection_read_logs_one_debug_completion(monkeypatch, caplog):
    table = MagicMock()
    table.scan.return_value = {"Items": [{"id": 17}]}
    monkeypatch.setattr(cocktail_service, "table", table)

    with caplog.at_level(logging.DEBUG, logger="cocktail_api"):
        result = cocktail_service.get_all_cocktails()

    assert result == [{"id": 17}]
    records = application_records(caplog)
    assert len(records) == 1
    assert records[0].levelno == logging.DEBUG
    assert "Retrieved cocktail collection" in records[0].getMessage()


def test_get_cocktail_not_found_logs_info_not_warning(monkeypatch, caplog):
    table = MagicMock()
    table.get_item.return_value = {}
    monkeypatch.setattr(cocktail_service, "table", table)

    with caplog.at_level(logging.INFO, logger="cocktail_api"):
        with pytest.raises(HTTPException) as exception_info:
            cocktail_service.get_cocktail(123)

    assert exception_info.value.status_code == 404
    assert exception_info.value.detail == "Cocktail not found"
    table.get_item.assert_called_once_with(Key={"id": 123})
    records = application_records(caplog)
    assert any(
        record.levelno == logging.INFO and "Cocktail not found" in record.getMessage()
        for record in records
    )
    assert not any(record.levelno == logging.WARNING for record in records)


def test_create_cocktail_logs_one_safe_info_completion(monkeypatch, caplog):
    table = MagicMock()
    monkeypatch.setattr(cocktail_service, "table", table)
    cocktail = Cocktail(
        id=17,
        name="User\nSupplied Name",
        spirit="Gin",
        ingredients=["Gin"],
    )

    with caplog.at_level(logging.INFO, logger="cocktail_api"):
        result = cocktail_service.create_cocktail(cocktail)

    assert result == {"message": "Cocktail added successfully"}
    records = [
        record
        for record in application_records(caplog)
        if record.levelno == logging.INFO
    ]
    assert len(records) == 1
    assert "Cocktail created" in records[0].getMessage()
    assert "17" in records[0].getMessage()
    assert cocktail.name not in records[0].getMessage()
    table.put_item.assert_called_once_with(
        Item={
            "id": 17,
            "name": "User\nSupplied Name",
            "spirit": "Gin",
            "ingredients": ["Gin"],
        }
    )


def test_get_cocktail_uses_correct_dynamodb_key(monkeypatch):
    table = MagicMock()
    table.get_item.return_value = {
        "Item": {
            "id": 42,
            "name": "Martini",
            "spirit": "Gin",
            "ingredients": ["Gin"],
        }
    }
    monkeypatch.setattr(cocktail_service, "table", table)

    result = cocktail_service.get_cocktail(42)

    assert result["id"] == 42
    table.get_item.assert_called_once_with(Key={"id": 42})


def test_delete_missing_cocktail_does_not_write_or_log_success(
    monkeypatch,
    caplog,
):
    table = MagicMock()
    table.get_item.return_value = {}
    monkeypatch.setattr(cocktail_service, "table", table)

    with caplog.at_level(logging.INFO, logger="cocktail_api"):
        with pytest.raises(HTTPException) as exception_info:
            cocktail_service.delete_cocktail(123)

    assert exception_info.value.status_code == 404
    assert exception_info.value.detail == "Cocktail not found"
    table.delete_item.assert_not_called()
    records = application_records(caplog)
    assert any("delete target not found" in record.getMessage() for record in records)
    assert not any("Cocktail deleted" in record.getMessage() for record in records)


def test_delete_existing_cocktail_uses_correct_key(monkeypatch):
    table = MagicMock()
    table.get_item.return_value = {"Item": {"id": 23}}
    monkeypatch.setattr(cocktail_service, "table", table)

    result = cocktail_service.delete_cocktail(23)

    assert result == {"message": "Cocktail 23 deleted"}
    table.get_item.assert_called_once_with(Key={"id": 23})
    table.delete_item.assert_called_once_with(Key={"id": 23})


def test_update_missing_cocktail_does_not_write(monkeypatch):
    table = MagicMock()
    table.get_item.return_value = {}
    monkeypatch.setattr(cocktail_service, "table", table)
    cocktail = Cocktail(
        id=99,
        name="Martini",
        spirit="Gin",
        ingredients=["Gin"],
    )

    with pytest.raises(HTTPException) as exception_info:
        cocktail_service.update_cocktail(7, cocktail)

    assert exception_info.value.status_code == 404
    assert exception_info.value.detail == "Cocktail not found"
    table.put_item.assert_not_called()


def test_update_uses_path_id_when_body_id_differs(monkeypatch):
    table = MagicMock()
    table.get_item.return_value = {"Item": {"id": 7}}
    monkeypatch.setattr(cocktail_service, "table", table)
    cocktail = Cocktail(
        id=99,
        name="Martini",
        spirit="Gin",
        ingredients=["Gin", "Vermouth"],
    )

    result = cocktail_service.update_cocktail(7, cocktail)

    expected_cocktail = {
        "id": 7,
        "name": "Martini",
        "spirit": "Gin",
        "ingredients": ["Gin", "Vermouth"],
    }
    assert result == expected_cocktail
    table.get_item.assert_called_once_with(Key={"id": 7})
    table.put_item.assert_called_once_with(Item=expected_cocktail)


def test_unexpected_dynamodb_failure_propagates(monkeypatch):
    table = MagicMock()
    failure = ClientError(
        error_response={
            "Error": {
                "Code": "InternalServerError",
                "Message": "Unavailable",
            }
        },
        operation_name="Scan",
    )
    table.scan.side_effect = failure
    monkeypatch.setattr(cocktail_service, "table", table)

    with pytest.raises(ClientError) as exception_info:
        cocktail_service.get_all_cocktails()

    assert exception_info.value is failure
