variable "region" {
  default = "ap-northeast-2"
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
