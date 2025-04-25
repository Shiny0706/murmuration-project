output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.survey_vpc.id
}

output "backend_security_group_id" {
  description = "The ID of the backend security group"
  value       = aws_security_group.backend_sg.id
}

output "frontend_security_group_id" {
  description = "The ID of the frontend security group"
  value       = aws_security_group.frontend_sg.id
} 