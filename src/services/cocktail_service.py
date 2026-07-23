from typing import Any

from fastapi import HTTPException

from src.database import table
from src.logging_config import logger
from src.models import Cocktail


def get_all_cocktails() -> list[dict[str, Any]]:
    response = table.scan()
    cocktails = response["Items"]

    logger.debug(
        "[SERVICE] Retrieved cocktail collection (count=%s)",
        len(cocktails),
    )

    return cocktails


def get_cocktail(cocktail_id: int) -> dict[str, Any]:
    response = table.get_item(Key={"id": cocktail_id})

    item = response.get("Item")

    if not item:
        logger.info(
            "[SERVICE] Cocktail not found (ID %s)",
            cocktail_id,
        )
        raise HTTPException(status_code=404, detail="Cocktail not found")

    logger.debug(
        "[SERVICE] Retrieved cocktail (ID %s)",
        cocktail_id,
    )

    return item


def create_cocktail(cocktail: Cocktail) -> dict[str, str]:
    table.put_item(
        Item={
            "id": cocktail.id,
            "name": cocktail.name,
            "spirit": cocktail.spirit,
            "ingredients": cocktail.ingredients,
        }
    )

    logger.info(
        "[SERVICE] Cocktail created (ID %s)",
        cocktail.id,
    )

    return {"message": "Cocktail added successfully"}


def delete_cocktail(cocktail_id: int) -> dict[str, str]:
    response = table.get_item(Key={"id": cocktail_id})

    item = response.get("Item")

    if not item:
        logger.info(
            "[SERVICE] Cocktail delete target not found (ID %s)",
            cocktail_id,
        )
        raise HTTPException(status_code=404, detail="Cocktail not found")

    table.delete_item(Key={"id": cocktail_id})

    logger.info(
        "[SERVICE] Cocktail deleted (ID %s)",
        cocktail_id,
    )

    return {"message": f"Cocktail {cocktail_id} deleted"}


def update_cocktail(cocktail_id: int, cocktail: Cocktail) -> dict[str, Any]:
    response = table.get_item(Key={"id": cocktail_id})

    if "Item" not in response:
        logger.info(
            "[SERVICE] Cocktail update target not found (ID %s)",
            cocktail_id,
        )
        raise HTTPException(status_code=404, detail="Cocktail not found")

    updated_cocktail = {
        "id": cocktail_id,
        "name": cocktail.name,
        "spirit": cocktail.spirit,
        "ingredients": cocktail.ingredients,
    }

    table.put_item(Item=updated_cocktail)

    logger.info(
        "[SERVICE] Cocktail updated (ID %s)",
        cocktail_id,
    )

    return updated_cocktail
