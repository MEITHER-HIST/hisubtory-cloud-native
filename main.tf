module "vpc" {
  source       = "./modules/vpc"
  vpc_cidr     = "10.0.0.0/16"
  project_name = var.project_name
}

module "sg" {
  source       = "./modules/sg"
  vpc_id       = module.vpc.vpc_id
  my_ip        = "210.124.140.19/32"
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

module "s3" {
  source       = "./modules/s3"
  project_name = var.project_name
}

module "ecs" {
  source             = "./modules/ecs"
  private_subnet_ids = module.vpc.private_subnet_ids
  ecs_app_sg_id      = module.sg.ecs_app_sg_id
  user_tg_arn        = module.alb.user_tg_arn
  story_tg_arn       = module.alb.story_tg_arn
  activity_tg_arn    = module.alb.activity_tg_arn
  web_tg_arn         = module.alb.web_tg_arn
  user_repo_url      = module.ecr.user_repo_url
  story_repo_url     = module.ecr.story_repo_url
  activity_repo_url  = module.ecr.activity_repo_url
  web_repo_url       = module.ecr.web_repo_url
  rds_endpoint       = module.rds.db_endpoint
  redis_endpoint     = module.redis.redis_endpoint
  s3_bucket_name     = module.s3.bucket_name
  aws_region         = var.region
  db_username        = var.db_username
  db_password        = var.db_password
  supabase_url       = var.supabase_url
  supabase_key       = var.supabase_key
  sb_db_name         = var.sb_db_name
  sb_db_user         = var.sb_db_user
  sb_db_password     = var.sb_db_password
  sb_db_host         = var.sb_db_host
  sb_db_port         = var.sb_db_port
  aws_access_key     = var.aws_access_key
  aws_secret_key     = var.aws_secret_key
  django_secret_key  = var.django_secret_key
  project_name       = var.project_name
  depends_on         = [module.alb, module.rds, module.redis, module.s3]
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

module "apigateway" {
  source       = "./modules/apigateway"
  project_name = var.project_name
  alb_dns_name = "http://${module.alb.alb_dns_name}"
}

# module "waf" {
#   source       = "./modules/waf"
#   project_name = var.project_name
#   alb_arn      = module.alb.alb_arn
# }

module "bastion" {
  source            = "./modules/bastion"
  public_subnet_ids = module.vpc.public_subnet_ids
  bastion_sg_id     = module.sg.bastion_sg_id
  key_name          = var.key_name
  project_name      = var.project_name
}

module "monitoring" {
  source             = "./modules/monitoring_tf"
  project_name       = var.project_name
  alb_arn_suffix     = module.alb.alb_arn_suffix
  user_tg_arn_suffix = module.alb.user_tg_arn_suffix
}
