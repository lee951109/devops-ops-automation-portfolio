provider "aws" {
  region = var.aws_region
}

# 최신 Amazon Linux AMI 조회
# - 소유지(owners)를 amazon으로 제한해서 신뢰 가능한 AMI를 선택
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners = ["amazon"]

  filter {
    name = "name"
    values = ["al2023-ami-*-x86_64"] # Amazon Linux 2023 계열
  }

  filter {
    name = "virtualization-type"
    values = ["hvm"]
  }
}

# Security Group: SSH는 내 IP만, HTTP는 전체 허용
resource "aws_security_group" "web_sg" {
  name = "${var.project_name}-sg"
  description = "Security Group for SSH and HTTP"
  vpc_id = data.aws_vpc.default.vpc_id

  # SSH - 22/tcp: 내 IP만 허용
  ingress {
    description = "SSH from my IP only"
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = [var.my_ip_cidr]
  }

  # HTTP - 80/tpc: 전체 허용
  ingress {
    description = "HTTP from anywhere"
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # 아웃바운드: 전체 허용(패키지 설치/업데이트 등에 필요)
  egress {
    description = "Allow all outbound"
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Project = var.project_name
  }
}

# Default VPC 사용
data "aws_vpc" "default" {
    default = true
}

# Default VPC의 Public Subnet 중 하나 선택
data "aws_subnets" "default_vpc_subnets" {
  filter {
    name = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# EC2(Elastic Compute Cloud) 인스턴스 생성
resource "aws_instance" "ops_host" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  key_name               = var.key_name
  subnet_id              = data.aws_subnets.default_vpc_subnets.ids[0]
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  # 퍼블릭 IP 부여(간단하게 SSH 접속/테스트 목적)
  associate_public_ip_address = true

  # 간단한 태그
  tags = {
    Name    = "${var.project_name}-ec2"
    Project = var.project_name
  }
}