resource "aws_secretsmanager_secret" "app" {
  name                    = var.secret_name
  description             = "Secret metadata managed by Terraform; value is provisioned out of band."
  recovery_window_in_days = 7

  tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

data "aws_iam_policy_document" "read_secret" {
  statement {
    sid       = "ReadOnlyThisSecret"
    effect    = "Allow"
    actions   = ["secretsmanager:DescribeSecret", "secretsmanager:GetSecretValue"]
    resources = [aws_secretsmanager_secret.app.arn]
  }
}

resource "aws_iam_policy" "read_secret" {
  name        = "${replace(var.secret_name, "/", "-")}-read"
  description = "Allow the workload role to read only the named application secret."
  policy      = data.aws_iam_policy_document.read_secret.json
}

resource "aws_iam_role_policy_attachment" "workload" {
  role       = var.workload_role_name
  policy_arn = aws_iam_policy.read_secret.arn
}
