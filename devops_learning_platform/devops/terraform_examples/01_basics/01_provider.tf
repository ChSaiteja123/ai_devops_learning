# 01_provider.tf — Configure AWS provider and required versions
# Usage: terraform init && terraform plan

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.30"   # pin minor version for stability
    }
  }

  # Remote state — uncomment for team use
  # backend "s3" {
  #   bucket         = "my-terraform-state-bucket"
  #   key            = "basics/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "terraform-locks"
  # }
}

provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      ManagedBy   = "terraform"
      Environment = "dev"
      Project     = "devops-practice"
    }
  }
}
