module "vpc" {
  source       = "./modules/vpc"
  vpc_cidr     = "10.0.0.0/16"
  project_name = var.project_name
}

module "sg" {
  source       = "./modules/sg"
  vpc_id       = module.vpc.vpc_id
  my_ip        = "112.221.198.140/32"
  project_name = var.project_name
}

module "ecr" {
  source       = "./modules/ecr"
  project_name = var.project_name
}

module "alb" {
  source            = "./modules/alb"
  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
  alb_sg_id         = module.sg.alb_sg_id
  project_name      = var.project_name
}

module "ecs" {
  source             = "./modules/ecs"
  private_subnet_ids = module.vpc.private_subnet_ids
  ecs_app_sg_id      = module.sg.ecs_app_sg_id
  target_group_arn   = module.alb.target_group_arn
  repository_url     = module.ecr.repository_url
  rds_endpoint       = module.rds.db_endpoint
  redis_endpoint     = module.redis.redis_endpoint
  project_name       = var.project_name
  depends_on         = [module.alb, module.rds, module.redis]
}

module "redis" {
  source          = "./modules/redis"
  data_subnet_ids = module.vpc.data_subnet_ids
  redis_sg_id     = module.sg.redis_sg_id
  project_name    = var.project_name
}

module "rds" {
  source          = "./modules/rds"
  data_subnet_ids = module.vpc.data_subnet_ids
  db_sg_id        = module.sg.rds_sg_id
  db_username     = var.db_username
  db_password     = var.db_password
  project_name    = var.project_name
}
