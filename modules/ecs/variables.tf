variable "private_subnet_ids" {
  type = list(string)
}

variable "ecs_app_sg_id" {
  type = string
}

variable "user_tg_arn" {
  type = string
}

variable "story_tg_arn" {
  type = string
}

variable "activity_tg_arn" {
  type = string
}

variable "web_tg_arn" {
  type = string
}

variable "user_repo_url" {
  type = string
}

variable "story_repo_url" {
  type = string
}

variable "activity_repo_url" {
  type = string
}

variable "web_repo_url" {
  type = string
}

variable "rds_endpoint" {
  type = string
}

variable "redis_endpoint" {
  type = string
}

variable "s3_bucket_name" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "db_username" {
  type = string
}

variable "db_password" {
  type = string
}

variable "django_secret_key" {
  type = string
}

variable "supabase_url" {
  type = string
}

variable "supabase_key" {
  type      = string
  sensitive = true
}

variable "sb_db_name" {
  type = string
}

variable "sb_db_user" {
  type = string
}

variable "sb_db_password" {
  type      = string
  sensitive = true
}

variable "sb_db_host" {
  type = string
}

variable "sb_db_port" {
  type = string
}

variable "aws_access_key" {
  type = string
}

variable "aws_secret_key" {
  type = string
}

variable "project_name" {
  type = string
}
