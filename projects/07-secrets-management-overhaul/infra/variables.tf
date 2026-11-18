variable "aws_region" {
  description = "AWS region for the secret metadata."
  type        = string
  default     = "ap-south-1"
}

variable "secret_name" {
  description = "Name for secret metadata; Terraform does not set the secret value."
  type        = string
}

variable "workload_role_name" {
  description = "Name of an existing workload IAM role to receive read access to this secret."
  type        = string
}

variable "environment" {
  description = "Environment tag."
  type        = string
  default     = "dev"
}
