# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"
}

# ECS Task Execution Role (IAM)
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.project_name}-ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Secrets Manager 접근 권한 추가
resource "aws_iam_role_policy" "ecs_task_execution_secrets_policy" {
  name = "${var.project_name}-ecs-task-execution-secrets-policy"
  role = aws_iam_role.ecs_task_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "secretsmanager:GetSecretValue",
          "kms:Decrypt"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

# ECS Task Role (IAM) - 컨테이너 내부 애플리케이션이 AWS 서비스를 사용할 때 필요
resource "aws_iam_role" "ecs_task_role" {
  name = "${var.project_name}-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "ecs_s3_policy" {
  name = "${var.project_name}-ecs-s3-policy"
  role = aws_iam_role.ecs_task_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:DeleteObject",
          "s3:PutObjectAcl"
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:s3:::${var.s3_bucket_name}",
          "arn:aws:s3:::${var.s3_bucket_name}/*"
        ]
      }
    ]
  })
}

# CloudWatch Log Groups for debugging
resource "aws_cloudwatch_log_group" "user" {
  name              = "/ecs/${var.project_name}-user"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_group" "story" {
  name              = "/ecs/${var.project_name}-story"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_group" "activity" {
  name              = "/ecs/${var.project_name}-activity"
  retention_in_days = 7
}

# ECS Task Definitions for each service
resource "aws_ecs_task_definition" "user" {
  family                   = "${var.project_name}-user-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "app"
      image     = "${var.user_repo_url}:latest"
      portMappings = [
        { containerPort = 80, hostPort = 80 },
        { containerPort = 8000, hostPort = 8000 }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.user.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
      environment = [
        { name = "DB_HOST", value = var.rds_endpoint },
        { name = "DB_PORT", value = "3306" },
        { name = "DB_NAME", value = "hisubtory_db" },
        { name = "DB_USER", value = var.db_username },
        { name = "DB_PASSWORD", value = var.db_password },
        { name = "REDIS_HOST", value = var.redis_endpoint },
        { name = "SERVICE_NAME", value = "user" },
        { name = "SECRET_KEY", value = var.django_secret_key },
        { name = "SUPABASE_URL", value = var.supabase_url },
        { name = "SUPABASE_KEY", value = var.supabase_key },
        { name = "SB_DB_NAME", value = var.sb_db_name },
        { name = "SB_DB_USER", value = var.sb_db_user },
        { name = "SB_DB_PASSWORD", value = var.sb_db_password },
        { name = "SB_DB_HOST", value = var.sb_db_host },
        { name = "SB_DB_PORT", value = var.sb_db_port },
        { name = "AWS_ACCESS_KEY_ID", value = var.aws_access_key },
        { name = "AWS_SECRET_ACCESS_KEY", value = var.aws_secret_key },
        { name = "AWS_STORAGE_BUCKET_NAME", value = var.s3_bucket_name },
        { name = "AWS_S3_REGION_NAME", value = var.aws_region },
        { name = "DEBUG", value = "True" }
      ]
    },
    {
      name      = "node-exporter"
      image     = "prom/node-exporter:latest"
      portMappings = [{ containerPort = 9100, hostPort = 9100 }]
    }
  ])
}

resource "aws_ecs_task_definition" "story" {
  family                   = "${var.project_name}-story-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "app"
      image     = "${var.story_repo_url}:latest"
      portMappings = [
        { containerPort = 80, hostPort = 80 },
        { containerPort = 8000, hostPort = 8000 }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.story.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
      environment = [
        { name = "DB_HOST", value = var.rds_endpoint },
        { name = "DB_PORT", value = "3306" },
        { name = "DB_NAME", value = "hisubtory_db" },
        { name = "DB_USER", value = var.db_username },
        { name = "DB_PASSWORD", value = var.db_password },
        { name = "REDIS_HOST", value = var.redis_endpoint },
        { name = "SERVICE_NAME", value = "story" },
        { name = "SECRET_KEY", value = var.django_secret_key },
        { name = "SUPABASE_URL", value = var.supabase_url },
        { name = "SUPABASE_KEY", value = var.supabase_key },
        { name = "SB_DB_NAME", value = var.sb_db_name },
        { name = "SB_DB_USER", value = var.sb_db_user },
        { name = "SB_DB_PASSWORD", value = var.sb_db_password },
        { name = "SB_DB_HOST", value = var.sb_db_host },
        { name = "SB_DB_PORT", value = var.sb_db_port },
        { name = "AWS_ACCESS_KEY_ID", value = var.aws_access_key },
        { name = "AWS_SECRET_ACCESS_KEY", value = var.aws_secret_key },
        { name = "AWS_STORAGE_BUCKET_NAME", value = var.s3_bucket_name },
        { name = "AWS_S3_REGION_NAME", value = var.aws_region },
        { name = "DEBUG", value = "True" }
      ]
    },
    {
      name      = "node-exporter"
      image     = "prom/node-exporter:latest"
      portMappings = [{ containerPort = 9100, hostPort = 9100 }]
    }
  ])
}

