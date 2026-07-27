locals {
  name_prefix          = "${var.project_name}-${var.environment}"
  lambda_function_name = "${local.name_prefix}-api"
  lambda_log_group     = "/aws/lambda/${local.lambda_function_name}"

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
