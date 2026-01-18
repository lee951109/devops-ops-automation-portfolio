
variable "aws_region" {
  description = "AWS Region"
  type = string
  default = "ap-northeast-2"
}

variable "project_name" {
  description = "리소스 태그에 붙일 프로젝트 이름"
  type = string
  default = "devops-ops-automation-portfolio"
}

variable "instance_type" {
  description = "EC2 인스턴스 타입."
  type = string
  default = "t3.micro"
}

variable "key_name" {
  description = "EC2 SSH 접속용 Key Pair"
  type = string
}

variable "my_ip_cidr" {
  description = "내 PC 공인 IP CIDR"
  type = string
}