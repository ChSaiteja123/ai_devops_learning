# 05_variables.tf — Input variables with types, defaults, and validation
# Usage: terraform apply -var-file=dev.tfvars
# Or:    terraform apply -var="environment=staging"

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "environment must be one of: dev, staging, production"
  }
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"

  validation {
    condition     = can(regex("^(t3|t3a|m5|m5a)\\.", var.instance_type))
    error_message = "Only t3, t3a, m5, or m5a family instances are allowed."
  }
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrnetmask(var.vpc_cidr))
    error_message = "vpc_cidr must be a valid CIDR block."
  }
}

variable "allowed_ips" {
  description = "List of CIDRs allowed SSH access"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "Additional resource tags"
  type        = map(string)
  default     = {}
}

variable "db_config" {
  description = "Database configuration object"
  type = object({
    engine         = string
    engine_version = string
    instance_class = string
    storage_gb     = number
    multi_az       = bool
  })
  default = {
    engine         = "postgres"
    engine_version = "15.4"
    instance_class = "db.t3.micro"
    storage_gb     = 20
    multi_az       = false
  }
}

# Sensitive variable — value hidden in plan and logs
variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true

  validation {
    condition     = length(var.db_password) >= 16
    error_message = "db_password must be at least 16 characters long."
  }
}
