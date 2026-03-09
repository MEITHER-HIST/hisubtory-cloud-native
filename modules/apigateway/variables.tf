variable "project_name" {
  type = string
}

variable "alb_dns_name" {
  type        = string
  description = "DNS name of the Load Balancer to forward traffic to"
}
