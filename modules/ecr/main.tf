resource "aws_ecr_repository" "user" {
  name                 = "hisubtory-user"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "story" {
  name                 = "hisubtory-story"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "activity" {
  name                 = "hisubtory-activity"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "user_repository_url" {
  value = aws_ecr_repository.user.repository_url
}

output "story_repository_url" {
  value = aws_ecr_repository.story.repository_url
}

output "activity_repository_url" {
  value = aws_ecr_repository.activity.repository_url
}
