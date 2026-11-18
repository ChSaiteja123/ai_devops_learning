output "vpc_id" {
  description = "ID of the environment VPC."
  value       = module.network.vpc_id
}

output "public_subnet_ids" {
  description = "IDs of public subnets."
  value       = module.network.public_subnet_ids
}

output "private_subnet_ids" {
  description = "IDs of private subnets. No NAT route is created in this cost-conscious baseline."
  value       = module.network.private_subnet_ids
}
