output "user_target_group_arn" {
  value = aws_lb_target_group.user_tg.arn
}

output "story_target_group_arn" {
  value = aws_lb_target_group.story_tg.arn
}

output "activity_target_group_arn" {
  value = aws_lb_target_group.activity_tg.arn
}

output "alb_dns_name" {
  value = aws_lb.web_alb.dns_name
}
