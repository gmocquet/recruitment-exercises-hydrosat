locals {
  bucket_name = "hydrosat-pipeline-bucket-${var.environment}-${var.workspace}"
}

resource "minio_s3_bucket" "public_bucket" {
  bucket         = local.bucket_name
  acl            = "public"
  object_locking = false
}

output "bucket_name" {
  value = minio_s3_bucket.public_bucket.bucket
}

output "bucket_arn" {
  value = minio_s3_bucket.public_bucket.arn
}
