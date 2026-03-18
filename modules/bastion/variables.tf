variable "project_name" {
  type = string
}

variable "public_subnet_ids" {
  type = list(string)
}

variable "bastion_sg_id" {
  type = string
}

variable "key_name" {
  type    = string
  default = "his_v2_key"
}
