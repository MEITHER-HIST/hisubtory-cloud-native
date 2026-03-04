variable "data_subnet_ids" {
  type = list(string)
}

variable "db_sg_id" {
  type = string
}

variable "db_username" {
  sensitive = true
  type      = string
}

variable "db_password" {
  sensitive = true
  type      = string
}
