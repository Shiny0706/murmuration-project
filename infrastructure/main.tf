provider "aws" {
  region = var.aws_region
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

resource "aws_security_group" "fastapi_sg" {
  name        = "fastapi-sg"
  description = "Allow SSH"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "fastapi" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.ec2_instance_type
  vpc_security_group_ids = [aws_security_group.fastapi_sg.id]
  key_name               = var.key_name

  tags = {
    Name = "fastapi-backend"
  }
}