# 06_locals_outputs.tf — Locals for computed values and structured outputs

locals {
  # Build a consistent name prefix for all resources
  name_prefix = "${var.environment}-${var.region}"

  # Compute AZs dynamically
  azs = ["${var.region}a", "${var.region}b", "${var.region}c"]

  # Merge default tags with caller-supplied tags
  common_tags = merge(
    {
      Environment = var.environment
      ManagedBy   = "terraform"
      UpdatedAt   = timestamp()
    },
    var.tags
  )

  # Determine instance size based on environment
  instance_type = var.environment == "production" ? "m5.large" : "t3.micro"

  # Build CIDR blocks for subnets based on VPC CIDR
  public_subnets  = [for i in range(3) : cidrsubnet(var.vpc_cidr, 8, i)]
  private_subnets = [for i in range(3) : cidrsubnet(var.vpc_cidr, 8, i + 10)]
}

# Outputs — exposed to callers, `terraform output`, and other modules

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "alb_dns_name" {
  description = "ALB DNS name for DNS CNAME record"
  value       = aws_lb.main.dns_name
}

output "rds_endpoint" {
  description = "RDS connection endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true   # hidden in CLI output unless explicitly requested
}

output "environment_summary" {
  description = "Summary of deployed environment"
  value = {
    environment  = var.environment
    region       = var.region
    vpc_cidr     = var.vpc_cidr
    az_count     = length(local.azs)
    name_prefix  = local.name_prefix
  }
}
