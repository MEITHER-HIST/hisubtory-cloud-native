resource "aws_ecs_cluster" "main" {
  name = "hisubtory-cluster"
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "hisubtory-ecs-task-execution-role"

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

# --------------------------------------------------------------------------------------------------
# User Service
# --------------------------------------------------------------------------------------------------
resource "aws_ecs_task_definition" "user" {
  family                   = "hisubtory-user-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "user-app"
      image     = var.user_repository_url
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
      environment = [
        { name = "DB_HOST", value = var.rds_endpoint },
        { name = "REDIS_HOST", value = var.redis_endpoint }
      ]
    }
  ])
}

resource "aws_ecs_service" "user" {
  name            = "hisubtory-user-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.user.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [var.ecs_app_sg_id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.user_target_group_arn
    container_name   = "user-app"
    container_port   = 80
  }
}

# --------------------------------------------------------------------------------------------------
# Story Service
# --------------------------------------------------------------------------------------------------
resource "aws_ecs_task_definition" "story" {
  family                   = "hisubtory-story-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "story-app"
      image     = var.story_repository_url
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
      environment = [
        { name = "DB_HOST", value = var.rds_endpoint },
        { name = "REDIS_HOST", value = var.redis_endpoint }
      ]
    }
  ])
}

resource "aws_ecs_service" "story" {
  name            = "hisubtory-story-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.story.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [var.ecs_app_sg_id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.story_target_group_arn
    container_name   = "story-app"
    container_port   = 80
  }
}

# --------------------------------------------------------------------------------------------------
# Activity Service
# --------------------------------------------------------------------------------------------------
resource "aws_ecs_task_definition" "activity" {
  family                   = "hisubtory-activity-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "activity-app"
      image     = var.activity_repository_url
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
      environment = [
        { name = "DB_HOST", value = var.rds_endpoint },
        { name = "REDIS_HOST", value = var.redis_endpoint }
      ]
    }
  ])
}

resource "aws_ecs_service" "activity" {
  name            = "hisubtory-activity-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.activity.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [var.ecs_app_sg_id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.activity_target_group_arn
    container_name   = "activity-app"
    container_port   = 80
  }
}
