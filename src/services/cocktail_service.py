from fastapi import HTTPException

from src.database import table
from src.logging_config import logger

def get_all_cocktails() -> list:

    logger.info("[SERVICE] Retrieving cocktail collection")

    response = table.scan()
    cocktails = response["Items"]

    logger.info(
        f"[SERVICE] Retrieved {len(cocktails)} cocktails"
    )

    return cocktails

def get_cocktail(cocktail_id: int) -> dict:

    logger.info(
        f"[SERVICE] Retrieving cocktail (ID {cocktail_id})"
    )

    response = table.get_item(
        Key={"id": cocktail_id}
    )

    item = response.get("Item")

    if not item:
        logger.warning(
            f"[SERVICE] Cocktail ID {cocktail_id} not found"
        )
        raise HTTPException(
            status_code=404,
            detail="Cocktail not found"
        )

    logger.info(
        f"[SERVICE] Retrieved cocktail '{item['name']}'"
    )

    return item