resource "aws_ecs_task_definition" "activity" {
  family                   = "${var.project_name}-activity-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "app"
      image     = "${var.activity_repo_url}:latest"
      portMappings = [
        { containerPort = 80, hostPort = 80 },
        { containerPort = 8000, hostPort = 8000 }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.activity.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
      environment = [
        { name = "DB_HOST", value = var.rds_endpoint },
        { name = "DB_PORT", value = "3306" },
        { name = "DB_NAME", value = "hisubtory_db" },
        { name = "DB_USER", value = var.db_username },
        { name = "DB_PASSWORD", value = var.db_password },
        { name = "REDIS_HOST", value = var.redis_endpoint },
        { name = "SERVICE_NAME", value = "activity" },
        { name = "SECRET_KEY", value = var.django_secret_key },
        { name = "SUPABASE_URL", value = var.supabase_url },
        { name = "SUPABASE_KEY", value = var.supabase_key },
        { name = "SB_DB_NAME", value = var.sb_db_name },
        { name = "SB_DB_USER", value = var.sb_db_user },
        { name = "SB_DB_PASSWORD", value = var.sb_db_password },
        { name = "SB_DB_HOST", value = var.sb_db_host },
        { name = "SB_DB_PORT", value = var.sb_db_port },
        { name = "AWS_ACCESS_KEY_ID", value = var.aws_access_key },
        { name = "AWS_SECRET_ACCESS_KEY", value = var.aws_secret_key },
        { name = "AWS_STORAGE_BUCKET_NAME", value = var.s3_bucket_name },
        { name = "AWS_S3_REGION_NAME", value = var.aws_region },
        { name = "DEBUG", value = "True" }
      ]
    },
    {
      name      = "node-exporter"
      image     = "prom/node-exporter:latest"
      portMappings = [{ containerPort = 9100, hostPort = 9100 }]
    }
  ])
}

resource "aws_ecs_task_definition" "web" {
  family                   = "${var.project_name}-web-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "app"
      image     = "${var.web_repo_url}:latest"
      portMappings = [
        { containerPort = 80, hostPort = 80 },
        { containerPort = 8000, hostPort = 8000 }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.web.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
    },
    {
      name      = "node-exporter"
      image     = "prom/node-exporter:latest"
      portMappings = [{ containerPort = 9100, hostPort = 9100 }]
    }
  ])
}

resource "aws_cloudwatch_log_group" "web" {
  name              = "/ecs/${var.project_name}-web"
  retention_in_days = 7
}

resource "aws_ecs_service" "web" {
  name            = "${var.project_name}-web-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.web.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [var.ecs_app_sg_id]
  }

  load_balancer {
    target_group_arn = var.web_tg_arn
    container_name   = "app"
    container_port   = 80
  }
}
resource "aws_ecs_service" "user" {
  name            = "${var.project_name}-user-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.user.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [var.ecs_app_sg_id]
  }

  load_balancer {
    target_group_arn = var.user_tg_arn
    container_name   = "app"
    container_port   = 80
  }
}

resource "aws_ecs_service" "story" {
  name            = "${var.project_name}-story-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.story.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [var.ecs_app_sg_id]
  }

  load_balancer {
    target_group_arn = var.story_tg_arn
    container_name   = "app"
    container_port   = 80
  }
}

resource "aws_ecs_service" "activity" {
  name            = "${var.project_name}-activity-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.activity.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [var.ecs_app_sg_id]
  }

  load_balancer {
    target_group_arn = var.activity_tg_arn
    container_name   = "app"
    container_port   = 80
  }
}
