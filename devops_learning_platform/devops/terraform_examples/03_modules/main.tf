# 03_modules/main.tf — Using the VPC module
# Usage: terraform init && terraform apply -var-file=../02_variables_outputs/dev.tfvars

module "vpc" {
  source = "./vpc_module"

  name               = "myapp-${var.environment}"
  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

  public_subnet_cidrs = [
    "10.0.1.0/24",
    "10.0.2.0/24",
    "10.0.3.0/24",
  ]

  private_subnet_cidrs = [
    "10.0.11.0/24",
    "10.0.12.0/24",
    "10.0.13.0/24",
  ]

  enable_nat_gateway = var.environment == "production" ? true : false

  tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# Use the module outputs in other resources
resource "aws_security_group" "alb" {
  name   = "alb-sg"
  vpc_id = module.vpc.vpc_id    # <-- using module output

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

variable "environment" {
  type    = string
  default = "dev"
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnets" {
  value = module.vpc.public_subnet_ids
}
