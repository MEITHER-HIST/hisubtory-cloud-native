output "user_tg_arn" {
  value = aws_lb_target_group.user_tg.arn
}

output "user_tg_arn_suffix" {
  value = aws_lb_target_group.user_tg.arn_suffix
}

output "story_tg_arn" {
  value = aws_lb_target_group.story_tg.arn
}

output "activity_tg_arn" {
  value = aws_lb_target_group.activity_tg.arn
}

output "alb_dns_name" {
  value = aws_lb.web_alb.dns_name
}

output "alb_arn" {
  value = aws_lb.web_alb.arn
}

output "alb_arn_suffix" {
  value = aws_lb.web_alb.arn_suffix
}
