variable "private_subnet_ids" { type = list(string) }
variable "ecs_app_sg_id" { type = string }

variable "user_target_group_arn" { type = string }
variable "user_repository_url" { type = string }

variable "story_target_group_arn" { type = string }
variable "story_repository_url" { type = string }

variable "activity_target_group_arn" { type = string }
variable "activity_repository_url" { type = string }

variable "rds_endpoint" { type = string }
variable "redis_endpoint" { type = string }
