variable "name" {
  description = "Name prefix for network resources."
  type        = string
}

variable "vpc_cidr" {
  description = "IPv4 CIDR block for the VPC."
  type        = string
}

variable "availability_zones" {
  description = "Availability zones in which to create public/private subnet pairs."
  type        = list(string)

  validation {
    condition     = length(var.availability_zones) >= 2 && length(var.availability_zones) <= 3
    error_message = "Provide between two and three availability zones."
  }
}

variable "tags" {
  description = "Tags applied to network resources."
  type        = map(string)
  default     = {}
}
