variable "private_subnet_ids" {
  type = list(string)
}

variable "ecs_app_sg_id" {
  type = string
}

variable "target_group_arn" {
  type = string
}

variable "repository_url" {
  type = string
}

variable "rds_endpoint" {
  type = string
}

variable "redis_endpoint" {
  type = string
}

variable "project_name" {
  type = string
}
