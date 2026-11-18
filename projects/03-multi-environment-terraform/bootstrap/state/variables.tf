variable "aws_region" {
  description = "AWS region for the Terraform state bucket."
  type        = string
  default     = "ap-south-1"
}

variable "state_bucket_name" {
  description = "Globally unique S3 bucket name for Terraform state."
  type        = string

  validation {
    condition     = length(var.state_bucket_name) >= 3 && length(var.state_bucket_name) <= 63
    error_message = "state_bucket_name must be between 3 and 63 characters."
  }
}

variable "tags" {
  description = "Tags applied to the state bucket."
  type        = map(string)
  default = {
    ManagedBy = "terraform"
    Purpose   = "terraform-state"
  }
}
