resource "aws_lb" "web_alb" {
  name               = "hisubtory-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.alb_sg_id]
  subnets            = var.public_subnet_ids
}

# 1. User Service 타겟 그룹
resource "aws_lb_target_group" "user_tg" {
  name        = "hisubtory-user-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path = "/api/user/health/" # 적절한 헬스체크 경로
  }
}

# 2. Story Service 타겟 그룹
resource "aws_lb_target_group" "story_tg" {
  name        = "hisubtory-story-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path = "/api/stories/health/"
  }
}

# 3. Activity Service 타겟 그룹
resource "aws_lb_target_group" "activity_tg" {
  name        = "hisubtory-activity-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path = "/api/activity/health/"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.web_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "Not Found"
      status_code  = "404"
    }
  }
}

# 리스너 규칙: User Service (/api/user/*)
resource "aws_lb_listener_rule" "user" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 10

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.user_tg.arn
  }

  condition {
    path_pattern {
      values = ["/api/user/*"]
    }
  }
}

# 리스너 규칙: Story Service (/api/stories/*)
resource "aws_lb_listener_rule" "story" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 20

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.story_tg.arn
  }

  condition {
    path_pattern {
      values = ["/api/stories/*"]
    }
  }
}

# 리스너 규칙: Activity Service (/api/activity/*, /api/bookmarks/*)
resource "aws_lb_listener_rule" "activity" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 30

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.activity_tg.arn
  }

  condition {
    path_pattern {
      values = ["/api/activity/*", "/api/bookmarks/*"]
    }
  }
}

