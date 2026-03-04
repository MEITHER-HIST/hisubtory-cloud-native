variable "public_subnet_id" {
  type = string
}

variable "bastion_sg_id" {
  type = string
}

variable "key_name" {
  type = string
}

variable "instance_type" {
  default = "t3.micro"
}
