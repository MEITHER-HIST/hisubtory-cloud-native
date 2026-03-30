output "bucket_name" {
  value = aws_s3_bucket.media_bucket.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.media_bucket.arn
}

output "bucket_domain_name" {
  value = aws_s3_bucket.media_bucket.bucket_regional_domain_name
}
