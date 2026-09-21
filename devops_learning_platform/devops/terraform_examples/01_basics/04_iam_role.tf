# 04_iam_role.tf — Create IAM role with instance profile and policy
# Pattern: least privilege — only grant what the application actually needs

# IAM role (the identity)
resource "aws_iam_role" "web_role" {
  name = "web-server-role"

  # Trust policy: who can assume this role
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "ec2.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

# Inline policy: what the role can do (least privilege)
resource "aws_iam_role_policy" "web_policy" {
  name = "web-app-policy"
  role = aws_iam_role.web_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "S3ReadAssets"
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:ListBucket"]
        Resource = [
          aws_s3_bucket.app_assets.arn,
          "${aws_s3_bucket.app_assets.arn}/*"
        ]
      },
      {
        Sid      = "SecretsManagerRead"
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = "arn:aws:secretsmanager:us-east-1:*:secret:/production/webapp/*"
      },
      {
        Sid      = "CloudWatchLogs"
        Effect   = "Allow"
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:log-group:/app/*"
      }
    ]
  })
}

# Instance profile: attaches IAM role to EC2
resource "aws_iam_instance_profile" "web" {
  name = "web-instance-profile"
  role = aws_iam_role.web_role.name
}

output "iam_role_arn" {
  value       = aws_iam_role.web_role.arn
  description = "Web server IAM role ARN"
}
