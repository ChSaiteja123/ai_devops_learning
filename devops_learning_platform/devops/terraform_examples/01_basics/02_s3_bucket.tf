# 02_s3_bucket.tf — Create a secure S3 bucket (logs, artifacts, static hosting)
# Usage: terraform apply
# Destroy: terraform destroy

resource "aws_s3_bucket" "app_assets" {
  bucket = "mycompany-app-assets-2026"

  tags = {
    Name    = "app-assets"
    Purpose = "application static assets"
  }
}

# Block ALL public access
resource "aws_s3_bucket_public_access_block" "app_assets" {
  bucket = aws_s3_bucket.app_assets.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable versioning
resource "aws_s3_bucket_versioning" "app_assets" {
  bucket = aws_s3_bucket.app_assets.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable server-side encryption with KMS
resource "aws_s3_bucket_server_side_encryption_configuration" "app_assets" {
  bucket = aws_s3_bucket.app_assets.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3_key.arn
    }
    bucket_key_enabled = true   # reduce KMS API costs
  }
}

# Lifecycle: transition old objects to cheaper storage
resource "aws_s3_bucket_lifecycle_configuration" "app_assets" {
  bucket = aws_s3_bucket.app_assets.id

  rule {
    id     = "transition-old-versions"
    status = "Enabled"

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}

# KMS key for S3 encryption
resource "aws_kms_key" "s3_key" {
  description             = "S3 encryption key for app-assets bucket"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}

output "bucket_name" {
  value       = aws_s3_bucket.app_assets.bucket
  description = "S3 bucket name"
}

output "bucket_arn" {
  value       = aws_s3_bucket.app_assets.arn
  description = "S3 bucket ARN"
}
