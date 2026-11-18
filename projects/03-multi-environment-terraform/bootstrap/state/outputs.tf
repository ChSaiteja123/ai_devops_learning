output "state_bucket_name" {
  description = "S3 bucket name to use in backend configuration."
  value       = aws_s3_bucket.state.id
}

output "state_bucket_region" {
  description = "AWS region containing the state bucket."
  value       = var.aws_region
}
