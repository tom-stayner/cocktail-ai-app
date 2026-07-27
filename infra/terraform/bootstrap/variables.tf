variable "aws_region" {
  description = "AWS region in which the Terraform state bucket will be created."
  type        = string
  default     = "ap-southeast-2"

  validation {
    condition     = length(trimspace(var.aws_region)) > 0
    error_message = "aws_region must not be empty."
  }
}

variable "project_name" {
  description = "Project identifier used for mandatory resource tags."
  type        = string
  default     = "cocktail-ai-app"

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]*[a-z0-9]$", var.project_name))
    error_message = "project_name must use lowercase letters, numbers, and hyphens."
  }
}

variable "environment" {
  description = "Environment identifier used for mandatory resource tags."
  type        = string
  default     = "bootstrap"

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]*[a-z0-9]$", var.environment))
    error_message = "environment must use lowercase letters, numbers, and hyphens."
  }
}

variable "state_bucket_name" {
  description = "Globally unique S3 bucket name selected for Terraform state."
  type        = string

  validation {
    condition = (
      length(var.state_bucket_name) >= 3 &&
      length(var.state_bucket_name) <= 63 &&
      can(regex("^[a-z0-9][a-z0-9.-]*[a-z0-9]$", var.state_bucket_name))
    )
    error_message = "state_bucket_name must be 3-63 characters, start and end with a lowercase letter or number, and contain only lowercase letters, numbers, periods, or hyphens."
  }
}

variable "additional_tags" {
  description = "Additional non-sensitive tags to apply without replacing mandatory tags."
  type        = map(string)
  default     = {}
}
