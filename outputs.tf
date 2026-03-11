output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnet_ids" {
  value = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  value = module.vpc.private_subnet_ids
}

output "alb_dns_name" {
  value = module.alb.alb_dns_name
}

output "ecs_task_execution_role_arn" {
  value = module.ecs.ecs_task_execution_role_arn
}

output "ecs_task_role_arn" {
  value = module.ecs.ecs_task_role_arn
}

output "rds_endpoint" {
  value = module.rds.db_endpoint
}
