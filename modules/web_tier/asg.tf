resource "aws_autoscaling_group" "web_asg" {

  desired_capacity = 2
  min_size         = 2
  max_size         = 2

  vpc_zone_identifier = var.subnet_ids

  launch_template {
    id      = aws_launch_template.web_lt.id
    version = "$Latest"
  }

  target_group_arns = [
  var.target_group_arn
]

  tag {
    key                 = "Name"
    value               = "web-server"
    propagate_at_launch = true
  }
}
