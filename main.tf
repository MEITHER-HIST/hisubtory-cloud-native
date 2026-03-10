module "vpc" {
  source   = "./modules/vpc"
  vpc_cidr = "10.0.0.0/16"
}

module "sg" {
  source = "./modules/sg"
  vpc_id = module.vpc.vpc_id
  my_ip  = "112.221.198.140/32"
}

module "ecr" {
  source = "./modules/ecr"
}

module "s3" {
  source = "./modules/s3"
}

module "alb" {
  source = "./modules/alb"

  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
  alb_sg_id         = module.sg.alb_sg_id
}

module "ecs" {
  source = "./modules/ecs"

  private_subnet_ids = module.vpc.private_subnet_ids
  ecs_app_sg_id      = module.sg.ecs_app_sg_id
  
  user_target_group_arn = module.alb.user_target_group_arn
  user_repository_url   = module.ecr.user_repository_url

  story_target_group_arn = module.alb.story_target_group_arn
  story_repository_url   = module.ecr.story_repository_url

  activity_target_group_arn = module.alb.activity_target_group_arn
  activity_repository_url   = module.ecr.activity_repository_url

  rds_endpoint       = module.rds.db_endpoint
  redis_endpoint     = module.redis.redis_endpoint

  depends_on = [module.alb, module.rds, module.redis]
}

module "redis" {
  source = "./modules/redis"

  data_subnet_ids = module.vpc.data_subnet_ids
  redis_sg_id     = module.sg.redis_sg_id
}

module "rds" {
  source = "./modules/rds"

  data_subnet_ids = module.vpc.data_subnet_ids
  db_sg_id        = module.sg.rds_sg_id

  db_username = var.db_username
  db_password = var.db_password
}

module "bastion" {
  source = "./modules/bastion"

  public_subnet_id = module.vpc.public_subnet_ids[0]
  bastion_sg_id    = module.sg.bastion_sg_id
  key_name         = var.key_name
}
