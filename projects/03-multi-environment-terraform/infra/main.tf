data "aws_availability_zones" "available" {
  state = "available"
}

module "network" {
  source = "../modules/network"

  name               = "${var.project_name}-${var.environment}"
  vpc_cidr           = var.vpc_cidr
  availability_zones = slice(data.aws_availability_zones.available.names, 0, var.az_count)
  tags               = var.tags
}
