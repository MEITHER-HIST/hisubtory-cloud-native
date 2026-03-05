resource "aws_s3_bucket" "media_bucket" {
  bucket = "${var.project_name}-media-bucket"
  
  tags = {
    Name = "${var.project_name}-media-bucket"
  }
}

output "bucket_name" {
  value = aws_s3_bucket.media_bucket.bucket
}
