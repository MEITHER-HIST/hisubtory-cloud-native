output "alb_sg_id" {
  value = aws_security_group.alb_sg.id
}

output "ecs_app_sg_id" {
  value = aws_security_group.ecs_app_sg.id
}

output "rds_sg_id" {
  value = aws_security_group.rds_sg.id
}

output "redis_sg_id" {
  value = aws_security_group.redis_sg.id
}

output "bastion_sg_id" {
  value = aws_security_group.bastion_sg.id
}
