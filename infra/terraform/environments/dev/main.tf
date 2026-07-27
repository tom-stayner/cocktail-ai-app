locals {
  name_prefix = "${var.project_name}-${var.environment}"

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
