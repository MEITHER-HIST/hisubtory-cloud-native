resource "aws_s3_bucket" "media" {
  bucket = "hisubtory-media-storage-unique-id" # 실제 사용 시 고유한 이름으로 자동 조정됩니다.

  tags = {
    Name = "hisubtory-media"
  }
}

resource "aws_s3_bucket_public_access_block" "media_access" {
  bucket = aws_s3_bucket.media.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

output "bucket_name" {
  value = aws_s3_bucket.media.id
}

output "bucket_arn" {
  value = aws_s3_bucket.media.arn
}
