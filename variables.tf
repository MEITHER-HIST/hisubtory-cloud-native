variable "region" {
  default = "ap-northeast-2"
}

variable "project_name" {
  description = "Project name to use for resource naming"
  type        = string
  default     = "hisubtory"
}

variable "instance_type" {
  type    = string
  default = "t3.medium"
}

variable "key_name" {
  type    = string
  default = "his_v2_key"
}

variable "db_username" {
  type    = string
  default = "admin"
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "supabase_url" {
  type    = string
  default = "https://jlvhwihvmivvihffhxse.supabase.co"
}

variable "supabase_key" {
  type      = string
  sensitive = true
}

variable "sb_db_name" {
  type    = string
  default = "postgres"
}

variable "sb_db_user" {
  type    = string
  default = "postgres.jlvhwihvmivvihffhxse"
}

variable "sb_db_password" {
  type      = string
  sensitive = true
}

variable "sb_db_host" {
  type    = string
  default = "aws-1-ap-northeast-2.pooler.supabase.com"
}

variable "sb_db_port" {
  type    = string
  default = "5432"
}

variable "aws_access_key" {
  type    = string
}

variable "aws_secret_key" {
  type      = string
  sensitive = true
}

variable "django_secret_key" {
  type      = string
  sensitive = true
}
