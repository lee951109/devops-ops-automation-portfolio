output "instance_public_ip" {
  description = "EC2(Elastic Compute Cloud) Public IP"
  value       = aws_instance.ops_host.public_ip
}

output "ssh_command" {
  description = "SSH 접속 예시 명령"
  value       = "ssh -i <YOUR_KEY_FILE.pem> ec2-user@${aws_instance.ops_host.public_ip}"
}
