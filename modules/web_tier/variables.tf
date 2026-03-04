variable "instance_type" {}
variable "key_name" {}
variable "security_group_id" {}

variable "subnet_ids" {
  type = list(string)
}

variable "vpc_id" {
  type = string
}

variable "target_group_arn" {
  type = string
}

variable "redis_endpoint" {}
variable "rds_endpoint" {}

variable "iam_profile_name" {
  type = string
}
