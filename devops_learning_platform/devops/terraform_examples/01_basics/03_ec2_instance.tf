# 03_ec2_instance.tf — Launch a basic EC2 instance
# Usage: terraform apply -var="key_name=my-keypair"

# Look up the latest Amazon Linux 2023 AMI automatically
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

variable "key_name" {
  description = "EC2 key pair name for SSH access"
  type        = string
}

resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Allow HTTP and SSH"
  vpc_id      = aws_vpc.main.id    # reference your VPC

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH from VPN only"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]  # restrict to internal network
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web" {
  ami                    = data.aws_ami.amazon_linux_2023.id
  instance_type          = "t3.micro"
  key_name               = var.key_name
  subnet_id              = aws_subnet.public_a.id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  # Use IAM instance profile instead of embedding credentials
  iam_instance_profile = aws_iam_instance_profile.web.name

  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  user_data = <<-EOF
    #!/bin/bash
    dnf update -y
    dnf install -y nginx
    systemctl start nginx
    systemctl enable nginx
  EOF

  tags = {
    Name = "web-server"
    Role = "frontend"
  }
}

output "instance_public_ip" {
  value       = aws_instance.web.public_ip
  description = "EC2 public IP address"
}
