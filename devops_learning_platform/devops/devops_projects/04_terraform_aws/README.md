# Terraform AWS Foundation

This folder demonstrates a small AWS VPC foundation using Terraform.

The example creates a VPC, public subnet, internet gateway, route table, and route.
Review costs and security before applying to a real AWS account.

## Commands

```powershell
terraform init
terraform fmt -check
terraform validate
terraform plan
```

Run `terraform apply` only after reviewing the plan and configuring AWS credentials.
