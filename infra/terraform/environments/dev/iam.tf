data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    sid     = "LambdaAssumeRole"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_execution" {
  name               = "${local.lambda_function_name}-execution"
  description        = "Least-privilege execution role for ${local.lambda_function_name}"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "lambda_logging" {
  statement {
    sid    = "WriteManagedLambdaLogGroup"
    effect = "Allow"

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["${aws_cloudwatch_log_group.lambda.arn}:*"]
  }
}

resource "aws_iam_role_policy" "lambda_logging" {
  name   = "write-managed-log-group"
  role   = aws_iam_role.lambda_execution.id
  policy = data.aws_iam_policy_document.lambda_logging.json
}

locals {
  dynamodb_read_actions = [
    "dynamodb:DescribeTable",
    "dynamodb:Scan",
    "dynamodb:GetItem",
  ]

  dynamodb_write_actions = [
    "dynamodb:PutItem",
    "dynamodb:DeleteItem",
  ]

  dynamodb_actions = concat(
    local.dynamodb_read_actions,
    var.allow_mutations ? local.dynamodb_write_actions : []
  )
}

data "aws_iam_policy_document" "lambda_dynamodb" {
  statement {
    sid       = "AccessExistingCocktailsTable"
    effect    = "Allow"
    actions   = local.dynamodb_actions
    resources = [data.aws_dynamodb_table.cocktails.arn]
  }
}

resource "aws_iam_role_policy" "lambda_dynamodb" {
  name   = "access-existing-cocktails-table"
  role   = aws_iam_role.lambda_execution.id
  policy = data.aws_iam_policy_document.lambda_dynamodb.json
}
