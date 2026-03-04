resource "aws_lb_target_group" "web_tg" {
  name        = "hisubtory-web-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip" # Fargate와 연동하기 위해 IP 방식 필수

  health_check {
    path = "/"
    port = "80"
  }
}

resource "aws_lb" "web_alb" {
  name               = "hisubtory-alb"
  load_balancer_type = "application"
  subnets            = var.public_subnet_ids
  security_groups    = [var.alb_sg_id]
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.web_alb.arn

  port     = 80
  protocol = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web_tg.arn
  }
}

output "target_group_arn" {
  value = aws_lb_target_group.web_tg.arn
}
