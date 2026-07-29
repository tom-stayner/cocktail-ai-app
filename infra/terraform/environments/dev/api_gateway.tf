resource "aws_apigatewayv2_api" "public" {
  name                         = local.http_api_name
  description                  = "${var.project_name} ${var.environment} public read-only HTTP API"
  protocol_type                = "HTTP"
  disable_execute_api_endpoint = false

  lifecycle {
    precondition {
      condition     = var.allow_mutations == false
      error_message = "The public HTTP API requires allow_mutations=false."
    }
  }
}

resource "aws_apigatewayv2_integration" "lambda_live" {
  api_id = aws_apigatewayv2_api.public.id

  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_alias.live.invoke_arn
  integration_method = "POST"

  payload_format_version = "2.0"
  timeout_milliseconds   = local.api_integration_timeout_milliseconds
}

resource "aws_apigatewayv2_route" "public_get" {
  for_each = local.public_get_route_keys

  api_id             = aws_apigatewayv2_api.public.id
  route_key          = each.value
  authorization_type = "NONE"
  target             = "integrations/${aws_apigatewayv2_integration.lambda_live.id}"
}

resource "aws_lambda_permission" "api_gateway_live" {
  statement_id  = "AllowHttpApiGetLiveAlias"
  action        = "lambda:InvokeFunction"
  principal     = "apigateway.amazonaws.com"
  function_name = aws_lambda_function.api.function_name
  qualifier     = aws_lambda_alias.live.name
  source_arn    = "${aws_apigatewayv2_api.public.execution_arn}/*/GET/*"
}

# The $default stage removes a URL path prefix. It is not a $default catch-all
# route; only the explicit GET route collection above is exposed.
resource "aws_apigatewayv2_stage" "default" {
  api_id = aws_apigatewayv2_api.public.id
  name   = "$default"

  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_access.arn
    format = jsonencode({
      requestId               = "$context.requestId"
      requestTime             = "$context.requestTime"
      httpMethod              = "$context.httpMethod"
      routeKey                = "$context.routeKey"
      path                    = "$context.path"
      protocol                = "$context.protocol"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      responseLatency         = "$context.responseLatency"
      integrationLatency      = "$context.integrationLatency"
      integrationStatus       = "$context.integrationStatus"
      integrationErrorMessage = "$context.integrationErrorMessage"
    })
  }

  default_route_settings {
    detailed_metrics_enabled = false
    throttling_rate_limit    = var.api_throttling_rate_limit
    throttling_burst_limit   = var.api_throttling_burst_limit
  }
}
