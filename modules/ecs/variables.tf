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

variable "supabase_url" {
  type = string
}

variable "supabase_key" {
  type = string
}

variable "aws_access_key" {
  type = string
}

variable "aws_secret_key" {
  type = string
}

variable "django_secret_key" {
  type = string
}

variable "project_name" {
  type = string
}
