output "name_prefix" {
  description = "Naming prefix reserved for future development resources."
  value       = local.name_prefix
}

output "existing_dynamodb_table_name" {
  description = "Existing cocktail table referenced by future resources but not owned by Terraform."
  value       = var.dynamodb_table_name
}

output "lambda_package_path" {
  description = "Configured path to the future Lambda deployment package."
  value       = var.lambda_package_path
}
