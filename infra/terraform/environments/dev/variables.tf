variable "aws_region" {
  description = "AWS region for the future development deployment."
  type        = string
  default     = "ap-southeast-2"

  validation {
    condition     = length(trimspace(var.aws_region)) > 0
    error_message = "aws_region must not be empty."
  }
}

variable "environment" {
  description = "Deployment environment identifier."
  type        = string
  default     = "dev"

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]*[a-z0-9]$", var.environment))
    error_message = "environment must use lowercase letters, numbers, and hyphens."
  }
}

variable "project_name" {
  description = "Project identifier used for naming and mandatory tags."
  type        = string
  default     = "cocktail-ai-app"

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]*[a-z0-9]$", var.project_name))
    error_message = "project_name must use lowercase letters, numbers, and hyphens."
  }
}

variable "application_name" {
  description = "Application name supplied to the future Lambda runtime."
  type        = string
  default     = "Tom's Cocktail API"

  validation {
    condition     = length(trimspace(var.application_name)) > 0
    error_message = "application_name must not be empty."
  }
}

variable "dynamodb_table_name" {
  description = "Name of the existing DynamoDB table; the table remains outside Terraform ownership."
  type        = string
  default     = "Cocktails"

  validation {
    condition     = length(trimspace(var.dynamodb_table_name)) > 0
    error_message = "dynamodb_table_name must not be empty."
  }
}

variable "lambda_package_path" {
  description = "Path to the validated Lambda ZIP used by a future hosting step."
  type        = string
  default     = "../../../../dist/cocktail-ai-lambda.zip"

  validation {
    condition     = endswith(lower(var.lambda_package_path), ".zip")
    error_message = "lambda_package_path must identify a ZIP archive."
  }
}

variable "lambda_memory_size" {
  description = "Memory allocation in MB for the future Lambda function."
  type        = number
  default     = 256

  validation {
    condition     = var.lambda_memory_size >= 128 && var.lambda_memory_size <= 10240
    error_message = "lambda_memory_size must be between 128 and 10240 MB."
  }
}

variable "lambda_timeout_seconds" {
  description = "Timeout in seconds for the future Lambda function."
  type        = number
  default     = 15

  validation {
    condition     = var.lambda_timeout_seconds >= 1 && var.lambda_timeout_seconds <= 900
    error_message = "lambda_timeout_seconds must be between 1 and 900 seconds."
  }
}

variable "application_version" {
  description = "Application version supplied to the future runtime."
  type        = string
  default     = "0.5.0"

  validation {
    condition     = length(trimspace(var.application_version)) > 0
    error_message = "application_version must not be empty."
  }
}

variable "application_environment" {
  description = "APP_ENV value supplied to the future runtime."
  type        = string
  default     = "development"

  validation {
    condition     = contains(["development", "test", "production"], var.application_environment)
    error_message = "application_environment must be development, test, or production."
  }
}

variable "log_level" {
  description = "LOG_LEVEL value supplied to the future runtime."
  type        = string
  default     = "INFO"

  validation {
    condition     = contains(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], var.log_level)
    error_message = "log_level must be a supported application logging level."
  }
}

variable "allow_mutations" {
  description = "Whether the future runtime enables cocktail mutations; false is fail-closed."
  type        = bool
  default     = false
}

variable "log_retention_days" {
  description = "Retention period for a future CloudWatch log group."
  type        = number
  default     = 14

  validation {
    condition = contains(
      [1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, 3653],
      var.log_retention_days
    )
    error_message = "log_retention_days must be a supported CloudWatch Logs retention value."
  }
}

variable "additional_tags" {
  description = "Additional non-sensitive tags to apply without replacing mandatory tags."
  type        = map(string)
  default     = {}
}
