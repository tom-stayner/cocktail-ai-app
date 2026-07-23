import boto3

from src.config import settings
from src.logging_config import logger

dynamodb = boto3.resource("dynamodb", region_name=settings.aws_region)

table = dynamodb.Table(settings.table_name)

logger.info(
    "[SYSTEM] DynamoDB configured (region=%s, table=%s)",
    settings.aws_region,
    settings.table_name,
)
