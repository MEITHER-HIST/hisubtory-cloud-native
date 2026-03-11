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
  default = "his-key"
}

variable "db_username" {
  type    = string
  default = "admin"
}

variable "db_password" {
  type      = string
  sensitive = true
  default   = "mysql_password"
}

variable "supabase_url" {
  type    = string
  default = "https://jlvhwihvmivvihffhxse.supabase.co"
}

variable "supabase_key" {
  type      = string
  sensitive = true
  default   = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impsdmh3aWh2bWl2dmloZmZoeHNlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIwODUzMzksImV4cCI6MjA4NzY2MTMzOX0.3333V0vn-TNXJgZ9eRScnb-kQ8FK8QO8J1YTdL4bEpA"
}

variable "aws_access_key" {
  type    = string
  default = "AKIA2MWGKAR4QH2XYKGO"
}

variable "aws_secret_key" {
  type      = string
  sensitive = true
  default   = "/Fqh7t2fQLx2j4BvZJ15njdWn+hRiMTkJSTj0T42"
}

variable "django_secret_key" {
  type      = string
  sensitive = true
  default   = "django-insecure-ti-prtjm(d_p7ve!r(g&4&(=+*_vn*x+*3z^ge567i72tr-5)1"
}
