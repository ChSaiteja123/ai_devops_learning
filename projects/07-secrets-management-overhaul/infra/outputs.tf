output "secret_arn" {
  description = "ARN for provisioning the secret value out of band."
  value       = aws_secretsmanager_secret.app.arn
}

output "read_policy_arn" {
  description = "IAM policy attached to the existing workload role."
  value       = aws_iam_policy.read_secret.arn
}
