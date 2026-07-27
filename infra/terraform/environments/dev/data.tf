data "aws_dynamodb_table" "cocktails" {
  name = var.dynamodb_table_name
}
