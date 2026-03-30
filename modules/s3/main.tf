resource "aws_s3_bucket" "media_bucket" {
  bucket = "${var.project_name}-media-bucket-v2"
  
  tags = {
    Name = "${var.project_name}-media-bucket-v2"
  }
}

# Block all public access
resource "aws_s3_bucket_public_access_block" "media_bucket_block" {
  bucket = aws_s3_bucket.media_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Allow CloudFront OAC to access the bucket
resource "aws_s3_bucket_policy" "media_bucket_policy" {
  bucket = aws_s3_bucket.media_bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowCloudFrontServicePrincipalReadOnly"
        Effect    = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.media_bucket.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = var.cloudfront_arn
          }
        }
      }
    ]
  })
}
