variable "project_name" {
  description = "Short project identifier used in resource names."
  type        = string
  default     = "devops-platform"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "project_name may contain lowercase letters, numbers, and hyphens only."
  }
}

variable "environment" {
  description = "Environment name used in resource names and tags."
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging, or prod."
  }
}

variable "aws_region" {
  description = "AWS region for all resources."
  type        = string
  default     = "ap-south-1"
}

variable "vpc_cidr" {
  description = "IPv4 CIDR block for the environment VPC."
  type        = string
  default     = "10.40.0.0/16"

  validation {
    condition     = can(cidrsubnet(var.vpc_cidr, 8, 5))
    error_message = "vpc_cidr must be valid and large enough for six subnet CIDR blocks."
  }
}

variable "az_count" {
  description = "Number of availability zones and subnet pairs to create."
  type        = number
  default     = 2

  validation {
    condition     = var.az_count >= 2 && var.az_count <= 3
    error_message = "az_count must be 2 or 3."
  }
}

variable "tags" {
  description = "Tags applied to all resources."
  type        = map(string)
  default     = {}
}
