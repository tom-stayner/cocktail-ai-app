locals {
  name_prefix          = "${var.project_name}-${var.environment}"
  lambda_function_name = "${local.name_prefix}-api"
  lambda_log_group     = "/aws/lambda/${local.lambda_function_name}"
  http_api_name        = "${local.name_prefix}-http-api"
  api_access_log_group = "/aws/apigateway/${local.http_api_name}"

  api_integration_timeout_milliseconds = min(
    var.lambda_timeout_seconds * 1000,
    30000
  )

  public_get_route_keys = toset([
    "GET /",
    "GET /favicon.ico",
    "GET /static/{proxy+}",
    "GET /docs",
    "GET /openapi.json",
    "GET /health",
    "GET /health/live",
    "GET /health/ready",
    "GET /cocktails",
    "GET /cocktails/html",
    "GET /cocktails/html/{cocktail_id}",
    "GET /cocktails/{cocktail_id}",
  ])

  tags = merge(
    var.additional_tags,
    {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
      Application = var.application_name
    }
  )
}
