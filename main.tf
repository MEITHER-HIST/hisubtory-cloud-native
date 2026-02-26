module "vpc" {
  source   = "./modules/vpc"
  vpc_cidr = "10.0.0.0/16"
}

module "sg" {
  source = "./modules/sg"

  vpc_id = module.vpc.vpc_id
}

module "web_tier" {
  source = "./modules/web_tier"

  instance_type = var.instance_type
  key_name      = var.key_name

  security_group_id = module.sg.frontend_sg_id
  subnet_ids        = module.vpc.public_subnet_ids
  vpc_id            = module.vpc.vpc_id
  target_group_arn  = module.alb.target_group_arn

  redis_endpoint = module.redis.redis_endpoint
  rds_endpoint   = module.rds.db_endpoint

  depends_on = [module.alb]
}

module "alb" {
  source = "./modules/alb"

  vpc_id = module.vpc.vpc_id

  public_subnet_ids = module.vpc.public_subnet_ids

  alb_sg_id = module.sg.alb_sg_id
}

module "redis" {
  source = "./modules/redis"

  private_subnet_ids = module.vpc.private_subnet_ids
  redis_sg_id        = module.sg.redis_sg_id
}

module "rds" {
  source = "./modules/rds"

  private_subnet_ids = module.vpc.private_subnet_ids
  db_sg_id           = module.sg.rds_sg_id

  db_username = var.db_username
  db_password = var.db_password
}
