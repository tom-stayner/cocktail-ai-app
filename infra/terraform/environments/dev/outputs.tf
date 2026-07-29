output "name_prefix" {
  description = "Naming prefix reserved for future development resources."
  value       = local.name_prefix
}

output "existing_dynamodb_table_name" {
  description = "Existing cocktail table referenced by future resources but not owned by Terraform."
  value       = data.aws_dynamodb_table.cocktails.name
}

output "existing_dynamodb_table_arn" {
  description = "ARN of the existing cocktail table referenced by the Lambda policy."
  value       = data.aws_dynamodb_table.cocktails.arn
}

output "lambda_package_path" {
  description = "Configured path to the future Lambda deployment package."
  value       = var.lambda_package_path
}

output "lambda_function_name" {
  description = "Name of the defined Lambda function."
  value       = aws_lambda_function.api.function_name
}

output "lambda_function_arn" {
  description = "ARN of the defined Lambda function."
  value       = aws_lambda_function.api.arn
}

output "lambda_live_alias_name" {
  description = "Name of the stable Lambda alias intended for future API integration."
  value       = aws_lambda_alias.live.name
}

output "lambda_live_alias_arn" {
  description = "ARN of the stable Lambda alias intended for future API integration."
  value       = aws_lambda_alias.live.arn
}

output "lambda_log_group_name" {
  description = "Name of the explicitly managed Lambda log group."
  value       = aws_cloudwatch_log_group.lambda.name
}

output "lambda_alarm_names" {
  description = "Names of the baseline Lambda alarms."
  value = {
    errors    = aws_cloudwatch_metric_alarm.lambda_errors.alarm_name
    throttles = aws_cloudwatch_metric_alarm.lambda_throttles.alarm_name
  }
}

output "http_api_id" {
  description = "ID of the defined public HTTP API."
  value       = aws_apigatewayv2_api.public.id
}

output "http_api_name" {
  description = "Name of the defined public HTTP API."
  value       = aws_apigatewayv2_api.public.name
}

output "http_api_endpoint" {
  description = "Execute API endpoint that will become public only after an approved apply."
  value       = aws_apigatewayv2_api.public.api_endpoint
}

output "http_api_stage_name" {
  description = "Name of the root-level auto-deploying HTTP API stage."
  value       = aws_apigatewayv2_stage.default.name
}

output "http_api_access_log_group_name" {
  description = "Name of the HTTP API structured access-log group."
  value       = aws_cloudwatch_log_group.api_access.name
}

output "http_api_5xx_alarm_name" {
  description = "Name of the HTTP API server-error alarm."
  value       = aws_cloudwatch_metric_alarm.api_server_errors.alarm_name
}

output "public_route_keys" {
  description = "Explicit unauthenticated GET routes defined for the public HTTP API."
  value       = sort(tolist(local.public_get_route_keys))
}
