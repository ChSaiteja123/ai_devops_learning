variable "aws_region" {
  description = "AWS region for the example network"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Prefix used for resource names"
  type        = string
  default     = "devops-learning"
}
