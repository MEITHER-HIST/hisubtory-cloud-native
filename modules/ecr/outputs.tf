output "user_repo_url" {
  value = aws_ecr_repository.user.repository_url
}

output "story_repo_url" {
  value = aws_ecr_repository.story.repository_url
}

output "activity_repo_url" {
  value = aws_ecr_repository.activity.repository_url
}
