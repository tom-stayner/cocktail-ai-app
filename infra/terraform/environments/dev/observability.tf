resource "aws_cloudwatch_log_group" "lambda" {
  name              = local.lambda_log_group
  retention_in_days = var.log_retention_days
}

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "${local.lambda_function_name}-errors"
  alarm_description   = "Lambda reported at least one error within five minutes."
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  threshold           = 1

  namespace   = "AWS/Lambda"
  metric_name = "Errors"
  statistic   = "Sum"
  period      = 300

  treat_missing_data = "notBreaching"

  dimensions = {
    FunctionName = aws_lambda_function.api.function_name
  }
}

resource "aws_cloudwatch_metric_alarm" "lambda_throttles" {
  alarm_name          = "${local.lambda_function_name}-throttles"
  alarm_description   = "Lambda reported at least one throttle within five minutes."
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  threshold           = 1

  namespace   = "AWS/Lambda"
  metric_name = "Throttles"
  statistic   = "Sum"
  period      = 300

  treat_missing_data = "notBreaching"

  dimensions = {
    FunctionName = aws_lambda_function.api.function_name
  }
}
