resource "aws_lambda_function" "api" {
  function_name = local.lambda_function_name
  description   = "${var.project_name} ${var.environment} API version ${var.application_version}"
  role          = aws_iam_role.lambda_execution.arn

  package_type     = "Zip"
  filename         = abspath(var.lambda_package_path)
  source_code_hash = filebase64sha256(var.lambda_package_path)

  runtime       = "python3.14"
  architectures = ["x86_64"]
  handler       = "src.lambda_handler.handler"

  memory_size = var.lambda_memory_size
  timeout     = var.lambda_timeout_seconds
  publish     = true

  environment {
    variables = {
      APP_NAME        = var.application_name
      APP_VERSION     = var.application_version
      APP_ENV         = var.application_environment
      TABLE_NAME      = data.aws_dynamodb_table.cocktails.name
      LOG_LEVEL       = var.log_level
      ALLOW_MUTATIONS = tostring(var.allow_mutations)
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda,
    aws_iam_role_policy.lambda_dynamodb,
    aws_iam_role_policy.lambda_logging,
  ]
}

resource "aws_lambda_alias" "live" {
  name             = "live"
  description      = "Stable live reference for the current approved Lambda version"
  function_name    = aws_lambda_function.api.function_name
  function_version = aws_lambda_function.api.version
}
