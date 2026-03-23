resource "aws_s3_bucket" "media_bucket" {
  bucket = "${var.project_name}-media-bucket-v2"
  
  tags = {
    Name = "${var.project_name}-media-bucket-v2"
  }
}

output "bucket_name" {
  value = aws_s3_bucket.media_bucket.bucket
}
