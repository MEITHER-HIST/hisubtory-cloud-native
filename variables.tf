variable "region" {
  default = "ap-northeast-2"
}

variable "project_name" {
  description = "Project name to use for resource naming"
  type        = string
  default     = "hisubtory"
}

variable "instance_type" {
  type = string
}

variable "key_name" {
  type = string
}


variable "db_username" {
  type = string
}

variable "db_password" {
  type      = string
  sensitive = true
}
